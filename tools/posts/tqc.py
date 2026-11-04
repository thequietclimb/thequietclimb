import sys, os, shutil; sys.path.insert(0, '/home/claude/posts4')
import base; base.OUT = '/home/claude/posts6/out'
from base import slide, render
O = base.OUT
for f in ['/home/claude/thequietclimb/public/free/p-1.jpg'] + [f'/home/claude/thequietclimb/public/share/fb1/{x}.jpg' for x in ['wed_eve_marina_1','thu_eve_katong_1','thu_pm_laksa','fri_pm_supertrees','sat_pm_spectra','wed_pm_laupasat']]:
    shutil.copy(f, O)
B = '<div class="brand">The Quiet Climb</div>'
F = '<div class="foot"><span>@thequietclimb.sg</span><span>Swipe →</span></div>'
pg = lambda n, t: f'<div class="pg">{n}/{t}</div>'
S = []
# ---- A: 10 years off social media
T = 6
S.append(slide('a1', B + '''<h1>10 years off social media.</h1>
<p class="big">I've been back for a couple of weeks. Here's what it actually feels like.</p>''' + F))
S.append(slide('a2', B + pg(2, T) + '''<h2 style="margin-top:auto">Showing my face was the hardest part.</h2>
<p class="mut">For years I kept things private. Hitting "post" on a video of myself still feels strange.</p>''' + F))
S.append(slide('a3', B + pg(3, T) + '''<h2 style="margin-top:auto">I'm not a natural on camera.</h2>
<p class="mut">So I write it down, film it again, and cut it shorter. My first video took 7 versions.</p>''' + F))
S.append(slide('a4', B + pg(4, T) + '''<h2 style="margin-top:auto">Speaking up is my real challenge.</h2>
<p class="mut">Not the trading. Not the business. Just saying things out loud, in public.</p>''' + F))
S.append(slide('a5', B + pg(5, T) + '''<h2 style="margin-top:auto"><span class="acc">Quiet</span> doesn't mean hidden.</h2>
<p class="mut">It means no noise, no hype. Just showing up and doing the work.</p>''' + F))
S.append(slide('a6', B + pg(6, T) + '''<h2 style="margin-top:auto">If you've been quiet too, start small.</h2>
<p class="big">One post. One step. Then the next one.</p>
<div class="foot"><span>Follow the climb</span><span>@thequietclimb.sg</span></div>'''))
# ---- B: AI built a travel business
T = 6
img = lambda f, st='': f'<img src="{f}" style="width:100%;border-radius:24px;border:2px solid var(--line);{st}">'
S.append(slide('b1', B + '''<h1>I started a travel business. <span class="acc">AI did the heavy lifting.</span></h1>
<p class="mut">I'm not very techy. Here's what got built in about a week.</p>''' + F))
S.append(slide('b2', B + pg(2, T) + '''<h2 style="margin-top:50px">A website</h2>
<div style="margin-top:36px;display:flex;justify-content:center"><img src="site.png" style="height:760px;border-radius:28px;border:2px solid var(--line)"></div>''' + F))
S.append(slide('b3', B + pg(3, T) + '''<h2 style="margin-top:50px">A free guide</h2>
<div style="margin-top:36px;display:flex;gap:30px;align-items:center"><img src="p-1.jpg" style="height:720px;border-radius:20px;border:2px solid var(--line)">
<p class="mut" style="margin:0">A 1-day Singapore plan for families. People get it free.</p></div>''' + F))
g = ''.join(f'<img src="{x}.jpg" style="width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:16px;border:2px solid var(--line)">' for x in ['wed_eve_marina_1','thu_eve_katong_1','thu_pm_laksa','fri_pm_supertrees','sat_pm_spectra','wed_pm_laupasat'])
S.append(slide('b4', B + pg(4, T) + f'''<h2 style="margin-top:50px">A week of posts</h2>
<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:16px;margin-top:36px">{g}</div>
<p class="mut">18 posts written, designed and scheduled.</p>''' + F))
S.append(slide('b5', B + pg(5, T) + '''<h2 style="margin-top:auto">Replies on autopilot</h2>
<p class="big">Someone comments "PLAN", they get the free guide by private message.</p>
<p class="mut">No one waits for me to wake up.</p>''' + F))
S.append(slide('b6', B + pg(6, T) + '''<h2 style="margin-top:auto">What I still do myself</h2>
<div class="list">
<div class="item"><div class="n">1</div><div><b>The local knowledge</b><span>Where we actually eat, where it's cool when it's hot.</span></div></div>
<div class="item"><div class="n">2</div><div><b>Talking to families</b><span>Every chat is me.</span></div></div>
<div class="item"><div class="n">3</div><div><b>Showing up</b><span>Airport, WhatsApp, the real stuff.</span></div></div>
</div>
<div class="foot"><span>Pocket Local · @pocketlocal.sg</span><span>@thequietclimb.sg</span></div>'''))
render(S)
for f in S: os.remove(f)
print('ok')
