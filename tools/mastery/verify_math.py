"""Independent exact arithmetic/symbolic checks for the 24 authored math exercises.
Run: python tools/mastery/verify_math.py
Requires development-only SymPy; output is kept under ignored work/.
"""
import json
from pathlib import Path
from collections import Counter
import sympy as S
R=S.Rational
x,y,t,h,a,b,c,s = S.symbols('x y t h a b c s', real=True)
def eq(lhs,rhs):
    if isinstance(lhs,S.MatrixBase):
        assert lhs.shape==rhs.shape and all(S.simplify(v)==0 for v in lhs-rhs), (lhs,rhs)
    else: assert S.simplify(lhs-rhs)==0,(lhs,rhs)
cases={}
def check(key,fn):
    fn();cases[key]='PASS'

def c0101():
    d=S.solve_univariate_inequality(6-x>=0,x,relational=False).intersect(S.solve_univariate_inequality(x+2>0,x,relational=False))-S.FiniteSet(1)
    assert d==S.Union(S.Interval.open(-2,1),S.Interval.Lopen(1,6))
    assert not d.contains(-2) and not d.contains(1) and d.contains(6)
check('calculus-01-01',c0101)
def c0102():
    T=18+R(5,2)*t
    for time,out in [(6,33),(8,38),(R(34,5),35),(R(44,5),40)]:eq(T.subs(t,time),out)
    assert 0<R(34,5)<8<R(44,5)
check('calculus-01-02',c0102)
def c0103():
    f=x*x;eq(f.subs(x,-1),f.subs(x,1));z=S.symbols('z',nonnegative=True)
    eq(S.sqrt(z*z),z);eq(S.sqrt(R(1,4)),R(1,2));eq(1/f.subs(x,R(1,4)),16)
check('calculus-01-03',c0103)
def c0301():
    f=3*t*t-2*t+1;q=S.cancel((f.subs(t,1+h)-f.subs(t,1))/h)
    eq(q,4+3*h);eq(S.limit(q,h,0),4);eq(q.subs(h,R(1,10)),R(43,10));eq(q.subs(h,-R(1,10)),R(37,10))
check('calculus-03-01',c0301)
def c0302():
    fa=3*t-2;fb=fa+2*(t-2)*(t-3)
    for f,v in [(fa,3),(fb,1)]:
        eq(f.subs(t,2),4);eq(f.subs(t,3),7);eq(S.limit((f.subs(t,2+h)-4)/h,h,0,dir='+'),v)
check('calculus-03-02',c0302)
def c0303():
    for delta,pred,actual,err in [(R(1,25),R(23,25),R(576,625),R(1,625)),(R(1,50),R(24,25),R(2401,2500),R(1,2500))]:
        eq(1-2*delta,pred);eq((-1+delta)**2,actual);eq(actual-pred,err)
    assert R(1,625)>R(1,1000)>R(1,2500);eq(R(1,2500)/R(1,625),R(1,4))
check('calculus-03-03',c0303)
def c0701():
    displacement=3*2-2*3;distance=abs(3)*2+abs(-2)*3
    eq(displacement,0);eq(distance,12);eq(R(displacement,5),0);eq(R(distance,5),R(12,5))
check('calculus-07-01',c0701)
def c0702():
    P=60+15*t;eq(sum(P.subs(t,j) for j in range(4)),330);eq(sum(P.subs(t,j) for j in range(1,5)),390)
    eq(S.integrate(P,(t,0,4)),360);eq((P.subs(t,0)+P.subs(t,4))/2*4,360)
check('calculus-07-02',c0702)
def c0703():
    H=S.integrate(2*t+1,(t,1,x*x));eq(H,x**4+x*x-2);eq(S.diff(H,x),(2*x*x+1)*2*x);eq(H.subs(x,0),-2);eq(S.diff(H,x).subs(x,-1),-6)
check('calculus-07-03',c0703)
def c1501():
    f=x*x+x*y+2*y*y;eq(S.diff(f,x).subs({x:1,y:2}),4);eq(S.diff(f,y).subs({x:1,y:2}),9)
    df=4*R(1,50)-9*R(1,100);delta=f.subs({x:R(51,50),y:R(199,100)})-f.subs({x:1,y:2})
    eq(df,-R(1,100));eq(delta,-R(6,625));eq(delta-df,R(1,2500));eq(f.subs({x:R(51,50),y:R(199,100)}),R(6869,625))
