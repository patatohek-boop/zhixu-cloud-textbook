"""Reproduce explicitly identified HEOS model data (not measurements).
Requires official CoolProp==7.2.0; installs are not part of this script.
Run from any directory: python tools/reproduce_thermal_properties.py
Writes content/thermal-property-cases.json in this checkout.
NIST saturation pressures below are short transcriptions from NISTIR5078 Table 1.
"""
import math,json,sys
from pathlib import Path
from CoolProp.CoolProp import PropsSI as P
import CoolProp
assert CoolProp.__version__ == "7.2.0", "Use the documented CoolProp==7.2.0 version"
ROOT=Path(__file__).resolve().parents[1]
def st(f,a,x,b,y):
 return {'p_kPa':P('P',a,x,b,y,f)/1000,'T_C':P('T',a,x,b,y,f)-273.15,'h_kJkg':P('H',a,x,b,y,f)/1000,'s_kJkgK':P('S',a,x,b,y,f)/1000,'v_m3kg':1/P('D',a,x,b,y,f),'quality':P('Q',a,x,b,y,f)}
d={'version':CoolProp.__version__,'gitrevision':CoolProp.__gitrevision__,'note':'HEOS computed model values; not experiments. Default CoolProp reference states unchanged.'}
d['water_lookup']=[st('Water','P',1e6,'T',t+273.15) for t in [260,265,270]]
L,H=2e5,1e6;Te=P('T','P',L,'Q',0,'R134a');Tc=P('T','P',H,'Q',0,'R134a')
s1=st('R134a','P',L,'T',Te+5);s2s=st('R134a','P',H,'S',s1['s_kJkgK']*1000);h2=s1['h_kJkg']+(s2s['h_kJkg']-s1['h_kJkg'])/.8;s3=st('R134a','P',H,'T',Tc-5)
s2=st('R134a','P',H,'H',h2*1000);s4=st('R134a','P',L,'H',s3['h_kJkg']*1000)
d['r134a']={'states':dict(one=s1,two_s=s2s,two=s2,three=s3,four=s4),'saturated':[st('R134a','P',p,'Q',q) for p in [L,H] for q in [0,1]],'lookup':[st('R134a','P',H,'T',t+273.15) for t in [50,55,60]],'results':{'qL':s1['h_kJkg']-s4['h_kJkg'],'win':h2-s1['h_kJkg'],'qH':h2-s3['h_kJkg'],'COP':(s1['h_kJkg']-s4['h_kJkg'])/(h2-s1['h_kJkg'])}}
d['water_pump_model']=st('Water','P',3e6,'S',649.2)
p=101.325;ps={10:1.2282,18:2.0647,19:2.1983,20:2.3393,30:4.2470,40:7.3849};pv=.5*ps[30]
w=lambda pv:.622*pv/(p-pv)
h=lambda t,w:1.006*t+w*(2501+1.86*t)
wA=w(pv);wC=w(ps[10]);hA=h(30,wA);hB=h(40,wA);hC=h(10,wC);dp=18+(pv-ps[18])/(ps[19]-ps[18])
d['humid']={'ps_kPa':ps,'pv':pv,'A':{'t':30,'w':wA,'h':hA},'B':{'t':40,'w':wA,'h':hB,'RH':pv/ps[40]},'C':{'t':10,'w':wC,'h':hC},'dew_C':dp,'heating_kW':hB-hA,'condensate_kgs':wA-wC,'cooling_kW':hB-hC-(wA-wC)*4.18*10}
# tube-bank model values
p=101325;Tin=293.15;Ts=333.15;U=2;ST=.03;SL=.03;D=.02;NL=20;NT=4;Lt=1
rho=P('D','T',Tin,'P',p,'Air');mdot=rho*U*(NT*ST*Lt);As=NT*NL*math.pi*D*Lt;T=320;its=[]
for i in range(8):
 Tb=(Tin+T)/2;rho_b=P('D','T',Tb,'P',p,'Air');mu=P('V','T',Tb,'P',p,'Air');k=P('L','T',Tb,'P',p,'Air');cp=P('C','T',Tb,'P',p,'Air');pr=P('PRANDTL','T',Tb,'P',p,'Air');prs=P('PRANDTL','T',Ts,'P',p,'Air');Vmax=mdot/(rho_b*NT*(ST-D)*Lt);Re=rho_b*Vmax*D/mu;Nu=.27*Re**.63*pr**.36*(pr/prs)**.25;hbar=k*Nu/D;NTU=hbar*As/(mdot*cp);nextT=Ts-(Ts-Tin)*math.exp(-NTU);its.append([T-273.15,Tb,Re,Nu,hbar,nextT-273.15]);T=nextT
