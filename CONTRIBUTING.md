# Contributing to Grana

Contributions to Grana are accepted under the [Apache License 2.0](LICENSE).
Preserve existing upstream copyright and license notices. When adding or
adapting third-party code, document its source, revision, license, and any
modifications in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md), and include
its required license text in [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md).

## Signing Your Work

Every contributor must sign off each commit under the
[Developer Certificate of Origin 1.1](https://developercertificate.org/).
A sign-off certifies that you created the contribution or have the right to
submit it under the applicable open-source license. This project uses DCO
sign-off and does not require a separate contributor license agreement.

Use your real name and email address:

```bash
git commit -s -m "Describe the change"
```

This adds a trailer such as:

```text
Signed-off-by: Your Name <your.email@example.com>
```

Commits without the required sign-off will not be accepted.

## Development workflow

1. Fork the repository and create a feature branch from `main`.
2. Follow the [README](README.md) to install the qualified runtime. The setup
   currently targets Linux aarch64, Python 3.12, CUDA 13, and NVIDIA GB300;
   other hardware requires its own validation.
3. Keep changes focused on the cached-data training, inference, and annotation
   workflows. Add or update tests when behavior changes, and describe the
   expected behavior and validation in your pull request.
4. Run the relevant tests while developing. Before submitting a change, run
   the complete suite in the configured environment:

   ```bash
   bash scripts/setup_env.sh
   source .venv-qwen35-unsloth/bin/activate
   python -m pip install -r requirements/annotation.txt
   python -m pytest tests
   ```

   Annotation API tests use local fixtures or mocks; do not include credentials
   or private robot recordings in a test or pull request. GPU training and
   external API runs are separate from the unit-test suite. Report their
   configuration and results when they are relevant to your change.
5. For packaging changes, build and inspect the source archive:

   ```bash
   python scripts/package_release.py --output dist/grana-source.tar.gz
   ```

   The packager uses an explicit source allowlist. Update it when new public
   source files are required; datasets, model weights, virtual environments,
   credentials, and local run artifacts do not belong in the release.
6. Open a pull request against `main` describing the problem, the resulting
   behavior, and the checks you ran. Preserve the distinction between an API
   annotation suggestion and a reviewed training annotation.

Follow [SECURITY.md](SECURITY.md) for private vulnerability reports and handling
of credentials, recordings, model artifacts, and local services. Contributors
are expected to communicate respectfully and professionally.

## Full text of the DCO

```text
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.


Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```
