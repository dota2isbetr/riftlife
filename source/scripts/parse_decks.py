import re,json,html,glob,collections,difflib
cards=json.load(open('cards.json'))['cards']
SET_ORDER=['OGN','OGS','SFD','UNL','VEN','RAD']
def nk(s): return re.sub(r'[^a-z0-9]','',re.sub(r'\bthe\b','',html.unescape(s).replace('’',"'").lower()))
def is_alt(c): return 'star' in c['id'] or bool(re.search(r'-\d+[a-z]-',c['id']))
def canon_sort(c): return (SET_ORDER.index(c['set']), is_alt(c), c['no'])
look=collections.defaultdict(list)
for c in cards:
    keys={c['n']}
    if c.get('s') and 'signature' not in c.get('st',[]): keys.add(c['n']+', '+c['s'])
    if 'legend' in c.get('t',[]):
        for t in c.get('tg',[]): keys.add(t+', '+c['n'])
    for k in keys: look[nk(k)].append(c)
KEYS=list(look)
fuzzy={}
def resolve(name):
    k=nk(name); cs=look.get(k)
    if not cs:
        m=difflib.get_close_matches(k,KEYS,n=1,cutoff=0.9)
        if not m: return None
        fuzzy[name]=sorted(look[m[0]],key=canon_sort)[0]['n']; cs=look[m[0]]
    return sorted(cs,key=canon_sort)[0]
CHAMP_TAGS={c['n'] for c in cards if 'champion' in c.get('st',[])}
LEGENDS=[c for c in cards if 'legend' in c.get('t',[]) and not is_alt(c)]
def legend_for(champ):
    cs=[l for l in LEGENDS if champ['n'] in l.get('tg',[])]
    return sorted(cs,key=canon_sort)[0] if cs else None
EVENTS={'from-garen-to-annie-rq-houstons-top-decks':('Houston','휴스턴'),'the-best-decks-out-of-bologna':('Bologna','볼로냐'),'vegas-top-decks':('Las Vegas','라스베이거스'),
 'lilles-top-decks':('Lille','릴'),'atlantas-top-decks':('Atlanta','애틀랜타'),'sydneys-top-decks':('Sydney','시드니'),'vancouvers-top-decks':('Vancouver','밴쿠버'),
 'utrechts-top-decks':('Utrecht','위트레흐트'),'barcelonas-top-decks':('Barcelona','바르셀로나'),'singapores-top-decks':('Singapore','싱가포르'),'los-angeles-top-decks':('Los Angeles','로스앤젤레스')}
