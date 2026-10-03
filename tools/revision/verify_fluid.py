"""Recalculate the 1.5.0 fluid examples without importing textbook solvers.

Uses only the standard library. Geometry clipping and direct-loss bisection
provide independent numerical checks of the printed worked solutions.
"""
from pathlib import Path
from fractions import Fraction
import math, json
ROOT=Path(__file__).resolve().parents[2]
checks=[]
def check(label,value,expected,rtol=1e-10,atol=1e-10):
    assert math.isfinite(float(value)) and math.isclose(value,expected,rel_tol=rtol,abs_tol=atol),(label,value,expected)
    checks.append(label)
for number,phrases in {
    3:['加速水箱','7.848','3.924'],
    4:['浮体初稳性','16/45','1.461'],
    8:['有效净载荷','实际湿壁','36'],
    9:['旋转叶排','静止导叶'],
    13:['linear-algebra-07','零空间'],
    16:['1.93768','0.013979'],
    26:['machine-learning-03','calculus-15'],
    39:['压力项','0.2381','5 K'],
    50:['相对','未定义'],
}.items():
    source=(ROOT/'content/fluid-mechanics'/f'fluid-mechanics-{number:02}.md').read_text()
    for phrase in phrases:assert phrase in source,(number,phrase)
# F39: start from h=u+pv and steady total-energy balance, not the shortcut.
rho,c,dp=1000.,4200.,-1e6
deltaT=-dp/(rho*c)
check('F39 liquid restriction temperature rise [K]',deltaT,5/21)
check('F39 liquid delta h [J/kg]',c*deltaT+dp/rho,0)
check('F39 air original 10 W [K]',10/(.002*1000),5)
check('F39 original exercise 9 W [K]',9/(.002*1000),4.5)
# F08: absolute and gauge balances independently formed from port normals.
mdot,A,V,patm=20.,.01,2.,100000.
flux=(-mdot*V,mdot*V)
pg=(30000.,20000.);portg=(pg[0]*A,-pg[1]*A)
porta=((pg[0]+patm)*A,-(pg[1]+patm)*A)
Rg=tuple(flux[i]-portg[i] for i in range(2));Ra=tuple(flux[i]-porta[i] for i in range(2))
for i in range(2):
    check(f'F08 gauge Rg component {i} [N]',Rg[i],(-340.,240.)[i])
    check(f'F08 actual Rabs component {i} [N]',Ra[i],(-1340.,1240.)[i])
    check(f'F08 actual wet-wall load plus atmosphere {i} [N]',-Ra[i]+(-1000.,1000.)[i],-Rg[i])
# Finite caught material over an interval, including absolute exit speed.
dt=.17;V=10.;Uw=4.;A=.001
mass=rho*A*(V-Uw)*dt
check('F08 moving plate caught mass flow [kg/s]',mass/dt,6)
check('F08 moving plate force [N]',-mass*(Uw-V)/dt,36)
check('F08 moving plate fixed limit [N]',rho*A*V**2,100)
check('F08 moving plate equal-speed limiting force [N]',rho*A*(V-V)**2,0)
# Torque and stationary-row counterexample.
check('F09 original rotor torque [N m]',2*(.2*15-.1*0),6)
check('F09 original rotor power [W]',100*2*(.2*15-.1*0),600)
check('F09 rotor plus stator angular momentum flux [N m]',10-4,6)
check('F09 power uses each boundary speed [W]',10*100+(-4)*0,1000)
# Wall units: uniform translations must cancel.
mu=.001;nu=1e-6;tau=4.;y=2e-5;ut=math.sqrt(tau/rho)
for wall in [-3.,0.,5.]:
    fluid=wall+tau*y/mu
    check(f'F50 wall-relative u+ = y+, wall={wall} m/s',(fluid-wall)/ut,y*ut/nu)
check('F50 original water ut [m/s]',math.sqrt(.032/8),.0632455532033676)
check('F50 original y1 [micrometres]',1e-6/math.sqrt(.032/8)*1e6,15.8113883008419)
# F03: recover free surface from the integrated pressure, volume by midpoint quadrature.
g=9.81;L=2.;W=1.;a=1.962;h0=.6
C=h0+a*L/(2*g)
heights=[C-a/g*x for x in [0.,L]]
check('F03 water rear height [m]',heights[0],.8)
check('F03 water front height [m]',heights[1],.4)
n=200;volume=sum((C-a/g*((k+.5)*L/n))*W*L/n for k in range(n))
check('F03 volume by 200-strip quadrature [m3]',volume,1.2)
check('F03 rear bottom gauge pressure [Pa]',rho*g*heights[0],7848)
check('F03 front bottom gauge pressure [Pa]',rho*g*heights[1],3924)
check('F03 horizontal pressure difference [Pa]',rho*g*(heights[1]-heights[0]),-rho*a*L)
check('F03 ideal freefall pressure gradient [Pa/m]',-rho*(g-g),0)
# F04 rectangular flotation; geometrical finite-tilt check independent of metacentric formula.
length,breadth,total_height=4.,2.,1.;mass=600*length*breadth*total_height
volume=mass/rho;draft=volume/(length*breadth);I=length*breadth**3/12
KB=draft/2;KG=total_height/2;BM=I/volume;GM=KB+BM-KG
for name,value,expected in [('mass',mass,4800),('displacement',volume,4.8),('draft',draft,.6),('KB',KB,.3),('KG',KG,.5),('I',I,8/3),('BM',BM,5/9),('GM',GM,16/45)]:check('F04 '+name,value,expected)
check('F04 5 degree linear moment [N m]',-mass*g*GM*math.radians(5),-1461.0500234294932)
def clip(poly,level):
    result=[]
    for p,q in zip(poly,poly[1:]+poly[:1]):
        pin=p[1]<=level;qin=q[1]<=level
        if pin:result.append(p)
        if pin!=qin:
            t=(level-p[1])/(q[1]-p[1]);result.append((p[0]+t*(q[0]-p[0]),level))
    return result
