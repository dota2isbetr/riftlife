import json,re,html,collections,sys
L=lambda l:{c['id']:c for c in json.load(open(f'{l}.json'))['props']['pageProps']['page']['blades'][2]['cards']['items']}
en,ko=L('en'),L('ko')
hang=re.compile('[가-힣]')
def txt(c):
    b=((c.get('text') or {}).get('richText') or {}).get('body') or ''
    b=re.sub(r'<br\s*/?>','\n',b); b=re.sub(r'</p>\s*<p>','\n',b); b=re.sub(r'<[^>]+>','',b)
    return html.unescape(b).strip()
def val(c,k):
    v=c.get(k); return v['value']['id'] if v and v.get('value') else None
# en->ko dictionary from cards that have Korean names
nm=collections.defaultdict(collections.Counter); sub={}
for k,c in ko.items():
    if hang.search(c['name']):
        nm[en[k]['name']][c['name']]+=1
        if en[k].get('subtitle') and c.get('subtitle'): sub[(en[k]['name'],en[k]['subtitle'])]=c['subtitle']
nm={e:k.most_common(1)[0][0] for e,k in nm.items()}
out=[]; stats=collections.Counter()
for k,e in en.items():
    k_=ko[k]; hasko=bool(hang.search(k_['name']))
    name_ko=k_['name'] if hasko else nm.get(e['name'])
    sub_ko=(k_.get('subtitle') if hasko else sub.get((e['name'],e.get('subtitle'))))
    kostate=2 if hasko else (1 if name_ko else 0)
    stats[kostate]+=1
    ct=e['cardType']
    out.append(dict(
        id=k, code=e['publicCode'], set=e['set']['value']['id'], no=e['collectorNumber'],
        n=e['name'], nk=name_ko, s=e.get('subtitle'), sk=sub_ko, ko=kostate,
        t=[x['id'] for x in ct.get('type') or []], st=[x['id'] for x in ct.get('superType') or []],
        r=val(e,'rarity'), d=[x['id'] for x in (e.get('domain') or {}).get('values',[])],
        e=val(e,'energy'), m=val(e,'might'), p=val(e,'power'),
        tg=(e.get('tags') or {}).get('tags') or [],
        tx=txt(e), txk=txt(k_) if hasko else None,
        il=', '.join(x['label'] for x in (e.get('illustrator') or {}).get('values',[])),
        img=e['cardImage']['url'].split('?')[0].replace('https://cmsassets.rgpub.io/sanity/images/dsfx7636/game_data_live/',''),
        o=e['orientation'][0]))
out.sort(key=lambda c:(c['set'],c['no'],c['id']))
for c in out:
    for kk in list(c):
        if c[kk] in (None,[],''): del c[kk]
sets=[{'id':s['id'],'en':None,'ko':s['name'],'max':s['collectorNumberMax']} for s in json.load(open('ko.json'))['props']['pageProps']['page']['blades'][2]['sets']['items']]
setsen={c['set']['value']['id']:c['set']['value']['label'] for c in en.values()}
for s in sets: s['en']=setsen[s['id']]
json.dump({'source':'playriftbound.com card gallery (en-us, ko-kr)','fetched':'2026-10-30','sets':sets,'cards':out},open('cards.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print(stats, len(out)); import os; print(os.path.getsize('cards.json'))
