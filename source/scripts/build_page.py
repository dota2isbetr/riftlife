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
import json
# meta.json comes from the official-article pipeline (build_meta.py); meta_extra.json holds other events' top decks with card ids
_meta = json.load(open(os.path.join(src, 'data', 'meta.json'), encoding='utf-8'))
_extra = json.load(open(os.path.join(src, 'data', 'meta_extra.json'), encoding='utf-8'))
_ix = {c['id']: c['ix'] for c in json.load(open(os.path.join(src, 'data', 'cards.json'), encoding='utf-8'))['cards']}
_e0 = len(_meta['events']); _meta['events'] += _extra['events']
for d in _extra['decks']:
    d = dict(d, e=d['e'] + _e0, L=_ix[d['L']], C=_ix[d['C']] if d.get('C') else None, b=[_ix[i] for i in d['b']],
             m=[[_ix[i], n] for i, n in d['m']], u=[[_ix[i], n] for i, n in d['u']], s=[[_ix[i], n] for i, n in d['s']])
    _meta['decks'].append(d)
meta = json.dumps(_meta, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
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
