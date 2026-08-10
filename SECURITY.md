# Security Policy

This repository is a public portfolio project. Do not commit secrets, advertising-platform credentials, customer identifiers, or original challenge rows without redistribution approval.

For real deployments:

- keep credentials in a secret manager,
- authenticate write or high-volume API access,
- rate-limit endpoints,
- log metadata rather than raw sensitive identifiers where possible,
- validate file size and schema before batch scoring,
- never load untrusted pickle/joblib artifacts.
