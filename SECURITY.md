# Reporting Security Vulnerabilities

Report suspected vulnerabilities in the Grana project website privately using NVIDIA's
[security vulnerability reporting page](https://www.nvidia.com/object/submit-security-vulnerability.html)
or email [psirt@nvidia.com](mailto:psirt@nvidia.com). For sensitive email,
use the [NVIDIA public PGP key](https://www.nvidia.com/en-us/security/pgp-key/).
Include the repository and affected page URLs, commit if known, browser version,
reproduction steps or a proof of concept, and the potential security impact.
Do not publish vulnerability details in a public GitHub issue or pull request.

See [NVIDIA's PSIRT policies](https://www.nvidia.com/en-us/security/psirt-policies/)
for coordinated disclosure information and
[NVIDIA Product Security](https://www.nvidia.com/en-us/security/) for other
security-related concerns.

## Website scope and local previews

This repository contains the public Grana website: HTML, CSS, browser JavaScript,
and static media deployed through GitHub Pages. Its security scope includes
page scripts, third-party browser dependencies, published assets, and the Pages
deployment workflow.

Run local previews from the website directory and bind the preview server to
loopback, for example `python3 -m http.server 8000 --bind 127.0.0.1`. The preview
server can expose files in that directory and is intended for local development.
Use an authenticated SSH port forward when previewing from a remote host.

## Browser code and dependencies

The website loads KaTeX JavaScript and CSS from jsDelivr using versioned URLs.
Review changes to external scripts and dependency versions: CDN scripts execute
in visitors' browsers with access to the page. Treat URL parameters and other
external input as untrusted; avoid inserting them as HTML or executable code.

## Public assets and credentials

Treat every file included in the Pages deployment as public, including files
that are not linked from a page. Publish only media and documents approved for
public sharing, and check their metadata for private information. Keep private
recordings, unpublished data, and local working files out of the repository and
deployment artifact.

Keep API keys, access tokens, and deployment credentials out of HTML, JavaScript,
assets, commits, and logs. Use GitHub Actions secrets for any deployment secrets;
never embed them in the published site. If a credential is exposed, revoke and
rotate it; removing a file or commit does not remove copies from repository
history or caches.
