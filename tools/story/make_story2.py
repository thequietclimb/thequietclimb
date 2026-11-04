"""Combined daily Story card (two accounts) for The Quiet Climb, 1080x1920 PNG.
Usage: python3 make_story2.py day2.json out.png
day2.json: {date, lesson, accounts:[{name, phase, amount, pct, balance, start_balance, trades, wins, losses, rules_kept, rules_total, progress, target}]}
"""
import json, sys, os, html, datetime, subprocess
d = json.load(open(sys.argv[1])); out = os.path.abspath(sys.argv[2]); e = html.escape
date_s = datetime.date.fromisoformat(d['date']).strftime('%a %-d %b %Y')
def cls(x): return 'pos' if x > 0 else ('neg' if x < 0 else 'flat')
def money(x): return f'{"+" if x > 0 else ("-" if x < 0 else "")}${abs(x):,.2f}'
total = sum(a['amount'] for a in d['accounts'])
cards = ''
for a in d['accounts']:
    ok = a['rules_kept'] == a['rules_total']
    prog = ''
    if a.get('target'):
        pct = max(0, min(100, a['progress'] / a['target'] * 100))
        prog = f'<div class="row"><span>Challenge progress</span><span>{a["progress"]:+.2f}% of {a["target"]:g}%</span></div><div class="bar"><i style="width:{pct:.1f}%"></i></div>'
    cards += f'''<div class="card">
<div class="top"><div><div class="nm">{e(a["name"])}</div><div class="ph">{e(a["phase"])}</div></div>
<div class="r"><div class="pct {cls(a["pct"])}">{a["pct"]:+.2f}%</div><div class="amt {cls(a["amount"])}">{money(a["amount"])}</div></div></div>
<div class="bal"><span>Balance</span><b>${a["balance"]:,.0f} <i>/ ${a["start_balance"]:,.0f}</i></b></div>
<div class="mini"><span><b>{a["trades"]}</b> trades</span><span><b>{a["wins"]}–{a["losses"]}</b> win–loss</span><span><b class="{"ok" if ok else "warn"}">{a["rules_kept"]}/{a["rules_total"]}</b> rules</span></div>
{prog}</div>'''
page = f'''<!doctype html><html><head><meta charset="utf-8"><style>
:root{{--bg:#16120e;--bg2:#221b15;--ink:#f3ebe0;--muted:#a89d8f;--line:#3a3028;--accent:#e0864c;--pos:#6fcf8e;--neg:#ef7a62}}
*{{box-sizing:border-box;margin:0;padding:0}}html,body{{width:1080px;height:1920px}}
body{{background:radial-gradient(1200px 900px at 85% 10%,#2c2118 0%,var(--bg) 60%);color:var(--ink);font-family:Inter,sans-serif;padding:230px 80px 250px;display:flex;flex-direction:column}}
.brand{{font:700 30px "Inter Display",Inter;letter-spacing:.22em;text-transform:uppercase;color:var(--accent)}}
.date{{font:600 46px "Inter Display",Inter;margin-top:16px}}
.label{{margin-top:44px;font:600 28px Inter;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}
.tot{{font:800 150px/1 "Inter Display",Inter;letter-spacing:-.03em;margin-top:6px;font-variant-numeric:tabular-nums}}
.sub{{font:500 28px Inter;color:var(--muted);margin-top:10px}}
.card{{margin-top:36px;background:var(--bg2);border:2px solid var(--line);border-radius:32px;padding:30px 34px}}
.top{{display:flex;justify-content:space-between;align-items:flex-start}}
.nm{{font:700 40px "Inter Display",Inter}}.ph{{font:500 26px Inter;color:var(--muted);margin-top:4px}}
.r{{text-align:right}}.pct{{font:800 58px "Inter Display",Inter;font-variant-numeric:tabular-nums}}.amt{{font:600 30px Inter;margin-top:2px;font-variant-numeric:tabular-nums}}
.bal{{margin-top:22px;display:flex;justify-content:space-between;align-items:baseline}}.bal span{{font:500 26px Inter;color:var(--muted)}}.bal b{{font:700 38px "Inter Display",Inter;font-variant-numeric:tabular-nums}}.bal i{{font-style:normal;font-weight:500;color:var(--muted)}}
.mini{{display:flex;gap:30px;margin-top:18px;font:500 26px Inter;color:var(--muted)}}.mini b{{color:var(--ink);font-weight:700;font-size:30px}}
.row{{display:flex;justify-content:space-between;font:500 24px Inter;color:var(--muted);margin-top:20px}}
.bar{{height:16px;border-radius:999px;background:var(--line);margin-top:10px;overflow:hidden}}.bar i{{display:block;height:100%;background:var(--accent)}}
.pos{{color:var(--pos)}}.neg{{color:var(--neg)}}.flat{{color:var(--ink)}}.ok{{color:var(--pos)!important}}.warn{{color:var(--accent)!important}}
.lesson{{margin-top:40px;border-left:6px solid var(--accent);padding:4px 0 4px 28px;font:500 32px/1.4 Inter}}
.lesson small{{display:block;font:600 22px Inter;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:8px}}
.foot{{margin-top:auto;padding-top:30px;font:500 26px Inter;color:var(--muted);display:flex;justify-content:space-between}}
</style></head><body>
<div class="brand">The Quiet Climb · Trading log</div>
<div class="date">{e(date_s)}</div>
<div class="label">Today, both accounts</div>
<div class="tot {cls(total)}">{money(total)}</div>
<div class="sub">net after commission</div>
{cards}
{f'<div class="lesson"><small>Lesson</small>{e(d["lesson"])}</div>' if d.get('lesson') else ''}
<div class="foot"><span>thequietclimbsg.com/trading</span><span>Not financial advice</span></div>
</body></html>'''
src = out.replace('.png', '.html'); open(src, 'w').write(page)
js = f"""const {{chromium}}=require('playwright');(async()=>{{const b=await chromium.launch();const p=await b.newPage({{viewport:{{width:1080,height:1920}}}});
await p.goto('file://{src}');await p.waitForTimeout(300);await p.screenshot({{path:'{out}'}});await b.close();}})()"""
subprocess.run(['node', '-e', js], check=True, env={**os.environ, 'NODE_PATH': subprocess.check_output(['npm', 'root', '-g'], text=True).strip()})
os.remove(src); print(out)
