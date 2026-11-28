#!/usr/bin/env python3
"""Builds the Pocket Local About, Privacy, Terms and Refunds pages into public/pl/.
Served at pocketlocalsg.com/about, /privacy, /terms, /refunds by src/index.js.
Edit the text below, then run: python3 tools/build_pl_pages.py"""
import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from pixel import PIXEL

PUB = os.path.join(os.path.dirname(__file__), '..', 'public')
SITE = 'https://pocketlocalsg.com'
UPDATED = ('27 November 2026', '2026年11月27日')


def t(en, zh):
    return f'<span data-en>{en}</span><span data-zh>{zh}</span>'


CSS = """:root{--ivory:#fbf8f2;--ink:#193447;--muted:#56656f;--line:#e7e2d8;--accent:#4d827d;--warm:#c98768}
*{box-sizing:border-box;margin:0;padding:0}html{scroll-behavior:smooth}
body{background:#fff;color:var(--ink);font:17px/1.7 Inter,"Noto Sans SC",system-ui,sans-serif;-webkit-font-smoothing:antialiased}
a{color:var(--accent)}img{max-width:100%}
[data-zh]{display:none}html[lang="zh"] [data-en]{display:none}html[lang="zh"] [data-zh]{display:revert}
.wrap{max-width:780px;margin:0 auto;padding:0 20px}
header{position:sticky;top:0;z-index:5;background:rgba(255,255,255,.94);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:62px;gap:10px;max-width:1080px}
.logo{font:600 21px Fraunces,Georgia,serif;text-decoration:none;color:var(--ink)}.logo span{color:var(--warm)}
.tools{display:flex;gap:10px;align-items:center}
.lang{border:1px solid var(--line);background:#fff;color:var(--ink);border-radius:999px;padding:6px 14px;font:inherit;font-size:14px;cursor:pointer}
.btn{display:inline-block;background:var(--accent);color:#fff;text-decoration:none;font-weight:600;font-size:15px;padding:12px 22px;border-radius:999px}
.btn.sm{padding:8px 16px;font-size:14px}
h1,h2{font-family:Fraunces,"Noto Sans SC",Georgia,serif;font-weight:600;line-height:1.2;letter-spacing:-.01em}
html[lang="zh"] h1,html[lang="zh"] h2{font-family:"Noto Sans SC",sans-serif;letter-spacing:0}
h1{font-size:clamp(32px,5vw,46px);margin:44px 0 8px}
h2{font-size:23px;margin:34px 0 8px}
.meta{color:var(--muted);font-size:14px;margin-bottom:26px}
main p,main li{margin-bottom:12px}main ul{padding-left:22px}
.lead{font-size:19px;color:var(--muted)}
.box{background:var(--ivory);border:1px solid var(--line);border-radius:18px;padding:22px 24px;margin:30px 0}
.trips{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:28px 0}
.trips figure{margin:0;position:relative;border-radius:14px;overflow:hidden;aspect-ratio:4/3}
.trips figure.big{grid-column:span 3;aspect-ratio:16/9}
.trips img{width:100%;height:100%;object-fit:cover;display:block}
.trips figcaption{position:absolute;left:10px;bottom:10px;background:rgba(0,0,0,.55);color:#fff;font-size:13px;padding:4px 10px;border-radius:999px}
.av{width:140px;height:140px;border-radius:50%;object-fit:cover;margin-top:36px;display:block}
.sign{font-style:italic;color:var(--muted)}

.btn.ghost{background:#fff;color:var(--ink);border:1px solid var(--line)}
.actions{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0 8px}
.price{display:inline-block;background:var(--ivory);border:1px solid var(--line);border-radius:999px;padding:4px 14px;font-weight:600;font-size:15px;margin-bottom:6px}
ol.steps{padding-left:22px}form.box label{display:block;font-weight:600;font-size:15px;margin-bottom:14px}form.box input,form.box textarea{display:block;width:100%;margin-top:6px;padding:10px 12px;border:1px solid var(--line);border-radius:10px;font:inherit;font-weight:400}ol.steps li{margin-bottom:10px}
footer{background:#122838;color:rgba(255,255,255,.75);padding:34px 0;font-size:14px;margin-top:60px}
footer a{color:rgba(255,255,255,.88);text-decoration:none;margin-right:14px}footer a:hover{text-decoration:underline}
footer .wrap{max-width:1080px}
@media (max-width:640px){.trips{grid-template-columns:1fr 1fr}.trips figure.big{grid-column:span 2}header .btn{display:none}}"""

