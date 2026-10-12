# Contributing

We welcome original contributions that improve reproducible, defensive AI agent security testing.

1. Open an issue for substantial new scenarios or scoring proposals.
2. Add *only synthetic* identities, business objects, tools and datasets.
3. Do **not** contribute source copied from private TRUSTELIS or other proprietary repositories, real credentials, customer data, internal architecture, or third-party source without appropriate rights.
4. Include explicit golden decision labels, a threat category, explanatory title, and tests. Keep the default test suite offline and dependency-free.
5. Run `python -m unittest discover -s tests -v` and `python -m trustelis_benchmark validate`.
6. State clearly whether results are generated using model APIs or hand-crafted fixtures; do not inflate safety claims.
7. Do not submit real-world exploit workflows, attack targets or dangerous operating instructions.

Contributions are submitted under the Apache-2.0 license in [LICENSE](LICENSE). Contributors are responsible for having rights to their contributions. Maintainers may request changes or decline contributions outside the defensive scope.
