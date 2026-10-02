"""Independent review arithmetic, not imported from exercise author's formulas."""
from pathlib import Path
import math,json,hashlib
import sympy as s
root=Path(__file__).resolve().parents[2]
output=root/'work/mastery';output.mkdir(parents=True,exist_ok=True)
p=root/'content/mastery-exercises-thermal.json'; data=json.loads(p.read_text());assert len(data)==18 and len({q['id'] for q in data})==18
r=[]
def record(id, result):r.append(dict(id=id,recomputed=result))
record('thermodynamics-01-01',dict(closed=True,adiabatic=False,isolated=False,boundary_work=0,electrical_work_nonzero=True))
record('thermodynamics-01-02',dict(density=.6/.2,specific_volume=.2/.6,U=.6*210,remaining_density=.4/.2,remaining_U=.4*210))
record('thermodynamics-01-03',dict(rhoA=.4/.1,rhoB=.6/.3,rhoTotal=(.4+.6)/(.1+.3),naive_mass=(.4/.1+.6/.3)/2*(.1+.3)))
record('thermodynamics-05-01',dict(Q=-3,W=-12,delta_E=12-3,delta_U=12-3-2,delta_T=(12-3-2)/(.7*2)))
record('thermodynamics-05-02',dict(WA=100*(.2-.1),WB=150*(.2-.1),QA=30+100*.1,QB=30+150*.1,cycle_W=(100-150)*.1))
R=50*.02/(.5*((6+4-50*.02)/(.5*.72)))
record('thermodynamics-05-03',dict(delta_U=6+4-50*.02,delta_T=(6+4-50*.02)/(.5*.72),R=R,required_new_delta_V=.5*R*50/50,corrected_electrical=.5*.72*50+.5*R*50-6))
record('thermodynamics-07-01',dict(final_mass=10+(.08-.05)*120,delta_U=((.08*120)-(.05*80)-.5+1)*120))
W= .5*((3000-2600)+(50**2-250**2)/2000+9.81*10/1000)-10
record('thermodynamics-07-02',dict(W=W,overestimate=.5*400-W,KEpower=.5*(250**2-50**2)/2000,PEpower=.5*9.81*10/1000))
record('thermodynamics-07-03',dict(Tout=(.04*80+.06*20-.84/4.2)/.1,target_hot=(.1*4.2*(40-20)+.84)/(4.2*(80-20))))
record('heat-transfer-01-01',dict(heatout=800*.04+200*.08,flux=(800*.04+200*.08)/.12,dTdt=(60-48)/120,deltaT=(60-48)*5/120))
sigma=5.670e-8;rad=.8*sigma*.02*(400**4-350**4)
record('heat-transfer-01-02',dict(convection=10*.02*(400-300),radiation=rad,power=20+rad,fraction=rad/(20+rad)))
h,e=s.symbols('h e');sol=s.solve([s.Rational(1,2)*h+s.Rational(str(sigma*.01*(350**4-300**4)))*e-s.Rational('7.9579'),h+s.Rational(str(sigma*.01*(400**4-300**4)))*e-s.Rational('16.9613')],(h,e))
record('heat-transfer-01-03',dict(h=float(sol[h]),epsilon=float(sol[e]),happ=7.9579/.5))
Rs=[.02/(.4*.4),.04/.4,.03/(.1*.4)];Q=50/sum(Rs)
record('heat-transfer-03-01',dict(Rs=Rs,Q=Q,flux=Q/.4,Tleft=70-Q*Rs[0],Tright=70-Q*sum(Rs[:2])))
qi=.05*.9*30/.1;qb=.5*.1*30/.1
record('heat-transfer-03-02',dict(Qi=qi,Qb=qb,Q=qi+qb,Req=30/(qi+qb),bridge_fraction=qb/(qi+qb),all_insulation=.05*30/.1))
fixed=1/(8*2)+.02/2+1/(20*2)
record('heat-transfer-03-03',dict(min_L=.04*2*(30/40-fixed),Q50=30/(fixed+.05/(.04*2)),Q60=30/(fixed+.06/(.04*2)),Tin=25-40/(8*2),Tout=-5+40/(20*2)))
radius=.01;V=4*math.pi*radius**3/3;A=4*math.pi*radius**2;C=2700*900*V;tau=C/(60*A)
record('heat-transfer-07-01',dict(Bi=60*(V/A)/150,tau=tau,Ttau=20+80/math.e,Bi_double_k=60*(V/A)/300,Bi_double_h=120*(V/A)/150))
rate=math.log((60-20)/(30-20))/(180-60);h=rate*.2*500/.02;T0=20+(60-20)*math.exp(rate*60)
record('heat-transfer-07-02',dict(tau=1/rate,h=h,T0=T0,Bi=h*(.2/5000)/.02/100))
C=200;G=2;P=100;tau=C/G;theta=P/G*(1-math.exp(-60/tau));tc=math.log(theta/5)*tau
record('heat-transfer-07-03',dict(T60=20+theta,cooling_seconds=tc,max_pulse=tau*math.log(2),stored=C*theta,loss=100*60-C*theta))
assert math.isclose(r[5]['recomputed']['corrected_electrical'],14)
assert math.isclose(r[6]['recomputed']['delta_U'],732)
assert math.isclose(r[11]['recomputed']['epsilon'],.5000448390,abs_tol=1e-9)
assert math.isclose(r[-1]['recomputed']['cooling_seconds'],150.6714724648,abs_tol=1e-8)
out=dict(exercise_count=18,status='passed',source_sha256=hashlib.sha256(p.read_bytes()).hexdigest(),records=r)
(output/'thermal-numerics.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
