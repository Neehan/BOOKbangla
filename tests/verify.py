#!/usr/bin/env python3
"""Inspect rendered book PDFs after tests/run.py has passed on both engines."""
import argparse
from pathlib import Path
import re
import unicodedata

import fitz

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--build-dir', type=Path, default=ROOT / 'build')
BUILD = parser.parse_args().build_dir.resolve()


def check(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def check_bibliography(document, engine, expected):
    """Check visible names and their Latin font, including separate accents."""
    spans = [span for page in document
             for block in page.get_text('dict')['blocks']
             for line in block.get('lines', []) for span in line['spans']]
    text = unicodedata.normalize('NFC', ' '.join(span['text'] for span in spans))
    for word, count in expected.items():
        check(text.count(word) == count, f'{engine}: bibliography lost or changed {word}')
        matching = [span for span in spans if word in unicodedata.normalize('NFC', span['text'])]
        check(bool(matching) and all(span['font'].startswith('LMRoman') for span in matching),
              f'{engine}: bibliography uses the wrong font for {word}')
    for span in spans:
        if any(0x0300 <= ord(char) <= 0x036F for char in span['text']):
            check(span['font'].startswith('LMRoman'),
                  f'{engine}: bibliography accent uses {span["font"]}')


def check_body_line_spacing(document, engine):
    # Catch severe collisions like a negative vertical skip after a display.
    # Font bounding boxes include unused ascender space; compare baselines
    # instead, restricting this check to overlapping long Bengali text lines.
    for number, page in enumerate(document, 1):
        lines = []
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines', []):
                bengali = [s for s in line['spans']
                           if sum(0x0980 <= ord(c) <= 0x09FF for c in s['text']) >= 12]
                if bengali:
                    span = bengali[0]
                    lines.append((fitz.Rect(line['bbox']), span['origin'][1], span['size']))
        for i, (rect, baseline, size) in enumerate(lines):
            for other, other_baseline, other_size in lines[i + 1:]:
                overlap = min(rect.x1, other.x1) - max(rect.x0, other.x0)
                if overlap > min(rect.width, other.width) / 2:
                    check(abs(baseline - other_baseline) > min(size, other_size) * .6,
                          f'{engine}: colliding body lines on page {number}')


for engine in ('xelatex', 'lualatex'):
    build = BUILD / engine
    with fitz.open(build / 'bibliography/bibliography.pdf') as document:
        check_bibliography(document, engine, {'Erdős': 3, 'Soberón': 3, 'Birkhäuser': 3})
    with fitz.open(build / 'main/main.pdf') as document:
        # The example uses abbrv.bst: full first names become initials, but
        # surnames, publisher accents and Western numeric labels must survive.
        bibliography_start = next(i for i, page in enumerate(document)
                                  if '[1]' in page.get_text() and 'Andreescu' in page.get_text())
        check_bibliography(list(document)[bibliography_start:], engine,
                           {'Erdős': 1, 'Soberón': 1, 'Birkhäuser': 2})
        text = ' '.join(page.get_text() for page in document)
        check('[8]' in text and '[৮]' not in text,
              f'{engine}: example bibliography should retain Western labels')
        check_body_line_spacing(document, engine)
    with fitz.open(build / 'boxes/boxes.pdf') as document:
        check_body_line_spacing(document, engine)
    with fitz.open(build / 'quotations/quotations.pdf') as document:
        spans = [span for page in document
                 for block in page.get_text('dict')['blocks'] if 'lines' in block
                 for line in block['lines'] for span in line['spans']]
        # Check both sides of a script switch, then the attribution and body.
        for word, font in (('Chorus', 'TeXGyreChorus-MediumItal'),
                           ('Bold', 'TeXGyreChorus-MediumItal'),
                           ('Default', 'TeXGyrePagella-Regular'),
                           ('Body', 'TeXGyrePagella-Regular'),
                           ('Ordinary', 'TeXGyrePagella-Italic')):
            matching = [span for span in spans if word in span['text']]
            check(bool(matching) and all(span['font'] == font for span in matching),
                  f'{engine}: wrong quotation font for {word}')
        quotation_size = next(span['size'] for span in spans if 'Chorus' in span['text'])
        attribution_size = next(span['size'] for span in spans if 'Default' in span['text'])
        check(abs(quotation_size / attribution_size - 1.05) < .001,
              f'{engine}: quotation font should be scaled to 105%')

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
        check(any('TeXGyreChorus' in font[3]
                  for page in document for font in page.get_fonts()),
              f'{engine}: English quotation font lost in Assamese mode')
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
    print(f'{engine}: PDF fonts, bibliography, line spacing, hints, links and chapter designs passed')
