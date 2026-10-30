import re,json,os,subprocess,sys,concurrent.futures as cf
seen=set(); queue=set()
for f in ['cat_op.html','p_news.html','p_news_rules-and-releases.html','a_atlantas-top-decks.html']:
    queue|=set(re.findall(r'/en-us/news/[a-z-]+/[a-z0-9-]+',open(f,encoding='utf-8').read()))
def get(u):
    fn='arts/'+u.strip('/').replace('/','_')+'.html'
    if not os.path.exists(fn):
        subprocess.run(['curl','-sSL','--max-time','40','-o',fn,'https://playriftbound.com'+u+'/'],check=False)
    try: return u,open(fn,encoding='utf-8').read()
    except: return u,''
while queue:
    batch=list(queue-seen); queue=set()
    if not batch: break
    seen|=set(batch)
    with cf.ThreadPoolExecutor(6) as ex:
        for u,s in ex.map(get,batch):
            queue|=set(re.findall(r'/en-us/news/[a-z-]+/[a-z0-9-]+',s))-seen
hits=[]
for u in sorted(seen):
    s=open('arts/'+u.strip('/').replace('/','_')+'.html',encoding='utf-8',errors='ignore').read()
    if 'Overall Ranking' in s or 'Main Deck' in s:
        m=re.search(r'"publishDate":"([^"]+)"',s); hits.append((m.group(1)[:10] if m else '?',u,s.count('Main Deck'),s.count('Overall Ranking')))
print('crawled',len(seen))
for h in sorted(hits): print(*h)
