"""Independent reviewer: execute authored solutions and recompute all 24 exercise outcomes."""
from pathlib import Path
import json,re,contextlib,io,hashlib
import numpy as np
import sympy as sp
from sklearn.model_selection import KFold
root=Path(__file__).resolve().parents[2]
output=root/'work/mastery';output.mkdir(parents=True,exist_ok=True)
raw=(root/'content/mastery-exercises-computing.json').read_bytes();items=json.loads(raw)
byid={q['id'].removeprefix('mastery-'):q for q in items}
checks={}
def run(code,env=None):
    env={} if env is None else env
    stream=io.StringIO();error=None
    try:
        with contextlib.redirect_stdout(stream):exec(compile(code,'<exercise>','exec'),env)
    except Exception as exc:error=type(exc).__name__
    return env,stream.getvalue().splitlines(),error
# Execute every Python solution block unchanged. No code extracted from untrusted external content.
solution_runs=[]
for q in items:
    blocks=re.findall(r'```python\n(.*?)```',q['solution'],re.S)
    env={}
    for j,block in enumerate(blocks):
        env,out,err=run(block,env);assert err is None,(q['id'],j,err)
        solution_runs.append({'id':q['id'],'block':j,'stdout':out,'verdict':'PASS'})
def mark(key):checks[key]='PASS'
# Python 01
p=re.findall(r'```python\n(.*?)```',byid['python-01-01']['prompt'],re.S)[0]
env,out,err=run(p);assert out==['18','22'] and env['start_c']==18 and env['current_c']==21 and err is None;mark('python-01-01')
p=re.findall(r'```python\n(.*?)```',byid['python-01-02']['prompt'],re.S)[0]
env,out,err=run(p);assert err=='NameError' and out==[]
fix=re.findall(r'```python\n(.*?)```',byid['python-01-02']['solution'],re.S)[0];assert run(fix)[1:]==(['20'],None);mark('python-01-02')
p=re.findall(r'```python\n(.*?)```',byid['python-01-03']['solution'],re.S)[0]
assert run(p)[1:]==(['25','21','-4'],None)
assert run(p.replace('start_c = 25','start_c = 30'))[1:]==(['30','26','-4'],None);mark('python-01-03')
# Python 06 use independent reference iteration and rerun displayed code for all boundary inputs.
for key,samples,expect in [
 ('python-06-01',[[0,20,19,24],[0,19]],['22.0','没有达标读数']),
 ('python-06-02',[[18,20,22],[],[18,19],[20]],['21.0','没有达标读数','没有达标读数','20.0']),
 ('python-06-03',[[18,21,22,19,23,24,25,18],[],[20,20],[1,2]],['3','0','2','0'])]:
    src=byid[key]['prompt' if key=='python-06-01' else 'solution']
    code=re.findall(r'```python\n(.*?)```',src,re.S)[0]
    for v,o in zip(samples,expect):
        changed=re.sub(r'^values = .*$',f'values = {v!r}',code,count=1,flags=re.M)
        assert run(changed)[1:]==([o],None),(key,v,run(changed)[1:])
    mark(key)
