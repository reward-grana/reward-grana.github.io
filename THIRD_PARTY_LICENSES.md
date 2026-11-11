# Third-party licenses

This inventory covers identified software, icons, and fonts in the Grana static
website, including the shipped `assets/draft/` files. It is separate from the
Grana training and inference source release. The website's [Apache-2.0
license](LICENSE) does not replace these components' licenses. Copyright
attributions are in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Bundled fonts

The 12 WOFF2 files in `assets/fonts/` are Latin and Latin Extended subsets
served locally through `assets/css/site.css`. Versions below come from the
font files' embedded metadata. The existing [OFL.txt](assets/fonts/OFL.txt)
contains their copyright notices and the full SIL Open Font License 1.1.

| Component | Version and files | License | Upstream |
|---|---|---|---|
| Inter | 4.001; `inter-*.woff2` (2 files), normal 400–700 | OFL-1.1 | [Inter](https://github.com/rsms/inter) |
| Newsreader | 1.003; `newsreader-*.woff2` (4 files), normal and italic 400–700 | OFL-1.1 | [Newsreader](https://github.com/productiontype/Newsreader) |
| IBM Plex Mono | 2.3; `ibm-plex-mono-*.woff2` (6 files), normal 400, 500, and 600 | OFL-1.1 | [IBM Plex](https://github.com/IBM/plex) |

## Inline icons

`index.html` contains SVG geometry matching or adapting the following icons.
Attribution is based on comparison with upstream SVGs; the original import
revision is not recorded. The references identify the versions compared,
not an established import history.

| Component | Website symbols and upstream reference | Full license text |
|---|---|---|
| Feather | `i-play`, `i-book`, `i-expand`, and adapted `i-copy` / `i-doc`; [v4.29.2 icons](https://github.com/feathericons/feather/tree/v4.29.2/icons) | [MIT](assets/licenses/Feather-LICENSE.txt) |
| Lucide braces | Adapted geometry in `i-braces`; [upstream braces SVG](https://github.com/lucide-icons/lucide/blob/175b2cd4831c27256c9f4a243a2812730b5b851a/icons/braces.svg) | [ISC, with upstream Feather attribution](assets/licenses/Lucide-LICENSE.txt) |

## Components loaded from jsDelivr

`index.html` requests KaTeX 0.16.22 CSS, and `assets/js/app.js` loads its
JavaScript and auto-render extension. The CSS also references KaTeX fonts.
These files are fetched from the CDN rather than bundled in this repository.

| Component | Version / payload | Full license text |
|---|---|---|
| KaTeX JavaScript, auto-render, and CSS | 0.16.22; [upstream release license](https://github.com/KaTeX/KaTeX/blob/v0.16.22/LICENSE) | [MIT](assets/licenses/KaTeX-LICENSE.txt) |
| KaTeX fonts | 20 faces in the 0.16.22 CSS, each offered as WOFF2, WOFF, and TTF; embedded metadata declares OFL-1.1 | [OFL-1.1](assets/fonts/OFL.txt); separate copyright and reserved names in [notices](THIRD_PARTY_NOTICES.md#katex-fonts) |

The KaTeX package's MIT license does not replace its fonts' OFL-1.1 terms.
The paper, photographs, videos, figures, and research data are outside this
software and font inventory; this inventory does not establish their provenance
or grant additional rights to them.
