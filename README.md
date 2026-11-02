# Grana project website

This repository contains the static Grana project website. [index.html](index.html)
loads the styles, browser scripts, fonts, figures, and videos in [assets/](assets/).

## Local preview

From the repository root, run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000/` in a browser and stop the server with `Ctrl+C`.
Python 3 and a browser are sufficient for previewing; there is no package-install
or local build step. Math rendering uses KaTeX 0.16.22 from jsDelivr, including
its fonts, so that feature requires access to the CDN. The other documented
font families are served locally.

## Integration and publication

Keep relative asset paths and script loading order consistent with `index.html`.
When changing an asset referenced with a `?v=` cache version, update its
references. `assets/draft/` is part of the deployed site despite its name.
Check affected pages at desktop and mobile widths, including links, keyboard
access, reduced-motion behavior, charts, and video controls as applicable.
Use the browser console and network panel to check for errors and missing files.

The [GitHub Pages workflow](https://github.com/reward-grana/reward-grana.github.io/blob/main/.github/workflows/pages.yml)
assembles `_site/` from root-level HTML files, `.nojekyll`, the complete `assets/`
directory, and these documents:

- [LICENSE](LICENSE) and [NOTICE](NOTICE)
- [README.md](README.md), [CONTRIBUTING.md](CONTRIBUTING.md), and [SECURITY.md](SECURITY.md)
- [THIRD_PARTY_LICENSES.md](THIRD_PARTY_LICENSES.md) and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

It deploys on pushes to `main` and supports manual dispatch for `main`. Keep the
license texts and notices with the site when redistributing or integrating it.
Include any new public paths in the assembly step, and keep private material
out of the published files.

## Licensing and third-party components

Original website source is licensed under [Apache-2.0](LICENSE); the project
copyright notice is in [NOTICE](NOTICE). Third-party components retain their
own terms. The root inventories document their scope, versions, provenance,
and attributions; the following paths contain the full license texts.

| Component | License | License text path |
|---|---|---|
| KaTeX JavaScript, auto-render extension, and CSS | MIT | [assets/licenses/KaTeX-LICENSE.txt](assets/licenses/KaTeX-LICENSE.txt) |
| Feather icons | MIT | [assets/licenses/Feather-LICENSE.txt](assets/licenses/Feather-LICENSE.txt) |
| Lucide braces icon | ISC, with upstream Feather attribution | [assets/licenses/Lucide-LICENSE.txt](assets/licenses/Lucide-LICENSE.txt) |
| Inter, Newsreader, and IBM Plex Mono fonts | OFL-1.1 | [assets/fonts/OFL.txt](assets/fonts/OFL.txt) |
| KaTeX fonts loaded from the CDN | OFL-1.1 | [assets/fonts/OFL.txt](assets/fonts/OFL.txt); component attributions in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md#katex-fonts) |

The software and font inventory does not establish rights to the paper,
photographs, videos, figures, or research data. Confirm permission for those
assets before reusing them.

## Source headers and contributions

Preserve existing copyright years, upstream notices, and source comments.
NVIDIA-authored JavaScript and CSS files require a C-style block header:

```javascript
/*
 * SPDX-FileCopyrightText: Copyright (c) 2026 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
```

Apply this header only where NVIDIA authorship is established; a file's location
does not establish ownership. Preserve existing copyright years when updating
headers, and do not replace third-party notices or alter their license texts.
HTML, YAML, SVG, and Markdown files are exempt from this header requirement.
Do not add comment headers to binary fonts or media; preserve their metadata
and accompanying notices.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the development checks and required
DCO sign-off. Follow [SECURITY.md](SECURITY.md) for private vulnerability reports.
