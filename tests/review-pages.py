#!/usr/bin/env python3
"""Render the book and layout fixtures side by side for visual review."""
import argparse
from html import escape
from pathlib import Path

import fitz

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--build-dir', type=Path, default=Path(__file__).parent / 'build')
args = parser.parse_args()
build = args.build_dir.resolve()
output = build / 'page-review'
output.mkdir(exist_ok=True)
html = ['<!doctype html><meta charset="utf-8"><title>BOOKbangla page review</title>',
        '<style>body{font:16px sans-serif;margin:2em;background:#eee}'
        'section{display:flex;gap:1em}figure{margin:0;width:50%}'
        'img{width:100%;background:white}h2{margin-top:2em}</style>',
        '<h1>BOOKbangla page review</h1>',
        '<p>Compare line spacing, page breaks, accents and font choices. '
        'Click a page to inspect it at full resolution.</p>']
for case, filename in (('main', 'main'), ('boxes', 'boxes'),
                       ('chapter-styles', 'chapter-styles'), ('book', 'book'),
                       ('bibliography', 'bibliography')):
    documents = {engine: fitz.open(build / engine / case / f'{filename}.pdf')
                 for engine in ('xelatex', 'lualatex')}
    for number in range(max(len(doc) for doc in documents.values())):
        html.append(f'<h2>{escape(case)} — page {number + 1}</h2><section>')
        for engine, document in documents.items():
            html.append(f'<figure><figcaption>{engine}</figcaption>')
            if number < len(document):
                image = f'{case}-{engine}-{number + 1}.png'
                document[number].get_pixmap(dpi=120).save(output / image)
                html.append(f'<a href="{image}"><img loading="lazy" src="{image}" '
                            f'alt="{case}, {engine}, page {number + 1}"></a>')
            else:
                html.append('<p>No corresponding page.</p>')
            html.append('</figure>')
        html.append('</section>')
    for document in documents.values():
        document.close()
(output / 'index.html').write_text('\n'.join(html), encoding='utf-8')
print(output / 'index.html')
