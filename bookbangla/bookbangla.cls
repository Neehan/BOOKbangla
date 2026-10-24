% BOOKbangla — Bangla and Assamese books with memoir and LaTeXbangla.
% Copyright 2019, 2026 Adib Hasan <latexbangla@googlegroups.com>.
% Distributed under LPPL 1.3c or later; see LICENSE.
% Maintained by Adib Hasan. This work consists of the files listed in README.
\NeedsTeXFormat{LaTeX2e}[2024-11-01]
\ProvidesClass{bookbangla}[2026/10/24 v1.0.1 Bangla and Assamese books with memoir]

% Forward language selection to LaTeXbangla; it remains the single source of
% language state. All other class options go to memoir.
\DeclareOption{language=bangla}{\PassOptionsToPackage{language=bangla}{latexbangla}}
\DeclareOption{language=assamese}{\PassOptionsToPackage{language=assamese}{latexbangla}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{memoir}}
\PassOptionsToClass{a4paper,12pt}{memoir}
\ProcessOptions\relax
\LoadClass{memoir}
\RequirePackage{iftex}
\RequireTUTeX
\RequirePackage{latexbangla}[2026/10/24]
\RequirePackage{amsmath,amssymb,amsthm}
\RequirePackage{graphicx,xcolor,tikz}
\RequirePackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\RequirePackage{enumitem,lettrine,xpatch}
% Save table notes until outside the float, retaining their hyperlink targets.
\RequirePackage{footnotehyper}
\makesavenoteenv{tabular}
\makesavenoteenv{table}
\makesavenoteenv{table*}
\RequirePackage{hyperref}
% Title pages and main matter may both start at page 1. Use unique internal
% destinations while leaving visible page numbers and references unchanged.
\hypersetup{hidelinks,bookmarksopen=true,hypertexnames=false}

% The source tree keeps modules together. The basename fallback also permits
% a TeX distribution to install them in its indexed tex/latex tree.
\newcommand*\bookbangla@loadmodule[1]{%
  \InputIfFileExists{code/bookbangla-#1.tex}{}%
    {\input{bookbangla-#1.tex}}}
% Polyglossia exposes the resolved language after LaTeXbangla has loaded.
% This also respects options supplied directly with \PassOptionsToPackage.
\ifdefstring{\mainlanguagename}{assamese}
  {\bookbangla@loadmodule{labels-assamese}}
  {\bookbangla@loadmodule{labels-bangla}}
\bookbangla@loadmodule{layout}
\bookbangla@loadmodule{chapters}
\bookbangla@loadmodule{environments}

% One interface for our own design choices; memoir remains the interface for
% margins, chapter styles, page styles, and other general book configuration.
\ExplSyntaxOn
\keys_define:nn {bookbangla}
  {
    accent-color .code:n = {\colorlet{bookbanglaaccent}{#1}},
    box-frame-color .code:n = {\colorlet{bookbanglaboxframe}{#1}},
    box-background-color .code:n = {\colorlet{bookbanglaboxbackground}{#1}},
    quote-font .code:n = {\renewcommand\bookbanglaquotefont{#1}},
  }
\NewDocumentCommand\bookbanglasetup{m}{\keys_set:nn {bookbangla}{#1}}
\ExplSyntaxOff
\endinput
