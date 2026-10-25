"""PAMS Part 2, rendered with original ManimGL 1.7.2.

Part 1 is imported only for its proven camera/hold and typography utilities.
Equations remain filled LaTeX outlines during every transition.
"""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from manimlib import *
from pams_part1 import Film,txt,panel,BG,INK,MUTED,BLUE,PURPLE,YELLOW,GREEN,RED,CYAN,GRID,ROOT
from part2_lesson import CHAPTERS,F
from pathlib import Path
import os,json

ORANGE='#F4AD6D';GCOLOR='#91D6C1'
QA=ROOT/'qa/part2'
# These ManimGL primitives have explicit fill/stroke defaults which can
# override a generic color keyword. Apply the palette after construction.
def palette_primitive(cls):
    def make(*args,**kwargs):
        color=kwargs.pop('color',None);obj=cls(*args,**kwargs)
        if color is not None:obj.set_color(color)
        return obj
    return make
Dot=palette_primitive(Dot);Circle=palette_primitive(Circle)
Arc=palette_primitive(Arc);Arrow=palette_primitive(Arrow);Line=palette_primitive(Line)
def math(key,height=None,width=11.7):
    svg=(ROOT/'assets/part2'/f'{key}.svg').read_text(encoding='utf8')
    # Match the TeX point size, not total equation height: fractions and sums
    # need more vertical space without shrinking their letters.
    tex=F[key]
    height=height or (1.25 if '\\sum' in tex or '\\begin' in tex else 1.08 if '\\frac' in tex or '\\tfrac' in tex else .65)
    m=SVGMobject(svg_string=svg,height=height)
    if m.get_width()>width:m.set_width(width)
    return m