d['tube']={'rho_in':rho,'mdot':mdot,'As':As,'rho_b':rho_b,'mu_b':mu,'k_b':k,'cp_b':cp,'Pr_b':pr,'Pr_s':prs,'Vmax':Vmax,'Re':Re,'Nu':Nu,'h':hbar,'NTU':NTU,'Tout_C':T-273.15,'Q_W':mdot*cp*(T-Tin),'iterations':its,'properties':[]}
for T in [300,305,310,315,333.15]:
 d['tube']['properties'].append({'T_K':T,'rho':P('D','T',T,'P',p,'Air'),'mu':P('V','T',T,'P',p,'Air'),'k':P('L','T',T,'P',p,'Air'),'cp':P('C','T',T,'P',p,'Air'),'Pr':P('PRANDTL','T',T,'P',p,'Air')})
# fixed-property natural convection, beta refreshed at film temperature
nu=1.575e-5;alpha=2.23e-5;k=.0264;L=.5;Ta=293.15;Pr=nu/alpha
def wall(T):
 Ra=9.81*2/(T+Ta)*(T-Ta)*L**3/(nu*alpha);Nu=.68+.67*Ra**.25/(1+(.492/Pr)**(9/16))**(4/9);h=k*Nu/L;return {'Ts_C':T-273.15,'Tf_K':(T+Ta)/2,'beta':2/(T+Ta),'Ra':Ra,'Nu':Nu,'h':h,'q':h*(T-Ta)}
a,b=Ta,Ta+30
for _ in range(70):
 m=(a+b)/2
 if wall(m)['q']<40:a=m
 else:b=m
d['wall']={'root':wall((a+b)/2),'trials':[wall(t+273.15) for t in [30,35,32.5,33.75,33.125,33.4375]]}
# Three surfaces linear elimination without numpy
sigma=5.670374419e-8;Ts=[600,400,300];eps=[.8,.6,.4];F=[[0,.5,.5],[.5,0,.5],[.5,.5,0]];E=[sigma*t**4 for t in Ts]
A=[[float(i==j)-(1-eps[i])*F[i][j] for j in range(3)]+[eps[i]*E[i]] for i in range(3)]
for i in range(3):
 v=A[i][i];A[i]=[x/v for x in A[i]]
 for j in range(3):
  if i!=j:
   v=A[j][i];A[j]=[A[j][k]-v*A[i][k] for k in range(4)]
J=[a[-1] for a in A];G=[sum(F[i][j]*J[j] for j in range(3)) for i in range(3)];Q=[J[i]-G[i] for i in range(3)]
d['radiation']={'E':E,'J':J,'G':G,'Q_W':Q,'sum':sum(Q)}
R=.287;T1=300;rp=4;n=1.3;gamma=1.4;T2=T1*rp**((n-1)/n);closed=R*(T2-T1)/(n-1);steady=n*closed;ct=.05;v1=R*T1/100;eta=1+ct-ct*rp**(1/n)
d['compressor']={'T2':T2,'closed_in':closed,'steady_in':steady,'isothermal':R*T1*math.log(rp),'isentropic':gamma*R*T1/(gamma-1)*(rp**((gamma-1)/gamma)-1),'q':gamma*R/(gamma-1)*(T2-T1)-steady,'etav':eta,'mdot_for_0.01m3s':eta*.01/v1,'power_kW':steady*eta*.01/v1,'V4_over_Vs':ct*rp**(1/n),'V2_over_Vs':(1+ct)/rp**(1/n)}
(ROOT/'content/thermal-property-cases.json').write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in d.items() if k not in ['r134a','tube','water_lookup']},ensure_ascii=False,indent=2))
