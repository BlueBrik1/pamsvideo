"""Verify the encoded movie and extract post-transition frames for visual QA."""
from pathlib import Path
import subprocess,json,os,hashlib
from PIL import Image,ImageDraw
from part2_lesson import F,CHAPTERS
root=Path(__file__).parent;qa=root/'qa/part2';video=root/'output/PAMS_Part_2.mp4'
ffbin=next((root/'tools/ffmpeg').glob('*/bin'))
ffmpeg=str(ffbin/'ffmpeg.exe');ffprobe=str(ffbin/'ffprobe.exe')
def run(args):return subprocess.run(args,check=True)
timeline=json.loads((qa/'PAMSPart2-timeline.json').read_text(encoding='utf8'))
events=json.loads((qa/'PAMSPart2-equations.json').read_text(encoding='utf8'))
chapters=json.loads((qa/'PAMSPart2-chapters.json').read_text())
assert len(timeline)==len(F)==len(events)
assert {e['key'] for e in events}==set(F)
raw=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_streams','-show_format','-of','json',str(video)]))
duration=float(raw['format']['duration'])
metadata=';FFMETADATA1\ntitle=PAMS - Part 2: Mathematical Derivations and Proofs\n'
for i,c in enumerate(chapters):
 end=chapters[i+1]['start'] if i+1<len(chapters) else duration
 title=CHAPTERS[i]['title'].replace('=','\\=')
 metadata+=f"[CHAPTER]\nTIMEBASE=1/1000\nSTART={int(c['start']*1000)}\nEND={int(end*1000)}\ntitle={i+1:02}. {title}\n"
(qa/'chapters.ffmeta').write_text(metadata,encoding='utf8')
temp=video.with_name('PAMS_Part_2_seekable.mp4')
run([ffmpeg,'-v','error','-y','-i',str(video),'-i',str(qa/'chapters.ffmeta'),'-map','0:v:0','-map_metadata','1','-map_chapters','1','-c','copy','-movflags','+faststart',str(temp)])
os.replace(temp,video)
report=json.loads(subprocess.check_output([ffprobe,'-v','error','-show_streams','-show_format','-show_chapters','-of','json',str(video)]))
stream=next(s for s in report['streams'] if s['codec_type']=='video')
assert(stream['width'],stream['height'])==(1920,1080)
assert stream['codec_name']=='h264' and stream['r_frame_rate']=='30/1'
assert 1080<duration<3600 and len(report['chapters'])==25
run([ffmpeg,'-v','error','-i',str(video),'-map','0:v:0','-f','null','-'])
samples=[]
for ci in range(1,26):
 states=[t for t in timeline if t['chapter']==ci]
 for t in [states[len(states)//2],states[-1]]:
  samples.append({'name':f"scene-{ci:02}-beat-{t['beat']:03}",'time':t['time']+min(2,t['hold']/2)})
fraction_events=[e for e in events if '\\frac' in F[e['key']] or '\\tfrac' in F[e['key']]]
for e in fraction_events:
 samples.append({'name':'fraction-'+e['key'],'time':e['time']+1/30})
# During the upward motion of a fraction, not only after the next reveal.
for key in ['p2_08_01','p2_13_02','p2_16_02','p2_16_03','p2_19_02','p2_23_04']:
 index=next(i for i,e in enumerate(events) if e['key']==key)
 following=events[index+1]
 samples.append({'name':'moving-'+key,'time':following['time']-.75-.32})
samples.append({'name':'ending','time':duration-2})
for s in samples:
 dest=qa/(s['name']+'.png');s['file']=str(dest)
 run([ffmpeg,'-v','error','-y','-ss',str(s['time']),'-i',str(video),'-frames:v','1',str(dest)])
 assert Image.open(dest).getbbox()
for kind,prefix in [('scene','scene-'),('fraction','fraction-'),('moving','moving-')]:
 subset=[s for s in samples if s['name'].startswith(prefix)]
 for start in range(0,len(subset),12):
  sheet=Image.new('RGB',(1920,1160),'#101723');draw=ImageDraw.Draw(sheet)
  for i,s in enumerate(subset[start:start+12]):
   im=Image.open(s['file']);im.thumbnail((640,360));x=i%3*640;y=i//3*290
   im=im.resize((480,270));sheet.paste(im,(x,y));draw.text((x+4,y+272),s['name'],fill='white')
  sheet.save(qa/f'encoded-{kind}-{start//12:02}.jpg')
original=json.loads((qa/'math-validation.json').read_text())['part1_sha256']
if original is not None:
 assert hashlib.sha256((root/'output/PAMS_Part_1.mp4').read_bytes()).hexdigest()==original
proof3=chapters[24]['start']-chapters[9]['start']
instruction=chapters[24]['start']-chapters[1]['start']
report['validation']={'full_decode':'passed','all_equations':len(events),'caption_states':len(timeline),'chapter_count':25,'fraction_events':len(fraction_events),'sample_count':len(samples),'proof3_fraction':proof3/instruction,'part1_unchanged':True if original is not None else None,'faststart':True}
(qa/'video-validation.json').write_text(json.dumps(report,indent=2))
(qa/'encoded-samples.json').write_text(json.dumps(samples,indent=2))
print(json.dumps({'video':str(video),'seconds':duration,'bytes':video.stat().st_size,**report['validation']},indent=2))
