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
kr = open(os.path.join(src, 'data', 'samples_kr.json'), encoding='utf-8').read().replace('</', '<\\/')
import datetime
stamp = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=9))).strftime('%Y-%m-%d %H:%M KST')
page = t.replace('__DATA__', cards).replace('__META__', meta).replace('__KR__', kr).replace('__BUILD__', stamp)
os.makedirs(os.path.join(src, 'build'), exist_ok=True)
open(os.path.join(src, 'build', 'artifact.html'), 'w', encoding='utf-8').write(page)
import re
title = re.search(r'<title>.*?</title>', page).group(0)   # the standalone page carries its title in <head>
body = page.replace(title, '', 1)
open(os.path.join(root, 'index.html'), 'w', encoding='utf-8').write(
    '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    '<link rel="icon" href="favicon.ico" sizes="48x48"><link rel="icon" href="favicon.svg" type="image/svg+xml">'
    '<link rel="apple-touch-icon" href="apple-touch-icon.png"><link rel="manifest" href="site.webmanifest">'
    '<meta name="theme-color" content="#EDF1F2" media="(prefers-color-scheme: light)">'
    '<meta name="theme-color" content="#0D141B" media="(prefers-color-scheme: dark)">' + title + '</head><body>'
    + body + '</body></html>')
print('index.html written,', len(page), 'chars')