check('calculus-15-01',c1501)
def c1502():
    T=15+3*x+2*t*t;eq(S.diff(T,x),3);eq(S.diff(T,t),4*t)
    for v,out_now,out_next in [(-1,1,5),(-R(4,3),0,4)]:
        path=T.subs(x,2+v*(t-1));eq(S.diff(path,t).subs(t,1),out_now);eq(S.diff(path,t).subs(t,2),out_next)
check('calculus-15-02',c1502)
def c1503():
    f=x*x*y/(x**4+y*y);eq(S.cancel(f.subs(y,0)),0);eq(S.cancel(f.subs(x,0)),0);eq(S.cancel(f.subs(y,x*x)),R(1,2))
check('calculus-15-03',c1503)
def l0101():
    A=S.Matrix([[1,2],[2,-1]]);w=S.Matrix([3,2]);eq(A*w,S.Matrix([7,4]));assert A.det()!=0
check('linear-algebra-01-01',l0101)
def l0102():
    A=S.Matrix([[2,1],[1,2]]);eq(A*S.Matrix([-1,2]),S.Matrix([0,3]));assert A.det()!=0
    # Nonnegative x,y and 2x+y=0 force x=y=0; that output differs from (0,3).
    assert A*S.zeros(2,1)!=S.Matrix([0,3])
check('linear-algebra-01-02',l0102)
def l0103():
    A=S.Matrix([[1,2],[2,4]]);eq(A*S.Matrix([3-2*t,t]),S.Matrix([3,6]));assert A.rank()==1
    assert A.row_join(S.Matrix([3,7])).rank()==2
check('linear-algebra-01-03',l0103)
def l0201():
    M=S.Matrix([[1,1,1,6],[2,3,1,11],[-1,1,2,7]])
    M[1,:]=M[1,:]-2*M[0,:];eq(M[1,:],S.Matrix([[0,1,-1,-1]]))
    M[2,:]=M[2,:]+M[0,:];eq(M[2,:],S.Matrix([[0,2,3,13]]))
    M[2,:]=M[2,:]-2*M[1,:];eq(M[2,:],S.Matrix([[0,0,5,15]]))
    eq(S.Matrix([[1,1,1],[2,3,1],[-1,1,2]])*S.Matrix([1,2,3]),S.Matrix([6,11,7]))
check('linear-algebra-02-01',l0201)
def l0202():
    A=S.Matrix([[1,2],[2,5]]);rhs=S.Matrix([5,12]);M=A.row_join(rhs)
    eq(M[1,:]-2*M[0,:],S.Matrix([[0,1,2]]));eq(A*S.Matrix([1,2]),rhs)
    eq(A*S.Matrix([-19,12])-rhs,S.Matrix([0,10]));eq(A*S.Matrix([5,0])-rhs,S.Matrix([0,-2]))
check('linear-algebra-02-02',l0202)
def l0203():
    A=S.Matrix([[1,1],[2,a]]);w=S.Matrix([(2*a-b)/(a-2),(b-4)/(a-2)])
    eq(A*w,S.Matrix([2,b]));eq(A.subs(a,2)*S.Matrix([2-t,t]),S.Matrix([2,4]))
    assert A.subs(a,2).rank()==1;assert A.subs(a,2).row_join(S.Matrix([2,3])).rank()==2
    eq(S.Matrix([[1,1,2],[2,a,b]])[1,:]-2*S.Matrix([[1,1,2],[2,a,b]])[0,:],S.Matrix([[0,a-2,b-4]]))
check('linear-algebra-02-03',l0203)
def l0301():
    A=S.Matrix([[1,2],[0,1]]);B=S.diag(2,1);v=S.Matrix([1,3])
    eq(B*v,S.Matrix([2,3]));eq(A*B,S.Matrix([[2,2],[0,1]]));eq(A*(B*v),S.Matrix([8,3]));eq((A*B)*v,A*(B*v))
    eq(A*v,S.Matrix([7,3]));eq(B*A,S.Matrix([[2,4],[0,1]]));eq(B*A*v,S.Matrix([14,3]))
