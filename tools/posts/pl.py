import os, subprocess, shutil
OUT = '/home/claude/posts6/out'
src = open('/home/claude/plpost2/post4.py').read()
CSS = src.split('CSS="""')[1].split('"""')[0]
CSS += """.n{position:relative;z-index:2;font:800 200px/1 'Inter Display',Inter;color:var(--sun);margin-top:auto;letter-spacing:-.04em}
.pdf{position:relative;z-index:2;display:flex;justify-content:center;margin-top:40px}.pdf img{height:860px;border-radius:18px;box-shadow:0 20px 60px rgba(0,0,0,.45)}"""
IMG = '/home/claude/plpost2/img/'
for f in ['p-1.jpg','p-2.jpg','p-3.jpg','p-4.jpg']: shutil.copy('/home/claude/thequietclimb/public/free/'+f, OUT+'/f'+f)
def slide(n, body, photo=None, credit='', cls=''):
    ph = f'<img class="ph" src="file://{IMG}{photo}"><div class="phfade"></div><div class="cr">{credit}</div>' if photo else ''
    p = f'{OUT}/{n}.html'
    open(p, 'w').write(f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{ph}{body}</body></html>')
    return p
B = '<div class="brand">Pocket Local · Singapore</div>'
F = '<div class="foot"><span>@pocketlocal.sg</span><span>Swipe →</span></div>'
S = []
T = 6
S.append(slide('c1', f'''{B}
<h1>Singapore with young kids: <span class="sun">5 things I wish someone told me</span></h1>
<div class="zh">带小孩玩新加坡 · 5个过来人建议</div>
<p>From a local dad who took his two boys around the world.</p>
{F}''', photo='tree.jpg', credit='Photo: Kanzcech, CC BY-SA 4.0', cls='cover'))
tips = [
 ("Go out early or late", "Plan outdoor stuff before 11am or after 5pm. The midday sun is no joke.", "户外活动安排在早上11点前或傍晚5点后"),
 ("Malls are your rest stops", "Clean toilets, baby rooms and food courts. Use them to recharge.", "商场有干净厕所、育婴室和美食街"),
 ("Hawker centres love kids", "Loud, casual, nobody minds the noise. Easy, cheap, tasty.", "小贩中心很适合带小孩"),
 ("Rain comes and goes fast", "Wait 30 to 60 minutes in a mall and carry on with your day.", "下雨通常很快就停，在商场等一下就好"),
 ("Don't pack the day too full", "One area in the morning, one in the evening. That's enough.", "一天两个区域就够了，别太赶"),
]
for i, (h, p, z) in enumerate(tips, 2):
    last = i == 6
    foot = '<div class="foot"><span>Save this for your trip 📌</span><span>@pocketlocal.sg</span></div>' if last else F
    S.append(slide(f'c{i}', f'''{B}<div class="pg">{i}/{T}</div>
<div class="n">{i-1}</div>
<h2 style="margin-top:20px">{h}</h2>
<div class="zh">{z}</div>
<p>{p}</p>
{foot}'''))
# ---- D: free plan
T = 5
S.append(slide('d1', f'''{B}
<h1>Free: <span class="sun">1 day in Singapore with kids</span></h1>
<div class="zh">免费 · 带孩子玩新加坡一日行程</div>
<p>Colourful Katong in the morning, a break from the heat, then satay and two free light shows at night.</p>
<div class="tip"><span>Get it:</span> link in bio, or comment "PLAN"</div>
{F}''', photo='spectra.jpg', credit='Photo: ScribblingGeek, CC BY-SA 4.0', cls='cover'))
for i in range(1, 5):
    foot = '<div class="foot"><span>Link in bio · comment "PLAN"</span><span>@pocketlocal.sg</span></div>' if i == 4 else F
    S.append(slide(f'd{i+1}', f'''{B}<div class="pg">{i+1}/{T}</div>
<div class="pdf"><img src="fp-{i}.jpg"></div>
{foot}'''))
js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});for(const f of process.argv.slice(1)){await p.goto('file://'+f);await p.waitForTimeout(250);await p.screenshot({path:f.replace('.html','.jpg'),type:'jpeg',quality:92});}await b.close();})()"
subprocess.run(['node', '-e', js, *S], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g'], text=True).strip()})
for f in S: os.remove(f)
print('ok')
