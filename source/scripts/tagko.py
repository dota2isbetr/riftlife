T={"Ahri":"아리","Akali":"아칼리","Akshan":"아크샨","Ambessa":"암베사","Anivia":"애니비아","Annie":"애니","Aphelios":"아펠리오스","Ashe":"애쉬","Azir":"아지르","Bard":"바드","Blitzcrank":"블리츠크랭크","Caitlyn":"케이틀린","Darius":"다리우스","Diana":"다이애나","Dr. Mundo":"문도 박사","Draven":"드레이븐","Ekko":"에코","Evelynn":"이블린","Ezreal":"이즈리얼","Fiora":"피오라","Fizz":"피즈","Galio":"갈리오","Gangplank":"갱플랭크","Garen":"가렌","Graves":"그레이브즈","Heimerdinger":"하이머딩거","Hwei":"흐웨이","Illaoi":"일라오이","Irelia":"이렐리아","Ivern":"아이번","Janna":"잔나","Jarvan IV":"자르반 4세","Jax":"잭스","Jayce":"제이스","Jhin":"진","Jinx":"징크스","K'Sante":"크산테","Kai'Sa":"카이사","Karma":"카르마","Karthus":"카서스","Katarina":"카타리나","Kayle":"케일","Kayn":"케인","Kennen":"케넨","Kha'Zix":"카직스","Kog'Maw":"코그모","LeBlanc":"르블랑","Lee Sin":"리 신","Leona":"레오나","Lillia":"릴리아","Lucian":"루시안","Lulu":"룰루","Lux":"럭스","Malzahar":"말자하","Master Yi":"마스터 이","Mel":"멜","Miss Fortune":"미스 포츈","Mordekaiser":"모데카이저","Morgana":"모르가나","Nami":"나미","Nasus":"나서스","Neeko":"니코","Nidalee":"니달리","Nilah":"닐라","Nocturne":"녹턴","Orianna":"오리아나","Ornn":"오른","Poppy":"뽀삐","Pyke":"파이크","Qiyana":"키아나","Rek'Sai":"렉사이","Rell":"렐","Renata Glasc":"레나타 글라스크","Renekton":"레넥톤","Rengar":"렝가","Riven":"리븐","Rumble":"럼블","Seraphine":"세라핀","Sett":"세트","Shen":"쉔","Sivir":"시비르","Sona":"소나","Soraka":"소라카","Swain":"스웨인","Syndra":"신드라","Taric":"타릭","Teemo":"티모","Tryndamere":"트린다미어","Twisted Fate":"트위스티드 페이트","Udyr":"우디르","Vayne":"베인","Vex":"벡스","Vi":"바이","Viktor":"빅토르","Volibear":"볼리베어","Warwick":"워윅","Xerath":"제라스","Xin Zhao":"신 짜오","Yasuo":"야스오","Yone":"요네","Yuumi":"유미","Zed":"제드","Ziggs":"직스","Zilean":"질리언",
"Bandle City":"밴들 시티","Bilgewater":"빌지워터","Demacia":"데마시아","Freljord":"프렐요드","Icathia":"이케시아","Ionia":"아이오니아","Ixtal":"익스탈","Mount Targon":"타곤 산","Noxus":"녹서스","Piltover":"필트오버","Shadow Isles":"그림자 군도","Shurima":"슈리마","The Void":"공허","Zaun":"자운",
"Bird":"새","Cat":"고양이","Demon":"악마","Dog":"개","Dragon":"용","Fae":"요정","Mech":"기계","Pirate":"해적","Poro":"포로","Spider":"거미","Spirit":"정령","Yordle":"요들"}
import json,sys
d=json.load(open('cards.json'))
champs=set(T)
n=0
for c in d['cards']:
    tk=[T[t] for t in c.get('tg',[]) if t in T]
    if tk: c['tk']=tk
    if c['ko']==0 and c['n'] in champs: c['nk']=T[c['n']]; c['ko']=1; n+=1
import collections; print('filled',n, collections.Counter(c['ko'] for c in d['cards']))
json.dump(d,open('cards.json','w',encoding='utf-8'),ensure_ascii=False,separators=(',',':'))
