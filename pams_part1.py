"""PAMS Part 1. Original 3b1b ManimGL; equations compiled by real LaTeX.

Render: manimgl pams_part1.py PAMSPart1 -w --hd --fps 30
PAMS_PREVIEW=1 shortens reading holds for production previews only.
"""
from manimlib import *
from pathlib import Path
import os, json

ROOT=Path(__file__).parent
BG='#101723'; INK='#F1F5FC'; MUTED='#AAB8CC'
BLUE='#67B5FF'; PURPLE='#C59AFF'; YELLOW='#FFD96A'
GREEN='#79DEA5'; RED='#FF7E8B'; CYAN='#69DAE3'; GRID='#34445A'
PREVIEW=os.getenv('PAMS_PREVIEW')=='1'

def txt(s,size=32,color=INK):
    m=Text(s,font='Segoe UI',font_size=size,color=color)
    if m.get_width()>12.0:m.set_width(12.0)
    return m

def eq(key,height=.62,width=11.8,color=INK):
    svg=(ROOT/'assets'/'outlined'/f'{key.encode().hex()}.svg').read_text(encoding='utf8')
    m=SVGMobject(svg_string=svg,height=height,color=color)
    if m.get_width()>width:m.set_width(width)
    return m

def panel(label,color=CYAN,width=2.4,height=.9):
    box=RoundedRectangle(width=width,height=height,corner_radius=.15,stroke_color=color,stroke_width=2,fill_color=BG,fill_opacity=1)
    text=txt(label,28,color)
    if text.get_width()>width-.3:text.set_width(width-.3)
    return VGroup(box,text)

def token(key,color=BLUE,width=1.5):
    box=RoundedRectangle(width=width,height=.8,corner_radius=.13,stroke_color=color,stroke_width=2,fill_color=color,fill_opacity=.1)
    return VGroup(box,eq(key,.36,width-.25,color))

def person(name,key,color,x):
    head=Circle(radius=.23,stroke_color=color,fill_color=color,fill_opacity=.18).move_to([x,1.22,0])
    body=Arc(start_angle=0,angle=PI,radius=.5,color=color).move_to([x,.67,0])
    lab=txt(name,32,color).move_to([x,.1,0])
    letter=eq(key,.33,color=color).move_to([x,1.9,0])
    return VGroup(head,body,lab,letter)

