"""Independent thermal-reviewer recomputation of the twelve fluid exercises."""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad, solve_ivp
root=Path(__file__).resolve().parents[2]
output=root/'work/mastery';output.mkdir(parents=True,exist_ok=True)
checks=[]
def ck(i,name,v,e):
 assert math.isclose(float(v),float(e),rel_tol=1e-8,abs_tol=1e-9),(i,name,v,e)
 checks.append(dict(id=i,quantity=name,value=float(v)))
for q,v,e in [('mass',800*2.5e-3,2),('weight',2*9.81,19.62),('nu',.08/800,1e-4)]:ck('01-01',q,v,e)
v=np.linalg.solve([[1,1],[800,1000]],[.005,4.6])
for q,x,e in [('V1',v[0],.002),('V2',v[1],.003),('mass',np.dot([800,1000],v),4.6)]:ck('01-02',q,x,e)
m=quad(lambda z:.02*(1000-200*z),0,.5)[0]
for q,v,e in [('mass',m,9.5),('density',m/.01,950),('weight',m*9.81,93.195),('error%',(10/m-1)*100,100/19)]:ck('01-03',q,v,e)
s=solve_ivp(lambda t,x:1+2*x+3*t,[1,1.01],[.5],rtol=1e-12,atol=1e-13)
for q,v,e in [('acceleration',3+2*5,13),('exact displacement',s.y[0,-1]-.5,3.25*math.expm1(.02)-.015),('exact velocity increment',1+2*s.y[0,-1]+3*1.01-5,6.5*math.expm1(.02))]:ck('06-01',q,v,e)
x=math.e;y=2/math.e
for q,v,e in [('X',x,2.718281828459),('Y',y,.735758882343),('Vx',.5*x,1.35914091423),('Vy',-.5*y,-.367879441171),('ax',.25*x,.679570457115),('ay',.25*y,.183939720586),('XY',x*y,2)]:ck('06-02',q,v,e)
J=np.array([[0,-2],[2,0]])
for q,v,e in [('ax',(J@J@[1.,0])[0],-4),('ay',(J@J@[1.,0])[1],0),('div',np.trace(J),0),('vorticity',J[1,0]-J[0,1],4),('strain norm',np.linalg.norm((J+J.T)/2),0)]:ck('06-03',q,v,e)
ck('07-01','outward flow',-3-2+4,-1);ck('07-01','H final',.1+.001*5/.1,.15)
h2=.2+(12-4)*2*.001/.25;qin2=.25*(.32-h2)*1000/2+4
for q,v,e in [('H2',h2,.264),('Qin2',qin2,11),('net litres',12*2+qin2*2-4*4,30)]:ck('07-02',q,v,e)
t=50*math.log(5);s=solve_ivp(lambda t,h:(.002-.01*h)/.5,[0,t],[.1],rtol=1e-12,atol=1e-13)
ck('07-03','numerical H',s.y[0,-1],.18);ck('07-03','time',t,80.471895621705)
v2=.8*(.03/.015)**2;dp=.5*1000*(v2*v2-.8*.8)+1000*9.81*.15
ck('10-01','V2',v2,3.2);ck('10-01','p2 kPa',35-dp/1000,28.7285)
Q=.003;v1=Q/(math.pi*.05**2/4);v2=Q/(math.pi*.04**2/4);hp=60000/9810+(v2*v2-v1*v1)/19.62+6+2
for q,v,e in [('hp',hp,14.2877103215),('Ph',9810*Q*hp,420.487314763),('Pshaft',9810*Q*hp/.7,600.696163947)]:ck('10-02',q,v,e)
ck('10-03','hL A',(108000-105000)/9810,3000/9810);ck('10-03','hL B',(108000-109000)/9810,-1000/9810);ck('10-03','p2 max',(100000+500*(16-4))/1000,106)
(output/'fluid-numerics.json').write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
print(f'PASS {len(checks)} independent quantities across twelve exercises')
