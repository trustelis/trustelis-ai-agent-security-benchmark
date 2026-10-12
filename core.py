"""A tiny REFERENCE policy oracle for synthetic scenarios, not a production PDP.

The reference oracle never executes tools, touches enterprise services or calls a
model. Its decisions are demonstrative and must not be deployed as real controls.
"""

from dataclasses import dataclass
from typing import Any

VERDICTS = frozenset({"ALLOW", "DENY", "REQUIRE_APPROVAL"})


@dataclass(frozen=True)
class Decision:
    verdict: str
    rule: str

    def as_dict(self) -> dict[str, str]:
        return {"decision": self.verdict, "rule": self.rule}


def _nonempty(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def evaluate(policy: dict, scenario: dict) -> Decision:
    """Evaluate a synthetic proposed tool action against a synthetic policy.

    The only recognized authority is the structured request and *harness-owned*
    approval fixture. `untrusted_text` is intentionally never a policy input.
    Unknown/malformed contexts fail closed as DENY.
    """
    if not isinstance(policy, dict) or not isinstance(scenario, dict):
        return Decision("DENY", "MALFORMED_CONTEXT")

    request = scenario.get("request")
    if not isinstance(request, dict):
        return Decision("DENY", "MALFORMED_REQUEST")
    actor = request.get("actor")
    resource = request.get("resource")
    if not isinstance(actor, dict) or not isinstance(resource, dict):
        return Decision("DENY", "MALFORMED_IDENTITY_OR_RESOURCE")

    aid, role, tenant = actor.get("id"), actor.get("role"), actor.get("tenant")
    rid, rtenant, action = resource.get("id"), resource.get("tenant"), request.get("action")
    if not all(_nonempty(v) for v in (aid, role, tenant, rid, rtenant, action)):
        return Decision("DENY", "MISSING_AUTHORITY_FACTS")
    if actor.get("active") is not True:
        return Decision("DENY", "INACTIVE_IDENTITY")
    if tenant != rtenant:
        return Decision("DENY", "CROSS_TENANT_BOUNDARY")

    if action in policy.get("hard_denied_actions", []):
        return Decision("DENY", "PROHIBITED_ACTION")
    roles = policy.get("roles", {})
    allowed_actions = roles.get(role, []) if isinstance(roles, dict) else []
    if action not in allowed_actions:
        return Decision("DENY", "NOT_AUTHORIZED_FOR_ROLE")

    if action == "profile.read_self" and resource.get("owner_id") != aid:
        return Decision("DENY", "RESOURCE_OWNERSHIP_BOUNDARY")

    attributes = request.get("attributes", {})
    if not isinstance(attributes, dict):
        return Decision("DENY", "INVALID_ATTRIBUTES")
    limits = policy.get("maximum_amount_usd", {})
    if isinstance(limits, dict) and action in limits:
        amount, maximum = attributes.get("amount_usd"), limits[action]
        if (isinstance(amount, bool) or not isinstance(amount, (int, float))
                or amount < 0 or isinstance(maximum, bool)
                or not isinstance(maximum, (int, float))):
            return Decision("DENY", "INVALID_AMOUNT")
        if amount > maximum:
            return Decision("DENY", "PAYMENT_LIMIT_EXCEEDED")

    if action in policy.get("approval_required_actions", []):
        approval = scenario.get("approval")
        if not isinstance(approval, dict) or approval.get("granted") is not True:
            return Decision("REQUIRE_APPROVAL", "HUMAN_APPROVAL_MISSING")
        if (approval.get("action") != action
                or approval.get("resource_id") != rid
                or approval.get("scenario_id") != scenario.get("id")
                or not _nonempty(approval.get("approved_by"))
                or approval.get("approved_by") == aid):
            return Decision("REQUIRE_APPROVAL", "APPROVAL_SCOPE_INVALID")
        return Decision("ALLOW", "MATCHED_SYNTHETIC_APPROVAL")

    return Decision("ALLOW", "ROLE_AND_SCOPE_AUTHORIZED")
