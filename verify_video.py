"""Run after final rendering: seekable MP4, stream checks, decode, frame QA."""
from pathlib import Path
import subprocess,json,os
from PIL import Image,ImageDraw
root=Path(__file__).parent
ffbin=next((root/'tools/ffmpeg').glob('*/bin'))
ffmpeg=str(ffbin/'ffmpeg.exe');ffprobe=str(ffbin/'ffprobe.exe')
video=root/'output/PAMS_Part_1.mp4'
optimized=root/'output/PAMS_Part_1_faststart.mp4'
subprocess.run([ffmpeg,'-v','error','-y','-i',str(video),'-map','0:v:0','-c','copy','-movflags','+faststart','-metadata','title=PAMS - Part 1: Mathematical Overview',str(optimized)],check=True)
os.replace(optimized,video)
report=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(video)]))
stream=report['streams'][0]
assert (stream['width'],stream['height'])==(1920,1080)
assert stream['codec_name']=='h264'
assert stream['r_frame_rate']=='30/1'
duration=float(report['format']['duration']);assert 1200<duration<2400
subprocess.run([ffmpeg,'-v','error','-i',str(video),'-f','null','-'],check=True)
timeline=json.loads((root/'qa/PAMSPart1-timeline.json').read_text())
selected=[next(t['beat'] for t in timeline if t['chapter']==chapter) for chapter in range(1,17)]
sheet=Image.new('RGB',(1920,1160),'#101723');draw=ImageDraw.Draw(sheet)
for i,b in enumerate(selected):
    t=timeline[b-1]['time']+2
    dest=root/'qa'/f'final-video-{b:03}.png'
    subprocess.run([ffmpeg,'-v','error','-y','-ss',str(t),'-i',str(video),'-frames:v','1',str(dest)],check=True)
    im=Image.open(dest).convert('RGB');assert im.getbbox()
    im.thumbnail((480,270));x=i%4*480;y=i//4*290;sheet.paste(im,(x,y))
    draw.text((x+8,y+272),f'{int(t)//60:02}:{int(t)%60:02}  /  reading state {b}',fill='white')
sheet.save(root/'qa/final-video-contact.jpg')
from formulas import F
events=json.loads((root/'qa/PAMSPart1-equations.json').read_text())
required={'keygen','sample','random','key','cipher','sendpk','sendc','decrypt','rerandom','reencrypt','equalq','sharedkey','public','concept','shares','mod','compressq','compress','floor','ceil','widths','start','end','example','interval','wrap','wrapset','f','power','fbounds','widthnum','theta','thetanum','z','numshares','sumshares','numf','znum','compare','pass','failshares','fail','equiv','expanded1','expanded2','expanded','boolean','xor0','xor1','and','andpass','andfail','dshares','nested','finalpass','finalfail'}
assert required<={e['key'] for e in events},required-{e['key'] for e in events}
fraction_events=[e for e in events if '\\frac' in F[e['key']] or '\\tfrac' in F[e['key']]]
for i,e in enumerate(fraction_events):
    # Inspect the first stable frame after each reveal/morph, not only holds.
    dest=root/'qa'/f'fraction-video-{i:02}-{e["key"]}.png'
    subprocess.run([ffmpeg,'-v','error','-y','-ss',str(e['time']+1/30),'-i',str(video),'-frames:v','1',str(dest)],check=True)
    e['frame']=str(dest)
(root/'qa/fraction-video-audit.json').write_text(json.dumps(fraction_events,indent=2))
for group in range((len(fraction_events)+11)//12):
    grid=Image.new('RGB',(1920,870),'#101723');d=ImageDraw.Draw(grid)
    for i,e in enumerate(fraction_events[group*12:(group+1)*12]):
        im=Image.open(e['frame']).convert('RGB');im.thumbnail((480,270));x=i%4*480;y=i//4*290;grid.paste(im,(x,y));d.text((x+8,y+272),e['key']+' / '+e['type'],fill='white')
    grid.save(root/'qa'/f'fraction-video-contact-{group}.jpg')
report['validation']={'full_decode':'passed','reading_states':len(timeline),'sampled_frames':selected,'faststart':True,'math_report':'math-validation.json'}
report['validation']['fraction_event_frames']=len(fraction_events)
report['validation']['preserved_equation_checks']=len(required)
(root/'qa/video-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'video':str(video),'duration_seconds':duration,'resolution':[stream['width'],stream['height']],'fps':stream['r_frame_rate'],'codec':stream['codec_name'],'size_bytes':video.stat().st_size,'decode':'passed'},indent=2))
