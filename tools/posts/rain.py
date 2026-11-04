import os, subprocess
OUT='/home/claude/posts7/out'
src=open('/home/claude/plpost2/post4.py').read()
CSS=src.split('CSS="""')[1].split('"""')[0]
CSS+="""
.list{position:relative;z-index:2;margin-top:40px;display:grid;gap:0}
.row{display:flex;justify-content:space-between;align-items:center;padding:15px 0;border-bottom:2px solid var(--line)}
.row:last-child{border-bottom:0}
.row b{font:700 38px Inter;color:var(--ink)}
.row span{font:500 34px Inter;color:var(--sun);text-align:right}
.hd{position:relative;z-index:2;margin-top:56px}
.hd h2{margin-top:0;font-size:78px}
"""
IMG='/home/claude/plpost2/img/'
B='<div class="brand">Pocket Local · Singapore</div>'
F='<div class="foot"><span>@pocketlocal.sg</span><span>Swipe →</span></div>'
T=6
def slide(n,body,photo=None,credit='',cls=''):
    ph=f'<img class="ph" src="file://{IMG}{photo}"><div class="phfade"></div><div class="cr">{credit}</div>' if photo else ''
    p=f'{OUT}/{n}.html'; open(p,'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{ph}{body}</body></html>'); return p
S=[]
S.append(slide('r1',f'''{B}
<h1>Rainy day cheat sheet: <span class="sun">MRT stations with a mall right there</span></h1>
<div class="zh">下雨天攻略 · 直通商场的地铁站</div>
<p>Rain here usually passes in 30 to 60 minutes. Hop off at one of these, stay dry, grab a snack, then carry on.</p>
{F}''',photo='mrt.jpg',credit='Photo: ZKang123, CC BY-SA 4.0',cls='cover'))
groups=[
 ('City & Orchard','市区 · 乌节路',[('Orchard','ION Orchard'),('Somerset','313@Somerset'),('Dhoby Ghaut','Plaza Singapura'),('City Hall','Raffles City'),('Bugis','Bugis Junction'),('Esplanade','CityLink / Suntec'),('Promenade','Suntec / Marina Square'),('Clarke Quay','Clarke Quay Central'),('Chinatown','Chinatown Point'),('Great World','Great World'),('Novena','Square 2 / Velocity')]),
 ('South & West','南部 · 西部',[('HarbourFront','VivoCity'),('Tiong Bahru','Tiong Bahru Plaza'),('Jurong East','JEM'),('Clementi','The Clementi Mall'),('Beauty World','Beauty World Centre'),('Bukit Panjang','Hillion Mall'),('Yew Tee','YewTee Point')]),
 ('North & Northeast','北部 · 东北部',[('Toa Payoh','HDB Hub'),('Bishan','Junction 8'),('Upper Thomson','Thomson Plaza'),('Ang Mo Kio','AMK Hub'),('Yishun','Northpoint City'),('Woodlands','Causeway Point'),('Serangoon','NEX'),('Hougang','Hougang Mall'),('Sengkang','Compass One'),('Punggol','Waterway Point')]),
 ('East','东部',[('Lavender','Aperia Mall'),('Paya Lebar','Paya Lebar Quarter'),('Tai Seng','18 Tai Seng'),('Bedok','Bedok Mall'),('Tampines','Tampines Mall'),('Simei','Eastpoint Mall'),('Pasir Ris','White Sands'),('Expo','Changi City Point')]),
]
for i,(h,z,rows) in enumerate(groups,2):
    r=''.join(f'<div class="row"><b>{a}</b><span>{b}</span></div>' for a,b in rows)
    S.append(slide(f'r{i}',f'''{B}<div class="pg">{i}/{T}</div>
<div class="hd"><h2>{h}</h2><div class="zh">{z}</div></div>
<div class="list">{r}</div>
<div class="foot" style="margin-top:auto"><span>@pocketlocal.sg</span><span>Swipe →</span></div>'''))
S.append(slide('r6',f'''{B}<div class="pg">6/{T}</div>
<h2 style="margin-top:auto">Save this for your trip</h2>
<div class="zh">收藏起来，下雨不用慌</div>
<p>Most are linked underground or by a covered walkway. A few are a short sheltered walk.</p>
<div class="tip"><span>Want a day planned around the weather?</span> Comment "PLAN" and I'll send you my free 1-day plan.</div>
<div class="foot"><span>Your local friend in Singapore</span><span>@pocketlocal.sg</span></div>'''))
js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});for(const f of process.argv.slice(1)){await p.goto('file://'+f);await p.waitForTimeout(250);await p.screenshot({path:f.replace('.html','.jpg'),type:'jpeg',quality:92});}await b.close();})()"
subprocess.run(['node','-e',js,*S],check=True,env={**os.environ,'NODE_PATH':subprocess.check_output(['npm','root','-g'],text=True).strip()})
for f in S: os.remove(f)
print('ok')
