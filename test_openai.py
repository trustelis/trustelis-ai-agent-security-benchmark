import json
import os
import unittest
from unittest.mock import patch

from trustelis_benchmark.openai_live import call_openai, extract_text, make_input, parse_decision


class OpenAIAdapterTests(unittest.TestCase):
    def setUp(self):
        self.policy = {"roles": {"test_role": ["read"]}}
        self.case = {"id": "TEST-001", "domain": "synthetic", "title": "Test case",
                     "request": {"actor": {"id": "a", "role": "test_role", "tenant": "o", "active": True},
                                 "resource": {"id": "r", "tenant": "o"}, "action": "read"},
                     "approval": None, "untrusted_text": "safe synthetic fixture",
                     "expected_decision": "ALLOW"}

    def test_ground_truth_never_sent_to_model(self):
        payload = json.dumps(make_input(self.policy, self.case))
        self.assertNotIn("expected_decision", payload)
        self.assertNotIn('"ALLOW"', payload)

    def test_parse_strict_model_output(self):
        self.assertEqual("ALLOW", parse_decision('{"decision":"ALLOW"}'))
        self.assertEqual("INVALID", parse_decision("Sure, I would allow it"))
        self.assertEqual("INVALID", parse_decision('{"decision":"EXECUTE"}'))

    def test_response_extract(self):
        body = {"output": [{"type": "message", "content": [
            {"type": "output_text", "text": '{"decision":"DENY"}'},
        ]}]}
        self.assertEqual("DENY", parse_decision(extract_text(body)))

    def test_no_api_key_prevents_request(self):
        with patch.dict(os.environ, {"OPENAI_API_KEY": ""}):
            with self.assertRaisesRegex(ValueError, "OPENAI_API_KEY is required"):
                call_openai(self.policy, self.case, model="synthetic-model")


if __name__ == "__main__":
    unittest.main()
