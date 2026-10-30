import json,re,sys
html=open(sys.argv[1],encoding='utf-8').read()
m=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',html,re.S)
d=json.loads(m.group(1))
json.dump(d,open(sys.argv[2],'w',encoding='utf-8'),ensure_ascii=False)
# find list of cards
def walk(o,path):
    if isinstance(o,list) and len(o)>200 and isinstance(o[0],dict):
        print(path,len(o),list(o[0].keys())[:30])
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+'.'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o[:50]): walk(v,path+f'[{i}]')
walk(d,'')
