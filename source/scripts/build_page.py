"""Assemble the published page: source/template.html + data/*.json -> index.html (repo root).

Run from the repository root:  python3 source/scripts/build_page.py
The claude.ai artifact version is the same page without the outer <html> wrapper
(the artifact service adds its own), written to source/build/artifact.html.
"""
import os
root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
src = os.path.join(root, 'source')
t = open(os.path.join(src, 'template.html'), encoding='utf-8').read()
cards = open(os.path.join(src, 'data', 'cards.json'), encoding='utf-8').read().replace('</', '<\\/')
meta = open(os.path.join(src, 'data', 'meta.json'), encoding='utf-8').read().replace('</', '<\\/')
page = t.replace('__DATA__', cards).replace('__META__', meta)
os.makedirs(os.path.join(src, 'build'), exist_ok=True)
open(os.path.join(src, 'build', 'artifact.html'), 'w', encoding='utf-8').write(page)
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(
    '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'
    + page + '</body></html>')
print('index.html written,', len(page), 'chars')
