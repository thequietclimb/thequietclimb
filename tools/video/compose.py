import json, subprocess, os, shutil
S=json.load(open('segs.json')); segs=S['segs']; DUR=S['dur']
def m(t):
    o=0
    for a,b in segs:
        if t<a: return o
        if t<=b: return o+t-a
        o+=b-a
    return o
C='/home/claude/kev/'
B=[(5.0,7.4,'ai/ai0'),(9.55,13.9,'ai/ai1'),(15.3,19.4,'ai/ai2'),(28.26,33.1,'ai/ai20'),(40.3,44.1,'cw/mt5'),
   (45.3,47.9,'cw/pl_katong'),(47.9,50.2,'cw/pl_marina'),(52.2,55.3,'ai/ai6'),(55.3,58.2,'cw/deskB'),
   (67.7,70.1,'cw/tradingpage'),(70.7,73.9,'cw/gold1'),(73.9,76.7,'cw/payout'),(84.95,86.9,'ai/ai4'),(93.0,97.4,'cw/deskA')]
EV=[(round(m(a)*30)/30, C+f+'.mp4', round((m(b)-m(a))*30)/30) for a,b,f in B]
G="eq=contrast=1.06:brightness=0.02:saturation=1.08:gamma=0.97,colorbalance=rm=0.03:bm=-0.04:rh=0.03:bh=-0.03"
shutil.rmtree('tl',ignore_errors=True); os.makedirs('tl'); L=[]; t=0; k=0
def base(a,b):
    global k
    p=f'tl/{k:03d}.mp4'; k+=1
    subprocess.run(['ffmpeg','-v','error','-y','-i','talk.mp4','-an','-vf',f"trim=start_frame={round(a*30)}:end_frame={round(b*30)},setpts=PTS-STARTPTS",'-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p',p],check=True); L.append(p)
for s,f,d in EV:
    if s>t+0.05: base(t,s)
    p=f'tl/{k:03d}.mp4'; k+=1
    n=round(d*30)
    # gentle push-in on b-roll
    vf=("setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,fps=30,setsar=1"+(","+G if '/ai/' in f else '')+
        f",tpad=stop_mode=clone:stop_duration={d},scale=w='trunc(1080*(1+0.06*n/{n})/2)*2':h='trunc(1920*(1+0.06*n/{n})/2)*2':eval=frame,crop=1080:1920")
    subprocess.run(['ffmpeg','-v','error','-y','-i',f,'-an','-vf',vf,'-c:v','libx264','-preset','veryfast','-crf','16','-pix_fmt','yuv420p','-frames:v',str(n),p],check=True); L.append(p)
    t=s+d
base(t,DUR)
tot=sum(float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',p]).decode()) for p in L)
print('timeline',round(tot,3),'vs',round(DUR,3)); assert abs(tot-DUR)<0.1
open('tl/list.txt','w').write('\n'.join(f"file '{os.path.basename(p)}'" for p in L))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-i','tl/list.txt','-c','copy','tl_video.mp4'],check=True)
subprocess.run(['ffmpeg','-v','error','-y','-threads','2','-i','tl_video.mp4','-i','talk.wav','-filter_complex',"[0:v]ass=caps.ass,format=yuv420p[v]",'-map','[v]','-map','1:a','-c:v','libx264','-preset','medium','-crf','20','-c:a','aac','-b:a','192k','-movflags','+faststart','-shortest','why_tqc_v8.mp4'],check=True)
print('done')