class Film(Scene):
    def wait(self,duration=None,**kwargs):
        # Reading holds contain no motion. Reuse the exact ManimGL camera
        # pixels instead of transferring an identical GPU frame repeatedly.
        duration=self.default_wait_time if duration is None else duration
        if self.skip_animations or self.window is not None or kwargs or not self.file_writer.write_to_movie or any(m.has_updaters() for m in self.get_mobject_family_members()):
            return super().wait(duration,**kwargs)
        self.pre_play();self.update_frame(force_draw=True)
        raw=self.camera.get_raw_fbo_data()
        frames=int(np.ceil(duration*self.camera.fps-1e-9))
        for _ in range(frames):self.file_writer.writing_process.stdin.write(raw)
        self.increment_time(frames/self.camera.fps)
        if self.file_writer.progress_display is not None:self.file_writer.progress_display.update(frames)
        self.post_play()
    def setup(self):
        super().setup(); self.caption=None; self.header=None; self.beat=0;self.timeline=[];self.events=[];self.chapter=0
    def title(self,n,s):
        self.chapter=n
        old=[m for m in self.mobjects if m is not self.camera.frame]
        if old:self.play(*[FadeOut(m) for m in old],run_time=.6)
        self.caption=None
        eyebrow=txt(f'PAMS  /  PART 1     {n:02d} / 16',18,MUTED).move_to([-4.8,3.65,0])
        title=txt(s,39).move_to([0,3.08,0])
        line=Line([-6,2.65,0],[6,2.65,0],color=GRID,stroke_width=1.5)
        self.header=VGroup(eyebrow,title,line);self.play(FadeIn(self.header),run_time=.65)
    def say(self,s,hold=6):
        new=VGroup(*[txt(line,30) for line in s.split('\n')]).arrange(DOWN,buff=.12).move_to([0,-2.94,0])
        if self.caption:self.play(FadeOut(self.caption),FadeIn(new),run_time=.4)
        else:self.play(FadeIn(new),run_time=.5)
        self.caption=new;self.beat+=1
        hold=max(hold,len(s.split())/2.6+1)
        self.timeline.append({'beat':self.beat,'chapter':self.chapter,'time':round(self.time,3),'hold':hold,'caption':s})
        # Save every reading state for contact-sheet QA.
        self.update_frame(force_draw=True)
        self.get_image().save(ROOT/'qa'/f'{type(self).__name__}-{self.beat:03}.png')
        for m in self.mobjects:
            if m is self.camera.frame:continue
            lo=m.get_corner(DL);hi=m.get_corner(UR)
            if lo[0]<-6.85 or hi[0]>6.85 or lo[1]<-3.85 or hi[1]>3.85:
                raise ValueError(f'Unsafe layout at beat {self.beat}: {lo}, {hi}')
        self.wait(.18 if PREVIEW else hold)
    def formula(self,key,y=1.25,height=.65,color=INK,width=11.8):
        m=eq(key,height,width,color).move_to([0,y,0]);self.play(FadeIn(m,shift=.12*UP),run_time=.75)
        self.events.append({'key':key,'time':round(self.time,3),'type':'reveal','chapter':self.chapter});return m
    def morph(self,old,key,y=None,height=.65,color=INK,width=11.8):
        m=eq(key,height,width,color).move_to(old.get_center() if y is None else [0,y,0])
        self.play(ReplacementTransform(old,m),run_time=1.5)
        self.events.append({'key':key,'time':round(self.time,3),'type':'morph','chapter':self.chapter});return m
    def remove_visuals(self):
        keep=[self.header,self.caption]
        mobs=[m for m in self.mobjects if m not in keep and m is not self.camera.frame]
        if mobs:self.play(*[FadeOut(m) for m in mobs],run_time=.5)
    def people(self):
        a=person('Alice','A',PURPLE,-4.7);b=person('Bob','B',BLUE,4.7)
        line=Line([-3.9,.8,0],[3.9,.8,0],color=GRID)
        public=txt('PUBLIC CONNECTION',20,MUTED).move_to([0,.35,0])
        self.play(FadeIn(a),FadeIn(b),ShowCreation(line),FadeIn(public),run_time=1)
        return a,b
    def travel(self,key,start,end,color=YELLOW):
        t=token(key,color).move_to(start);self.play(FadeIn(t),run_time=.4)
        self.play(t.animate.move_to(end),run_time=2.3);return t
    def share_row(self,keys=('s1','s2','s3'),y=.1):
        g=VGroup(*[token(k,BLUE) for k in keys]).arrange(RIGHT,buff=.8).move_to([0,y,0])
        self.play(LaggedStart(*[FadeIn(m,shift=.3*UP) for m in g],lag_ratio=.2),run_time=1)
        self.add(g)
        return g
    def numberline(self,lo,hi,y=-.5,width=10):
        left=-width/2
        p=lambda x:np.array([left+(x-lo)/(hi-lo)*width,y,0])
        line=Line(p(lo),p(hi),color=MUTED,stroke_width=2)
        self.play(ShowCreation(line),run_time=.7)
        return line,p
    def interval(self,p,a,b,labels=True):
        g=VGroup(Line(p(a),p(b),color=GREEN,stroke_width=12),Dot(p(a),radius=.065,color=GREEN),Circle(radius=.07,stroke_color=GREEN,fill_color=BG,fill_opacity=1).move_to(p(b)))
        if labels:
            for x in [a,b]:g.add(eq(str(x),.28,color=GREEN).move_to(p(x)+DOWN*.45))
        self.play(ShowCreation(g),run_time=1);return g
    def point(self,p,x,label=None,color=BLUE):
        dot=Dot(p(x),radius=.09,color=color)
        lab=eq(label or str(x),.35,color=color).move_to(p(x)+UP*.48)
        g=VGroup(dot,lab);self.play(FadeIn(g,shift=.4*DOWN),run_time=.8);return g
    def close(self):
        (ROOT/'qa'/f'{type(self).__name__}-timeline.json').write_text(json.dumps(self.timeline,indent=2),encoding='utf8')
        (ROOT/'qa'/f'{type(self).__name__}-equations.json').write_text(json.dumps(self.events,indent=2),encoding='utf8')

    def s01(self):
        self.title(1,'How can a secret cross a public connection?')
        self.people()
        self.say('How can Alice and Bob agree on a secret\nwhen someone else can watch their connection?',7)
        msg=panel('visible message',YELLOW,2.7,.65).move_to([-2.6,1.5,0])
        observer=txt('Someone else can read what passes here',25,YELLOW).move_to([0,-.7,0])
        self.play(FadeIn(msg),FadeIn(observer));self.play(msg.animate.shift(5.2*RIGHT),run_time=2)
        self.say('A public connection is one other people can observe.\nAnything sent across it might be copied.',7)
        self.play(FadeOut(msg),FadeOut(observer))
        keys=VGroup(token('K',GREEN).move_to([-4.7,-1.05,0]),token('K',GREEN).move_to([4.7,-1.05,0]))
        self.play(FadeIn(keys))
        self.say('A secret key is a value that controls how messages are protected.\nWe will call their shared key K.',8)
        self.say('With the same key, Alice can protect a message\nand Bob can read it. This is called symmetric encryption.',8)
        self.say('But sending K openly would give the observer the key too.\nWe need a way for both sides to get it without sending it.',9)
        name=txt('ML-KEM',43,CYAN).move_to([0,-.8,0]);self.play(FadeIn(name))
        self.say('ML-KEM is a way to establish that shared key.\nIt sends other information that should not reveal the key.',8)
        self.say('Establishing a key comes first. Encrypting ordinary messages\nis a separate job that uses the key afterward.',8)
        self.play(FadeOut(name))
        ops=VGroup(panel('Encapsulation',PURPLE,3),panel('Decapsulation',BLUE,3)).arrange(RIGHT,buff=.7).move_to([0,-1.6,0])
        self.play(FadeIn(ops))
        self.say('Alice’s step is called encapsulation. Bob’s is decapsulation.\nWe will follow what each of them does.',7)
        self.say('They also need a way to check who they are talking to.\nThat is authentication; ML-KEM alone does not provide it.',8)

    def s02(self):
        self.title(2,'Two keys with different jobs');self.people()
        f=self.formula('keygen',-1.05,color=BLUE)
        self.say('Bob starts by making a pair of keys.\nKeyGen is simply the name of the key-generation procedure.',7)
        self.play(FadeOut(f))
        pk=token('pk',YELLOW).move_to([3.25,-.9,0]);sk=token('sk',BLUE).move_to([5.1,-.9,0])
        self.play(FadeIn(pk),FadeIn(sk))
        self.say('The public key, pk, is something Bob can give to anyone.\nThe secret key, sk, is something only Bob should have.',8)
        self.play(pk.animate.move_to([-4.7,-.9,0]),run_time=2.8)
        self.formula('sendpk',-1.8,.45,YELLOW)
        self.say('Alice receives the public key. Notice that the secret key\nhas stayed with Bob. Alice does not need to know it.',8)
        self.say('The keys are related, but knowing the public key should not\nlet someone work out the secret key. Their jobs are different.',8)
        self.say('Alice uses pk to create a shared secret and something to send.\nBob uses sk to recover the shared secret on his side.',8)

    def s03(self):
        self.title(3,'Alice makes a shared key and a ciphertext')
        f=self.formula('bit',1.4,.75,PURPLE)
        self.say('A bit is either a zero or a one.\nComputers can store a value as a sequence of these bits.',7)
        f=self.morph(f,'bits',1.4,.5,PURPLE)
        self.say('A 256-bit value contains 256 zeros and ones.\nOnly the beginning of the sequence is shown here.',7)
        self.play(FadeOut(f));f=self.formula('sample',1.5,.75,PURPLE)
        self.say('Alice chooses a sequence at random and calls it m.\nThe braces describe all possible 256-bit sequences.',8)
        arrow=self.formula('randomarrow',-.1,.55,PURPLE)
        self.say('The dollar-marked arrow means choose uniformly at random:\nevery sequence has the same chance of being chosen.',8)
        self.play(FadeOut(arrow));f=self.morph(f,'random',1.5,color=PURPLE)
        p=panel('inputs → function → output',PURPLE,6).move_to([0,-.1,0]);self.play(FadeIn(p))
        self.say('R is a function. Give it m and the public key pk,\nand it produces r, a value needed to make the ciphertext.',8)
        self.play(ReplacementTransform(p,panel('same inputs → same output',PURPLE,6).move_to([0,-.1,0])))
        self.say('This step is deterministic: the same inputs give the same output.\nThat matters because Bob will need to repeat it later.',8)
        self.say('We call r the encryption randomness. Although m was chosen\nat random, r is calculated from m and pk.',8)
        self.remove_visuals();f=self.formula('key',1.5,color=GREEN)
        self.say('Alice calculates K, the shared secret she will keep.\nK with parentheses names the calculation; K on the left is its result.',9)
        c=self.formula('cipher',.15,color=YELLOW)
        self.say('She also calculates C, the ciphertext she will send.\nIt carries information Bob needs without openly giving away K.',8)
        self.say('These functions are shorthand. The real ML-KEM standard\nhas more steps inside them than we are showing here.',8)
        self.say('We leave those steps inside the functions because our question is\nhow Bob checks the ciphertext, not how every encryption step works.',9)
        self.remove_visuals();self.people()
        k=token('K',GREEN).move_to([-4.7,-1,0]);self.play(FadeIn(k))
        self.travel('C',[-3,.8,0],[3,.8,0]);self.formula('sendc',-1.3,.5,YELLOW)
        self.say('C travels across the public connection. K stays with Alice.\nSeeing C should not let the observer recover the shared key.',8)

    def s04(self):
        self.title(4,'Why does Bob make the ciphertext again?')
        f=self.formula('decrypt',1.3,color=BLUE)
        self.say('Bob receives C and uses his secret key to decrypt it:\nhe tries to recover the internal value Alice started with.',8)
        self.say('The recovered value is called m-prime. The little prime mark\ntells us this is Bob’s version; we have not yet checked it.',8)
        self.say('Decrypt is another shorthand function.\nIt stands for the decryption calculations inside ML-KEM.',7)
        f=self.morph(f,'rerandom',1.3,color=BLUE)
        self.say('Bob puts his recovered value into R and obtains r-prime.\nIf the inputs agree with Alice’s, this result will agree too.',8)
        f=self.morph(f,'reencrypt',1.3,color=BLUE)
        self.say('Decrypting works backward to recover a value.\nRe-encrypting works forward again to make a new ciphertext.',8)
        self.say('Bob calls that new ciphertext C-prime.\nThe prime again marks his recomputed version.',7)
        self.play(FadeOut(f));left=token('C',YELLOW,2).move_to([-3,.9,0]);right=token('Cp',BLUE,2).move_to([3,.9,0])
        self.play(FadeIn(left),FadeIn(right));f=self.formula('equalq',-.65,.85)
        self.say('Why make it again? Bob needs to check that what arrived\nagrees with what his recovered value would produce.',8)
        self.say('A match passes this check. A mismatch means Bob must use\na different secret instead of accepting the normal one.',8)
        self.remove_visuals();self.formula('sharedkey',1,.7,GREEN)
        self.say('K-prime names Bob’s shared secret. For a valid encapsulation,\nit equals Alice’s K, so they have the same key.',8)
        self.remove_visuals()
        choices=VGroup(panel('match → normal shared secret',GREEN,7),panel('mismatch → fallback secret',RED,7)).arrange(DOWN,buff=.7).move_to([0,.7,0])
        self.play(FadeIn(choices))
        self.say('On a mismatch, ML-KEM chooses a fallback secret.\nThis is called implicit rejection; it does not simply return an error.',9)
        self.say('The implementation must make that choice without exposing\nthe secret values used along the way.',7)

    def s05(self):
        self.title(5,'Checking numbers that are held in pieces')
        self.formula('public',1.7,.65,YELLOW)
        self.say('PAMS is the part we are focusing on:\nchecking whether Bob’s recomputed ciphertext matches the one he received.',8)
        row=VGroup(*[token(k,YELLOW) for k in ['c1','c2','c3']]).arrange(RIGHT,buff=.8).move_to([0,-.05,0]);self.play(FadeIn(row))
        self.say('For this check, think of the ciphertext as a list of numbers.\nThe relevant numbers are called compressed coefficients.',8)
        for i,t in enumerate(row):
            self.play(Indicate(t,color=YELLOW),run_time=.7)
            self.say(['The small 1 means the first coefficient in the list.',
                      'The small 2 means the second coefficient.',
                      'The small 3 means the third. The dots mean the list continues.'][i],4)
        self.say('A subscript tells us which item we mean.\nThe letter i stands for whichever coefficient we are checking.',7)
        self.play(FadeOut(row));self.formula('concept',.1,.65,BLUE)
        self.say('X names Bob’s numbers before they are compressed\nto make C-prime. C and C-prime contain compressed values.',8)
        self.say('Here is the complication: PAMS is not given those secret\nnumbers as whole values. It gets separate pieces instead.',8)
        self.remove_visuals();f=self.formula('simple_shares',1.4,.75,BLUE)
        pieces=self.share_row(('4','3','5'),y=-.1)
        self.say('Start with ordinary addition: 4 plus 3 plus 5 is 12.\nThree separate numbers can together represent one number.',8)
        self.say('We call the separate pieces shares.\nThis little sum illustrates the idea, not a security guarantee.',7)
        self.say('Representing a secret with shares is called masking.\nKeeping the operations protected takes more care than just splitting numbers.',8)
        self.remove_visuals();clock=Circle(radius=.8,stroke_color=CYAN).move_to([0,.2,0]);dot=Dot(clock.point_from_proportion(0),color=CYAN)
        self.play(ShowCreation(clock),FadeIn(dot));self.play(MoveAlongPath(dot,clock),run_time=2)
        self.say('Next, imagine a clock that wraps back to zero.\nAfter the last position, counting starts again at the beginning.',7)
        f=self.formula('mod',1.8,.6,CYAN)
        self.say('ML-KEM uses 3329 positions, numbered 0 through 3328.\nAdding one to 3328 takes us back to zero.',8)
        self.say('“Modulo 3329” means keep the remainder after removing\nwhole groups of 3329. It is the arithmetic version of wrapping.',9)
        self.remove_visuals();shares=self.share_row(y=.1);f=self.formula('shares',1.6,1.2,BLUE)
        self.say('For a coefficient, add its three shares and then wrap modulo 3329.\nThat describes the value the shares represent together.',9)
        self.say('i selects the coefficient. j selects share 1, 2, or 3.\nThe large sum sign tells us to add those three shares.',8)
        self.say('PAMS is designed to do the check while keeping the pieces separate.\nPutting them together in ordinary storage could expose the secret.',9)
        self.remove_visuals();shares=self.share_row(y=1.65)
        proc=panel('PAMS',CYAN,3.5).move_to([0,-.15,0]);public=token('c',YELLOW).move_to([-4.6,-.15,0])
        arrows=VGroup(*[Arrow(t.get_bottom(),proc.get_top(),buff=.15,color=BLUE) for t in shares],Arrow(public.get_right(),proc.get_left(),buff=.15,color=YELLOW))
        self.play(FadeIn(proc),FadeIn(public),ShowCreation(arrows))
        self.say('These are the inputs: three arithmetic shares\nand one public compressed coefficient. There is no reconstructed X.',8)
        self.formula('compressq',-1.55,.55)
        self.say('The question is: would the number represented by these pieces\ncompress to the public coefficient? What does “compress” mean?',9)

    def s06(self):
        self.title(6,'Many original numbers, one compressed value')
        scores=VGroup(*[token(s,BLUE) for s in ['81','82','84']]).arrange(RIGHT,buff=.7).move_to([0,1.5,0])
        rounded=token('80',YELLOW).move_to([0,-.6,0]);self.play(FadeIn(scores),FadeIn(rounded))
        arrows=VGroup(*[Arrow(h.get_bottom(),rounded.get_top(),buff=.15,color=MUTED) for h in scores]);self.play(ShowCreation(arrows))
        self.say('Round these test scores to the nearest ten.\n81, 82, and 84 all become 80.',7)
        self.say('Knowing the rounded score does not tell us the exact original.\nSeveral numbers lead to the same answer.',7)
        self.say('Ciphertext compression has that same many-to-one property,\nalthough it uses a different formula.',7)
        self.remove_visuals();self.formula('fivebits',1.2,.65,YELLOW)
        self.say('The letter d tells us how many bits we keep.\nWith five bits, there are 32 possible values: 0 through 31.',8)
        t=self.formula('twopower',-.5,1.0,CYAN)
        self.say('Two to the power d means multiply d copies of 2.\nEach extra bit doubles the number of possible bit patterns.',8)
        self.remove_visuals();f=self.formula('compress',1.2,1.2)
        self.say('This is the ML-KEM compression formula.\nWe will read it one piece at a time.',7)
        f=self.morph(f,'compress_numerator',1.2,1.2,color=None)
        self.say('Start with the original coefficient x.\nMultiply it by the number of possible outputs, two to the power d.',8)
        f=self.morph(f,'compress_denominator',1.2,1.2,color=None)
        self.say('Then divide by 3329, the original coefficient modulus.\nThis changes the scale to the smaller output range.',8)
        f=self.morph(f,'compress',1.2,1.2);fl=self.formula('floor',-.65,.56,CYAN)
        self.say('The floor brackets mean round down to an integer.\nFor example, 3.7 becomes 3; minus 0.2 becomes minus 1.',8)
        self.play(FadeOut(fl));f=self.morph(f,'compress_half',1.2,1.2,color=None)
        r=self.formula('rounding',-.65,.65,CYAN)
        self.say('Adding one half before rounding down gives nearest-integer\nrounding here. 3.2 goes to 3, while 3.8 goes to 4.',9)
        self.play(FadeOut(r));f=self.morph(f,'compress_modulo',1.2,1.2,color=None)
        r=self.formula('wrap32',-.65,.6,CYAN)
        self.say('Finally, wrap into the allowed output range.\nWith five bits, 32 wraps to 0 and 33 wraps to 1.',8)
        self.play(FadeOut(r));f=self.morph(f,'compress',1.2,1.2)
        self.say('So: multiply, divide, add one half, round down, and wrap.\nThat is how the original coefficient becomes its compressed value.',9)
        self.formula('widths',-.65,.6,YELLOW)
        self.say('ML-KEM uses these four widths for different ciphertext parts.\nThe same idea applies to each: a range of inputs shares one output.',9)

    def s07(self):
        self.title(7,'Which original numbers would match?')
        line,p=self.numberline(940,1140,-.1);band=self.interval(p,989,1093)
        self.say('An interval is simply a range of numbers.\nThe green segment marks one such range.',7)
        inside=self.point(p,1050);outside=self.point(p,980,color=RED)
        self.say('1050 is inside this range; 980 is outside it.\nAll the integer values inside this compression interval give one output.',9)
        self.play(FadeOut(inside),FadeOut(outside))
        a=eq('a',.5,color=GREEN).move_to(p(989)+UP*.7);an=eq('an',.5,color=GREEN).move_to(p(1093)+UP*.7)
        self.play(FadeIn(a));self.say('We call the starting boundary a with subscript c-i.\nThe public compressed value tells us which range to use.',8)
        self.play(FadeIn(an));self.say('The next boundary is where the following interval begins.\nOur interval includes its start, but stops before that next boundary.',8)
        self.remove_visuals();fl=self.formula('floor',1.3,.6,CYAN);ce=self.formula('ceil',-.1,.6,GREEN)
        self.say('We already met floor, which rounds down.\nCeiling does the opposite: it rounds upward to an integer.',7)
        self.say('For example, the ceiling of 3.2 is 4.\nThe ceiling of minus 0.2 is 0, the next integer above it.',8)
        self.remove_visuals();f=self.formula('start',1.5,1.05,GREEN)
        self.say('This formula gives the starting boundary.\nIts inputs are the public coefficient and the bit width d.',8)
        e=self.formula('end',-.1,1.05,GREEN)
        self.say('The next-boundary formula changes minus one to plus one.\nBoth use ceiling, then wrap modulo 3329.',8)
        self.say('For now, these formulas tell us where the range is.\nPart 2 will explain why they give the right boundaries.',8)
        self.remove_visuals();self.formula('example',1.75,.48)
        line,p=self.numberline(940,1140,-.15);self.interval(p,989,1093)
        self.say('Take five bits and a public coefficient of 10.\nThe formulas give a starting boundary of 989 and a next boundary of 1093.',9)
        self.formula('interval',-1.35,.52,GREEN)
        self.say('Read this as: x is at least 989, but less than 1093.\nFor integers, that means 989 through 1092.',8)
        self.point(p,1000)
        self.say('1000 lies inside, so it compresses to 10.\nWe will keep using this example.',7)
        self.say('The displayed 1000 helps us follow the mathematics.\nPAMS does not need to expose that whole value while it works.',8)
        self.remove_visuals();self.formula('wrap',1.75,.52)
        circle=Circle(radius=1.05,stroke_color=GRID).move_to([-2,-.25,0])
        arc=Arc(start_angle=PI/2-.48,angle=.96,radius=1.05,color=GREEN,stroke_width=12).shift([-2,-.25,0])
        zero=eq('0',.35,color=YELLOW).move_to([-2,1.1,0])
        self.play(ShowCreation(circle),ShowCreation(arc),FadeIn(zero));self.formula('wrapset',-.8,.48,width=5.9).shift(2.3*RIGHT)
        self.say('Some ranges cross zero, just as a clock does.\nFor four bits and output 0, this one begins at 3225.',8)
        self.say('It runs through 3328, wraps to 0, and ends at 104.\nThe next boundary, 105, is excluded. It is still one continuous range.',9)

    def s08(self):
        self.title(8,'Use a ruler with a different scale')
        l,p=self.numberline(0,3328,.8);l2,p2=self.numberline(0,16383,-.7)
        for key,pos in [('0',p(0)),('3328',p(3328)),('0',p2(0)),('16383',p2(16383))]:self.add(eq(key,.28,color=MUTED).move_to(pos+DOWN*.35))
        point=Dot(p(989),color=BLUE);self.play(FadeIn(point))
        self.say('Two rulers can describe the same position with different numbers.\nHere the lower ruler has more numbered positions.',8)
        self.play(point.animate.move_to(p2(4867)).set_color(CYAN),run_time=2)
        self.say('PAMS moves to a different numerical scale for the comparison.\nThe point stays in roughly the same place along the ruler.',8)
        self.remove_visuals();self.formula('power',1.5,.7,CYAN)
        self.say('Fourteen bits give 16384 possible bit patterns.\nWe use them to represent integers from 0 through 16383.',8)
        self.formula('f',-.1,1.2,CYAN)
        self.say('F-sub-14 is the function that changes the scale.\nGive it a number t: it multiplies by 16384, divides by 3329, then floors.',9)
        self.say('Flooring makes the result an integer. The input t can be\na share or a public boundary. This function does not hide a secret.',9)
        self.remove_visuals();self.formula('fbounds',1.55,.62,CYAN)
        l,p=self.numberline(4500,5700,-.3);self.interval(p,4867,5379)
        self.say('Our boundaries 989 and 1093 become 4867 and 5379.\nWe can now describe the same range on this larger scale.',8)
        self.say('Why use 14 bits? We will leave that question for Part 2.\nHere we are learning what the transformation does.',8)

    def s09(self):
        self.title(9,'The width gives us a comparison limit')
        l,p=self.numberline(4500,5700,.65);band=self.interval(p,4867,5379)
        self.formula('widthnum',-.65,.6,CYAN)
        self.say('Subtract the starting boundary from the next one.\nThe distance between them is 512 units.',7)
        delta=np.array([-5-p(4867)[0],0,0]);target=band.copy().shift(delta);target.remove(target[-1],target[-2])
        target.add(eq('0',.28,color=GREEN).move_to(p(4867)+delta+DOWN*.45));target.add(eq('512',.28,color=GREEN).move_to(p(5379)+delta+DOWN*.45))
        self.play(ReplacementTransform(band,target),run_time=2.5)
        self.say('Slide the range until its start is zero.\nIts position changes, but its width stays 512.',8)
        self.remove_visuals();self.formula('theta',1.1,.82,CYAN)
        self.say('The comparison uses a limit called theta.\nIt starts with that width, then subtracts one and wraps modulo 16384.',9)
        self.formula('thetanum',-.55,.65,CYAN)
        self.say('Here the width is 512, while the comparison threshold is 511.\nThose are different numbers; the minus-one adjustment matters.',9)
        self.say('We need the exact adjusted threshold to make the test.\nPart 2 will explain the minus one, rather than proving it here.',8)

    def s10(self):
        self.title(10,'Where is our number relative to the start?')
        l,p=self.numberline(940,1140,.5);band=self.interval(p,989,1093);pt=self.point(p,1000)
        self.say('How far is our number from the beginning of the acceptable range?\nThat is the position we want to describe.',8)
        delta=np.array([-5-p(989)[0],0,0]);target=band.copy().shift(delta)
        target.remove(target[-1],target[-2])
        target.add(eq('0',.28,color=GREEN).move_to(p(989)+delta+DOWN*.45))
        target.add(eq('104',.28,color=GREEN).move_to(p(1093)+delta+DOWN*.45))
        newpt=VGroup(Dot(p(1000)+delta,radius=.09,color=BLUE),eq('11',.35,color=BLUE).move_to(p(1000)+delta+UP*.48))
        self.play(ReplacementTransform(band,target),ReplacementTransform(pt,newpt),run_time=2)
        self.say('Imagine measuring from the start of the range instead of from\nthe old zero. The point keeps the same distance from that start.',9)
        self.say('But PAMS has pieces of the number, not the whole number.\nIt must get the comparison right using those pieces.',8)
        self.remove_visuals();shares=self.share_row(y=1.4)
        self.say('Begin with the three arithmetic shares.\nWe apply the scale-changing function to each one separately.',8)
        new=VGroup(*[token(k,CYAN,2.6) for k in ['fs1','fs2','fs3']]).arrange(RIGHT,buff=.55).move_to([0,-.15,0])
        self.play(ReplacementTransform(shares,new),run_time=1.5)
        self.say('These are three transformed shares.\nWe will combine them to find the position we need.',7)
        self.play(FadeOut(new));f=self.formula('z_sum',.9,1.2,CYAN)
        self.say('First, add the transformed shares.\nThe sum sign runs through j = 1, 2, and 3.',7)
        f=self.morph(f,'z_plus',.9,1.2,CYAN)
        self.say('Then add 2. This corrects for rounding\nwhen the shares were transformed separately.',7)
        f=self.morph(f,'z_minus',.9,1.2,CYAN)
        self.say('Subtract the transformed starting boundary.\nThat makes the position relative to the beginning of the range.',8)
        f=self.morph(f,'z',.9,1.4,CYAN)
        self.say('Finally, wrap modulo 16384. This is the full definition of Z.\nIt is a corrected relative position on the transformed scale.',9)
        self.say('It is not just the original coefficient on a new ruler.\nThe separate transformations and the +2 correction are essential.',8)
        self.remove_visuals();self.formula('numshares',1.65,.53,BLUE);self.formula('sumshares',.4,.56,BLUE)
        self.say('Use our example again: 300, 400, and 300\ntogether represent 1000 modulo 3329.',7)
        self.remove_visuals();f=self.formula('numf',1.6,.6,CYAN)
        self.say('300 becomes 1476. 400 becomes 1968.\nThe third share is also 300, so it also becomes 1476.',8)
        step=self.formula('zsteps',-.1,.65,CYAN)
        self.say('Adding those three transformed values gives 4920.',5)
        step=self.morph(step,'zcorrection',-.1,.65,CYAN)
        self.say('Add the correction of 2. The total is now 4922.',5)
        step=self.morph(step,'zrelative',-.1,.65,CYAN)
        self.say('Subtract 4867, our transformed starting boundary.\nThe result is 55. Wrapping modulo 16384 leaves it unchanged.',8)
        self.remove_visuals();self.formula('znum',.8,.73,CYAN)
        self.say('So the corrected relative position is 55.\nNext we compare it with the threshold, 511.',7)
        self.say('We show these totals to explain the mathematics.\nA protected implementation must not expose them as ordinary secret values.',8)
        self.say('Z does not make a number secret by itself.\nThe shares provide the representation; Part 2 explains the correction.',8)

    def s11(self):
        self.title(11,'Turn the comparison into yes or no')
        self.formula('yesno',1.4,.7)
        self.say('The answer we need is just yes or no.\nWe write yes as 1 and no as 0. This is a Boolean result.',8)
        self.remove_visuals();f=self.formula('compare',1.7,.75)
        l,p=self.numberline(0,650,-.3);self.interval(p,0,511);self.point(p,55,color=CYAN)
        self.say('The square brackets ask whether the statement inside is true.\nIf Z is less than theta, b is 1. Otherwise, b is 0.',9)
        self.say('The superscript in parentheses tells us which coefficient\nthis result belongs to. It is a label, not a power.',8)
        self.formula('pass',-1.55,.5,GREEN)
        self.say('55 is less than 511, so this coefficient passes.\nThe comparison is strictly less than: equality would not pass.',8)
        self.remove_visuals();self.formula('failshares',1.7,.5,BLUE);self.formula('fail',.4,.65,RED)
        self.say('Try shares 400, 400, and 400 instead. They represent 1200.\nThe corrected position is 1039, which is not below 511.',9)
        self.say('That gives a 0: this coefficient does not match\nthe public compressed value 10.',7)
        self.remove_visuals();self.formula('equiv',.8,.72)
        self.say('The two tests describe the same match: being below the threshold\nand compressing to the expected public value.',8)
        self.say('We have seen what the test means. Part 2 will prove why it works,\nincluding the rounding adjustments and ranges that cross zero.',9)

    def s12(self):
        self.title(12,'Write out what each short name means')
        f=self.formula('compare',.7,.8)
        self.say('We have given names to the pieces of the calculation.\nWhat happens if we replace each name with its formula?',8)
        f=self.morph(f,'expanded1',.6,2.4)
        self.say('First replace Z and theta.\nAbove is the corrected position; below is its comparison limit.',8)
        self.play(Indicate(f,color=CYAN,scale_factor=1.025),run_time=1)
        self.say('Both sides still use F, our scale-changing function.\nNext we write that function out wherever it appears.',8)
        f=self.morph(f,'expanded2',.5,2.8)
        self.say('Each F has become a fraction followed by a floor operation.\nThe boundaries still have their short names.',9)
        self.play(Indicate(f,color=GREEN,scale_factor=1.025),run_time=1)
        self.say('One last substitution remains:\nreplace the two boundaries with their ceiling formulas.',7)
        f=self.morph(f,'expanded',.25,3.65,width=11.4)
        self.say('Here is the whole comparison, with every definition written out.\nTake a moment to follow the fractions, brackets, and two modulo operations.',14)
        self.say('The upper part combines the shares and measures from the start.\nThe lower part finds the adjusted threshold from the two boundaries.',11)
        self.say('The expression is long because the same definitions appear again.\nIt is still asking the same one question.',9)
        f=self.morph(f,'compare',.65,.9)
        self.say('Is the corrected position below the threshold?\nThe short expression and the expanded one are the same calculation.',8)

    def s13(self):
        self.title(13,'Keep the yes-or-no answer in pieces too')
        f=self.formula('xor00',1,.8)
        self.say('The answer is a bit, and we want to keep it shared too.\nFor bits, we use a different operation: XOR, shown by a circled plus.',9)
        self.say('With two inputs, XOR is 1 when the bits differ\nand 0 when they are the same. Two zeros give zero.',8)
        f=self.morph(f,'xor01',1,.8,GREEN);self.say('Zero and one differ, so their XOR is one.',5)
        f=self.morph(f,'xor10',1,.8,GREEN);self.say('One and zero also differ. The answer is still one.',5)
        f=self.morph(f,'xor11',1,.8);self.say('Two ones are the same, so their XOR is zero.',5)
        f=self.morph(f,'xor0',1,.85)
        self.say('With more bits, an even number of ones gives zero.\nHere the two ones cancel.',7)
        f=self.morph(f,'xor1',1,.85,GREEN)
        self.say('An odd number of ones gives one.\nThree ones therefore have XOR equal to one.',7)
        self.remove_visuals();shares=self.share_row(('b1','b2','b3'),y=.3);self.formula('boolean',1.75,.65)
        self.say('These three Boolean shares together represent one match bit.\nAn individual share is not the answer to the comparison.',8)
        self.say('For the coefficient, we added arithmetic shares modulo 3329.\nFor its yes-or-no result, we combine Boolean shares using XOR.',9)
        self.say('Keeping values shared is part of a protected implementation.\nIt does not, by itself, prove protection against every way secrets can leak.',9)

    def s14(self):
        self.title(14,'All the coefficients must pass')
        f=self.formula('and11',1,.8,GREEN)
        self.say('AND asks whether both inputs are true.\nOne AND one is one: both tests passed.',7)
        f=self.morph(f,'and10',1,.8,RED)
        self.say('One AND zero is zero.\nIf either test fails, “both passed” is false.',7)
        self.remove_visuals();self.formula('results',1.8,.55)
        self.say('A ciphertext has many coefficients, so there are many match bits.\nN is the total number of coefficients we check.',8)
        self.formula('and',.4,1.5)
        self.say('The large AND sign means apply that same rule to all the bits.\nThe final result is called D.',8)
        self.remove_visuals();f=self.formula('andpass',1.5,.7,GREEN)
        bits=VGroup(*[token('1',GREEN,1) for _ in range(4)]).arrange(RIGHT,buff=1).move_to([0,-.1,0]);self.play(FadeIn(bits))
        for i in range(3):self.play(ShowCreation(Arrow(bits[i].get_right(),bits[i+1].get_left(),buff=.1,color=GREEN)),run_time=.5)
        self.say('Every comparison passes, so D is one.\nThe complete recomputed ciphertext matches the received ciphertext.',8)
        f=self.morph(f,'andfail',1.5,.7,RED);zero=token('0',RED,1).move_to(bits[2]);self.play(ReplacementTransform(bits[2],zero))
        self.say('Change just one result to zero and the final answer becomes zero.\nOne mismatch is enough to make the ciphertexts different.',8)
        self.say('This row illustrates the logic. In hardware, protected AND\noperations combine shared answers without first exposing each bit.',9)

    def s15(self):
        self.title(15,'Read the final shared result')
        self.share_row(('d1','d2','d3'),y=.2);self.formula('dshares',1.7,.65)
        self.say('The final answer also stays in three Boolean shares.\nTheir XOR represents D, the overall match result.',8)
        self.remove_visuals();self.formula('nested',.6,2.1)
        self.say('Read the right side from the inside out.\nThree Boolean shares represent each coefficient’s match bit.',9)
        self.say('The AND across coefficients says they must all pass.\nThe left side says three final shares represent that overall answer.',9)
        self.say('Here j numbers a coefficient’s three shares.\nk numbers the three shares of the final answer.',8)
        self.say('This equality describes what the shares mean mathematically.\nIt is not an instruction to unmask every bit inside the circuit.',9)

    def s16(self):
        self.title(16,'Back to Alice and Bob')
        self.people();k=token('K',GREEN).move_to([-4.7,-1,0]);self.play(FadeIn(k));self.travel('C',[-3,.8,0],[3,.8,0])
        self.say('Bob makes his two keys. Alice uses the public one\nto make a shared secret K and a ciphertext C.',8)
        self.say('She sends C. Bob decrypts it, repeats the calculation,\nand checks whether his new ciphertext C-prime agrees with C.',8)
        self.remove_visuals();self.share_row(y=1.5)
        proc=panel('PAMS comparison',CYAN,4).move_to([0,-.1,0]);c=token('c',YELLOW).move_to([-4.5,-.1,0]);self.play(FadeIn(proc),FadeIn(c))
        self.formula('compare',-1.3,.55)
        self.say('PAMS does that check using the separate arithmetic shares\nand the public compressed coefficients.',8)
        self.say('Each range test produces a shared yes-or-no answer.\nProtected AND operations combine the answers.',7)
        self.remove_visuals();self.formula('finalpass',1.2,.65,GREEN);self.formula('finalfail',-.1,.65,RED)
        self.say('D is one exactly when the ciphertexts match.\nD is zero when at least one coefficient does not match.',8)
        self.say('PAMS stops at this shared answer. Decapsulation then uses it\nto choose the normal shared secret or the implicit-rejection secret.',9)
        self.remove_visuals();big=txt('PAMS',76,CYAN).move_to([0,1.3,0]);sub=txt('Part 1: Mathematical Overview',37).move_to([0,.1,0]);self.play(FadeIn(big),FadeIn(sub))
        self.say('The check works with the pieces,\nwithout needing to put the secret coefficients back together.',8)
        nextline=txt('Next: Why do these equations work?',28,MUTED).move_to([0,-1.25,0]);self.play(FadeIn(nextline))
        self.say('Based on the supplied PAMS notes and the ML-KEM standard, FIPS 203.\nAnimated with 3b1b ManimGL.',7)

class PAMSPart1(Film):
    def construct(self):
        for i in range(1,17):getattr(self,f's{i:02}')()
        self.close()

class Preview(Film):
    def construct(self):
        for i in [1,7,10,12,15,16]:getattr(self,f's{i:02}')()
        self.close()

class EquationDiagnostics(Film):
    def construct(self):
        self.title(6,'Equation rendering check')
        previous=None
        for key,height in [('compress',1.3),('compress_numerator',1.3),('compress_denominator',1.3),('compress_half',1.3),('compress_modulo',1.3),('f',1.3),('start',1.3),('end',1.3),('rounding',.8),('expanded1',2.4),('expanded2',2.8),('expanded',3.65),('nested',2.1)]:
            if previous is None:previous=self.formula(key,.25,height)
            else:previous=self.morph(previous,key,.25,height,color=None if key.startswith('compress_') else INK)
            self.say(key,1)
        self.close()
