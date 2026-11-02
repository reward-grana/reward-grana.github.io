# Reporting Security Vulnerabilities

Report suspected vulnerabilities in Grana privately using NVIDIA's
[security vulnerability submission form](https://www.nvidia.com/object/submit-security-vulnerability.html)
or email [psirt@nvidia.com](mailto:psirt@nvidia.com). For sensitive email,
use the [NVIDIA public PGP key](https://www.nvidia.com/en-us/security/pgp-key).
Include the repository URL, affected commit or version, vulnerability type,
reproduction steps or a proof of concept, and the potential security impact.
Do not publish vulnerability details in a public GitHub issue or pull request.

See [NVIDIA's PSIRT policies](https://www.nvidia.com/en-us/security/psirt-policies/)
for coordinated disclosure information and
[NVIDIA Product Security](https://www.nvidia.com/en-us/security/) for other
security-related concerns.

## Deployment boundaries

Grana's inference and annotation-review servers are local research tools.
They require an IPv4 loopback bind and do not provide application-level user
authentication or TLS. Access a remote server through an authenticated SSH
port forward. If you place a gateway in front of a service, keep the Grana
backend on loopback and enforce authentication, authorization, and TLS at the
gateway; only trusted users should reach it. Do not bypass the server's
loopback or request-validation checks to expose it publicly.

Inference review media is served from an explicit file allowlist. Only add
recordings approved for the intended reviewers. Review pages and API responses
may contain private task descriptions, images, annotations, or model outputs.
Restrict access to the host, forwarded ports, and artifact directories.

## Credentials and artifacts

- Keep API keys, access tokens, and W&B credentials outside the repository.
  Supply credentials through the documented environment variables or an
  external secret manager, and avoid including them in command arguments,
  configuration files, prompts, logs, screenshots, or reports.
- Keep private datasets, robot recordings, cache payloads, checkpoints, and
  machine-specific paths out of commits and release archives. Treat local
  annotation receipts and review artifacts as private unless approved for
  sharing.
- API annotation sends selected visual evidence and task context to the
  configured provider. Use an approved provider endpoint and only submit
  material you are authorized to share. Configure W&B destinations and
  checkpoint uploads according to the same data-sharing requirements.
- Load datasets, checkpoints, model code, and configuration only from sources
  you trust. A local research environment is not a sandbox for untrusted
  artifacts. Keep dependency versions and their licenses under review when
  changing the runtime.
- If a credential is exposed, revoke and rotate it. Removing the latest file
  or commit does not remove copies from repository history or external logs.

Grana produces model predictions and annotation suggestions; it does not
provide a safety controller for robot actuation. Integrations that use these
outputs to command hardware need their own operator controls and safety checks.