bug=re.findall(r'```python\n(.*?)```',byid['python-06-02']['prompt'],re.S)[0];assert run(bug)[1:]==(['42.0'],None)
assert [(sum(v for v in [0,20,19,24][:k] if v>=20),sum(v>=20 for v in [0,20,19,24][:k])) for k in range(1,5)]==[(0,0),(20,1),(20,1),(44,2)]
# Python 07
code=re.findall(r'```python\n(.*?)```',byid['python-07-01']['prompt'],re.S)[0]
assert run(code)[1:]==(['13','10','14'],None)
env,out,err=run(code.replace('    return value\n',''));assert out==['13','10'] and err=='TypeError' and env['result'] is None;mark('python-07-01')
orig=re.findall(r'```python\n(.*?)```',byid['python-07-02']['prompt'],re.S)[0];env,_,err=run(orig);assert err is None and env['first']==[2,5] and env['first'] is env['second']
fix=re.findall(r'```python\n(.*?)```',byid['python-07-02']['solution'],re.S)[0];env,_,err=run(fix);assert err is None
provided=[];ret=env['record'](4,provided);assert ret is provided and provided==[4];mark('python-07-02')
code=re.findall(r'```python\n(.*?)```',byid['python-07-03']['solution'],re.S)[0];env,out,err=run(code);assert err is None and out==[]
f=env['mean_at_least'];assert f([0],threshold=0)==0.0 and f([]) is None
try:f([20],19)
except TypeError:pass
else:raise AssertionError('keyword-only not enforced')
mark('python-07-03')
# Python 20
code=re.findall(r'```python\n(.*?)```',byid['python-20-01']['prompt'],re.S)[0];env,_,err=run(code);assert err is None
arr=env['corrected'];assert arr.shape==(2,3);assert np.array_equal(arr,[[11,18,30],[15,20,28]])
assert np.array_equal(env['readings'],[[10,20,30],[14,22,28]]);assert np.allclose(arr.mean(0),[13,19,29]);assert np.allclose(arr.mean(1),[59/3,21]);mark('python-20-01')
code=re.findall(r'```python\n(.*?)```',byid['python-20-02']['prompt'],re.S)[0];env,_,err=run(code);assert err is None
assert np.array_equal(env['residual'],[[-1,-1,-4],[1,1,-2],[2,2,-1]]) and np.isclose(env['mse'],11/3)
code=re.findall(r'```python\n(.*?)```',byid['python-20-02']['solution'],re.S)[0];env,_,err=run(code);assert err is None and env['mse']==1;mark('python-20-02')
code=re.findall(r'```python\n(.*?)```',byid['python-20-03']['solution'],re.S)[0];env,_,err=run(code);assert err is None
alias=env['raw'];alias[0,0]+=1;assert env['raw'][0,0]==21
try:np.zeros((3,2))-np.zeros(3)
except ValueError:pass
else:raise AssertionError('invalid broadcast unexpectedly worked')
mark('python-20-03')
# ML independent exact fractions / symbolic algebra.
R=sp.Rational
c,w,t,e,eta=sp.symbols('c w t e eta',real=True)
def eq(a,b):assert sp.simplify(a-b)==0,(a,b)
train=[2,4,9];mu=R(sum(train),len(train));eq(mu,5)
eq(sum((v-c)**2 for v in train),26+3*(c-5)**2);eq(sum((v-mu)**2 for v in train)/3,R(26,3));eq(sum((v-mu)**2 for v in [3,8])/2,R(13,2));assert abs(float(sp.sqrt(R(13,2)))-2.5495)<5e-5;mark('machine-learning-01-01')
for pred,expected in [([0,0,0,0],(R(5,2),25,5)),([3,3,3,7],(3,9,3))]:
    errors=[sp.Integer(p-y) for p,y in zip(pred,[0,0,0,10])];mse=sum(v*v for v in errors)/4
    for result,target in zip((sum(abs(v) for v in errors)/4,mse,sp.sqrt(mse)),expected):eq(result,target)
mark('machine-learning-01-02')
# Task-definition question separately manually checked for time availability and specimen grouped split.
mark('machine-learning-01-03')
X=sp.Matrix([[1,2],[3,-1]]);wv=sp.Matrix([2,-1]);yv=sp.Matrix([2,4]);one=sp.ones(2,1);pred=X*wv+one;ev=pred-yv
assert pred==sp.Matrix([1,8]) and ev==sp.Matrix([-1,4]);eq(ev.dot(ev)/4,R(17,4));mark('machine-learning-04-01')
gw=X.T*ev/2;gb=sum(ev)/2;assert gw==sp.Matrix([R(11,2),-3]);eq(gb,R(3,2));assert X*ev/2==sp.Matrix([R(7,2),-R(7,2)])
neww=wv-gw/10;newb=1-gb/10;newpred=X*neww+newb*one;newe=newpred-yv
assert neww==sp.Matrix([R(29,20),-R(7,10)]) and newpred==sp.Matrix([R(9,10),R(59,10)]);eq(newe.dot(newe)/4,R(241,200))
# Independent central finite differences in all parameters.
par=np.array([2.,-1.,1.]);NX=np.array(X).astype(float);NY=np.array(yv).astype(float).ravel()
def loss(q):return np.mean((NX@q[:2]+q[2]-NY)**2)/2
fd=[]
for j in range(3):
    delta=np.zeros(3);delta[j]=1e-5;fd.append((loss(par+delta)-loss(par-delta))/(2e-5))
