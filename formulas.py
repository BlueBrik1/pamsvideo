"""LaTeX notation transcribed from mlkem.pdf and the supplied storyboard."""
F = {
'A':r'A', 'B':r'B', 'K':r'K', 'pk':r'pk', 'sk':r'sk', 'C':r'C', 'Cp':r"C'",
'keygen':r'B:\quad\operatorname{KeyGen}()\longrightarrow(pk,sk)',
'sendpk':r'B\xrightarrow{pk}A',
'sample':r'm\xleftarrow{\$}\{0,1\}^{256}',
'bits':r'0\;1\;1\;0\;1\;0\;0\;1\;\cdots\quad(256\ \text{bits})',
'random':r'r=R(m,pk)',
'key':r'K=K(pk,m,r)',
'cipher':r'C=C(pk,m,r)',
'sendc':r'A\xrightarrow{C}B',
'decrypt':r"B:\quad m'=\operatorname{Decrypt}(sk,C)",
'rerandom':r"r'=R(m',pk)",
'reencrypt':r"C'=\operatorname{Encrypt}(pk,m',r')",
'equalq':r"C'=C\;?",
'equal':r"C'=C",
'unequal':r"C'\ne C",
'sharedkey':r"K'=K",
'public':r'C=(c_1,c_2,c_3,\ldots)',
'concept':r'X=(x_1,x_2,x_3,\ldots)',
'shares':r'x_i=\left(\sum_{j=1}^{3}x_{ij}\right)\bmod3329',
'x':r'x_i', 's1':r'x_{i1}', 's2':r'x_{i2}', 's3':r'x_{i3}', 'c':r'c_i',
'compressq':r'\operatorname{Compress}_d(x_i)=c_i\;?',
'compress':r'\operatorname{Compress}_d(x)=\left\lfloor\frac{2^d x}{3329}+\frac12\right\rfloor\bmod2^d',
'widths':r'd\in\{4,5,10,11\}',
'floor':r'\lfloor3.7\rfloor=3,\qquad\lfloor-0.2\rfloor=-1',
'ceil':r'\lceil3.2\rceil=4,\qquad\lceil-0.2\rceil=0',
'mod':r'3328+1\equiv0\pmod{3329}',
'start':r'a_{c_i}=\left\lceil\frac{(2c_i-1)\cdot3329}{2^{d+1}}\right\rceil\bmod3329',
'end':r'a_{c_i+1}=\left\lceil\frac{(2c_i+1)\cdot3329}{2^{d+1}}\right\rceil\bmod3329',
'a':r'a_{c_i}', 'an':r'a_{c_i+1}',
'example':r'd=5,\quad c_i=10,\quad a_{10}=989,\quad a_{11}=1093',
'interval':r'989\le x_i<1093', 'inside':r'x_i=1000',
'wrap':r'd=4,\quad c_i=0:\quad a_0=3225,\quad a_1=105',
'wrapset':r'\{3225,\ldots,3328,0,\ldots,104\}',
'f':r'F_{14}(t)=\left\lfloor\frac{2^{14}t}{3329}\right\rfloor',
'power':r'2^{14}=16384',
'fbounds':r'F_{14}(989)=4867,\qquad F_{14}(1093)=5379',
'theta':r'\Theta_{c_i}=\left(F_{14}(a_{c_i+1})-F_{14}(a_{c_i})-1\right)\bmod2^{14}',
'thetanum':r'\Theta_{10}=(5379-4867-1)\bmod16384=511',
'widthnum':r'5379-4867=512',
'z':r'Z_i=\left(\sum_{j=1}^{3}F_{14}(x_{ij})+2-F_{14}(a_{c_i})\right)\bmod2^{14}',
'fs1':r'F_{14}(x_{i1})', 'fs2':r'F_{14}(x_{i2})', 'fs3':r'F_{14}(x_{i3})',
'numshares':r'x_{i1}=300,\qquad x_{i2}=400,\qquad x_{i3}=300',
'sumshares':r'(300+400+300)\bmod3329=1000',
'numf':r'F_{14}(300)=1476,\quad F_{14}(400)=1968',
'znum':r'Z_i=(1476+1968+1476+2-4867)\bmod16384=55',
'compare':r'b^{(i)}=[Z_i<\Theta_{c_i}]',
'pass':r'55<511\quad\Longrightarrow\quad b^{(i)}=1',
'fail':r'x_i=1200:\quad Z_i=1039\not<511\quad\Longrightarrow\quad b^{(i)}=0',
'failshares':r'(x_{i1},x_{i2},x_{i3})=(400,400,400)',
'equiv':r'[Z_i<\Theta_{c_i}]=[\operatorname{Compress}_d(x_i)=c_i]',
'expanded1':r'\begin{aligned}b^{(i)}=\Bigg[&\left(\sum_{j=1}^{3}F_{14}(x_{ij})+2-F_{14}(a_{c_i})\right)\bmod2^{14}\\&<\left(F_{14}(a_{c_i+1})-F_{14}(a_{c_i})-1\right)\bmod2^{14}\Bigg]\end{aligned}',
'expanded2':r'\begin{aligned}b^{(i)}=\Bigg[&\left(\sum_{j=1}^{3}\left\lfloor\frac{2^{14}x_{ij}}{3329}\right\rfloor+2-\left\lfloor\frac{2^{14}a_{c_i}}{3329}\right\rfloor\right)\bmod2^{14}\\&<\left(\left\lfloor\frac{2^{14}a_{c_i+1}}{3329}\right\rfloor-\left\lfloor\frac{2^{14}a_{c_i}}{3329}\right\rfloor-1\right)\bmod2^{14}\Bigg]\end{aligned}',
'boolean':r'b^{(i)}=b_1^{(i)}\oplus b_2^{(i)}\oplus b_3^{(i)}',
'xor0':r'1\oplus0\oplus1=0', 'xor1':r'1\oplus1\oplus1=1',
'b1':r'b_1^{(i)}', 'b2':r'b_2^{(i)}', 'b3':r'b_3^{(i)}',
'results':r'b^{(1)},\ b^{(2)},\ b^{(3)},\ \ldots,\ b^{(N)}',
'and':r'D=\bigwedge_{i=1}^{N}b^{(i)}',
'andpass':r'1\land1\land1\land1=1', 'andfail':r'1\land1\land0\land1=0',
'dshares':r'D=D_1\oplus D_2\oplus D_3',
'd1':r'D_1', 'd2':r'D_2', 'd3':r'D_3',
'nested':r'\boxed{D=\bigoplus_{k=1}^{3}D_k=\bigwedge_{i=1}^{N}\left(\bigoplus_{j=1}^{3}b_j^{(i)}\right)}',
'finalpass':r"D=1\iff C'=C", 'finalfail':r"D=0\iff C'\ne C",
}
boundary=lambda sign:r'\left\lfloor\frac{2^{14}}{3329}\left(\left\lceil\frac{(2c_i'+sign+r'1)\cdot3329}{2^{d+1}}\right\rceil\bmod3329\right)\right\rfloor'
F['expanded']=r'\begin{aligned}b^{(i)}=\Bigg[&\Bigg(\sum_{j=1}^{3}\left\lfloor\frac{2^{14}x_{ij}}{3329}\right\rfloor+2\\&\quad-'+boundary('-')+r'\Bigg)\bmod2^{14}\\&<\Bigg('+boundary('+')+r'\\&\quad-'+boundary('-')+r'-1\Bigg)\bmod2^{14}\Bigg].\end{aligned}'
for n in [0,1,3,4,5,10,11,55,104,105,300,400,511,512,989,1000,1093,1200,1476,1968,3225,3328,4867,5379,16383]: F[str(n)]=str(n)
F['domain']=r'0\le t\le3328';F['range']=r'0,1,\ldots,16383'
F.update({
 'bit':r'0\quad\text{or}\quad1',
 'possibilities':r'\{0,1\}^{256}',
 'randomarrow':r'\xleftarrow{\$}',
 'primes':r"m',\quad r',\quad C',\quad K'",
 'simple_shares':r'4+3+5=12',
 'c1':r'c_1','c2':r'c_2','c3':r'c_3',
 'twopower':r'2^d=\underbrace{2\times2\times\cdots\times2}_{d\ \text{factors}}',
 'fivebits':r'd=5:\quad2^5=32\quad\text{values: }0,1,\ldots,31',
 'rounding':r'\lfloor3.2+\tfrac12\rfloor=3,\qquad\lfloor3.8+\tfrac12\rfloor=4',
 'wrap32':r'32\bmod32=0,\qquad33\bmod32=1',
 'xor00':r'0\oplus0=0', 'xor01':r'0\oplus1=1',
 'xor10':r'1\oplus0=1', 'xor11':r'1\oplus1=0',
 'and11':r'1\land1=1','and10':r'1\land0=0',
 'z_sum':r'\sum_{j=1}^{3}F_{14}(x_{ij})',
 'z_plus':r'\sum_{j=1}^{3}F_{14}(x_{ij})+2',
 'z_minus':r'\sum_{j=1}^{3}F_{14}(x_{ij})+2-F_{14}(a_{c_i})',
 'fraction':r'\frac{2^d x}{3329}', 'half':r'\frac12',
 'F300':r'F_{14}(300)=1476', 'F400':r'F_{14}(400)=1968',
 'zsteps':r'1476+1968+1476=4920',
 'zcorrection':r'4920+2=4922', 'zrelative':r'4922-4867=55',
 'yesno':r'\text{yes}=1,\qquad\text{no}=0',
})
for n in [2,12,81,82,84,80,980,1050,1100,4920,4922]:F[str(n)]=str(n)
for key,term in [('numerator','2^d x'),('denominator','3329'),('half',r'\frac12'),('modulo',r'\bmod2^d')]:
    F['compress_'+key]=r'\color[HTML]{F1F5FC}'+F['compress'].replace(term,r'\textcolor[HTML]{FFD96A}{'+term+'}')

