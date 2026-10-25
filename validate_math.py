"""Independent numerical checks, not an animation of the Part 2 proof."""
from fractions import Fraction
from math import ceil,floor
import random,json
from pathlib import Path
q=3329;M=16384
F=lambda t:floor(Fraction(M*t,q))
a=lambda c,d:ceil(Fraction((2*c-1)*q,2**(d+1)))%q
compress=lambda x,d:floor(Fraction(2**d*x,q)+Fraction(1,2))%2**d
assert (a(10,5),a(11,5))==(989,1093)
assert (a(0,4),a(1,4))==(3225,105)
assert (F(989),F(1093),F(300),F(400))==(4867,5379,1476,1968)
assert (3*F(400)+2-F(989))%M==1039
assert (2*F(300)+F(400)+2-F(989))%M==55
assert (F(1093)-F(989)-1)%M==511
for d in [4,5,10,11]:
    for x in range(q):
        c=compress(x,d)
        assert (x-a(c,d))%q<(a(c+1,d)-a(c,d))%q
rng=random.Random(203); checks=0
for d in [4,5,10,11]:
    for _ in range(30000):
        s=[rng.randrange(q) for _ in range(3)];x=sum(s)%q
        right=compress(x,d)
        for c in [right,(right+1)%2**d,(right-1)%2**d,rng.randrange(2**d)]:
            z=(sum(F(v) for v in s)+2-F(a(c,d)))%M
            theta=(F(a(c+1,d))-F(a(c,d))-1)%M
            assert (z<theta)==(right==c),(d,s,c,z,theta)
            checks+=1
report={'numeric_examples':'passed','interval_checks':4*q,'random_share_comparisons':checks,'result':'passed','scope':'Numerical validation only; not a formal proof.'}
Path('qa/math-validation.json').write_text(json.dumps(report,indent=2))
print(report)