LABEL=re.compile(r'^(Legend Rank|Overall Ranking|Legend|Champion|Chosen Champion|Main Deck|Main|Battlefields?|Rune Pool|Rune Deck|Runes|Sideboard)\s*:?\s*(.*)$',re.I)
SEC={'legend':'legend','champion':'champion','chosen champion':'champion','main deck':'main','main':'main','battlefields':'bf','battlefield':'bf','rune pool':'runes','rune deck':'runes','runes':'runes','sideboard':'side'}
unmatched=collections.Counter(); events=[]; decks=[]
for f in sorted(glob.glob('rd/arts/*.html')):
    slug=f.rsplit('_',1)[-1][:-5]
    if slug not in EVENTS: continue
    d=json.loads(re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',open(f,encoding='utf-8').read(),re.S).group(1))
    body=''; title=date=''
    for b in d['props']['pageProps']['page']['blades']:
        if b['type']=='articleMasthead': title=b['title']; date=b.get('publishDate','')[:10]
        if b['type']=='articleRichText': body+=b['richText']['body']
    s=re.sub(r'<h([12])[^>]*>',r'\n@@G ',body); s=re.sub(r'<h3[^>]*>',r'\n@@D ',s)
    s=re.sub(r'</?(span|em|i|a|u|meta|strong|b)\b[^>]*>','',s)
    s=re.sub(r'<[^>]+>','\n',s); s=html.unescape(s).replace('\xa0',' ')
    plain=re.sub(r'\s+',' ',s)
    m=re.search(r'(\d[\d,]*)\+?\s+players',plain); players=int(m.group(1).replace(',','')) if m else None
    ev={'slug':slug,'en':EVENTS[slug][0],'ko':EVENTS[slug][1],'title':title,'date':date,'players':players,
        'url':'https://playriftbound.com/en-us/news/'+('announcements/' if 'houston' in slug else 'organizedplay/')+slug+'/'}
    events.append(ev)
    lines=[]
    for l in s.split('\n'):
        l=re.sub(r'\s+',' ',l).strip()
        if not l: continue
        lines+= [x.strip() for x in re.split(r'(?<=[a-z!\)])(?=\d+ [A-Z])',l)]   # source typo: two card lines glued together
    group=None; cur=None; sec=None; pending_player=False; last_free=''; frag=None
    def flush():
        if cur and (cur['legend'] or cur['champion']):
            if not cur['legend'] and cur['champion']:
                lg=legend_for([c for c in cards if c['id']==cur['champion']][0]); cur['legend']=lg['id'] if lg else None; cur['legend_inferred']=True
            decks.append(cur)
    for l in lines:
        if l.startswith('@@G'): group=l[4:].strip(); continue
        if l.startswith('@@D'):
            flush(); cur={'ev':slug,'player':l[4:].strip(),'group':group,'legend':None,'champion':None,'main':[],'bf':[],'runes':[],'side':[]}; sec=None
            pending_player = not cur['player']; continue
        if cur is None: continue
        if pending_player and not LABEL.match(l): cur['player']=l; pending_player=False; continue
        m=LABEL.match(l)
        if m:
            lab=m.group(1).lower(); rest=m.group(2).strip()
            if lab=='legend rank':
                if cur['legend'] or cur['champion']:   # next deck started without its own heading; its player name was the last free-text line
                    flush(); cur={'ev':slug,'player':last_free,'group':group,'legend':None,'champion':None,'main':[],'bf':[],'runes':[],'side':[]}; sec=None
                mm=re.search(r'#?\s*(\d+)\s*/\s*(\d+)',rest)
                if mm: cur['lrank'],cur['lof']=int(mm.group(1)),int(mm.group(2))
                continue
            if lab=='overall ranking':
                mm=re.search(r'(\d+)',rest)
                if mm: cur['rank']=int(mm.group(1))
                continue
            sec=SEC[lab]
            if not rest: continue
            l=rest
        if sec is None: continue
        mm=re.match(r'^(\d+)\s*[xX]?\s+(.+)$',l)
        n,name=(int(mm.group(1)),mm.group(2).strip()) if mm else (1,l)
        c=resolve(name)
        if not c and frag and resolve(frag[1]+name):   # source split one card name across two lines ("2 Se" / "a Monkey")
            n,c=frag[0],resolve(frag[1]+name); unmatched[frag[1]]-=1
        if not c:
            unmatched[name]+=1; last_free=l; frag=(n,name)
            if sec=='bf' and name.lower() in('x','-','tbd'): cur['note']='원문 덱리스트 오류(전장 정보 없음)'
            continue
        frag=None
        t=c.get('t',[])
        if 'legend' in t: cur['legend']=c['id']; continue
        if sec=='champion': cur['champion']=c['id']; continue
        target=sec
        if sec!='side':
            if 'rune' in t: target='runes'
            elif 'battlefield' in t: target='bf'
            elif sec in('runes','bf'): target='main'
        if target=='bf' and any(e[0]==c['id'] for e in lst): cur['note']='원문 덱리스트 오류(룬 구성 누락)'; continue
        lst=cur[target]
        for e in lst:
            if e[0]==c['id']: e[1]+=n; break
        else: lst.append([c['id'],n])
    flush()
tot=lambda dk,k: sum(n for _,n in dk[k])
print('events',len(events),'decks',len(decks))
print(collections.Counter(dk['ev'][:12] for dk in decks))
print('unmatched',[x for x in unmatched.most_common(30) if x[1]>0]); print('fuzzy',fuzzy)
bad=[(dk['ev'][:10],dk['player'],tot(dk,'main'),tot(dk,'runes'),tot(dk,'bf'),tot(dk,'side'),dk.get('rank'),bool(dk['legend'])) for dk in decks if tot(dk,'main')!=39 or tot(dk,'runes')!=12 or tot(dk,'bf')!=3 or not dk.get('rank') or not dk['legend'] or not dk['champion']]
print('notes',[(dk['player'],dk.get('note')) for dk in decks if dk.get('note')])
print('irregular',len(bad)); [print(' ',b) for b in bad[:30]]
json.dump({'events':events,'decks':decks},open('decks_raw.json','w',encoding='utf-8'),ensure_ascii=False)