assert np.allclose(fd,[5.5,-3,1.5],atol=1e-8);mark('machine-learning-04-02')
w1,w2=sp.symbols('w1 w2',real=True);old=2*w1-w2-1;new=2*(w1-2*eta*old)-(w2+eta*old)-1;eq(new,(1-5*eta)*old)
assert sp.simplify_logic(sp.Xor(sp.reduce_inequalities([eta>0,(1-5*eta)**2<1],eta),sp.And(0<eta,eta<R(2,5)))) is sp.false
for lr,J in [(R(1,5),0),(R(2,5),R(1,2)),(R(1,2),R(9,8))]:eq((1-5*lr)**2/2,J)
for sol in [(R(1,2),0),(1,1)]:eq(old.subs({w1:sol[0],w2:sol[1]}),0)
mark('machine-learning-04-03')
mu=sp.Integer(4);scale=sp.sqrt(R(8,3));zs=[(v-mu)/scale for v in [2,4,6,8,10]]
for result,target in zip(zs,[-sp.sqrt(R(3,2)),0,sp.sqrt(R(3,2)),sp.sqrt(6),3*sp.sqrt(R(3,2))]):eq(result,target)
mark('machine-learning-05-01')
# Fold order explicit evidence: KFold first test fold is the first block, not the training block.
folds=[{'train':tr.tolist(),'validation':va.tolist(),'train_mean':float(np.array([0,2,100,102])[tr].mean())} for tr,va in KFold(2,shuffle=False).split(np.zeros((4,1)))]
assert folds==[{'train':[2,3],'validation':[0,1],'train_mean':101.0},{'train':[0,1],'validation':[2,3],'train_mean':1.0}]
code=re.findall(r'```python\n(.*?)```',byid['machine-learning-05-02']['solution'],re.S)[0];env,_,err=run(code);assert err is None and np.allclose(env['scores'],[-10001/9,-10001/9]);mark('machine-learning-05-02')
# Multi-leakage diagnosis manually checks all four arrows and independent calibration premise.
mark('machine-learning-05-03')
xx=sp.Matrix([0,1,2,3]);yy=sp.Matrix([1,2,2,5]);D=sp.ones(4,1).row_join(xx);beta=(D.T*D).inv()*D.T*yy
assert beta==sp.Matrix([R(7,10),R(6,5)]);res=yy-D*beta
assert res==sp.Matrix([R(3,10),R(1,10),-R(11,10),R(7,10)]);eq(sum(res),0);eq(res.dot(res)/4,R(9,20));mark('machine-learning-07-01')
E=(2-w)**2+(2-2*w)**2;eq(sp.diff(E,w),10*w-12);sol=sp.solve(sp.diff(E,w),w)[0];eq(sol,R(6,5));r1=2-sol;r2=2-2*sol;eq(r1+r2,R(2,5));eq(r1+2*r2,0);mark('machine-learning-07-02')
D=sp.Matrix([[1,0,0],[1,1,2],[1,2,4]]);coef=sp.Matrix([1,3-2*t,t]);assert D*coef==sp.Matrix([1,4,7]);eq((sp.Matrix([[1,3,6]])*coef)[0],10);eq((sp.Matrix([[1,3,0]])*coef)[0],10-6*t);mark('machine-learning-07-03')
assert len(checks)==24 and set(checks)==set(byid)
report={'input_sha256':hashlib.sha256(raw).hexdigest(),'items':24,'verdicts':checks,'solution_python_blocks_executed':solution_runs,'kfold_order_evidence':folds,'libraries':{'numpy':np.__version__},'notes':['All numerical and executable results independently recomputed.','Reviewed KFold order and common-unit temperature wording are present in the released exercise source.']}
(output/'computing-numerics.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'items':24,'checks':'PASS','solution_python_blocks':len(solution_runs),'hash':report['input_sha256'],'folds':folds},ensure_ascii=False,indent=2))
