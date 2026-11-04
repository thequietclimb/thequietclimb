import os,subprocess
OUT='/home/claude/posts4/out'
CSS = """
:root{--bg:#16120e;--bg2:#221b15;--ink:#f3ebe0;--muted:#a89d8f;--line:#3a3028;--accent:#e0864c;--pos:#6fcf8e}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:1350px}
body{background:radial-gradient(1100px 800px at 90% 0%,#2c2118 0%,var(--bg) 62%);color:var(--ink);font-family:Inter,sans-serif;padding:96px 90px;display:flex;flex-direction:column;position:relative}
.brand{font:700 26px 'Inter Display',Inter;letter-spacing:.22em;text-transform:uppercase;color:var(--accent)}
.pg{position:absolute;right:90px;top:96px;font:600 26px Inter;color:var(--muted);font-variant-numeric:tabular-nums}
h1{font:800 104px/1.02 'Inter Display',Inter;letter-spacing:-.035em;margin-top:auto}
h2{font:800 84px/1.05 'Inter Display',Inter;letter-spacing:-.03em;margin-top:70px}
p.big{font:500 46px/1.35 Inter;color:var(--ink);margin-top:40px}
p.mut{font:500 38px/1.4 Inter;color:var(--muted);margin-top:28px}
.acc{color:var(--accent)}
.list{display:grid;gap:26px;margin-top:60px}
.item{display:grid;grid-template-columns:84px 1fr;gap:24px;align-items:start;background:var(--bg2);border:2px solid var(--line);border-radius:30px;padding:30px 34px}
.item .n{font:800 52px/1 'Inter Display',Inter;color:var(--accent)}
.item b{display:block;font:700 38px/1.25 Inter}
.item span{display:block;font:500 30px/1.35 Inter;color:var(--muted);margin-top:6px}
.foot{margin-top:auto;font:500 28px Inter;color:var(--muted);display:flex;justify-content:space-between}
.handle{font:800 70px 'Inter Display',Inter;letter-spacing:-.02em;margin-top:40px}
.acct{background:var(--bg2);border:2px solid var(--line);border-radius:30px;padding:34px 38px;margin-top:28px}
.acct .t{font:600 24px Inter;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}
.acct b{display:block;font:800 60px 'Inter Display',Inter;margin:6px 0}
.acct span{font:500 30px Inter;color:var(--muted)}
.cover{padding:0}
.cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;object-position:50% 20%}
.cover .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(22,18,14,0) 35%,rgba(22,18,14,.92) 72%,#16120e 100%)}
.cover .txt{position:absolute;left:90px;right:90px;bottom:96px}
.cover h1{font-size:112px}
"""

def slide(name, body, cls=''):
    html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body class="{cls}">{body}</body></html>'
    p = f'{OUT}/{name}.html'; open(p, 'w').write(html); return p
def render(S):
    js = "const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1350}});for(const f of process.argv.slice(1)){await p.goto('file://'+f);await p.waitForTimeout(250);await p.screenshot({path:f.replace('.html','.jpg'),type:'jpeg',quality:92});}await b.close();})()"
    subprocess.run(['node','-e',js,*S],check=True,env={**os.environ,'NODE_PATH':subprocess.check_output(['npm','root','-g'],text=True).strip()})
