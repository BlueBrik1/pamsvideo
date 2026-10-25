from pathlib import Path
import json, hashlib
import numpy as np
q=3329;M=16384
F=lambda t:M*t//q
ceildiv=lambda a,b:-((-a)//b)
a=lambda c,d:ceildiv((2*c-1)*q,2**(d+1))%q
report={}
assert [a(10,5),a(11,5),a(0,4),a(1,4)]==[989,1093,3225,105]
assert (105-3225)%q==209 and (50-3225)%q==154
assert (200-3225)%q==304
assert (28+37+49)//10==11 and 2+3+4==9
assert (208+54)//10==26 and 20+5==25
assert set(F(t+1)-F(t) for t in range(q))=={4,5}
assert set(8192*(t+1)//q-8192*t//q for t in range(q))=={2,3}
s=np.arange(q,dtype=np.int64)
for start in range(q):
 alpha_n=M*start%q
 G=(M*s+alpha_n)//q
 assert np.array_equal(G,(M*((start+s)%q)//q-F(start))%M)
 assert G[0]==0 and np.all(np.diff(G)>=4)
 assert np.all(G+2<M) and G[-1]<=M-4
report['all_start_distance_pairs']=q*q
checks=0
for d in [4,5,10,11]:
 compressed=((2**(d+1)*s+q)//(2*q))%(2**d)
 for c in range(2**d):
  start=a(c,d);end=a(c+1,d);L=(end-start)%q
  assert 1<=L<q
  dist=(s-start)%q;G=(M*dist+(M*start%q))//q
  GL=(M*L+(M*start%q))//q
  theta=(F(end)-F(start)-1)%M
  assert theta==GL-1 and GL>=4
  assert np.array_equal(dist<L,compressed==c)
  for delta in [0,1,2]:
   assert np.array_equal((G+delta)%M<theta,compressed==c)
   checks+=q
report['coefficient_comparison_checks']=checks
rng=np.random.default_rng(14)
shares=rng.integers(0,q,(250000,3),dtype=np.int64)
total=shares.sum(axis=1);w=(M*shares//q).sum(axis=1)
e=M*total//q-w;delta=2-e
assert set(e)=={0,1,2}
assert np.array_equal((w+2)%M,(M*(total%q)//q+delta)%M)
report['canonical_share_samples']=len(shares)
examples={}
for start,L,x in [(989,104,1000),(3225,209,50),(3225,209,200)]:
 dist=(x-start)%q;G=lambda t:(M*t+M*start%q)//q
 examples[str(x)]={'a':start,'L':L,'s':dist,'alpha_numerator':M*start%q,'F_a':F(start),'F_x':F(x),'G_s':G(dist),'G_L':G(L),'G_last':G(L-1),'theta':G(L)-1,'Z_range':[G(dist),G(dist)+2]}
report['examples']=examples
part1=Path('output/PAMS_Part_1.mp4')
report['part1_sha256']=hashlib.sha256(part1.read_bytes()).hexdigest() if part1.exists() else None
Path('qa/part2/math-validation.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
