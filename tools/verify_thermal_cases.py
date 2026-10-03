"""Recompute 2026-10-03 thermal cases from source-table inputs, using only stdlib.
Run: python tools/verify_thermal_cases.py [--baseline /path/to/checkout]
Optional reproducibility (official PyPI): pip install CoolProp==7.2.0
python tools/reproduce_thermal_properties.py  # recomputes model table, not experiments
"""
from pathlib import Path
import argparse,json,math,re,subprocess,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
checks=[]
def check(ok,label):
 if not ok:raise AssertionError(label)
 checks.append(label)
def near(a,b,label,tol=1e-6):check(abs(a-b)<=tol,f'{label}: {a} vs {b}')
def bisect(f,a,b):
 assert f(a)*f(b)<0
 for _ in range(70):
  m=(a+b)/2
  if f(a)*f(m)<=0:b=m
  else:a=m
 return (a+b)/2
# Real NIST table, 1 MPa, 260/270 C; volume already SI.
for name,a,b,wanted in [('h',2965.1,2986.9,2976.0),('s',6.9681,7.0087,6.9884),('v',.23788,.24296,.24042)]:near(a+.5*(b-a),wanted,'NIST midpoint '+name)
near(1/.24042,4.1594,'water density',.0001);near(260+10*(2970.55-2965.1)/(2986.9-2965.1),262.5,'water inverse table')
check(265>179.878,'water is superheated')
# Rankine reconstructed from NIST printed endpoints.
hf,hg,sf,sg,vf,vg=191.81,2583.9,.64920,8.1488,.00101027,14.670
h3,s3=3231.7,6.9234
wp=vf*(3000-10);h2=hf+wp;xs=(s3-sf)/(sg-sf);h4s=hf+xs*(hg-hf);h4=h3-.85*(h3-h4s);x4=(h4-hf)/(hg-hf);s4=sf+x4*(sg-sf);v4=vf+x4*(vg-vf)
wt=h3-h4;qin=h3-h2;qout=h4-hf;wnet=wt-wp
for label,val,target,tol in [('wp',wp,3.0207,.0001),('h2',h2,194.8307,.0001),('x4s',xs,.83660,.00001),('h4s',h4s,2193.0435,.0001),('h4',h4,2348.8420,.0001),('x4',x4,.90174,.00001),('s4',s4,7.41185,.00001),('v4',v4,13.2286,.0001),('wt',wt,882.858,.001),('qin',qin,3036.869,.001),('qout',qout,2157.032,.001),('wnet',wnet,879.837,.001),('eta',wnet/qin,.28972,.00001),('ideal eta',(h3-h4s-wp)/qin,.34102,.00001)]:near(val,target,'Rankine '+label,tol)
near(qin-qout,wnet,'Rankine energy closure');check(0<xs<x4<1 and s4>s3,'Rankine phase and entropy')
# R134a HEOS table, use stored raw properties only as inputs (no answer fields).
d=json.loads((ROOT/'content/thermal-property-cases.json').read_text());st=d['r134a']['states'];sat=d['r134a']['saturated'];one=st['one'];two=st['two'];ts=st['two_s'];three=st['three'];four=st['four']
check(one['T_C']>sat[0]['T_C'] and three['T_C']<sat[2]['T_C'],'R134a superheat/subcool');near(one['T_C']-sat[0]['T_C'],5,'R134a superheat');near(sat[2]['T_C']-three['T_C'],5,'R134a subcool')
check(one['s_kJkgK']>sat[3]['s_kJkgK'],'R134a 2s in superheated zone');near(ts['s_kJkgK'],one['s_kJkgK'],'R134a isentropic reference')
h2c=one['h_kJkg']+(ts['h_kJkg']-one['h_kJkg'])/.8;near(h2c,two['h_kJkg'],'R134a compressor efficiency')
near(three['h_kJkg'],four['h_kJkg'],'R134a throttling');x=(four['h_kJkg']-sat[0]['h_kJkg'])/(sat[1]['h_kJkg']-sat[0]['h_kJkg']);near(x,.29851,'R134a valve quality',.00001)
qL=one['h_kJkg']-three['h_kJkg'];wc=two['h_kJkg']-one['h_kJkg'];qH=two['h_kJkg']-three['h_kJkg']
near(qL,148.7828,'R134a cooling',.0001);near(wc,43.0260,'R134a input',.0001);near(qH,191.8088,'R134a heat rejection',.0001);near(qL/wc,3.4580,'R134a COP',.0001);near(qL+wc,qH,'R134a closure');check(two['s_kJkgK']>one['s_kJkgK'] and four['s_kJkgK']>three['s_kJkgK'],'R134a entropy signs')
frac=(one['s_kJkgK']-1.748162)/(1.764603-1.748162);near(50+5*frac,50.391,'R134a entropy table inverse',.001);near(430.8845+frac*(436.2383-430.8845),431.303,'R134a enthalpy interpolation',.001)
near((sat[2]['h_kJkg']-sat[0]['h_kJkg'])/(sat[1]['h_kJkg']-sat[0]['h_kJkg']),.33443,'R134a no-subcool quality',.00001);near((one['h_kJkg']-sat[2]['h_kJkg'])/wc,3.2860,'R134a no-subcool COP',.0001)
# Humid air: independently transcribed NIST psat and course approximate enthalpy convention.
p=101.325;pv=.5*4.2470;wA=.622*pv/(p-pv);wC=.622*1.2282/(p-1.2282)
H=lambda t,w:1.006*t+w*(2501+1.86*t)
ha,hb,hc=H(30,wA),H(40,wA),H(10,wC);cond=wA-wC;heating=hb-ha;cooling=hb-hc-cond*41.8
for label,val,target,tol in [('wA',wA,.0133145,1e-7),('wC',wC,.0076320,1e-7),('hA',ha,64.2225,.0001),('hB',hb,74.5301,.0001),('hC',hc,29.2896,.0001),('RH_B',pv/7.3849,.28755,.00001),('dew',18+(pv-2.0647)/(2.1983-2.0647),18.440,.001),('heat',heating,10.3076,.0001),('cond',cond,.00568247,1e-8),('cond_kg_h',cond*3600,20.4569,.0001),('cooling',cooling,45.0030,.0001),('h25',H(25,wA),59.0687,.0001),('cool25',hb-H(25,wA),15.4615,.0001)]:near(val,target,'humid '+label,tol)
near(hb,hc+cond*41.8+cooling,'humid independent flow enthalpy balance')
# Compressor and explicit four-segment pressure-volume integration.
R,T1,rp,n,gamma=.287,300,4,1.3,1.4;T2=T1*rp**((n-1)/n);wb=R*(T2-T1)/(n-1);win=n*wb;etav=1.05-.05*rp**(1/n);v1=R*T1/100;massflow=etav*.01/v1
for label,val,target,tol in [('T2',T2,413.103,.001),('closed work',wb,108.202,.001),('flow work',win,140.662,.001),('difference',win-wb,32.461,.001),('isothermal',R*T1*math.log(4),119.360,.001),('isentropic',gamma*R*T1/(gamma-1)*(rp**((gamma-1)/gamma)-1),146.454,.001),('q',gamma*R/(gamma-1)*(T2-T1)-win,-27.050,.001),('etav',etav,.904758,1e-6),('mdot',massflow,.0105082,1e-7),('power',massflow*win,1.47811,.00001),('zero-clearance power',.01/v1*win,1.63371,.00001)]:near(val,target,'compressor '+label,tol)
V1,V3=1.05,.05;V2=V1/rp**(1/n);V4=V3*rp**(1/n)
W12=V1**n*(V2**(1-n)-V1**(1-n))/(1-n);W23=4*(V3-V2);W34=4*V3**n*(V4**(1-n)-V3**(1-n))/(1-n);W41=V1-V4
near(-100*(W12+W23+W34+W41)/((V1-V4)/v1),win,'compressor whole pV loop per fresh kg');check(W12+W23+W34+W41<0,'compressor counterclockwise input loop');near((V1-V4),etav,'compressor intake volume')
# Natural convection root, independent bisection.
Pr=1.575/2.23
def wall(Tc):
 Ts=Tc+273.15;Ra=9.81*2/(Ts+293.15)*(Ts-293.15)*.5**3/(1.575e-5*2.23e-5);Nu=.68+.67*Ra**.25/(1+(.492/Pr)**(9/16))**(4/9);h=.0264/.5*Nu;return Ra,Nu,h,h*(Tc-20)
