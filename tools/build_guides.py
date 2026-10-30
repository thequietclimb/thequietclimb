"""Builds Pocket Local guide pages + the 'Local guides' section from tools/guides.json.
Run: python3 tools/build_guides.py  (from repo root). Add new posts to guides.json (newest first)."""
import json, os, shutil, html, re, datetime
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUB = os.path.join(ROOT, 'public')
G = json.load(open(os.path.join(ROOT, 'tools', 'guides.json')))
G.sort(key=lambda g: g['date'], reverse=True)
e = html.escape
SITE = 'https://pocketlocalsg.com'

def fmt(d): return datetime.date.fromisoformat(d).strftime('%-d %b %Y')

for g in G:
    d = os.path.join(PUB, 'guides', g['slug']); os.makedirs(d, exist_ok=True)
    g['imgs'] = []
    for i, src in enumerate(g['images'], 1):
        out = os.path.join(d, f'{i}.jpg')
        if os.path.exists(src):
            im = Image.open(src).convert('RGB'); im.thumbnail((1080, 1350)); im.save(out, quality=84, optimize=True, progressive=True)
        g['imgs'].append(f'/guides/{g["slug"]}/{i}.jpg')

CSS = """:root{--bg:#f5f6fa;--surface:#fff;--ink:#141c2b;--muted:#5d6678;--line:#dfe3ec;--accent:#1f3d73;--accent-ink:#fff;--warm:#b7791f}
@media (prefers-color-scheme:dark){:root{--bg:#0d1320;--surface:#151d2e;--ink:#eaeef6;--muted:#9aa6bc;--line:#263149;--accent:#f5b93e;--accent-ink:#14284b;--warm:#f5b93e}}
*{box-sizing:border-box;margin:0;padding:0}body{background:var(--bg);color:var(--ink);font:17px/1.65 Inter,"Noto Sans SC",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:inherit}.wrap{max-width:820px;margin:0 auto;padding:0 20px}
header{border-bottom:1px solid var(--line);background:var(--bg);position:sticky;top:0;z-index:2}header .wrap{display:flex;justify-content:space-between;align-items:center;height:60px}
.logo{font:600 20px Fraunces,Georgia,serif;text-decoration:none}.logo span{color:var(--warm)}
.btn{display:inline-block;background:var(--accent);color:var(--accent-ink);text-decoration:none;font-weight:600;font-size:15px;padding:11px 20px;border-radius:999px}
.btn.ghost{background:transparent;color:var(--ink);border:1px solid var(--line)}
h1,h2{font-family:Fraunces,"Noto Sans SC",Georgia,serif;font-weight:600;line-height:1.15;letter-spacing:-.01em}
h1{font-size:clamp(30px,5vw,44px);margin:36px 0 8px}.meta{color:var(--muted);font-size:15px}.lead{font-size:19px;color:var(--muted);margin:14px 0 26px}
.slides{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:10px;margin:0 -20px;padding-left:20px;padding-right:20px}
.slides img{flex:0 0 min(78%,380px);width:min(78%,380px);height:auto;aspect-ratio:4/5;object-fit:cover;border-radius:14px;scroll-snap-align:start;border:1px solid var(--line)}
.hint{font-size:13px;color:var(--muted);margin-top:4px}
section.tip{margin-top:30px}section.tip h2{font-size:24px;margin-bottom:8px}section.tip p{color:var(--ink)}
.cta{margin:44px 0;padding:26px;border-radius:18px;background:var(--surface);border:1px solid var(--line)}.cta h2{font-size:24px}.cta p{color:var(--muted);margin:6px 0 16px}.cta .row{display:flex;gap:10px;flex-wrap:wrap}
.more{margin:10px 0 50px}.more a{display:block;padding:14px 0;border-top:1px solid var(--line);text-decoration:none;font-weight:600}
.credit{font-size:13px;color:var(--muted);margin-top:24px}footer{padding:30px 0;color:var(--muted);font-size:14px;border-top:1px solid var(--line)}"""

FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600&family=Inter:wght@400;500;600&family=Noto+Sans+SC:wght@400;600&display=swap" rel="stylesheet">'

for g in G:
    url = f'{SITE}/guides/{g["slug"]}'
    slides = ''.join(f'<img src="{s}" alt="{e(g["alt"])} ({i}/{len(g["imgs"])})" loading="{"eager" if i==1 else "lazy"}" width="1080" height="1350">' for i, s in enumerate(g['imgs'], 1))
    secs = ''.join(f'<section class="tip"><h2>{e(h)}</h2><p>{e(p)}</p></section>' for h, p in g['sections'])
    others = ''.join(f'<a href="/guides/{o["slug"]}">{e(o["title"])} →</a>' for o in G if o is not g)
    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": g['title'], "datePublished": g['date'], "image": [SITE + g['imgs'][0]], "author": {"@type": "Person", "name": "Kev, Pocket Local"}, "publisher": {"@type": "Organization", "name": "Pocket Local Singapore"}, "mainEntityOfPage": url}, ensure_ascii=False)
    page = f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(g["title"])} | Pocket Local Singapore</title><meta name="description" content="{e(g["summary"])}"><link rel="canonical" href="{url}">
