#!/usr/bin/env python3
"""Inspect rendered book PDFs after tests/run.py has passed on both engines."""
from pathlib import Path
import re
import unicodedata

import fitz

ROOT = Path(__file__).resolve().parent


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


for engine in ('xelatex', 'lualatex'):
    build = ROOT / 'build' / engine
    with fitz.open(build / 'book/book.pdf') as document:
        links = [link for page in document for link in page.get_links()
                 if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED)]
        check(len(links) >= 8, f'{engine}: missing navigation/reference links')
        check(all(0 <= link.get('page', -1) < len(document) for link in links),
              f'{engine}: a link has no valid destination')
        fonts = {span['font'] for page in document
                 for block in page.get_text('dict')['blocks'] if 'lines' in block
                 for line in block['lines'] for span in line['spans']}
        check(any('Kalpurush' in font for font in fonts), f'{engine}: no Bangla font')
        check(any('Pagella' in font for font in fonts), f'{engine}: English font lost')

    with fitz.open(build / 'overrides/overrides.pdf') as document:
        text = ' '.join(page.get_text() for page in document)
        check(len(re.findall('A first hint', text)) == 1,
              f'{engine}: hint omitted or leaked into a later exercise')
        check('OVERRIDE:' in text, f'{engine}: custom title hook was overwritten')
        fonts = {span['font'] for page in document
                 for block in page.get_text('dict')['blocks'] if 'lines' in block
                 for line in block['lines'] for span in line['spans']}
        check(any('Cursor' in font and 'Italic' in font for font in fonts),
              f'{engine}: quotation font override lost')

    with fitz.open(build / 'chapter-styles/chapter-styles.pdf') as document:
        check(len(document) == 5, f'{engine}: expected one page per chapter design')
        # Default examples must remain suitable for monochrome printing.
        for page in document:
            for drawing in page.get_drawings():
                for key in ('color', 'fill'):
                    color = drawing.get(key)
                    if color and len(color) == 3:
                        check(max(color) - min(color) < .001,
                              f'{engine}: a chapter design introduced colour')
    with fitz.open(build / 'chapter-headings/chapter-headings.pdf') as document:
        check(len(document) == 8, f'{engine}: chapter headings displaced the body text')
        for page in document:
            check(abs(page.rect.width - 148 / 25.4 * 72) < 1,
                  f'{engine}: the A5 stock override was lost')

    with fitz.open(build / 'paper-options/paper-options.pdf') as document:
        for page in document:
            check(abs(page.rect.width - 148 / 25.4 * 72) < 1
                  and abs(page.rect.height - 210 / 25.4 * 72) < 1,
                  f'{engine}: the a5paper option produced the wrong page size')

    with fitz.open(build / 'assamese/assamese.pdf') as document:
        text = unicodedata.normalize('NFC', ' '.join(page.get_text() for page in document))
        check('উদাহৰণ' in text and 'উদাহরণ' not in text,
              f'{engine}: Assamese example heading or reference was not translated')
        links = [link for page in document for link in page.get_links()
                 if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED)]
        check(len(links) >= 5 and all(0 <= link.get('page', -1) < len(document) for link in links),
              f'{engine}: Assamese references have missing destinations')

    with fitz.open(build / 'manual/bookbangla.pdf') as document:
        guides = {title: page - 1 for level, title, page in document.get_toc()
                  if level == 1}
        bangla_start = guides.get('বাংলা ব্যবহার নির্দেশিকা', -1)
        assamese_start = guides.get('অসমীয়া ব্যৱহাৰ নিৰ্দেশিকা', -1)
        check(guides.get('English user guide') == 0
              and 0 < bangla_start < assamese_start,
              f'{engine}: manual language bookmarks are missing or misplaced')
        links = [link for page in document for link in page.get_links()
                 if link['kind'] in (fitz.LINK_GOTO, fitz.LINK_NAMED)]
        check(len(links) >= 12, f'{engine}: manual examples or language links are missing')
        check(all(0 <= link.get('page', -1) < len(document) for link in links),
              f'{engine}: a manual example has a broken reference link')
        # Restarted example counters must not send readers to the other guide.
        for page_number, page in enumerate(document):
            for link in page.get_links():
                if link.get('nameddest', '').startswith(('example', 'exercise', 'theorem')):
                    source_guide = sum(page_number >= start for start in (bangla_start, assamese_start))
                    target_guide = sum(link['page'] >= start for start in (bangla_start, assamese_start))
                    check(source_guide == target_guide,
                          f'{engine}: a manual example links to the other language')
    print(f'{engine}: PDF fonts, hints, links, overrides and chapter designs passed')
