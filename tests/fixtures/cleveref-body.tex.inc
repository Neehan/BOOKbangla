\makeatletter
\typeout{BOOK-CREF-EXAMPLE: \cref@example@name}
\typeout{BOOK-CREF-EXERCISES: \cref@exercise@name@plural}
\makeatother
\mainmatter
\chapter{গণনা}\label{ch:first}
\begin{theorem}\label{thm:first}Test.\end{theorem}
\begin{example}\label{ex:first}Test.\end{example}
\begin{example}\label{ex:second}Test.\end{example}
\begin{exercise}\label{pr:first}Test.\end{exercise}
\begin{exercise}\label{pr:second}Test.\end{exercise}
\begin{exercise}\label{pr:third}Test.\end{exercise}
Theorem: \cref{thm:first}.\par
Examples: \cref{ex:first,ex:second}.\par
Problems: \cref{pr:third,pr:first,pr:second}.\par
Capital: \Cref{ex:first}.\par
Mixed: \cref{ex:first,pr:first,thm:first}.\par
\chapter{গণনা}
\begin{exercise}\label{pr:reset}Test.\end{exercise}
Reset: \cref{pr:reset}.\par
\appendix
\chapter{গণনা}
\begin{exercise}\label{pr:appendix}Test.\end{exercise}
Appendix: \cref{pr:appendix}.\par
\crefname{exercise}{problem}{problems}
Custom: \cref{pr:first}.