<meta property="og:title" content="{e(g["title"])}"><meta property="og:description" content="{e(g["summary"])}"><meta property="og:image" content="{SITE}{g["imgs"][0]}"><meta property="og:url" content="{url}"><meta name="twitter:card" content="summary_large_image">
{FONTS}<style>{CSS}</style><script type="application/ld+json">{ld}</script></head><body>
<header><div class="wrap"><a class="logo" href="{SITE}/">Pocket <span>Local</span></a><a class="btn" href="{SITE}/#plan-form">Plan my trip</a></div></header>
<main class="wrap"><h1>{e(g["title"])}</h1><div class="meta">{e(g["title_zh"])} · {fmt(g["date"])}</div><p class="lead">{e(g["summary"])}</p>
<div class="slides">{slides}</div><div class="hint">Swipe for more →</div>
{secs}
<div class="cta"><h2>Want a plan like this for your whole trip?</h2><p>I'm Kev, a Singaporean dad. Tell me your dates and who's coming, and I'll plan your days around you. English and 中文.</p><div class="row"><a class="btn" href="{SITE}/#plan-form">Plan my trip</a><a class="btn ghost" href="{g["instagram"]}" target="_blank" rel="noopener">See this post on Instagram</a></div></div>
{('<div class="more"><b>More local guides</b>' + others + '</div>') if others else ''}
{f'<p class="credit">{e(g["credits"])}</p>' if g["credits"] else ''}
</main><footer><div class="wrap">Pocket Local Singapore · 口袋本地通 · <a href="{SITE}/">pocketlocalsg.com</a></div></footer></body></html>'''
    open(os.path.join(PUB, 'guides', f'{g["slug"]}.html'), 'w').write(page)

cards = ''.join(f'''<a class="gcard" href="/guides/{g["slug"]}"><img src="{g["imgs"][0]}" alt="{e(g["title"])}" loading="lazy" width="1080" height="1350"><div class="gbody"><div class="gdate">{fmt(g["date"])}</div><h3>{e(g["title"])}</h3><p>{e(g["summary"])}</p><span class="gmore"><span data-en>Read the guide →</span><span data-zh>查看攻略 →</span></span></div></a>''' for g in G)
section = f'''<!--GUIDES-->
  <section id="guides">
    <h2><span data-en>Local guides</span><span data-zh>本地攻略</span></h2>
    <p class="lead"><span data-en>Free tips from our posts. Save them for your trip.</span><span data-zh>来自我们帖子的免费贴士，收藏起来旅行时用。</span></p>
    <div class="ggrid">{cards}</div>
    <div class="gfollow"><span data-en>New tips every week:</span><span data-zh>每周更新：</span> <a href="https://www.instagram.com/pocketlocal.sg/" target="_blank" rel="noopener">Instagram</a> · <a href="https://www.tiktok.com/@pocketlocal.sg" target="_blank" rel="noopener">TikTok</a> · <a href="https://www.facebook.com/pocketlocal.sg" target="_blank" rel="noopener">Facebook</a></div>
  </section>
  <style>
  #guides .ggrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:18px;margin-top:22px}}
  #guides .gcard{{display:flex;flex-direction:column;background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden;text-decoration:none;transition:transform .15s}}
  #guides .gcard:hover{{transform:translateY(-2px)}}
  #guides .gcard img{{width:100%;height:auto;aspect-ratio:4/5;object-fit:cover;display:block}}
  #guides .gbody{{padding:16px 18px 18px}}#guides .gdate{{font-size:13px;color:var(--muted)}}
  #guides .gcard h3{{font-size:20px;margin:4px 0 6px}}#guides .gcard p{{font-size:15px;color:var(--muted);margin:0 0 10px}}
  #guides .gmore{{font-weight:600;font-size:15px;color:var(--accent)}}#guides .gfollow{{margin-top:18px;font-size:15px;color:var(--muted)}}#guides .gfollow a{{font-weight:600;color:var(--ink)}}
  </style>
<!--/GUIDES-->'''
p = os.path.join(PUB, 'pocketlocal.html'); s = open(p).read()
if '<!--GUIDES-->' in s:
    s = re.sub(r'<!--GUIDES-->.*?<!--/GUIDES-->', section, s, flags=re.S)
else:
    s = s.replace('  <section id="how">', section + '\n\n  <section id="how">', 1)
open(p, 'w').write(s)
urls = [SITE + '/'] + [f'{SITE}/guides/{g["slug"]}' for g in G]
open(os.path.join(PUB, 'pl-sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
print('built', [g['slug'] for g in G])