root=bisect(lambda T:wall(T)[3]-40,30,35);Ra,Nu,h,q=wall(root)
near(root,33.105,'wall root',.001);near(h,3.0523,'wall h',.0001);near(Ra,1.5267e8,'wall Ra',5000);near(q,40,'wall residual');check(Ra<1e9 and (root-20)/(293.15+(root-20)/2)<.05,'wall stated validity checks')
wrong=20+40/wall(30)[2];near(wall(wrong)[3],43.39,'wall one-step diagnosis',.01)
# Three-surface network independent Gauss-Jordan elimination.
eps=[.8,.6,.4];E=[5.670374419e-8*T**4 for T in [600,400,300]];F=[[0,.5,.5],[.5,0,.5],[.5,.5,0]]
M=[[float(i==j)-(1-eps[i])*F[i][j] for j in range(3)]+[eps[i]*E[i]] for i in range(3)]
for i in range(3):
 z=M[i][i];M[i]=[v/z for v in M[i]]
 for j in range(3):
  if i!=j:
   z=M[j][i];M[j]=[M[j][k]-z*M[i][k] for k in range(4)]
J=[row[3] for row in M];G=[sum(F[i][j]*J[j] for j in range(3)) for i in range(3)];Q=[J[i]-G[i] for i in range(3)]
for i in range(3):
 near(Q[i],[3602.173,-1946.398,-1655.775][i],'radiation Q'+str(i),.001);near(Q[i],eps[i]*(E[i]-J[i])/(1-eps[i]),'radiation surface-resistance check'+str(i));near(sum(F[i]),1,'viewfactor row sum');check(all(F[i][j]==F[j][i] for j in range(3)),'viewfactor reciprocity')
