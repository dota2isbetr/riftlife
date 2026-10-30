import json,re,html,glob,collections
cards=json.load(open('cards.json'))['cards']; byid={c['id']:c for c in cards}
raw=json.load(open('decks_raw.json'))
ORDER=['OGN','OGS','SFD','UNL','VEN','RAD']
META={'OGN':('Origins','오리진'),'SFD':('Spiritforged','스피릿포지드'),'UNL':('Unleashed','언리시드'),'VEN':('Vendetta','벤데타'),'RAD':('Radiance','레디언스')}
# players: largest "N players" figure in the article intro (deck sections also say "1 / 31 players")
for ev in raw['events']:
    f=glob.glob('rd/arts/*'+ev['slug']+'.html')[0]
    d=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',open(f,encoding='utf-8').read(),re.S).group(1))
    body=''.join(b['richText']['body'] for b in d['props']['pageProps']['page']['blades'] if b['type']=='articleRichText')
    intro=re.sub(r'\s+',' ',html.unescape(re.sub(r'<[^>]+>',' ',body.split('<h1')[0].split('<h2')[0])))
    nums=[int(x.replace(',','')) for x in re.findall(r'(\d[\d,]*)\+?\s+(?:players|competitors|participants)',intro)]
    nums=[n for n in nums if n>=100]; ev['players']=max(nums) if nums else None
    used=collections.Counter()
    for dk in raw['decks']:
        if dk['ev']==ev['slug']:
            for k in ['main','bf','runes','side']:
                for i,n in dk[k]: used[byid[i]['set']]+=n
    ev['meta']=max((s for s in used if s!='OGS'),key=ORDER.index)
events=sorted(raw['events'],key=lambda e:e['date']); eidx={e['slug']:i for i,e in enumerate(events)}
merged={}
for dk in raw['decks']:
    # same list printed in both the Best-of and Top 8 sections (sometimes with a typo'd name or a different 3rd/4th label): keep one, trust Top 8's rank
    key=(dk['ev'],dk['legend'],dk['champion'],tuple(sorted(map(tuple,dk['main']))))
    g='top8' if (dk['group'] or '').lower().startswith('top') else 'best'
    if key in merged:
        m=merged[key]; m['g'].add(g)
        if g=='top8' and dk.get('rank'): m['rank']=dk['rank']
        if len(dk['player'])>len(m['player']): m['player']=dk['player']
        continue
    dk=dict(dk); dk['g']={g}; merged[key]=dk
ix=lambda i: byid[i]['ix']
out=[]
for dk in merged.values():
    o={'e':eidx[dk['ev']],'p':dk['player'],'r':dk.get('rank'),'L':ix(dk['legend']),'C':ix(dk['champion']) if dk['champion'] else None,
       'm':[[ix(i),n] for i,n in dk['main']],'b':[ix(i) for i,n in dk['bf']],'u':[[ix(i),n] for i,n in dk['runes']],'s':[[ix(i),n] for i,n in dk['side']],
       't8':1 if 'top8' in dk['g'] else 0}
    if dk.get('lrank'): o['lr']=[dk['lrank'],dk.get('lof')]
    if dk.get('note'): o['note']=dk['note']
    out.append(o)
out.sort(key=lambda o:(-events[o['e']]['date'].__hash__()*0+o['e'],o['r'] or 9999))
def ids(*names):
    res=[]
    for n in names:
        k=re.sub(r'[^a-z0-9]','',n.lower().replace('’',"'"))
        hit=[c for c in cards if re.sub(r'[^a-z0-9]','',(c['n']+(', '+c['s'] if c.get('s') else '')).lower())==k or re.sub(r'[^a-z0-9]','',c['n'].lower())==k]
        assert hit,n; res.append(n)
    return res
bans=[
 {'date':'2026-03-31','fmt':'std','names':ids('Called Shot','Draven, Vanquisher','Fight or Flight','Scrapheap','The Dreaming Tree','Obelisk of Power',"Reaver's Row")},
 {'date':'2026-07-24','fmt':'std','names':ids('Stealthy Pursuer',"The Arena's Greatest","Aspirant's Climb")},
 {'date':'2026-07-24','fmt':'2v2','names':['Master Yi, Wuju Bladesman']},
 {'date':'2026-09-18','fmt':'std','names':ids('Ekko, Recurrent','Stacked Deck')},
]
metas=[{'id':s,'en':META[s][0],'ko':META[s][1]} for s in ORDER if s in META and any(e['meta']==s for e in events)]
json.dump({'events':[{k:e[k] for k in ['en','ko','title','date','players','url','meta']} for e in events],'decks':out,'bans':bans,'metas':metas,
  'source':'playriftbound.com Organized Play top-deck articles'},open('meta.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
import os
print(len(out),'decks', os.path.getsize('meta.json'),'bytes')
print(collections.Counter((events[o['e']]['meta'], 'top4' if (o['r'] or 99)<=4 else 'top8' if (o['r'] or 99)<=8 else 'other') for o in out))
for e in events: print(e['date'],e['en'],e['players'],e['meta'])