def area_centroid(poly):
    cross=[p[0]*q[1]-q[0]*p[1] for p,q in zip(poly,poly[1:]+poly[:1])]
    ar=sum(cross)/2
    cx=sum((p[0]+q[0])*v for p,q,v in zip(poly,poly[1:]+poly[:1],cross))/(6*ar)
    return abs(ar),cx
phi=1e-4
poly0=[(-breadth/2,-KG),(breadth/2,-KG),(breadth/2,total_height-KG),(-breadth/2,total_height-KG)]
poly=[(x*math.cos(phi)-z*math.sin(phi),x*math.sin(phi)+z*math.cos(phi)) for x,z in poly0]
lo,hi=-1.,1.
for _ in range(80):
    mid=(lo+hi)/2;ar,cx=area_centroid(clip(poly,mid)) if len(clip(poly,mid))>2 else (0,0)
    if ar<volume/length:lo=mid
    else:hi=mid
ar,cx=area_centroid(clip(poly,(lo+hi)/2))
check('F04 tilted clipped geometry displacement [m3]',ar*length,volume)
check('F04 finite-tilt buoyancy horizontal shift / phi [m]',-cx/phi,GM,rtol=1e-7)
# F16: solve Q1+Q2=Q by bisection of direct speed-based Darcy losses.
Q=.02
specs=[(.025,40.,.1,2.),(.03,60.,.08,4.)]
def head(q,s):
    f,l,d,k=s;v=q/(math.pi*d*d/4)
    return (f*l/d+k)*v*v/(2*g)
lo,hi=0.,Q
trace=[]
for it in range(60):
    q1=(lo+hi)/2;res=head(q1,specs[0])-head(Q-q1,specs[1])
    if it in (0,1,2,3,7,15,31,59):trace.append({'iteration':it+1,'Q1':q1,'Q2':Q-q1,'head_residual_m':res})
    if res>0:hi=q1
    else:lo=q1
q1=(lo+hi)/2;q2=Q-q1;h1=head(q1,specs[0]);h2=head(q2,specs[1])
check('F16 branch 1 flow [m3/s]',q1,.013979434713241461)
check('F16 branch 2 flow [m3/s]',q2,.006020565286758538)
check('F16 mass residual [m3/s]',q1+q2-Q,0)
check('F16 energy residual [m]',h1-h2,0)
check('F16 common head [m]',h1,1.937678411574092)
check('F16 r1 coefficient [s2/m5]',head(1,specs[0]),9915.222864081983)
check('F16 r2 coefficient [s2/m5]',head(1,specs[1]),53457.31728071544)
check('F16 Re1',4*q1/(math.pi*.1*nu),177991.69089942487)
check('F16 Re2',4*q2/(math.pi*.08*nu),95820.27255950957)
check('F16 false equal split head1 [m]',head(.01,specs[0]),.9915222864081984)
check('F16 false equal split head2 [m]',head(.01,specs[1]),5.345731728071544)
# F13: rational elimination, rank and null vectors.
D=[[Fraction(v) for v in row] for row in [[1,1,0,0,1],[1,-3,1,1,-1],[-2,0,-1,0,-1]]]
def rank(a):
    a=[row[:] for row in a];r=0
    for col in range(len(a[0])):
        pivot=next((j for j in range(r,len(a)) if a[j][col]),None)
        if pivot is None:continue
        a[r],a[pivot]=a[pivot],a[r];p=a[r][col];a[r]=[v/p for v in a[r]]
        for j in range(len(a)):
            if j!=r:
                p=a[j][col];a[j]=[x-p*y for x,y in zip(a[j],a[r])]
        r+=1
        if r==len(a):break
    return r
check('F13 dimension matrix rank',rank(D),3)
for j,vec in enumerate([[1,-1,-2,-2,0],[0,-1,-1,-1,1]]):
    for i,row in enumerate(D):check(f'F13 null basis {j}, dimension row {i}',sum(a*b for a,b in zip(row,vec)),0)
check('F13 null basis independence',rank([[Fraction(v) for v in row] for row in [[1,-1,-2,-2,0],[0,-1,-1,-1,1]]]),2)
# F26 sensitivity/covariance terms and preserved example.
V=10.;dp=60.;rho_air=1.2;up=2.;ur=.03
fp=V/(2*dp);fr=-V/(2*rho_air)
check('F26 original standard uncertainty [m/s]',math.sqrt((fp*up)**2+(fr*ur)**2),5/24)
for correlation in [-1.,0.,1.]:
    covariance=correlation*up*ur
    general=((fp*up)**2+(fr*ur)**2+2*fp*fr*covariance)/V**2
    relative=.25*((up/dp)**2+(ur/rho_air)**2)-covariance/(2*dp*rho_air)
    check(f'F26 equivalent covariance forms, corr={correlation}',general,relative)
print(json.dumps({'status':'passed','numeric_assertions':len(checks),'checks':checks},ensure_ascii=False,indent=2))