def outline_svg_strokes(svg):
    """Preserve TeX rules as filled vector outlines at their original thickness.

    MuPDF exports fraction rules as open stroked paths. SVGMobject's default
    stroke_width=0 removes these. Outlining before import makes their geometry
    scale with the glyphs and survive transforms without thin pixel strokes.
    Numerators, denominators, and rule positions remain TeX-generated.
    """
    import xml.etree.ElementTree as ET
    import pathops
    from fontTools.svgLib.path import parse_path
    from fontTools.pens.svgPathPen import SVGPathPen
    ET.register_namespace('', 'http://www.w3.org/2000/svg')
    ET.register_namespace('xlink','http://www.w3.org/1999/xlink')
    root=ET.fromstring(svg);count=0
    for element in root.iter():
        if element.tag.endswith('path') and element.get('stroke') not in [None,'none']:
            assert element.get('fill')=='none',element.attrib
            p=pathops.Path();parse_path(element.get('d'),p.getPen())
            p.stroke(float(element.get('stroke-width','1')),pathops.LineCap.BUTT_CAP,pathops.LineJoin.MITER_JOIN,10)
            pen=SVGPathPen(None);p.draw(pen)
            color=element.get('stroke')
            for key in list(element.attrib):
                if key.startswith('stroke'):del element.attrib[key]
            element.set('d',pen.getCommands());element.set('fill',color);count+=1
    return ET.tostring(root,encoding='unicode'),count

