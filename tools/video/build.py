import json, subprocess, wave, array, os, shutil
W=json.load(open('words.json'))
RM=[(27.8,28.26),(44.68,45.30),(51.04,51.58),(67.48,67.64),(77.82,78.22)]
def removed(w): return any(a-0.01<=w[0] and w[1]<=b+0.01 for a,b in RM)
K=[w for w in W if not removed(w)]
# build kept intervals
segs=[]; s=K[0][0]-0.35
for i in range(len(K)-1):
    a,b=K[i],K[i+1]
    adj = W.index(b)==W.index(a)+1
    gap=b[0]-a[1]
    if adj and gap<=0.42: continue
    if adj: e=a[1]+0.2; ns=b[0]-0.14
    else:  e=a[1]+0.05; ns=b[0]-0.05
    segs.append([s,e]); s=ns
segs.append([s,K[-1][1]+0.7])
fr=lambda x: round(x*30)/30
segs=[(fr(a),fr(b)) for a,b in segs if b-a>0.1]
def m(t):
    o=0
    for a,b in segs:
        if t<a: return o
        if t<=b: return o+t-a
        o+=b-a
    return o
DUR=sum(b-a for a,b in segs)
json.dump(dict(segs=segs,dur=DUR),open('segs.json','w'))
print('segments',len(segs),'dur',round(DUR,2))
# ---- base video per segment with alternating punch-in
shutil.rmtree('k',ignore_errors=True); os.makedirs('k')
vl=[]
for i,(a,b) in enumerate(segs):
    z=[1.0,1.12][i%2]
    W2=int(1080/z)//2*2; H2=int(1920/z)//2*2
    vf=f"trim=start_frame={round(a*30)}:end_frame={round(b*30)},setpts=PTS-STARTPTS,crop={W2}:{H2}:(iw-{W2})/2:(ih-{H2})*0.35,scale=1080:1920,setsar=1"
    p=f'k/v{i:02d}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-i','base30.mp4','-an','-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',p],check=True)
    vl.append(p)
open('k/vl.txt','w').write('\n'.join(f"file '{os.path.basename(p)}'" for p in vl))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-i','k/vl.txt','-c','copy','talk.mp4'],check=True)
# ---- audio sample-exact
src=wave.open('full.wav'); sr=src.getframerate(); nch=src.getnchannels(); sw=src.getsampwidth()
out=wave.open('talk.wav','wb'); out.setnchannels(nch); out.setsampwidth(sw); out.setframerate(sr)
for a,b in segs:
    n0=round(a*30)*sr//30; n1=round(b*30)*sr//30
    src.setpos(n0); arr=array.array('h',src.readframes(n1-n0)); n=len(arr)//nch; f=int(0.015*sr)
    for k in range(min(f,n)):
        g=k/f
        for c in range(nch): arr[k*nch+c]=int(arr[k*nch+c]*g); arr[(n-1-k)*nch+c]=int(arr[(n-1-k)*nch+c]*g)
    out.writeframes(arr.tobytes())
out.close()
# ---- captions (ASS)
def extra():
    E=[]
    def add(st,en,style,txt): E.append(f"Dialogue: 1,{ts(st)},{ts(en)},{style},,0,0,0,,{txt}")
    # name tag
    add(0.25,3.6,'Tag','{\\fad(200,200)\\3c&H141414&}KEV {\\c&H4C86E0&}· THE QUIET CLIMB')
    # titles
    for a,b in [(35.1,37.0),(89.66,91.0)]:
        add(m(a),m(b),'Title','{\\fad(120,200)\\fscx85\\fscy85\\t(0,200,\\fscx100\\fscy100)}THE QUIET\\N{\\c&H4C86E0&}CLIMB')
    # three things tags
    for a,b,t in [(39.3,44.4,'01  PROP FIRM TRADING'),(44.5,50.6,'02  POCKET LOCAL'),(50.7,58.2,'03  BUILDING WITH AI')]:
        add(m(a),m(b),'Tag','{\\fad(150,150)\\3c&H4C86E0&\\c&H141414&}'+t)
    # end card
    add(m(99.5),DUR,'Title','{\\fad(250,0)\\fs96}FOLLOW\\NTHE CLIMB\\N{\\fs54\\c&H4C86E0&}@thequietclimb.sg')
    return E

def ts(t):
    h=int(t//3600); mi=int(t%3600//60); s=t%60; return f"{h}:{mi:02d}:{s:05.2f}"
KEY={'million','public.','Quiet','Climb.','real','numbers,','Pocket','Local.','AI','honest','first','step.','scratch.','hype,','10'}
chunks=[]; cur=[]
for w in K:
    t=w[2].strip()
    if not t: continue
    cur.append((m(w[0]),m(w[1]),t))
    if len(cur)>=3 or t[-1] in ',.?' : chunks.append(cur); cur=[]
if cur: chunks.append(cur)
ev=[]
for j,c in enumerate(chunks):
    if any(t=='Quiet' for _,_,t in c): continue
    st=c[0][0]; en=chunks[j+1][0][0] if j+1<len(chunks) else c[-1][1]+0.6
    en=min(en,c[-1][1]+0.8)
    txt=' '.join(('{\\c&H4C86E0&}'+t.upper()+'{\\c&HFFFFFF&}') if t in KEY else t.upper() for _,_,t in c)
    ev.append(f"Dialogue: 0,{ts(st)},{ts(en)},Cap,,0,0,0,,{{\\fad(60,40)\\fscx92\\fscy92\\t(0,90,\\fscx100\\fscy100)}}{txt}")
ass=f"""[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Title,Inter ExtraBold,118,&H00FFFFFF,&H00FFFFFF,&H00141414,&H90000000,-1,0,0,0,100,100,2,0,1,0,6,5,60,60,0,1
Style: Tag,Inter ExtraBold,46,&H00FFFFFF,&H00FFFFFF,&H00141414,&H00000000,-1,0,0,0,100,100,1,0,3,18,0,7,80,80,240,1
Style: Cap,Inter ExtraBold,74,&H00FFFFFF,&H00FFFFFF,&H00141414,&H80000000,-1,0,0,0,100,100,0,0,1,5,3,2,90,90,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""+'\n'.join(ev+extra())+'\n'
open('caps.ass','w').write(ass)
print('captions',len(ev))
