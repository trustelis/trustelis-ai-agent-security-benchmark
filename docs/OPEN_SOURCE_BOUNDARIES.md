# Open source / proprietary separation

This repository is an **independent, from-scratch, synthetic research artifact**. It is not an open-source release of the proprietary TRUSTELIS AI Control Platform.

**May be public**: new generic example policy rules, synthetic finance/IT/HR scenarios, standalone scoring code, generic documentation, reproducible benchmark reports without real customer data, and independently written provider API adapters.

**Must remain private**: actual platform source files; implementation details of internal Policy Rules Engine, Gateway, Trust Pack, commercial flows, Blueprints or customer integrations; worker, database, identity and production environments; API keys, tokens, organizational IDs; security findings with real targets; actual business/customer data; internal operating procedures; trademarks, logos and premium design assets.

Reference concepts such as `ALLOW`, `DENY`, `REQUIRE_APPROVAL`, tenant isolation, and scoped approval are common, generic security patterns. The *reference implementation in this repository is intentionally simplified and is not copied from the commercial engine*.

Do not place a pointer to a private repository's secrets, environment configuration or source files in this project. Publication is a separate voluntary action and does not alter existing TRUSTELIS repositories or services.
