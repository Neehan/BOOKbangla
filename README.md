<p align="center">
  <img src="bookbangla/logo.png" alt="BOOKbangla" width="650">
</p>

# BOOKbangla

Write your Bangla or Assamese book using familiar LaTeX commands, with chapter headings,
worked examples and exercises ready to use. Built on memoir and
[LaTeXbangla](https://github.com/Neehan/LaTeXbangla), **BOOKbangla** lets you choose
your fonts and adapt the layout to your book.

**For Overleaf,** make a copy of [this demo](https://www.overleaf.com/project/6adc6a64e207c9e858a5c4ba/share#f620335030ef2a824fafcc0cfb1f6e2548f3d2154965545f) and start your own book.

BOOKbangla grew out of the template I used to write *কম্বিনেটরিকসে হাতেখড়ি*
(*Introduction to Combinatorics*): [Part 1](https://rokomari.com/book/180324/combinatoricse-hatekhori--1st-part)
and [Part 2](https://www.rokomari.com/book/185613/combinatoricse-hatekhori--2nd-part).

BOOKbangla is free to use under [LPPL 1.3c or later](LICENSE). If you use it to
publish a book, I would appreciate an acknowledgement of BOOKbangla and its
author, Adib Hasan. :))

See the [example book](examples/bangla/main.pdf) and [chapter designs](examples/chapter-styles.pdf),
or start with this short example:

```latex
\documentclass{bookbangla}
\setbanglamainfont{Kalpurush}
\title{আমার বই}
\author{লেখকের নাম}
\date{}

\begin{document}
\maketitle
\mainmatter
\chapter{শুরু}
\begin{example}
আটজন বন্ধুর মধ্যে অন্তত দুজনের জন্ম একই বারে কেন?
\end{example}
\begin{solution}
সপ্তাহে মাত্র সাতটি বার আছে।
\end{solution}
\begin{exercise}[hint={বছরের মাসগুলোকে খোপ ধরো।}]
তেরোজন মানুষের মধ্যে অন্তত দুজনের জন্ম একই মাসে, দেখাও।
\end{exercise}
\end{document}
```

Compile with **XeLaTeX or LuaLaTeX**, using an updated TeX Live 2024 or later and LaTeXbangla **2.1 or newer**.
Use any suitable Bangla font; Kalpurush is just one choice.
For an Assamese book, use `\documentclass[language=assamese]{bookbangla}`;
the font commands stay the same. Choose a font with ৰ and ৱ.

- Classic, modern, minimal and ruled chapter designs; memoir’s default remains available.
- Numbered examples, theorems and problems, optional hints, solutions and reference links.
- “নিজে করো” and “মনে রাখবে” boxes, chapter quotations and configurable lists.
- Your choice of fonts and bibliography. Use `\bookbanglasetup` for the class's
  design settings and memoir's commands for further customization.

The example book includes the title page, contents, a complete
pigeonhole-principle chapter, exercises and bibliography from my book.
Start with [main.tex](examples/bangla/main.tex) to write your own book.
The manual ([English](bookbangla/bookbangla.pdf#nameddest=guide-english) /
[বাংলা](bookbangla/bookbangla.pdf#nameddest=guide-bangla) /
[অসমীয়া](bookbangla/bookbangla.pdf#nameddest=guide-assamese)) explains how to customize
your book. See [build instructions](CONTRIBUTING.md) to compile the full example.

Adib Hasan · [latexbangla@googlegroups.com](mailto:latexbangla@googlegroups.com)