check('linear-algebra-03-01',l0301)
def l0302():
    A=S.Matrix([[1,2],[1,3]]);N=S.Matrix([[3,-2],[-1,1]]);eq(A*N,S.eye(2));eq(N*A,S.eye(2))
    eq(N*S.Matrix([7,10]),S.Matrix([1,3]));eq(A*S.Matrix([1,3]),S.Matrix([7,10]));eq((A*S.Matrix([[1,R(1,2)],[1,R(1,3)]]))[0,0],3)
check('linear-algebra-03-02',l0302)
def l0303():
    A=S.diag(1,0);B=S.Matrix([[0,0],[2,3]]);eq(A*B,S.zeros(2));assert A!=S.zeros(2) and B!=S.zeros(2)
    u=S.Matrix([1,2]);v=S.Matrix([1,-3]);eq(A*u,A*v);assert u!=v
check('linear-algebra-03-03',l0303)
def l1001():
    b=S.Matrix([4,1]);u=S.Matrix([2,1]);co=b.dot(u)/u.dot(u);p=co*u;r=b-p
    eq(co,R(9,5));eq(p,S.Matrix([R(18,5),R(9,5)]));eq(r,S.Matrix([R(2,5),-R(4,5)]));eq(r.dot(u),0);eq(r.dot(r),R(4,5))
    u2=2*u;co2=b.dot(u2)/u2.dot(u2);eq(co2,R(9,10));eq(co2*u2,p)
check('linear-algebra-10-01',l1001)
def l1002():
    E=(1-c)**2+(2-c)**2+(6-c)**2;Ew=(1-c)**2+(2-c)**2+2*(6-c)**2
    eq(E,3*(c-3)**2+14);eq(Ew,4*(c-R(15,4))**2+R(83,4));assert S.solve(S.diff(E,c),c)==[3];assert S.solve(S.diff(Ew,c),c)==[R(15,4)]
check('linear-algebra-10-02',l1002)
def l1003():
    b=S.Matrix([3,1,2]);p=S.Matrix([2,2,2]);r=b-p
    eq(r.dot(S.Matrix([1,1,0])),0);eq(r.dot(S.Matrix([0,0,1])),0);eq(r.dot(r),2)
    e=b-S.Matrix([t,t,s]);eq(e.dot(e),2*(t-2)**2+(s-2)**2+2)
check('linear-algebra-10-03',l1003)
root=Path(__file__).resolve().parents[2]
output=root/'work/mastery';output.mkdir(parents=True,exist_ok=True)
items=json.loads((root/'content/mastery-exercises-math.json').read_text())
fields={'id','courseId','lessonId','type','level','prompt','solution','checkpoints','pitfall','verification','knowledgePoints','technique'}
assert len(items)==24 and len({q['id'] for q in items})==24
assert set(cases)=={q['id'].removeprefix('mastery-') for q in items}
assert set(Counter(q['lessonId'] for q in items).values())=={3}
for q in items:
    assert set(q)-{'prerequisites'}==fields,q['id']
    assert q['level'] in {'基础理解','常规应用','综合提高'}
    assert q['type'] and q['prompt'] and q['solution'] and q['pitfall'] and q['technique']
    assert isinstance(q['verification'],str)
    assert isinstance(q['knowledgePoints'],list) and q['knowledgePoints']
    assert isinstance(q['checkpoints'],list) and len(q['checkpoints'])>=3
    assert q['prompt'].count('$')%2==0 and q['solution'].count('$')%2==0,q['id']
for lid in {q['lessonId'] for q in items}:
    assert {q['level'] for q in items if q['lessonId']==lid}=={'基础理解','常规应用','综合提高'}
report={'exerciseCount':24,'anchorCount':8,'schema':'PASS','exactArithmeticAndSymbolicChecks':cases,'notes':['Every exercise has a case; symbolic equalities and concrete counterexamples checked with SymPy 1.14.0.','Manual scope, units, hypotheses, proof/answer reasoning and prerequisite checks performed separately; symbolic pass does not replace independent human review.','No repository files modified.']}
(output/'math-numerics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
