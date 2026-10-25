#!/usr/bin/env python3
"""Compile BOOKbangla examples and focused regressions with an installed TeX Live."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

# Check the values actually written for references, not just the counter state.
# This catches environment packages silently replacing a chapter formatter.
EXPECTED_LABELS = {
    'section-headings': {f'sec:{style}': '১.১'
                         for style in ('classic', 'modern', 'minimal', 'ruled', 'default')},
    'paper-options': {'example:smallpaper': '১.১'},
    'manual': {'ex:weekdays': '১.১', 'ex:months': '১.১',
               'bn:weekdays': '১.১', 'bn:months': '১.১',
               'thm:pigeonhole': '১.১', 'bn:theorem': '১.১',
               'as:weekdays': '১.১', 'as:months': '১.১', 'as:theorem': '১.১'},
    'assamese': {'as:example': '১.১', 'as:theorem': '১.১',
                 'as:exercise': '১.১', 'as:continued': '১.২',
                 'as:reset': '২.১', 'as:appendix': 'ৰ.১'},
    'assamese-western': {'as:western': '1.1', 'as:western-appendix': 'R.1'},
    'theorems': {'thm:named': '১.১', 'thm:continued': '১.২',
                 'thm:reset': '২.১', 'thm:appendix': 'ক.১',
                 'example:separate': '১.১', 'exercise:separate': '১.১'},
    'book': {'example:weekdays': '১.১', 'example:sum': '২.১',
             'exercise:months': '১.১', 'exercise:remainders': '১.২',
             'exercise:continued': '১.৩', 'exercise:newchapter': '২.১',
             'exercise:appendix': 'ক.১', 'sec:pigeonhole': '১.১'},
    'overrides': {'ex:first': '1.1', 'ex:second': '1.2', 'ex:third': '1.3',
                  'example:first': '1.1', 'ex:reset': '2.1', 'ex:appendix': 'A.1',
                  'example:continuous': '8', 'ex:section': 'A.1.1'},
}


def run(command: list[str], cwd: Path, output: Path, env: dict[str, str]) -> None:
    result = subprocess.run(command, cwd=cwd, env=env, text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    output.write_text(result.stdout)
    if result.returncode:
        raise RuntimeError(f"{output}:\n{result.stdout[-2500:]}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine', choices=('xelatex', 'lualatex'), default='xelatex')
    parser.add_argument('--build-dir', type=Path, default=ROOT / 'tests/build',
                        help='Build root; each engine uses its own subdirectory')
    parser.add_argument('cases', nargs='*', help='Optional case names to rerun')
    args = parser.parse_args()
    # The trailing separator preserves the installed distribution search path.
    env = dict(os.environ)
    env['TEXINPUTS'] = str(ROOT / 'bookbangla') + '//:' + env.get('TEXINPUTS', '')
    cases = {
        'main': (ROOT / 'examples/bangla/main.tex', 'biber'),
        'chapter-styles': (ROOT / 'examples/chapter-styles.tex', None),
        'section-styles': (ROOT / 'examples/section-styles.tex', None),
        'manual': (ROOT / 'bookbangla/bookbangla.tex', None),
        **{p.stem: (p, 'biber' if p.stem.startswith('bibliography-biber')
                   else 'bibtex' if p.stem == 'bibliography' else None)
           for p in sorted((ROOT / 'tests/fixtures').glob('*.tex'))},
    }
    if unknown := set(args.cases) - cases.keys():
        parser.error(f"Unknown cases: {', '.join(sorted(unknown))}")
    results = {}
    for name in args.cases or cases:
        source, backend = cases[name]
        build = args.build_dir.resolve() / args.engine / name
        # A stale bibliography can contain commands removed from the source.
        # Each case owns this generated directory, so start it cleanly.
        if build.exists():
            shutil.rmtree(build)
        build.mkdir(parents=True, exist_ok=True)
        # The manual writes live examples beside its output; the highlighter
        # must find those files through the same search path as TeX.
        case_env = dict(env, TEXINPUTS=str(build) + ':' + str(source.parent)
                        + ':' + env['TEXINPUTS'])
        # Include files need corresponding directories inside the output folder.
        (build / 'chap').mkdir(exist_ok=True)
        # Only the manual needs TeX Live's allowlisted syntax highlighter.
        shell_policy = '-shell-restricted' if name == 'manual' else '-no-shell-escape'
        command = [args.engine, '-interaction=nonstopmode', '-halt-on-error',
                   shell_policy, f'-output-directory={build}', str(source)]
        for pass_number in range(1, 4):
            # Keep compiler/highlighter temporary files away from shipped PDFs.
            run(command, build, build / f'pass-{pass_number}.stdout', case_env)
            if backend and pass_number == 1:
                bib_env = dict(case_env, BIBINPUTS=str(source.parent) + ':'
                               + str(ROOT / 'examples/bangla') + ':')
                run([backend, source.stem], build, build / f'{backend}.stdout', bib_env)
        log = (build / f'{source.stem}.log').read_text(errors='replace')
        failures = [line for line in log.splitlines() if re.search(
            r'Missing character:|undefined references|undefined citations|'
            r'Font shape .*undefined|multiply defined|destination with the same|'
            r'ignoring duplicate destination|unreferenced destination|'
            r'You have requested release|You have requested, on input line|'
            r'bookbangla-test-failed', line)]
        if failures:
            raise RuntimeError(f"{name}: " + '\n'.join(failures))
        aux = (build / f'{source.stem}.aux').read_text()
        for label, expected in EXPECTED_LABELS.get(name, {}).items():
            if f'\\newlabel{{{label}}}{{{{{expected}}}' not in aux:
                raise RuntimeError(f'{name}: reference {label} should be {expected}')
        pdf = build / f'{source.stem}.pdf'
        if not pdf.is_file():
            raise RuntimeError(f'{name}: no PDF produced')
        results[name] = {'pdf': os.path.relpath(pdf, ROOT),
                         'overfull_boxes': len(re.findall(r'Overfull \\[hv]box', log))}
        print(f'{args.engine}: {name}: passed', flush=True)
    (args.build_dir.resolve() / args.engine / 'results.json').write_text(
        json.dumps(results, indent=2) + '\n')


if __name__ == '__main__':
    main()