JS = """<script>(function(){var r=document.documentElement,b=document.getElementById('lang');function s(l){r.lang=l;b.textContent=l==='zh'?'English':'中文';try{localStorage.setItem('pocketlocal-lang',l)}catch(e){}}var v=null;try{v=localStorage.getItem('pocketlocal-lang')}catch(e){}if(v){s(v)}else if((navigator.language||'').toLowerCase().indexOf('zh')===0){s('zh')}b.addEventListener('click',function(){s(r.lang==='zh'?'en':'zh')})})();</script>"""


def page(slug, title, desc, body, index=True):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} | Pocket Local Singapore</title><meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{slug}">{'' if index else '<meta name="robots" content="noindex">'}
<meta property="og:title" content="{title} | Pocket Local Singapore"><meta property="og:description" content="{desc}"><meta property="og:url" content="{SITE}/{slug}"><meta property="og:image" content="{SITE}/img/pl_share.jpg"><meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#193447">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,wght@0,600;1,400&family=Inter:wght@400;600&family=Noto+Sans+SC:wght@400;600&display=swap" rel="stylesheet">
<style>{CSS}</style>{PIXEL}</head><body>
<header><div class="wrap"><a class="logo" href="/">Pocket <span>Local</span></a><div class="tools"><button class="lang" id="lang" type="button" aria-label="Switch language">中文</button><a class="btn sm" href="/#plan-form">{t('Plan my trip','规划我的行程')}</a></div></div></header>
<main class="wrap">
{body}
</main>
<footer><div class="wrap"><p>Pocket Local Singapore · 口袋本地通</p><p style="margin-top:10px"><a href="/">{t('Home','首页')}</a><a href="/about">{t('About','关于')}</a><a href="/privacy">{t('Privacy','隐私')}</a><a href="/terms">{t('Terms','条款')}</a><a href="/refunds">{t('Cancellation & refunds','取消及退款')}</a><a href="mailto:pocketlocal.sg@gmail.com">pocketlocal.sg@gmail.com</a><a href="https://wa.me/6582756686">WhatsApp +65 8275 6686</a></p></div></footer>
{JS}
</body></html>
'''


def updated():
    return f'<p class="meta">{t("Last updated: " + UPDATED[0], "最后更新：" + UPDATED[1])}</p>'


def P(en, zh):
    return f'<p>{t(en, zh)}</p>'


def H(en, zh):
    return f'<h2>{t(en, zh)}</h2>'


def UL(*items):
    return '<ul>' + ''.join(f'<li>{t(en, zh)}</li>' for en, zh in items) + '</ul>'


CONTACT = P('Questions? Email <a href="mailto:pocketlocal.sg@gmail.com">pocketlocal.sg@gmail.com</a> or WhatsApp <a href="https://wa.me/6582756686">+65 8275 6686</a>.',
            '有疑问？请发电邮至 <a href="mailto:pocketlocal.sg@gmail.com">pocketlocal.sg@gmail.com</a> 或 WhatsApp <a href="https://wa.me/6582756686">+65 8275 6686</a>。')

# ---------- About ----------
about = f'''<img class="av" src="/img/avatar.jpg" alt="Kev, founder of Pocket Local">
<h1>{t("Why I started Pocket Local", "为什么我创办口袋本地通")}</h1>
<p class="meta">{t("Kev, founder · born and raised in Singapore", "Kev，创办人 · 土生土长的新加坡人")}</p>
{P("Hi, I'm Kev. Growing up, I hardly travelled, and I didn't know much about what lay beyond Singapore.", "你好，我是 Kev。我小时候很少出国旅行，对新加坡以外的世界了解不多。")}
{P("That changed when I had two kids. I wanted to world-school them: to let them learn about the world by seeing it, meeting people and experiencing other cultures, not just reading about them. So from when they were little until their teenage years, we travelled together: all over Japan, Jeju in Korea, China, Malaysia, Thailand and Indonesia, Perth and Margaret River in Australia, and the UK, France and Italy. Many of those trips were self-drive, just us and a map.", "有了两个孩子之后，一切都改变了。我想让他们“以世界为课堂”：亲眼看世界、认识不同的人、体验不同的文化，而不只是从书本上学习。所以从他们年幼到青少年时期，我们一家一起去了很多地方：走遍日本各地，还去了韩国济州岛、中国、马来西亚、泰国、印尼、澳洲珀斯和玛格丽特河，以及英国、法国和意大利。其中很多趟都是自驾游，一家人一张地图就出发。")}
<div class="trips">
<figure class="big"><img src="/img/trips/london.jpg" alt="Kev and family at Tower Bridge, London" loading="lazy"><figcaption>{t("London, UK", "英国伦敦")}</figcaption></figure>
<figure><img src="/img/trips/italy.jpg" alt="Family on a self-drive trip through the Italian countryside" loading="lazy"><figcaption>{t("Self-drive, Italy", "意大利自驾")}</figcaption></figure>
<figure><img src="/img/trips/paris.jpg" alt="Family at the Louvre, Paris" loading="lazy"><figcaption>{t("Paris, France", "法国巴黎")}</figcaption></figure>
<figure><img src="/img/trips/rome.jpg" alt="Family in Rome" loading="lazy"><figcaption>{t("Rome, Italy", "意大利罗马")}</figcaption></figure>
<figure><img src="/img/trips/japan.jpg" alt="Family at Universal Studios Japan" loading="lazy"><figcaption>{t("Osaka, Japan", "日本大阪")}</figcaption></figure>
<figure><img src="/img/trips/tokyo.jpg" alt="Family above the Tokyo skyline at night" loading="lazy"><figcaption>{t("Tokyo, Japan", "日本东京")}</figcaption></figure>
<figure><img src="/img/trips/korea.jpg" alt="Family in the snow in Korea when the kids were small" loading="lazy"><figcaption>{t("Korea, when the boys were little", "韩国，孩子们还小的时候")}</figcaption></figure>
</div>
{P("On those trips, we loved going off the beaten path: the small towns, local markets and quiet corners where tourists don't usually go. That's where we met the real people and tasted the real food, and it's still the best way I know to experience a country.", "旅途中，我们最喜欢走出热门景点，去游客很少去的地方：小镇、当地市场和安静的角落。在那里，我们遇见真正的当地人，吃到地道的食物。这至今仍是我认为体验一个国家最好的方式。")}
{P("Planning all those self-drive routes taught me what makes or breaks a trip: a good plan. When the plan is right, travel stops being stressful and becomes the best part of the year.", "规划那么多自驾路线，让我明白了一件事：一份好的行程规划，决定了一趟旅行的好坏。计划做对了，旅行就不再是压力，而是一年中最美好的时光。")}
{P("Over those years, people in so many countries welcomed us, helped us and hosted us well. Pocket Local is my way of returning that kindness. When you come to Singapore, I want you to feel as welcome as my family felt everywhere we went, and to show you the Singapore that most tourists miss.", "这些年来，世界各地的人热情地接待和帮助过我们。口袋本地通是我回馈这份善意的方式：当你来到新加坡，我希望你也能感受到我们一家在各地感受到的那份温暖，也带你看看大多数游客错过的新加坡。")}
<p class="sign">{t("Kev, founder of Pocket Local", "Kev，口袋本地通创办人")}</p>
<div class="box"><p><b>{t("How I work", "我的原则")}</b></p>{UL(("Planning only. You book and pay for hotels and tickets yourself, in your own name.", "只做规划。酒店和门票由你自己以本人名义预订和付款。"), ("Independent picks. I don't take money from shops or attractions to send you there.", "独立推荐。我不收商家或景点的钱来推荐给你。"), ("English and 中文, by WhatsApp, call or email.", "中英文皆可，通过 WhatsApp、电话或电邮联系。"))}<p style="margin:16px 0 0"><a class="btn" href="/#plan-form">{t("Plan my Singapore trip", "规划我的新加坡之旅")}</a></p></div>'''

# ---------- Privacy ----------
privacy = f'''<h1>{t("Privacy policy", "隐私政策")}</h1>
{updated()}
<p class="lead">{t("Pocket Local Singapore (“Pocket Local”, “I”, “we”) plans trips in Singapore. This page explains what personal information we collect, why, and what you can ask us to do with it. We follow Singapore's Personal Data Protection Act 2012 (PDPA).", "口袋本地通（Pocket Local Singapore，以下称“我们”）提供新加坡行程规划服务。本页说明我们收集哪些个人资料、用途，以及你的权利。我们遵守新加坡《2012年个人资料保护法》（PDPA）。")}</p>
{H("What we collect", "我们收集什么")}
{UL(("What you tell us when you fill in the trip form or message us: your name, email, phone or WhatsApp number, where you're travelling from, travel dates, who is travelling (including children's ages), budget, interests, and notes such as diet or mobility needs.", "你填写行程表格或联系我们时提供的资料：姓名、电邮、电话或 WhatsApp 号码、出发地、旅行日期、同行人员（包括孩子年龄）、预算、兴趣，以及饮食或行动需求等备注。"),
     ("Flight details if you choose an airport welcome.", "如选择机场迎接，你的航班资料。"),
     ("Payment records (amount, date, payer name). Payments are processed by PayPal; we never see or store your full card details.", "付款记录（金额、日期、付款人姓名）。付款由 PayPal 处理，我们不会看到或储存你的完整银行卡资料。"))}
{H("How the trip form works", "行程表格如何运作")}
{P("The form on our website doesn't store anything on our servers. When you press send, it opens WhatsApp on your device with your answers filled in, and nothing is sent until you press send in WhatsApp. WhatsApp's own privacy policy applies to that chat.", "网站上的表格不会把资料存到我们的服务器。按下发送后，会在你的设备上打开 WhatsApp 并填好你的答案；在你于 WhatsApp 按发送之前，不会传送任何资料。该对话适用 WhatsApp 自身的隐私政策。")}
{H("Why we use it", "使用目的")}
{UL(("To plan your trip, talk to you about it and send you your plan.", "规划你的行程、与你沟通并发送行程。"),
     ("To meet you at the airport, if your plan includes it.", "如方案包含机场迎接，用于接机。"),
     ("To take payment and keep records we're required to keep.", "收款及保存法律要求的记录。"),
     ("To send you travel tips or offers, only if you ask to receive them. You can stop at any time.", "仅在你要求时，发送旅行贴士或优惠。你可以随时取消。"))}
{H("Who we share it with", "与谁分享")}
{P("We don't sell your personal information. We only share what's needed with the services we use to run Pocket Local: WhatsApp (messages), Google (email and documents for your plan) and PayPal (payments). We won't share your details with shops, hotels or attractions.", "我们不会出售你的个人资料。只会把必要的资料提供给我们运营所用的服务：WhatsApp（讯息）、Google（电邮及行程文件）和 PayPal（付款）。我们不会把你的资料分享给商家、酒店或景点。")}
{H("Photos and reviews", "照片与评价")}
{P("We will only post your photos, videos or review with your clear permission, and you can ask us to take them down at any time.", "只有在你明确同意后，我们才会发布你的照片、视频或评价，你也可以随时要求删除。")}
{H("How long we keep it", "保存期限")}
{P("We keep trip details for up to 12 months after your trip, in case you have questions or come back. Payment records are kept as long as the law requires. You can ask us to delete your details sooner.", "行程资料会在旅行结束后保存最多 12 个月，方便你日后查询或再次来访。付款记录按法律要求保存。你可以要求我们提早删除你的资料。")}
{H("Your choices", "你的权利")}
{P("You can ask to see the personal information we hold about you, correct it, or withdraw your consent and have it deleted. Just message us and we'll reply within 30 days.", "你可以要求查看、更正我们持有的个人资料，或撤回同意并要求删除。联系我们即可，我们会在 30 天内回复。")}
{H("Our website", "我们的网站")}
{P("Our website saves your language choice (English or 中文) in your browser so the site remembers it. We also use the Meta Pixel, a small piece of code from Meta (Facebook and Instagram). It tells us when someone who saw our ads visits the site, taps to pay or sends a form, so we can measure and improve our ads. Meta may use cookies for this and processes the data under its own privacy policy. It doesn't give us your name or contact details. You can control ad tracking in your Facebook or Instagram ad settings and in your browser.", "网站会在你的浏览器中保存语言选择（English 或 中文），方便下次记住。我们也使用 Meta 像素（Meta Pixel），这是来自 Meta（Facebook 和 Instagram）的一小段代码，用来了解看过我们广告的人是否访问网站、点击付款或提交表格，以便衡量和改进广告效果。Meta 可能为此使用 Cookie，并按其隐私政策处理数据。它不会把你的姓名或联系方式提供给我们。你可以在 Facebook 或 Instagram 的广告设置以及浏览器中管理广告追踪。")}
{H("Contact", "联系我们")}
{CONTACT}'''

# ---------- Terms ----------
terms = f'''<h1>{t("Terms of service", "服务条款")}</h1>
{updated()}
<p class="lead">{t("These terms apply when you buy a plan or an Itinerary Check from Pocket Local Singapore. By paying, you agree to them.", "当你向口袋本地通购买行程方案或行程检查时，适用以下条款。付款即表示你同意这些条款。")}</p>
{H("1. What we do", "1. 我们的服务")}
{P("Pocket Local is a trip planning service. We give you a personal itinerary, advice and, on selected plans, an airport welcome and WhatsApp support. We are not a travel agent or tour operator: we don't sell or book flights, hotels, tickets, tours or transport, and we don't guide tours.", "口袋本地通是行程规划服务。我们提供个人化行程、建议，以及指定方案中的机场迎接和 WhatsApp 支援。我们不是旅行社或旅游团经营者：不出售或预订机票、酒店、门票、旅游团或交通，也不提供导游带团服务。")}
{H("2. Your bookings", "2. 你的预订")}
{P("You book and pay for everything in your plan directly with the provider, using the links we give you. Your contract for those services is with the provider, and their terms, prices and availability apply.", "行程中的所有项目由你使用我们提供的链接，直接向供应商预订和付款。这些服务的合约属于你与供应商之间，适用供应商的条款、价格和名额。")}
{H("3. What's included", "3. 服务内容")}
{P('Each plan includes what is listed on our <a href="/#plans">plans and prices</a> section at the time you pay, including the number of days and rounds of changes. Extras (extra days, groups of 5 or more, 48-hour rush) are charged as listed.', '每个方案的内容以你付款时<a href="/#plans">方案与价格</a>中所列为准，包括天数及修改次数。附加项目（加天、5 人以上、48 小时加急）按所列收费。')}
{H("4. Payment", "4. 付款")}
{UL(("Itinerary Check (S$29): paid in full before we start. The S$29 is credited toward any of our three trip-planning packages if you upgrade, and comes off the deposit.", "行程检查（S$29）：开始前全额付款。如之后升级，这 S$29 可抵扣任何一个规划方案，直接从订金中扣除。"),
     ("Plans: a 50% deposit starts the planning; the balance is due before we send your final plan.", "行程方案：先付 50% 订金开始规划，发送最终行程前付清余款。"),
     ("Prices are in Singapore dollars. Any PayPal, bank or currency conversion fees on your side are yours to pay.", "价格以新元计。你方产生的 PayPal、银行或货币兑换费用由你承担。"))}
{H("5. Your information", "5. 你提供的资料")}
{P("Please give us accurate dates, flight times, ages and any health, diet or mobility needs. Your plan is built on what you tell us.", "请提供准确的日期、航班时间、年龄，以及健康、饮食或行动方面的需求。行程会根据你提供的资料来规划。")}
{H("6. Information in your plan", "6. 行程资料")}
{P("We check opening hours, prices and show times when we write your plan, but they can change without notice. Please check anything important (especially tickets and timed shows) close to the day. Weather, crowds, closures and transport delays are outside our control.", "我们在规划时会核对营业时间、价格和表演时间，但这些可能随时变动。重要事项（尤其是门票和定时表演）请在当天前再次确认。天气、人潮、关闭和交通延误不在我们控制范围内。")}
{H("7. Airport welcome", "7. 机场迎接")}
{P("Please send your flight number at least 48 hours before you land. We track your flight and will wait for delays. If your flight changes to a different day, tell us as soon as you can and we'll do our best to rearrange.", "请在抵达前至少 48 小时发送航班号。我们会追踪航班，航班延误会等候。如航班改到其他日期，请尽早通知，我们会尽量重新安排。")}
{H("8. Your safety and insurance", "8. 安全与保险")}
{P("You are responsible for your own travel, health, safety and belongings, and for supervising children in your group. We strongly recommend travel insurance.", "你需自行负责旅途、健康、安全和财物，并照顾同行的孩子。我们强烈建议购买旅游保险。")}
{H("9. Our liability", "9. 责任限制")}
{P("We take care with every plan. As far as the law allows, we aren't responsible for losses caused by third-party providers, events outside our control, or information that changed after your plan was written, and our total liability to you is limited to the amount you paid us. Nothing here limits your rights under Singapore law that cannot be limited.", "我们用心对待每份行程。在法律允许的范围内，我们不对第三方供应商、不可控事件或行程完成后发生变动的资料所造成的损失负责，我们对你的总责任以你支付给我们的金额为限。本条款不限制你在新加坡法律下不可被限制的权利。")}
{H("10. Your plan is for you", "10. 行程仅供个人使用")}
{P("Your plan is for your own trip. Please don't resell or publish it.", "行程仅供你本人旅行使用，请勿转售或公开发布。")}
{H("11. Cancellations and refunds", "11. 取消及退款")}
{P('See our <a href="/refunds">cancellation and refund policy</a>.', '请参阅<a href="/refunds">取消及退款政策</a>。')}
{H("12. Governing law", "12. 适用法律")}
{P("These terms are governed by the laws of Singapore. If something goes wrong, please talk to us first; we'll try hard to fix it.", "本条款受新加坡法律管辖。如有问题，请先联系我们，我们会尽力解决。")}
{H("Contact", "联系我们")}
{CONTACT}'''

# ---------- Refunds ----------
refunds = f'''<h1>{t("Cancellation & refund policy", "取消及退款政策")}</h1>
{updated()}
<p class="lead">{t("Plain and simple: if we haven't started, you get your money back.", "简单来说：我们还没开始，就全额退款。")}</p>
{H("Itinerary Check (S$29)", "行程检查（S$29）")}
{UL(("Full refund if you cancel before we start checking your itinerary.", "在我们开始检查你的行程前取消，可全额退款。"),
     ("Once we've started, it can't be refunded, but you'll still get your check and call.", "开始检查后不予退款，但你仍会收到检查结果和通话。"),
     ("Upgrade later and your S$29 Itinerary Check fee is credited toward any of our three trip-planning packages (S$129, S$269 or S$399). It comes off your deposit.", "之后升级的话，这 S$29 行程检查费用可抵扣任何一个规划方案（S$129、S$269 或 S$399），直接从订金中扣除。"))}
{H("Plans (S$129, S$269, S$399)", "行程方案（S$129、S$269、S$399）")}
{UL(("Full refund of your deposit if you cancel before planning starts (before our planning call).", "在开始规划前（规划通话前）取消，可全额退还订金。"),
     ("Once planning has started, the deposit isn't refundable, but you'll still receive your plan.", "开始规划后，订金不予退还，但你仍会收到行程。"),
     ("Once the final plan has been sent, the plan fee isn't refundable.", "最终行程发送后，方案费用不予退还。"),
     ("If you cancel your trip after paying for a plan with an airport welcome or WhatsApp support, and you tell us at least 72 hours before you land, we refund the part of the price for the welcome and support you won't use. Message us and we'll confirm the amount.", "如果你已购买含机场迎接或 WhatsApp 支援的方案后取消旅行，并在抵达前至少 72 小时通知我们，我们会退还你不会使用的迎接及支援部分费用。联系我们，我们会确认金额。"))}
{H("Changing your dates", "更改日期")}
{P("Trip moved? Tell us and we'll move your plan to the new dates for free if the days and places stay the same. Bigger changes count as a round of changes, or an extra day at S$40.", "旅行改期？告诉我们，如天数和地点不变，可免费调整到新日期。较大的改动算作一次修改，或按每天 S$40 加天收费。")}
{H("If we can't deliver", "如果我们无法提供服务")}
{P("If we can't deliver your plan or welcome for any reason on our side, you get a full refund for the part we couldn't deliver.", "如因我方原因无法提供行程或迎接服务，未能提供的部分将全额退款。")}
{H("How refunds are paid", "退款方式")}
{P("Refunds go back the way you paid (PayPal or bank transfer), usually within 7 working days. To cancel, message us on WhatsApp or by email.", "退款会按原付款方式（PayPal 或银行转账）退回，通常在 7 个工作日内完成。如需取消，请通过 WhatsApp 或电邮联系我们。")}
{CONTACT}'''

PAYPAL = 'https://www.paypal.com/ncp/payment/NCU8WPGLESDBE'
WA_CHECK = 'https://wa.me/6582756686?text=Hi%20Kev%2C%20I%27d%20like%20an%20Itinerary%20Check%20(S%2429).'
CHECK_BTNS = f'''<div class="actions"><a class="btn" href="{PAYPAL}" target="_blank" rel="noopener">{t("Pay S$29 with PayPal or card", "用 PayPal 或银行卡付款 S$29")}</a><a class="btn ghost" href="{WA_CHECK}" target="_blank" rel="noopener">{t("Ask me first on WhatsApp", "先在 WhatsApp 问问")}</a></div>'''

CHECK_FORM = """<h2 id="send">""" + t("Paid? Send me your trip", "已付款？把行程发给我") + """</h2>
<form id="checkform" class="box">
<label>""" + t("Name on your PayPal payment", "PayPal 付款人姓名") + """<input name="name" required></label>
<label>""" + t("Country you live in", "你居住的国家") + """<input name="country" required></label>
<label>""" + t("Travel dates", "旅行日期") + """<input name="dates" placeholder="12–16 Jan 2027" required></label>
<label>""" + t("Travellers (adults, children and ages)", "同行人员（大人、孩子及年龄）") + """<input name="who" placeholder="2 adults, 2 kids (6, 9)" required></label>
<label>""" + t("Your time zone for the call", "通话用的时区") + """<input name="tz" placeholder="Sydney (AEDT)"></label>
<label>""" + t("Paste your itinerary (or attach the file in WhatsApp after this opens)", "贴上你的行程（或在打开 WhatsApp 后附上文件）") + """<textarea name="plan" rows="7"></textarea></label>
<button class="btn" type="submit">""" + t("Send via WhatsApp", "通过 WhatsApp 发送") + """</button>
</form>
<script>document.getElementById('checkform').addEventListener('submit',function(e){e.preventDefault();var f=e.target,v=function(n){return (f[n].value||'').trim()};var m=['Hi Kev! I paid for the S$29 Itinerary Check.','Payment name: '+v('name'),'Country: '+v('country'),'Dates: '+v('dates'),'Travellers: '+v('who'),'Call time zone: '+v('tz'),'Itinerary:',v('plan')||'(attaching it here)'].join('\\n');window.open('https://wa.me/6582756686?text='+encodeURIComponent(m),'_blank')});</script>"""

# ---------- Itinerary Check ----------
check = f'''<h1>{t("Itinerary Check — S$29", "行程检查 — S$29")}</h1>
<p class="lead">{t("Already planned your Singapore trip? Send it to me. A local checks it and tells you what to fix, and why.", "已经排好新加坡行程了？发给我。本地人帮你检查，告诉你哪里要改、为什么。")}</p>
{CHECK_BTNS}
{H("Who it's for", "适合谁")}
{UL(("You've made your own plan and want a local to look it over before you book.", "自己排好了行程，想在预订前请本地人看一看。"),
     ("First time in Singapore, or travelling with kids or older parents.", "第一次来新加坡，或带着孩子、长辈出行。"),
     ("You don't need a full plan, just a second opinion.", "不需要完整规划，只想听听意见。"))}
{H("What you get", "你会得到")}
{UL(("A check of one itinerary, up to 5 days.", "检查一份行程，最多 5 天。"),
     ("Written fixes for timing, routes, queues, food and rain, with the reason for each.", "书面修改建议：时间、路线、排队、美食和雨天安排，每一点都说明原因。"),
     ("Back within 24 hours. The clock starts once I have both your payment and your itinerary details, whichever comes later.", "24 小时内回复。从我收到付款和行程资料（以较晚者为准）开始计算。"),
     ("One follow-up question by WhatsApp after you get your fixes.", "收到修改建议后，可通过 WhatsApp 再问一个跟进问题。"),
     ("Plus a 20-minute call to answer your questions, in English or 中文.", "再加 20 分钟通话解答你的问题，中英文都可以。"))}
{H("What to send me", "需要提供什么")}
{UL(("Your itinerary, in any format: a document, PDF, screenshots or notes are all fine.", "你的行程，任何格式都可以：文档、PDF、截图或笔记都行。"),
     ("Your travel dates and arrival and departure times.", "旅行日期，以及抵达和离开的时间。"),
     ("Who's travelling, including children's ages.", "同行人员，包括孩子的年龄。"),
     ("Where you're staying (hotel or area).", "住宿地点（酒店或区域）。"),
     ("Anything you must do, and anything you'd like to avoid.", "一定要去的地方，以及想避开的事情。"))}
{H("How it works", "流程")}
<ol class="steps">
<li>{t("Pay S$29 by PayPal or card using the button on this page.", "用本页的按钮，以 PayPal 或银行卡付款 S$29。")}</li>
<li>{t('Fill in the short form below (it opens WhatsApp with your answers), or WhatsApp your itinerary and the details above to <a href="https://wa.me/6582756686">+65 8275 6686</a>, with the name on your payment. Email works too: <a href="mailto:pocketlocal.sg@gmail.com">pocketlocal.sg@gmail.com</a>.', '填写下面的简短表格（会自动打开 WhatsApp 并带上你的答案），或把行程和以上资料 WhatsApp 发到 <a href="https://wa.me/6582756686">+65 8275 6686</a>，并注明付款人姓名。也可以发电邮至 <a href="mailto:pocketlocal.sg@gmail.com">pocketlocal.sg@gmail.com</a>。')}</li>
<li>{t("Within 24 hours of getting both, you get your written fixes by WhatsApp or email.", "收到付款和行程资料后 24 小时内，你会通过 WhatsApp 或电邮收到书面修改建议。")}</li>
<li>{t("We book your 20-minute call at a time that suits you.", "再约一个你方便的时间，进行 20 分钟通话。")}</li>
</ol>
<div class="box"><p><b>{t("Want me to plan the whole trip later?", "之后想让我规划整个行程？")}</b></p>{P("Your S$29 Itinerary Check fee will be credited towards any of our three trip-planning packages: Plan (S$129), Plan + Welcome (S$269) or Plan + Welcome + Support (S$399). It comes off your 50% deposit when you upgrade.", "你的 S$29 行程检查费用可抵扣任何一个规划方案：行程规划（S$129）、规划 + 机场迎接（S$269）或规划 + 迎接 + 全程支援（S$399）。升级时直接从 50% 订金中扣除。")}<p><a href="/#plans">{t("See the packages →", "查看方案 →")}</a></p></div>
{CHECK_FORM}
{H("Good to know", "注意事项")}
{UL(("Planning advice only. You book and pay attractions, restaurants and other providers directly. No commissions.", "只提供规划建议。景点、餐厅和其他服务由你直接预订和付款。我们不收任何佣金。"),
     ('Full refund if you cancel before I start checking. See the <a href="/refunds">refund policy</a>.', '在我开始检查前取消，可全额退款。请参阅<a href="/refunds">退款政策</a>。'),
     ("Prices are in Singapore dollars.", "价格以新元计。"))}
{CHECK_BTNS}
{CONTACT}'''

PAGES = [
    ('about', 'About Kev, founder', "Why a Singaporean dad who world-schooled his kids started Pocket Local, and how he plans your Singapore trip.", about),
    ('privacy', 'Privacy policy', 'How Pocket Local Singapore collects, uses and protects your personal information.', privacy),
    ('terms', 'Terms of service', 'The terms for Pocket Local Singapore trip plans and Itinerary Checks.', terms),
    ('check', 'Itinerary Check S$29', 'Already planned your Singapore trip? A local checks your itinerary for S$29, back within 24 hours, plus a 20-minute call.', check),
    ('refunds', 'Cancellation and refund policy', 'How cancellations and refunds work for Pocket Local Singapore plans and Itinerary Checks.', refunds),
]

os.makedirs(os.path.join(PUB, 'pl'), exist_ok=True)
for slug, title, desc, body in PAGES:
    open(os.path.join(PUB, 'pl', f'{slug}.html'), 'w').write(page(slug, title, desc, body))
print('built', [p[0] for p in PAGES])
