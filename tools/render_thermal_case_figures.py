"""Regenerate four original SVG diagrams from the declared properties/model.
Requires official CoolProp==7.2.0. No third-party diagrams are reproduced.
Run: python tools/render_thermal_case_figures.py
"""
from pathlib import Path
import json,math,html
from CoolProp.CoolProp import PropsSI as P
import CoolProp
assert CoolProp.__version__ == "7.2.0", "Use the documented CoolProp==7.2.0 version"
S=Path(__file__).resolve().parents[1];OUT=S/'site/assets/diagrams';D=json.loads((S/'content/thermal-property-cases.json').read_text())
BLUE='#17618c';RED='#ba3f35';GRAY='#627080';GREEN='#1e7760'
def header(title,subtitle,H=740):
 return [f'<svg xmlns="http://www.w3.org/2000/svg" width="720" height="{H}" viewBox="0 0 720 {H}" role="img" aria-label="{title}"><title>{title}</title><desc>{subtitle}</desc><defs><marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto-start-reverse"><path d="M0 0L8 4L0 8Z" fill="context-stroke"/></marker></defs><style>text{{font-family:"Noto Sans CJK SC","Microsoft YaHei",sans-serif;fill:#172d40;font-size:18px}}.small{{font-size:16px}}.title{{font-size:26px;font-weight:700}}.tick{{font-size:16px}}</style><rect width="720" height="100%" fill="#fff"/><text x="28" y="38" class="title">{title}</text><text x="28" y="65" class="small">{subtitle}</text>']
