import json,sys,os
from PIL import Image
raw,out=sys.argv[1],sys.argv[2]
os.makedirs(out+'/img',exist_ok=True)
d=json.load(open('cards.json'))
CW,CH,DN=420,588,4      # detail cell, 4x4 per sheet
TW,TH,TN=80,112,8       # thumb cell, 8x8 per sheet
cards=d['cards']; sizes=[]
def sheet(n,cw,ch): return Image.new('RGB',(n*cw,n*ch),(20,28,36))
dsheet=tsheet=None
for i,c in enumerate(cards):
    im=Image.open(f"{raw}/{c['id']}.webp").convert('RGB')
    rot=0
    if im.width>im.height: im=im.rotate(90,expand=True); rot=1      # store landscape cards upright in a portrait cell
    if im.width!=CW: im=im.resize((CW,round(im.height*CW/im.width)),Image.LANCZOS)
    im=im.crop((0,0,CW,min(im.height,CH)))
    c['ix']=i; c['wh']=[im.width,im.height] if not rot else [im.height,im.width]; 
    if rot: c['rot']=1
    k=i%(DN*DN)
    if k==0: dsheet=sheet(DN,CW,CH)
    dsheet.paste(im,((k%DN)*CW,(k//DN)*CH))
    if k==DN*DN-1 or i==len(cards)-1:
        p=f"{out}/img/d{i//(DN*DN):03d}.webp"; dsheet.save(p,'WEBP',quality=82,method=6); sizes.append(os.path.getsize(p))
    # thumbs: show orientation as-is, fitted inside the portrait cell
    t=Image.open(f"{raw}/{c['id']}.webp").convert('RGB'); t.thumbnail((TW,TH),Image.LANCZOS)
    k2=i%(TN*TN)
    if k2==0: tsheet=sheet(TN,TW,TH)
    tsheet.paste(t,((k2%TN)*TW+(TW-t.width)//2,(k2//TN)*TH+(TH-t.height)//2))
    if k2==TN*TN-1 or i==len(cards)-1:
        p=f"{out}/img/t{i//(TN*TN):03d}.webp"; tsheet.save(p,'WEBP',quality=72,method=6)
d['img']={'cw':CW,'ch':CH,'dn':DN,'tw':TW,'th':TH,'tn':TN}
json.dump(d,open('cards.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
print('detail sheets',len(sizes),'MB',round(sum(sizes)/1e6,1))