if __name__=='__main__':
    import json,subprocess
    from pathlib import Path
    import pymupdf
    root=Path(__file__).parent; assets=root/'assets';assets.mkdir(exist_ok=True)
    # One real LaTeX document, one tightly cropped page per equation.
    pre=r'\documentclass[multi=equationpage,border=2pt]{standalone}\usepackage{amsmath,amssymb,xcolor}\newenvironment{equationpage}{}{}\begin{document}'
    body='\n'.join(r'\begin{equationpage}$\displaystyle '+s+r'$\end{equationpage}' for s in F.values())
    (assets/'equations.tex').write_text(pre+'\n'+body+r'\end{document}',encoding='utf8')
    subprocess.run([str(root/'tools/tectonic.exe'),str(assets/'equations.tex')],check=True)
    doc=pymupdf.open(assets/'equations.pdf')
    assert len(doc)==len(F),(len(doc),len(F))
    fixed=assets/'outlined';fixed.mkdir(exist_ok=True);audit={}
    for key,page in zip(F,doc):
        svg=page.get_svg_image(text_as_path=True)
        (assets/(key.encode().hex()+'.svg')).write_text(svg,encoding='utf8')
        corrected,count=outline_svg_strokes(svg)
        (fixed/(key.encode().hex()+'.svg')).write_text(corrected,encoding='utf8')
        audit[key]=count
    (root/'qa/stroke-audit.json').write_text(json.dumps(audit,indent=2))
    pdf=pymupdf.open(root/'references/mlkem.pdf')
    for i,p in enumerate(pdf):p.get_pixmap(matrix=pymupdf.Matrix(1.5,1.5)).save(root/'qa'/f'reference-{i+1}.png')
    (assets/'formulas.json').write_text(json.dumps(F,indent=2),encoding='utf8')
    print('Compiled',len(F),'LaTeX equations')
