import os, subprocess
OUT='/home/claude/plpost2/post4'
CSS="""
:root{--navy:#14284b;--navy2:#2a4b8c;--sun:#f5b93e;--ink:#ffffff;--muted:#c9d4ea;--card:rgba(255,255,255,.07);--line:rgba(255,255,255,.14)}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{background:radial-gradient(1000px 800px at 85% 5%,var(--navy2) 0%,var(--navy) 60%);color:var(--ink);font-family:Inter,'Noto Sans CJK SC',sans-serif;padding:90px;display:flex;flex-direction:column;position:relative;overflow:hidden}
.brand{font:700 26px Inter;letter-spacing:.2em;text-transform:uppercase;color:var(--sun)}
.pg{position:absolute;right:90px;top:90px;font:600 26px Inter;color:var(--muted)}
.time{position:relative;z-index:2;display:inline-block;align-self:flex-start;background:var(--sun);color:var(--navy);font:800 46px 'Inter Display',Inter;padding:12px 30px;border-radius:999px;margin-top:auto}
h1{position:relative;z-index:2;font:800 112px/1.0 'Inter Display',Inter;letter-spacing:-.035em;margin-top:auto}
h2{position:relative;z-index:2;font:800 86px/1.04 'Inter Display',Inter;letter-spacing:-.03em;margin-top:34px}
p{position:relative;z-index:2;font:500 42px/1.4 Inter;color:var(--muted);margin-top:30px}
p b{color:var(--ink);font-weight:700}
.tip{position:relative;z-index:2;margin-top:40px;background:var(--card);border:2px solid var(--line);border-radius:28px;padding:28px 34px;font:500 34px/1.4 Inter;color:var(--ink)}
.tip span{color:var(--sun);font-weight:700}
.foot{position:relative;z-index:2;margin-top:60px;font:500 28px Inter;color:var(--muted);display:flex;justify-content:space-between}
.route{margin-top:50px;display:grid;gap:18px}
.route div{display:flex;gap:24px;align-items:center;font:600 40px Inter}
.route i{font-style:normal;background:var(--sun);color:var(--navy);font:800 30px Inter;border-radius:999px;padding:8px 18px;min-width:150px;text-align:center}
.sun{color:var(--sun)}
.zh{position:relative;z-index:2;font:600 34px "Noto Sans CJK SC";color:var(--sun);margin-top:12px;letter-spacing:.02em}
.ph{position:absolute;left:0;top:0;width:1080px;height:580px;object-fit:cover}
.phfade{position:absolute;left:0;top:0;width:1080px;height:582px;background:linear-gradient(180deg,rgba(20,40,75,.75) 0%,rgba(20,40,75,0) 28%,rgba(20,40,75,0) 62%,#14284b 100%)}
.cr{position:absolute;right:24px;top:540px;font:500 18px Inter;color:rgba(255,255,255,.75);text-shadow:0 1px 3px rgba(0,0,0,.8)}
.top{position:relative;z-index:2}
.cover .ph{height:1350px}.cover .phfade{top:0;height:1350px;background:linear-gradient(180deg,rgba(20,40,75,.35) 0%,rgba(20,40,75,.15) 35%,rgba(20,40,75,.9) 68%,#14284b 100%)}.cover .cr{top:24px}
.brand,.pg{z-index:2;position:relative}.pg{position:absolute}

"""
IMG='/home/claude/plpost2/img/'
def slide(n, body, photo=None, credit='', cls=''):
    ph=f'<img class="ph" src="file://{IMG}{photo}"><div class="phfade"></div><div class="cr">{credit}</div>' if photo else ''
    open(f'{OUT}/s{n}.html','w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{ph}{body}</body></html>')
    return f'{OUT}/s{n}.html'
T=5
S=[]
S.append(slide(1,f'''<div class="brand">Pocket Local · Singapore</div>
<h1>Half a day in <span class="sun">Katong & Joo Chiat</span></h1>
<div class="zh">加东与如切 · 半日游</div>
<p>Colourful shophouses, laksa and kueh. A side of Singapore most tourists miss.</p>
<div class="foot"><span>@pocketlocal.sg</span><span>Swipe →</span></div>''',photo='ks.jpg',credit='Photo: Basile Morin, CC BY-SA 4.0',cls='cover'))
S.append(slide(2,f'''<div class="brand">Pocket Local · Singapore</div><div class="pg">2/{T}</div>
<div class="time">Morning</div>
<h2>The colourful houses</h2>
<div class="zh">如切彩色娘惹排屋</div>
<p>Peranakan shophouses along Koon Seng Road and Joo Chiat Road. Go in the morning when it's cooler, great for family photos.</p>
<div class="foot"><span>@pocketlocal.sg</span><span>Swipe →</span></div>''',photo='jc.jpg',credit='Photo: Kate Branch, CC BY-SA 4.0'))
S.append(slide(3,f'''<div class="brand">Pocket Local · Singapore</div><div class="pg">3/{T}</div>
<div class="time">Lunch</div>
<h2>Katong laksa</h2>
<div class="zh">加东叻沙</div>
<p>Short rice noodles in spicy coconut broth. The noodles are cut short so you eat it with just a spoon. Must try when you're here.</p>
<div class="foot"><span>@pocketlocal.sg</span><span>Swipe →</span></div>''',photo='laksa.jpg',credit='Photo: ProjectManhattan, CC0'))
S.append(slide(4,f'''<div class="brand">Pocket Local · Singapore</div><div class="pg">4/{T}</div>
<div class="time">Snack</div>
<h2>Nyonya kueh</h2>
<div class="zh">娘惹糕</div>
<p>Colourful Peranakan cakes. Get a mix to share, kids always go for the rainbow ones.</p>
<div class="foot"><span>@pocketlocal.sg</span><span>Swipe →</span></div>''',photo='kueh.jpg',credit='Photo: ProjectManhattan, CC BY-SA 3.0'))
S.append(slide(5,f'''<div class="brand">Pocket Local · Singapore</div><div class="pg">5/{T}</div>
<h2 style="margin-top:auto">Getting there 🚇</h2>
<div class="zh">怎么去：褐线到马林百列站 · 先逛本地邻里中心</div>
<p>Brown line to <b>Marine Parade</b>. You come out at Marine Parade Central, a real local neighbourhood with a hawker centre. Then cross the road into Katong.</p>
<div class="tip"><span>Local tip:</span> too hot or raining? Parkway Parade mall is right there for air-con and shelter.</div>
<p style="font-size:34px">Save this for your trip 📌 Want a plan like this? DM us, we're locals 😊</p>
<div class="foot"><span>@pocketlocal.sg</span><span>口袋本地通</span></div>'''))
js="const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});for(const f of process.argv.slice(1)){await p.goto('file://'+f);await p.waitForTimeout(250);await p.screenshot({path:f.replace('.html','.jpg'),type:'jpeg',quality:92});}await b.close();})()"
subprocess.run(['node','-e',js,*S],check=True,env={**os.environ,'NODE_PATH':subprocess.check_output(['npm','root','-g'],text=True).strip()})
print('ok')