def text(s,x,y,t,cls='',anchor='start',color=None):s.append(f'<text x="{x:.2f}" y="{y:.2f}" class="{cls}" text-anchor="{anchor}"'+(f' style="fill:{color}"' if color else '')+'>'+html.escape(t)+'</text>')
def path(s,coords,col=BLUE,width=3,dash=None,arrow=False):
 pts=' '.join(f'{x:.3f},{y:.3f}' for x,y in coords);s.append(f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="{width}"'+(f' stroke-dasharray="{dash}"' if dash else '')+(' marker-end="url(#arrow)"' if arrow else '')+'/>')
def circle(s,x,y,c=RED):s.append(f'<circle cx="{x:.3f}" cy="{y:.3f}" r="5.4" fill="{c}" stroke="white" stroke-width="1.5"/>')
def save(s,name):s.append('</svg>');(OUT/(name+'.svg')).write_text('\n'.join(s))
def equipment(s,names):
 xs=[28,205,382,559]
 for i,(x,n) in enumerate(zip(xs,names)):
  s.append(f'<rect x="{x}" y="85" width="132" height="50" rx="10" fill="#eaf3f8" stroke="{BLUE}"/>');text(s,x+66,108,n,'','middle');text(s,x+66,128,f'{i+1} → {((i+1)%4)+1}','small','middle')
  if i<3:path(s,[(x+132,110),(xs[i+1]-6,110)],BLUE,2,arrow=True)
 path(s,[(691,110),(703,110),(703,157),(15,157),(15,110),(23,110)],BLUE,2,arrow=True)
def axes(s,x0,y0,w,h,xlim,ylim,xticks,yticks,xlab,ylab):
 def xy(x,y):return x0+w*(x-xlim[0])/(xlim[1]-xlim[0]),y0+h-h*(y-ylim[0])/(ylim[1]-ylim[0])
 for x in xticks:
  xx,yy=xy(x,ylim[0]);path(s,[(xx,y0),(xx,y0+h)],'#e4e9ed',1);text(s,xx,yy+25,str(x),'tick','middle')
 for y in yticks:
  xx,yy=xy(xlim[0],y);path(s,[(x0,yy),(x0+w,yy)],'#e4e9ed',1);text(s,x0-12,yy+6,str(y),'tick','end')
 path(s,[(x0,y0-5),(x0,y0+h),(x0+w+6,y0+h)],GRAY,2)
 text(s,x0+w/2,y0+h+58,xlab,'','middle');text(s,x0,y0-23,ylab)
 return xy
# Water map
s=header('水蒸汽循环：先编号，再定位','10 kPa / 3 MPa / 400 ℃；涡轮效率0.85，泵近似理想')
equipment(s,['泵','锅炉','涡轮','冷凝器']);xy=axes(s,74,218,602,398,(0,9),(0,450),range(0,10),range(0,451,100),'比熵 s / [kJ/(kg·K)]','温度 T / ℃')
for q in [0,1]:
 pts=[]
 for i in range(190):
  T=283.15+(647.09599-283.15)*i/189;pts.append(xy(P('S','T',T,'Q',q,'Water')/1000,T-273.15))
 path(s,pts,BLUE,2)
sf=P('S','P',3e6,'Q',0,'Water')/1000;sg=P('S','P',3e6,'Q',1,'Water')/1000;Ts=P('T','P',3e6,'Q',0,'Water')-273.15
boil=[]
for i in range(55):
 T=319.06+(Ts+273.15-319.06-.0001)*i/54;boil.append(xy(P('S','P',3e6,'T',T,'Water')/1000,T-273.15))
boil+=[xy(sg,Ts)]
for i in range(1,40):
 T=Ts+273.15+(400-Ts)*i/39;boil.append(xy(P('S','P',3e6,'T',T,'Water')/1000,T-273.15))
path(s,boil,RED,3)
pts={'1/2':(.6492,45.85),'3':(6.9234,400),'4s':(6.9234,45.806),'4':(7.411854,45.806)}
path(s,[xy(*pts['3']),xy(*pts['4'])],RED,3,'8 5',True);path(s,[xy(*pts['3']),xy(*pts['4s'])],GRAY,2,'4 5',True);path(s,[xy(*pts['4']),xy(*pts['1/2'])],RED,3,arrow=True)
for k,(x,y) in pts.items():
 xx,yy=xy(x,y);circle(s,xx,yy,GRAY if k=='4s' else RED)
 dx,dy={'1/2':(-4,26),'3':(12,-3),'4s':(-15,32),'4':(17,-10)}[k];text(s,xx+dx,yy+dy,k)
text(s,280,492,'液汽两相区',color=BLUE);text(s,275,323,'高压定压换热',cls='small',color=RED);text(s,28,710,'虚线只连端点；实际不可逆设备不能用 ∫Tds 代替热量','small');save(s,'thermal-rankine-state-map')
# R134a
s=header('R134a：两种压力，四个状态','0.200 / 1.000 MPa；过热与过冷各5 K；压缩机效率0.80')
equipment(s,['压缩机','冷凝器','节流阀','蒸发器']);xy=axes(s,76,218,594,398,(.75,1.95),(-40,110),[.8,1,1.2,1.4,1.6,1.8],[ -40,-20,0,20,40,60,80,100],'比熵 s / [kJ/(kg·K)]','温度 T / ℃')
for q in [0,1]:
 pts=[]
 for i in range(180):
  T=233.15+(374.21195-233.15)*i/179;pts.append(xy(P('S','T',T,'Q',q,'R134a')/1000,T-273.15))
 path(s,pts,BLUE,2)
r=D['r134a']['states'];p={str(i):r[key] for i,key in enumerate(['one','two','three','four'],1)}
a=lambda z:xy(z['s_kJkgK'],z['T_C'])
path(s,[a(p['1']),a(p['2'])],RED,3,'8 5',True);path(s,[a(p['1']),a(r['two_s'])],GRAY,2,'4 5',True)
# isobar heat rejection/supply traced by enthalpy samples, continuous across saturation
for z1,z2,pressure in [(p['2'],p['3'],1e6),(p['4'],p['1'],2e5)]:
 curve=[]
 for i in range(130):
  h=(z1['h_kJkg']+(z2['h_kJkg']-z1['h_kJkg'])*i/129)*1000;curve.append(xy(P('S','P',pressure,'H',h,'R134a')/1000,P('T','P',pressure,'H',h,'R134a')-273.15))
 path(s,curve,RED,3,arrow=True)
path(s,[a(p['3']),a(p['4'])],RED,3,'8 5',True)
for k,z in p.items():
 xx,yy=a(z);circle(s,xx,yy);dx,dy={'1':(12,12),'2':(12,-5),'3':(-25,-12),'4':(-27,25)}[k];text(s,xx+dx,yy+dy,k)
xx,yy=a(r['two_s']);circle(s,xx,yy,GRAY);text(s,xx-33,yy-5,'2s','small')
text(s,285,484,'液汽两相区',color=BLUE);text(s,28,710,'冷凝与蒸发的实线用于状态定位；压缩/节流的虚线仅连端点','small');save(s,'thermal-refrigeration-state-map')
# humid h-w
s=header('湿空气：加热、露点与除湿','总压101.325 kPa；理想混合物近似；干空气质量基准',H=760)
xy=axes(s,82,126,572,486,(0,25),(0,115),[0,5,10,15,20,25],[0,20,40,60,80,100],'含湿量 ω / [g/kg干空气]','比焓 h / [kJ/kg干空气]')
p=101.325
ws=lambda t:.622*(P('P','T',t+273.15,'Q',0,'Water')/1000)/(p-P('P','T',t+273.15,'Q',0,'Water')/1000)
hum=lambda t,w:1.006*t+w*(2501+1.86*t)
# isotherms clipped at saturation and chart upper right
for t in [0,10,20,30,40,50]:
 wmax=min(ws(t),.025);path(s,[xy(0,hum(t,0)),xy(wmax*1000,hum(t,wmax))],'#adb8c2',1.4)
 xx,yy=xy(.3,hum(t,.0003));text(s,xx+2,yy-5,f'{t}℃','small',color=GRAY)
curve=[]
for i in range(180):
 t=40*i/179;w=ws(t)
 if w<=.025 and hum(t,w)<=115:curve.append(xy(w*1000,hum(t,w)))
path(s,curve,BLUE,3);text(s,420,240,'饱和线 φ=100%','small',color=BLUE)
hu=D['humid'];A=hu['A'];B=hu['B'];C=hu['C'];Dew={'w':A['w'],'h':hum(hu['dew_C'],A['w'])}
path(s,[xy(A['w']*1000,A['h']),xy(B['w']*1000,B['h'])],RED,3,arrow=True)
path(s,[xy(B['w']*1000,B['h']),xy(Dew['w']*1000,Dew['h'])],GREEN,3,'7 4',True)
c=[]
for i in range(90):
 t=hu['dew_C']+(10-hu['dew_C'])*i/89;w=ws(t);c.append(xy(w*1000,hum(t,w)))
path(s,c,GREEN,3,arrow=True)
for key,z,off in [('A',A,(13,8)),('B',B,(13,-4)),('D',Dew,(13,15)),('C',C,(-27,20))]:
 xx,yy=xy(z['w']*1000,z['h']);circle(s,xx,yy,RED if key in ['A','B'] else GREEN);text(s,xx+off[0],yy+off[1],key)
text(s,345,710,'A→B：加热  B→D：冷却  D→C：凝结除湿','small','middle');text(s,345,738,'灰色斜线：等干球温度；露点约18.44 ℃','small','middle');save(s,'thermal-psychrometric-map')
# compressor normalized PV
s=header('往复式压气机：四段指示图','余隙比0.05；p2/p1=4；压缩与再膨胀指数n=1.3',H=700)
xy=axes(s,90,129,552,417,(0,1.1),(0,4.6),[0,.2,.4,.6,.8,1.0],[0,1,2,3,4],'缸内容积 V / 扫气容积 Vs','压力 p / 吸气压力 p1')
c=D['compressor'];v1=1.05;v2=c['V2_over_Vs'];v3=.05;v4=c['V4_over_Vs'];n=1.3
cur=[(v1+(v2-v1)*i/100,(v1/(v1+(v2-v1)*i/100))**n) for i in range(101)];path(s,[xy(*z) for z in cur],RED,3,arrow=True)
path(s,[xy(v2,4),xy(v3,4)],RED,3,arrow=True)
cur=[(v3+(v4-v3)*i/100,4*(v3/(v3+(v4-v3)*i/100))**n) for i in range(101)];path(s,[xy(*z) for z in cur],BLUE,3,arrow=True);path(s,[xy(v4,1),xy(v1,1)],BLUE,3,arrow=True)
for key,z,off in [('1',(v1,1),(10,-9)),('2',(v2,4),(10,-12)),('3',(v3,4),(-26,-12)),('4',(v4,1),(-22,29))]:
 xx,yy=xy(*z);circle(s,xx,yy);text(s,xx+off[0],yy+off[1],key)
text(s,428,330,'1→2 压缩',color=RED);text(s,170,154,'2→3 排气',color=RED);text(s,111,326,'3→4 再膨胀',cls='small',color=BLUE);text(s,310,490,'4→1 吸气',color=BLUE)
text(s,360,631,'V4/Vs=0.14524；新吸气体积比=1.05−0.14524','small','middle');text(s,360,662,'吸排气时工质穿越边界，不能当作同一团气体的闭口循环','small','middle');save(s,'thermal-compressor-cycle')
print('generated four original SVGs')
