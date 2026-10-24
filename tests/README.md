# Tests

Use these checks when adapting BOOKbangla or contributing a change. They compile
the example book and manual, then check numbering, references and font handling.

With Python 3.10+, XeLaTeX, LuaLaTeX, BibTeX and LaTeXbangla 2.1 or newer
installed, run from the repository root:

```sh
python3 tests/run.py
python3 tests/run.py --engine lualatex
```

Install Kalpurush, SolaimanLipi and Siyam Rupali for these examples. The English
fonts come with TeX Live. Generated files stay in `tests/build/`.
For additional PDF checks of fonts, bibliography accents, body-line spacing,
hint placement, links and monochrome chapter designs:

```sh
python3 -m pip install -r tests/requirements.txt
python3 tests/verify.py
```

To rerun selected cases, append their names:

```sh
python3 tests/run.py book overrides boxes
```

The cases cover chapter designs, front matter, appendices, theorems, long boxes,
nested lists, paper-size options, Assamese labels and custom memoir settings.
The manual also runs its displayed examples in all three guides; its syntax highlighting uses minted with
restricted shell escape.

Inspect the PDFs after changes to typography, especially chapter headings,
box page breaks, quotations and proof end marks. Overfull boxes are recorded
in the build results to help locate layout problems.
Run `python3 tests/review-pages.py` to generate a side-by-side engine comparison
at `tests/build/page-review/index.html`. The spacing checks catch severe line
collisions; visual review is still needed for subtler layout problems.

Test environments:

| TeX Live | LaTeX | memoir |
| --- | --- | --- |
| 2024, final archived update | 2024-11-01 | 3.8.3 |
| 2026 | 2026-06-01 | 3.8.4b |

The pinned container images are recorded in
[LaTeXbangla's test guide](https://github.com/Neehan/LaTeXbangla/blob/master/tests/latex/README.md#test-environment-and-fonts).
The archived 2024 environment uses Python 3.12 for minted; it includes updates
through March 2025, rather than the original 2024 installer.
Use `--build-dir tests/build/texlive2024` with `run.py` and `verify.py` to
keep that distribution's results separate. Memoir 3.8.3 emits an `\addtodef`
deprecation warning when used with natbib; this also occurs without BOOKbangla.
Fonts and the dependency are installed in the test environment, not bundled
with this project.
