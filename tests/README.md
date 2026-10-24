# Tests

Use these checks when adapting BOOKbangla or contributing a change. They compile
the example book and manual, then check numbering, references and font handling.

With Python 3.10+, XeLaTeX, LuaLaTeX, BibTeX and LaTeXbangla 2.0 or newer
installed, run from the repository root:

```sh
python3 tests/run.py
python3 tests/run.py --engine lualatex
```

Install Kalpurush, SolaimanLipi and Siyam Rupali for these examples. The English
fonts come with TeX Live. Generated files stay in `tests/build/`.
For additional PDF checks of fonts, hint placement, links and monochrome
chapter designs:

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

Tested with TeX Live 2026, memoir 3.8.4b and LaTeXbangla 2.0.
The container image used for verification is
`texlive/texlive@sha256:7334b00bf8e7a0996f7ddd65482363aaf7711d372e569f3ea78509619e3083ff`.
Fonts and the dependency are installed in the test environment, not bundled
with this project.