near(sum(Q),0,'closed radiation balance');check(J[2]>J[1],'cold reflective surface can have higher J')
for i in range(3):near(E[i]-.5*(sum(E)-E[i]),[6393.347,-2452.437,-3940.910][i],'radiation blackbody limit',.001)
# Tube bank: final property values are inputs, not stored solver result fields.
rhoi=1.2045751824931505;rhob=1.1429212599898093;mu=1.8964541728303878e-5;k=.02704385192949949;cp=1006.7295733472529;Pr=.7059706232911209;Prs=.7033837965818982
mdot=rhoi*2*.12;As=20*4*math.pi*.02;vmax=mdot/(rhob*.04);Re=rhob*vmax*.02/mu;Nu=.27*Re**.63*Pr**.36*(Pr/Prs)**.25;h=Nu*k/.02;Tout=60-40*math.exp(-h*As/(mdot*cp));Q=mdot*cp*(Tout-20);LMTD=(40-(60-Tout))/math.log(40/(60-Tout))
for label,val,target,tol in [('mdot',mdot,.289098,.000001),('As',As,5.02655,.00001),('vmax',vmax,6.32366,.00001),('Re',Re,7622.07,.01),('Nu',Nu,66.5321,.0001),('h',h,89.9642,.0001),('Tout',Tout,51.5419,.0001),('Q_kW',Q/1000,9.1801,.0001),('LMTD',LMTD,20.300,.001)]:near(val,target,'tube '+label,tol)
near(h*As*LMTD,Q,'tube independent LMTD closure');check(1e3<=Re<=2e5 and .7<Pr<500 and 20>16,'tube chosen branch/range');near((293.15+Tout+273.15)/2,308.92094,'tube mean evaluation temperature',.0001);check(Q<h*As*40,'tube inlet-delta overestimate')
# Files, cross-links, preservation against exact original git blob.
files=[*sorted((ROOT/'content/heat-transfer').glob('*.md')),*sorted((ROOT/'content/thermodynamics').glob('*.md'))]
parser=argparse.ArgumentParser();parser.add_argument('--baseline',type=Path);args=parser.parse_args()
allowed_removed={'heat-transfer-16.md':{'**练习 2**　同温差下，上热下冷的静止水平流体层通常比下热上冷更稳定，为什么？'},'thermodynamics-24.md':{'这里假设各组分可在所列相间达到平衡、约束独立；化学反应或指定温压还会减少自由度。纯物质两相 $F=1$，三相 $F=0$。'}}
new_exercises=0
for f in files:
 t=f.read_text();m,b=t[8:].split('\n---\n',1);m=json.loads(m);check(len(re.findall(r'<details\b[^>]*>',t))==t.count('</details>'),'details balance '+f.name)
 for match in re.findall(r'assets/diagrams/([^"\s]+\.svg)',t):check((ROOT/'site/assets/diagrams'/match).exists() or (args.baseline is not None and (args.baseline/'site/assets/diagrams'/match).exists()),'diagram exists '+match)
 if args.baseline:
  rel=str(f.relative_to(ROOT));old=subprocess.check_output(['git','-C',str(args.baseline),'show','b735293:'+rel],text=True);om,ob=old[8:].split('\n---\n',1);om=json.loads(om)
  for k in om:
   if k!='prerequisites':check(om[k]==m[k],'unchanged metadata '+f.name+' '+k)
  check(all(x in m['prerequisites'] for x in om['prerequisites']),'preserved old prerequisites '+f.name)
  absent=[line for line in ob.splitlines() if line.strip() and line not in b and line not in allowed_removed.get(f.name,set())];check(not absent,'preserved original body lines '+f.name+str(absent))
  oldn=len(re.findall(r'\*\*练习\s*\d+',ob));newn=len(re.findall(r'\*\*练习\s*\d+',b));new_exercises+=newn-oldn
  for course,lid in re.findall(r'\]\(#/course/([a-z-]+)/([a-z-]+-\d+)\)',b):check((args.baseline/'content'/course/(lid+'.md')).exists(),'crosslink '+lid)
for name in ('thermal-compressor-cycle.svg','thermal-psychrometric-map.svg','thermal-rankine-state-map.svg','thermal-refrigeration-state-map.svg'):
 p=ROOT/'site/assets/diagrams'/name
 tree=ET.parse(p);check(tree.getroot().get('viewBox').startswith('0 0 720 '),'SVG responsive viewport '+p.name);check('font-size:16px' in p.read_text(),'SVG min font '+p.name)
caption='吸排气时工质穿越边界，不能当作同一团气体的闭口循环'
check(caption in (ROOT/'site/assets/diagrams/thermal-compressor-cycle.svg').read_text(),'compressor caption distinguishes material identity from equal cycle mass throughput')
check(caption in (ROOT/'tools/render_thermal_case_figures.py').read_text(),'compressor generator preserves the reviewed open-system caption')
result={'status':'passed','check_count':len(checks),'new_numbered_exercises':new_exercises if args.baseline else None,'checks':checks}
print(json.dumps(result,ensure_ascii=False,indent=2))
