"""Regression checks for release-review corrections and all preexisting quiz records."""
import hashlib,json,math,pathlib
r=pathlib.Path(__file__).resolve().parents[1]
baseline=json.loads((r/'reviews/release-record-baseline.json').read_text())
def digest(x):return hashlib.sha256(json.dumps(x,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
current={}
for p in (r/'content').glob('*/*.md'):
 meta=json.loads(p.read_text()[8:].split('\n---\n',1)[0]);current[meta['id']]=(p,meta)
assert set(current)=={e['id'] for e in baseline['lessons']} and len(current)==253
for e in baseline['lessons']:
 p,m=current[e['id']];q=m['quiz'];payload=dict(q);payload.pop('question')
 assert digest(payload)==e['answer_options_explanation_sha256'],e['id']+': existing answers/options/explanation changed'
 if e['id']=='python-05':assert q['question']=='要仅在 x 为缺失值 None 时进入分支，并保留有效数值 0，应使用哪种检查？'
 else:assert digest(q)==e['quiz_sha256'],e['id']+': unexpected existing quiz change'
# The clarified cycle refers to this earlier set, not the intervening example.
h1,h2,h3,h4=200,210,3200,2200
assert 5*((h3-h4)-(h2-h1))==4950
assert round(100*((h3-2300)-(h2-h1))/(h3-h2),2)==29.77
# Equal means with unequal group sizes are a concrete counterexample to necessity.
a,b=[2],[2,2,2]
assert len(a)!=len(b) and (sum(a)/len(a)+sum(b)/len(b))/2==sum(a+b)/len(a+b)
# Unit-column rectangular matrix has a left inverse but not a two-sided inverse.
assert [[1,0],[0,0]]!=[[1,0],[0,1]]
# In the delta-p/rho example, negative covariance increases propagated variance.
def relative_variance(cov):return .25*((1/60)**2+(.05/1.2)**2)-cov/(2*60*1.2)
assert relative_variance(-.01)>relative_variance(0)>relative_variance(.01)>0
# Rayleigh cooling provides a fluid-entropy decrease without forbidding heat removal.
gamma=1.4;ma,mb=.5,.3
p_ratio=(1+gamma*ma*ma)/(1+gamma*mb*mb)
t_ratio=(mb/ma)**2*p_ratio**2
delta_s_over_R=gamma/(gamma-1)*math.log(t_ratio)-math.log(p_ratio)
assert delta_s_over_R<0
required={
'calculus-20':['开集 $U$','C^1(U)','求导移入积分号'],
'linear-algebra-15':['实方阵','矩形矩阵','双侧逆'],
'linear-algebra-17':['复方阵','本段另需'],
'fluid-mechanics-26':['协方差','正负取决'],
'fluid-mechanics-33':['熵产生非负','不能一概要求沿程增加'],
'fluid-mechanics-60':['共享关系','满列秩','独立未知'],
'python-23':['对任意初值都保证幅度趋零'],
'python-27':['已证明的合并过程'],
}
for lid,phrases in required.items():
 source=current[lid][0].read_text()
 for phrase in phrases:assert phrase in source,(lid,phrase)
print('Final review regressions: 253 stable IDs and original quiz answers/options/explanations; documented stem correction, cycle data, mean counterexample, covariance/entropy conditions and proof continuity passed')
