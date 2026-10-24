# Contributing

Keep the class small and build on memoir and LaTeXbangla. Use descriptive,
prefixed internal commands, and explain non-obvious behavior in comments.
Discuss changes to existing appearance or author commands before implementing
them. Keep translated labels in `bookbangla-labels-bangla.tex` and
`bookbangla-labels-assamese.tex`, with shared layout and environment code.

The `bookbangla/` directory is the CTAN package. Examples and tests live beside
it. To build without installing this class, run from `examples/bangla/`:

```sh
TEXINPUTS=../../bookbangla//: xelatex main.tex
bibtex main
TEXINPUTS=../../bookbangla//: xelatex main.tex
TEXINPUTS=../../bookbangla//: xelatex main.tex
```

Use `lualatex` in place of `xelatex` for LuaLaTeX. Install LaTeXbangla 2.0.1 or
newer, SolaimanLipi and Siyam Rupali. The example includes title material,
contents, a complete combinatorics chapter, exercises and bibliography.

Run the [tests](tests/README.md) on both engines and inspect the PDFs after
changes to typography. Rebuild the manual from `bookbangla/bookbangla.tex`, and
keep the distributed PDFs in sync with their sources.
Keep the Bangla and Assamese guides aligned with the English guide, including
the text inside their examples.

The manual uses minted for syntax highlighting and executes its Code/Result
examples. Build it with TeX Live's restricted shell escape (`-shell-restricted`);
the test runner supplies this option automatically.

Contributions use LPPL 1.3c or later, as described in [LICENSE](LICENSE).
