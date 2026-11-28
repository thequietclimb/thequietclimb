"""Meta Pixel for the Pocket Local site (pocketlocalsg.com).
Events: PageView on every page; InitiateCheckout on PayPal (S$29) clicks;
Lead on the trip form and the post-payment /check form; Contact on WhatsApp clicks.
Run `python3 tools/pixel.py` to (re)inject into the static PL pages. Builders import PIXEL."""
import glob, os, re

PIXEL_ID = '2096718900979050'
PIXEL = f'''<!-- Meta Pixel --><script>!function(f,b,e,v,n,t,s){{if(f.fbq)return;n=f.fbq=function(){{n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)}};if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');fbq('init','{PIXEL_ID}');fbq('track','PageView');
document.addEventListener('click',function(ev){{var a=ev.target.closest&&ev.target.closest('a');if(!a)return;var h=a.href||'';if(h.indexOf('paypal.com/ncp')>-1){{fbq('track','InitiateCheckout',{{value:29,currency:'SGD',content_name:'Itinerary Check'}})}}else if(h.indexOf('wa.me/')>-1){{fbq('track','Contact')}}}},true);
document.addEventListener('submit',function(ev){{var id=ev.target&&ev.target.id;if(id==='tripform'||id==='checkform'){{fbq('track','Lead',{{content_name:id==='checkform'?'Itinerary Check details':'Trip enquiry'}})}}}},true);</script><noscript><img height="1" width="1" style="display:none" alt="" src="https://www.facebook.com/tr?id={PIXEL_ID}&ev=PageView&noscript=1"></noscript><!-- /Meta Pixel -->'''

def inject(html):
    html = re.sub(r'<!-- Meta Pixel -->.*?<!-- /Meta Pixel -->', '', html, flags=re.S)
    return html.replace('</head>', PIXEL + '</head>', 1)

if __name__ == '__main__':
    pub = os.path.join(os.path.dirname(__file__), '..', 'public')
    files = [os.path.join(pub, f) for f in ('pocketlocal.html', 'free.html')] + glob.glob(os.path.join(pub, 'guides', '*.html'))
    for f in files:
        s = open(f).read(); open(f, 'w').write(inject(s))
    print('pixel in', len(files), 'files')
