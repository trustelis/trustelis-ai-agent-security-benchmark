# Security policy

This project processes **synthetic** proposed agent actions and optionally sends those synthetic text fixtures to a model API. It intentionally does not implement or execute enterprise tools.

Never place API keys, organization credentials, customer records or real production configuration in pull requests, issues, fixtures or reports.

Before publishing a GitHub repository, maintainers should enable GitHub's **private vulnerability reporting** in repository Security settings (where available). Once enabled, use **Security > Report a vulnerability** instead of disclosing sensitive findings in a public issue. Until a private route exists, do not publish exploit details publicly.

If the adapter behaves unexpectedly, disable live API use and continue using the offline validator. The reference policy evaluator is not production-ready and must not be deployed as an authorization service.
