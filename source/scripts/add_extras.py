"""Append promo / regional cards from data/extras.json to data/cards.json and pack their images.

Run from the repo root:  python3 -I source/scripts/add_extras.py [--fetch]
--fetch crops each card out of its official news image (img URL) into source/extras/<id>.webp first.
Extras always go after the gallery cards, so gallery ix values (and meta.json, which indexes CARDS) stay put.
Each extra gets 'after' = the printing it sits next to in set order.
"""
import json, os, sys, io, urllib.request
from PIL import Image, ImageChops, ImageDraw

root = os.getcwd(); src = os.path.join(root, 'source')
cpath = os.path.join(src, 'data', 'cards.json')
d = json.load(open(cpath, encoding='utf-8'))
ex = json.load(open(os.path.join(src, 'data', 'extras.json'), encoding='utf-8'))['cards']
cards = [c for c in d['cards'] if 'x' not in c]        # drop extras from a previous run
byid = {c['id']: c for c in cards}
G = d['img']; CW, CH, DN, TW, TH, TN = G['cw'], G['ch'], G['dn'], G['tw'], G['th'], G['tn']
edir = os.path.join(src, 'extras')

def crop_card(url):
    im = Image.open(io.BytesIO(urllib.request.urlopen(url).read())).convert('RGB')
    diff = ImageChops.difference(im, Image.new('RGB', im.size, (255, 255, 255))).convert('L').point(lambda v: 255 if v > 24 else 0)
    l, t, r, b = diff.getbbox()
    w = round((b - t) * 744 / 1039); cx = (l + r) // 2      # card aspect 744x1039, centred on the content box
    im = im.crop((cx - w // 2, t, cx - w // 2 + w, b)).resize((744, 1039), Image.LANCZOS)
    mask = Image.new('L', (744 * 4, 1039 * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 744 * 4 - 1, 1039 * 4 - 1), radius=30 * 4, fill=255)
    out = Image.new('RGB', im.size, (0, 0, 0)); out.paste(im, (0, 0), mask.resize(im.size, Image.LANCZOS))   # black corners like the gallery art
    return out

if '--fetch' in sys.argv:
    os.makedirs(edir, exist_ok=True)
    for e in ex: crop_card(e['img']).save(os.path.join(edir, e['id'] + '.webp'), 'WEBP', quality=90)

order = {c['id']: i for i, c in enumerate(cards)}
n0 = len(cards); new = []
for j, e in enumerate(ex):
    b = byid[e['base']]
    c = {k: v for k, v in b.items() if k not in ('ix', 'wh', 'rot')}
    c.update({k: v for k, v in e.items() if k not in ('base', 'src')})
    c['no'] = b['no']; c['ix'] = n0 + j
    # place right after the last printing of the same set+number (e.g. 303a after 303*)
    c['after'] = max((x for x in cards if x['set'] == b['set'] and x['no'] == b['no']), key=lambda x: order[x['id']])['id']
    im = Image.open(os.path.join(edir, e['id'] + '.webp')).convert('RGB')
    im = im.resize((CW, round(im.height * CW / im.width)), Image.LANCZOS).crop((0, 0, CW, CH))
    c['wh'] = [im.width, im.height]; new.append((c, im))

def put(prefix, n, cw, ch, items, fit):
    per = n * n; sheets = {}
    for c, im in items:
        s, k = divmod(c['ix'], per)
        if s not in sheets:
            p = os.path.join(root, 'img', f'{prefix}{s:03d}.webp')
            sheets[s] = Image.open(p).convert('RGB') if k and os.path.exists(p) else Image.new('RGB', (n * cw, n * ch), (20, 28, 36))
        t = fit(im)
        sheets[s].paste(t, ((k % n) * cw + (cw - t.width) // 2, (k // n) * ch + (ch - t.height) // 2))
    for s, sh in sheets.items():
        sh.save(os.path.join(root, 'img', f'{prefix}{s:03d}.webp'), 'WEBP', quality=82 if prefix == 'd' else 72, method=6)
    return sorted(sheets)

def thumb(im):
    t = im.copy(); t.thumbnail((TW, TH), Image.LANCZOS); return t

print('detail sheets', put('d', DN, CW, CH, new, lambda im: im))
print('thumb sheets', put('t', TN, TW, TH, new, thumb))
d['cards'] = cards + [c for c, _ in new]
json.dump(d, open(cpath, 'w', encoding='utf-8'), ensure_ascii=False, separators=(',', ':'))
print('cards', len(cards), '+', len(new))