class PAMSPart2(Film):
    def setup(self):
        super().setup();self.previous=None;self.current=None;self.diagram=None;self.chapter_times=[]
    def title(self,n,s):
        self.chapter=n;self.chapter_times.append({'chapter':n,'start':self.time})
        old=[m for m in self.mobjects if m is not self.camera.frame]
        if old:self.play(*[FadeOut(m) for m in old],run_time=.6)
        self.caption=self.previous=self.current=self.diagram=None
        part='RECAP' if n==1 else 'PROOF 1' if n<=6 else 'PROOF 2' if n<=9 else 'PROOF 3' if n<=24 else 'CONCLUSION'
        brow=txt(f'PAMS  /  PART 2      {part}                                      {n:02} / 25',18,MUTED).move_to([0,3.65,0])
        heading=txt(s,37).move_to([0,3.1,0])
        line=Line([-6,2.65,0],[6,2.65,0],color=GRID,stroke_width=1.5)
        self.header=VGroup(brow,heading,line);self.play(FadeIn(self.header),run_time=.7)
    def equation(self,key):
        if self.previous is not None:self.play(FadeOut(self.previous),run_time=.25)
        if self.current is not None:
            self.play(self.current.animate.scale(.65).move_to([0,2.05,0]).set_opacity(.62),run_time=.65)
            self.previous=self.current
        else:self.previous=None
        self.current=math(key).move_to([0,.85,0])
        self.play(FadeIn(self.current,shift=.16*DOWN),run_time=.75)
        self.events.append({'key':key,'time':round(self.time,3),'type':'reveal' if self.previous is None else 'derivation','chapter':self.chapter})
    def say(self,s,hold=0):
        new=VGroup(*[txt(line,29) for line in s.split('\n')]).arrange(DOWN,buff=.13).move_to([0,-3.02,0])
        if self.caption is not None:self.play(FadeOut(self.caption),run_time=.18)
        self.play(FadeIn(new),run_time=.28);self.caption=new;self.beat+=1
        # Reading estimates leave time to return from the caption to the equation.
        hold=max(hold,6.3,len(s.split())/2.8+1)
        if 2<=self.chapter<=9:hold+=1.5
        self.timeline.append({'beat':self.beat,'chapter':self.chapter,'time':round(self.time,3),'hold':hold,'caption':s})
        self.update_frame(force_draw=True)
        self.get_image().save(QA/f'{type(self).__name__}-{self.beat:03}.png')
        for m in self.mobjects:
            if m is self.camera.frame:continue
            lo=m.get_corner(DL);hi=m.get_corner(UR)
            assert lo[0]>=-6.85 and hi[0]<=6.85 and lo[1]>=-3.85 and hi[1]<=3.85,(self.beat,lo,hi)
        self.wait(.15 if os.getenv('PAMS_PREVIEW')=='1' else hold)
    def dclear(self):
        if self.diagram is not None:self.play(FadeOut(self.diagram),run_time=.35)
        self.diagram=VGroup();self.add(self.diagram)
    def put(self,*mobs):
        self.diagram.add(*mobs);self.play(*[FadeIn(m) for m in mobs],run_time=.55)
    def label(self,text,pos,color=MUTED,size=23):
        return txt(text,size,color).move_to(pos)
    def axis(self,lo,hi,y=-1.15,width=10):
        p=lambda x:np.array([-width/2+(x-lo)/(hi-lo)*width,y,0])
        axis=Line(p(lo),p(hi),color=GRID,stroke_width=2);self.put(axis)
        return p
    def mark(self,p,x,label,color=INK,dy=-.42):
        mark=VGroup(Line(p(x)+UP*.1,p(x)+DOWN*.1,color=color),self.label(label,p(x)+UP*dy,color,21))
        self.put(mark);return mark
    def draw(self,kind):
        if not kind:return
        # Meaningful motions update an existing diagram, retaining its scale.
        if kind=='discard':
            self.play(*[f.animate.shift(.65*DOWN).set_opacity(.15) for f in self.fracs],run_time=1.6);return
        if kind=='collect':
            self.dclear();p=self.axis(0,3)
            for k in range(4):self.mark(p,k,str(k))
            self.put(Line(p(0),p(2.4),color=PURPLE,stroke_width=18))
            self.put(self.label('discarded fractions: 2.4',[-.9,-.5,0],PURPLE))
            self.play(Indicate(self.diagram[-1]),run_time=1);return
        if kind=='correct':
            self.play(self.dot.animate.move_to(self.p(1)),run_time=1.8)
            self.put(self.label('add 2',self.p(0)+UP*.45,YELLOW));return
        if kind=='shift2':
            self.play(self.dot.animate.move_to(self.p(2)),run_time=1.8)
            self.put(Arrow(self.p(0)+UP*.22,self.p(2)+UP*.22,color=YELLOW,buff=0),self.label('up to 2',self.p(1)+DOWN*.85,YELLOW,21));return
        if kind=='inside_outside':
            self.play(self.dot.animate.move_to(self.p(1100)).set_color(RED),run_time=1.7)
            self.play(self.dot.animate.move_to(self.p(1000)).set_color(BLUE),run_time=1.7);return
        if kind=='relative':
            self.dclear();p=self.axis(-10,120);self.p=p
            self.put(Line(p(0),p(104),color=GREEN,stroke_width=9))
            for x,l,c in [(0,'0 = start',GREEN),(11,'11 = s',CYAN),(104,'104 = L',ORANGE)]:
                self.mark(p,x,l,c,dy=.45 if x==11 else -.42)
            self.put(Dot(p(11),color=CYAN,radius=.08));return
        if kind in ['around','circle50','circle200']:
            target={'around':0,'circle50':PI/6,'circle200':-PI/4}[kind]
            if kind=='circle50':
                self.play(FadeOut(self.dot),run_time=.25)
                self.dot.move_to(self.ccenter+LEFT*.9);self.cangle=PI
                self.play(FadeIn(self.dot),run_time=.25)
            start=self.cangle
            path=Arc(start_angle=start,angle=target-start,radius=.9,arc_center=self.ccenter)
            self.play(MoveAlongPath(self.dot,path),run_time=2.3);self.cangle=target;return
        if kind=='alpha_combine':
            self.dclear();p=self.axis(0,1.5)
            for x in [0,1]:self.mark(p,x,str(x))
            self.put(Line(p(0),p(.8),color=PURPLE,stroke_width=15))
            piece=Line(p(.8)+UP*.45,p(1.2)+UP*.45,color=CYAN,stroke_width=15);self.put(piece)
            self.play(piece.animate.shift(DOWN*.45),run_time=1.4)
            self.put(self.label('0.8 + 0.4 crosses one whole unit',[0,-.45,0],PURPLE));return
        if kind=='z_shift':
            self.play(self.dot.animate.move_to(self.p(760)),run_time=1.6)
            self.put(self.label('0, 1, or 2 more',[-1,-.45,0],YELLOW));return
        if kind=='edge_shift':
            self.play(self.dot.animate.move_to(self.p(-2)),run_time=1.8)
            self.put(Arrow(self.p(-4)+UP*.35,self.p(-2)+UP*.35,color=YELLOW,buff=0),self.label('+2 at most',self.p(-3)+UP*.65,YELLOW,21));return
        if kind=='edge_threshold':
            self.put(Line(self.p(-1)+DOWN*.28,self.p(-1)+UP*.6,color=RED,stroke_width=4),self.label('threshold',self.p(-1)+UP*.85,RED,22));return
        if kind=='outside_shift':
            self.play(self.dot.animate.move_to(self.p(2)),run_time=1.7);return
        if kind=='no_wrap_shift':
            self.play(self.dot.animate.move_to(self.p(-2)),run_time=1.7);return
        if kind in ['recap1','recap2','recap3']:
            self.draw('roadmap');self.play(Indicate(self.diagram[int(kind[-1])-1],color=YELLOW),run_time=1.2);return
        self.dclear()
        if kind=='roadmap':
            names=['1   Why add 2?','2   Why 14 bits?','3   Why this test?']
            boxes=VGroup(*[panel(t,c,3.3,.8) for t,c in zip(names,[YELLOW,CYAN,GREEN])]).arrange(RIGHT,buff=.6).move_to([0,-1.1,0])
            self.put(*boxes)
            for i in range(2):self.put(Arrow(boxes[i].get_right(),boxes[i+1].get_left(),buff=.08,color=GRID))
        elif kind in ['floor','split']:
            self.fracs=[]
            vals=[(2,.8),(3,.7),(4,.9)] if kind=='floor' else [(4,.7),(3,.2),(2,.9)]
            for i,(whole,frac) in enumerate(vals):
                x=-3.8+i*3.8;w=whole*.35
                rect=Rectangle(width=w,height=.45,fill_color=BLUE,fill_opacity=.8,stroke_width=0).move_to([x,-1,0])
                f=Rectangle(width=frac*.35,height=.45,fill_color=PURPLE,fill_opacity=.9,stroke_width=0).next_to(rect,RIGHT,buff=.04)
                self.put(rect,f,self.label(str(whole),[x,-1.6,0],BLUE),self.label(str(frac),[x+1.25,-1.6,0],PURPLE))
                self.fracs.append(f)
            self.put(self.label('whole parts',[-3.8,-.45,0],BLUE),self.label('fractional pieces',[3.8,-.45,0],PURPLE))
        elif kind=='fraction_sum':
            p=self.axis(0,3)
            for k in range(4):self.mark(p,k,str(k))
            for k,c in enumerate([BLUE,CYAN,PURPLE]):self.put(Line(p(k),p(k+1)-RIGHT*.07,color=c,stroke_width=12))
            self.put(self.label('floor 0',p(.5)+UP*.4,BLUE),self.label('floor 1',p(1.5)+UP*.4,CYAN),self.label('floor 2',p(2.5)+UP*.4,PURPLE))
            self.put(Circle(radius=.08,color=RED,fill_color=BG,fill_opacity=1).move_to(p(3)))
        elif kind=='correction':
            self.p=self.axis(-3,3)
            for x in [-2,-1,0,1,2]:self.mark(self.p,x,str(x),YELLOW if x>0 else MUTED)
            self.dot=Dot(self.p(-1),radius=.11,color=BLUE);self.put(self.dot,self.label('difference from the true transform',[0,-.45,0]))
        elif kind=='cases':
            boxes=VGroup(*[panel(t,YELLOW,3,.7) for t in ['loss 0 → remains 2','loss 1 → remains 1','loss 2 → remains 0']]).arrange(RIGHT,buff=.55).move_to([0,-1.15,0]);self.put(*boxes)
        elif kind in ['modulo','two_circles']:
            for x,label,amount,c in [(-3.1,'original circle','3329',BLUE),(3.1,'transformed circle','16384',CYAN)]:
                center=np.array([x,-1.2,0]);circle=Circle(radius=.66,color=c).move_to(center)
                self.put(circle,self.label(amount,center,c,25),self.label(label,center+DOWN*.95,c,20))
                dot=Dot(center+UP*.66,radius=.07,color=YELLOW);self.put(dot)
                self.play(MoveAlongPath(dot,Arc(start_angle=PI/2,angle=-TAU,radius=.66,arc_center=center)),run_time=1.1)
            self.put(Arrow([-1.9,-1.2,0],[1.9,-1.2,0],color=YELLOW),self.label('one full turn',[0,-.7,0],YELLOW))
        elif kind in ['spacing','thirteen']:
            self.p=self.axis(-.5,10.5);step=2 if kind=='thirteen' else 4
            self.mark(self.p,0,'F(0) = 0',BLUE);self.mark(self.p,step,f'F(1) = {step}',GCOLOR)
            self.dot=Dot(self.p(0),radius=.1,color=BLUE);self.put(self.dot)
            self.put(Line(self.p(0),self.p(step),color=GCOLOR,stroke_width=7))
            self.put(self.label(f'{step}-unit gap',self.p(step/2)+UP*.5,GCOLOR))
        elif kind=='floor_step':
            p=self.axis(4,7)
            for x in [4,5,6,7]:self.mark(p,x,str(x))
            d=Dot(p(4.2),color=BLUE);self.put(d);self.play(d.animate.move_to(p(4.8)),run_time=1.3)
            self.put(self.label('floor stays 4',[-3,-.4,0],BLUE));self.play(d.animate.move_to(p(5.1)),run_time=1.3)
            self.put(self.label('then becomes 5',[3,-.4,0],CYAN))
        elif kind in ['interval','ordinary']:
            self.p=self.axis(975,1110);p=self.p
            self.put(Line(p(989),p(1093),color=GREEN,stroke_width=10))
            self.mark(p,989,'989 = a',GREEN);self.mark(p,1093,'1093: next boundary',ORANGE)
            self.dot=Dot(p(1000),radius=.1,color=BLUE);self.put(self.dot,self.label('1000',p(1000)+UP*.45,BLUE))
        elif kind=='circle':
            self.ccenter=np.array([-3.5,-1.35,0]);self.cangle=PI
            c=Circle(radius=.9,color=GRID).move_to(self.ccenter);self.put(c)
            arc=Arc(start_angle=PI,angle=-PI,radius=.9,arc_center=self.ccenter,color=GREEN,stroke_width=8);self.put(arc)
            for theta,label,color in [(PI,'3225',GREEN),(PI/2,'0',MUTED),(0,'105',ORANGE),(-PI/4,'200',RED)]:
                p=self.ccenter+1.3*np.array([np.cos(theta),np.sin(theta),0]);self.put(self.label(label,p,color,21))
            self.dot=Dot(self.ccenter+LEFT*.9,radius=.09,color=CYAN);self.put(self.dot)
            self.put(self.label('forward around the circle',[2,-.8,0],CYAN,26),self.label('schematic; not to scale',[2,-1.4,0],MUTED,21))
        elif kind=='alpha':
            self.put(panel('scaled start = whole + fraction',PURPLE,7,.8).move_to([0,-1,0]),self.label('Keep the fraction until after adding the distance.',[0,-1.8,0],MUTED,23))
        elif kind in ['g','g_steps']:
            p=self.axis(0,15)
            for n,v in enumerate([0,5,10,15]):
                self.mark(p,v,f'G({n}) = {v}',GCOLOR,dy=-.45 if n%2==0 else .45)
                self.put(Dot(p(v),color=GCOLOR,radius=.08))
            self.put(self.label('example: a = 989, same alpha at each step',[0,-2.05,0],PURPLE,21))
        elif kind=='z_distance':
            self.p=self.axis(754,764)
            for x in [758,759,760]:self.mark(self.p,x,str(x),YELLOW if x!=758 else GCOLOR)
            self.dot=Dot(self.p(758),radius=.1,color=BLUE);self.put(self.dot)
        elif kind=='threshold':
            p=self.axis(1022,1030)
            self.mark(p,1028,'1028: width',ORANGE,dy=.5);self.mark(p,1027,'1027: threshold',RED,dy=-.5)
            self.put(Arrow(p(1028),p(1027),buff=0,color=RED),self.label('subtract one',[0,-2.1,0],RED))
        elif kind in ['edge','outside']:
            self.p=self.axis(-5,3);p=self.p
            for x,l,c,dy in [(-4,'G(L) − 4',GCOLOR,-.45),(-2,'G(L) − 2',YELLOW,-.85),(-1,'G(L) − 1',RED,-.45),(0,'G(L)',ORANGE,.45)]:self.mark(p,x,l,c,dy)
            self.dot=Dot(p(-4 if kind=='edge' else 0),color=BLUE if kind=='edge' else RED,radius=.11);self.put(self.dot)
        elif kind=='edge_original':
            p=self.axis(-3,2)
            for x in [-3,-2,-1,0,1,2]:
                self.put(Dot(p(x),color=GREEN if x<0 else RED,radius=.09))
            self.mark(p,-1,'L − 1: last allowed',GREEN,dy=-.5);self.mark(p,0,'L: first outside',RED,dy=.5)
        elif kind in ['no_wrap','danger']:
            self.p=self.axis(-6,1);p=self.p
            for x,l,c in [(-4,'M − 4',GCOLOR),(-2,'M − 2',YELLOW),(0,'M',RED)]:self.mark(p,x,l,c)
            self.dot=Dot(p(-4),color=BLUE,radius=.1);self.put(self.dot)
            self.put(Line(p(0)+DOWN*.25,p(0)+UP*.55,color=RED,stroke_width=4),self.label('full turn',p(0)+UP*.85,RED))
            if kind=='danger':self.put(self.label('Beyond M, the remainder starts over.',[-1,-.4,0],RED))
        elif kind=='equivalence':
            boxes=VGroup(*[panel(t,c,3.3,.8) for t,c in [('compresses to c',BLUE),('inside interval',CYAN),('Z below theta',GREEN)]]).arrange(RIGHT,buff=.6).move_to([0,-1.15,0]);self.put(*boxes)
            for i in range(2):self.put(Arrow(boxes[i].get_right(),boxes[i+1].get_left(),buff=.06,color=YELLOW))
        elif kind=='end':
            self.put(self.label('PAMS — Part 2: Mathematical Proofs',[0,-.8,0],INK,32),self.label('Next: Hardware Realization',[0,-1.6,0],CYAN,29))
    def construct(self):
        selected=os.getenv('PAMS_CHAPTERS','')
        selected={int(i) for i in selected.split(',')} if selected else set(range(1,26))
        for ci,ch in enumerate(CHAPTERS,1):
            if ci not in selected:continue
            self.title(ci,ch['title']);self.draw(ch['diagram'])
            for beat in ch['beats']:
                self.equation(beat['key'])
                if beat['action']:self.draw(beat['action'])
                self.say(beat['caption'],beat['hold'])
        self.wait(.2 if os.getenv('PAMS_PREVIEW')=='1' else 3)
        (QA/f'{type(self).__name__}-timeline.json').write_text(json.dumps(self.timeline,indent=2),encoding='utf8')
        (QA/f'{type(self).__name__}-equations.json').write_text(json.dumps(self.events,indent=2),encoding='utf8')
        (QA/f'{type(self).__name__}-chapters.json').write_text(json.dumps(self.chapter_times,indent=2))

class Part2Preview(PAMSPart2):pass
