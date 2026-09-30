(function(root){
'use strict';
const LABS={
 'python-loop':{icon:'↻',title:'一步一步看循环执行',description:'跟踪 for 循环中的变量，观察每一步如何更新累计结果。',controls:[['step','已完成的迭代次数',0,4,1,0]],caption:'演示固定 Python 代码：total = 0；for x in [1, 2, 3, 4]: total += x * x。图形模拟此例的计算步骤，并非浏览器中的通用 Python 解释器。',draw:v=>{const n=Math.round(v.step),values=[1,2,3,4],total=values.slice(0,n).reduce((s,x)=>s+x*x,0);return {svg:base(values.map((x,i)=>`<rect x="${27+i*115}" y="50" width="90" height="65" rx="6" fill="${i<n?'var(--accent)':'var(--muted)'}" opacity="${i<n?'.9':'.13'}"/><text x="${72+i*115}" y="91" text-anchor="middle" fill="${i<n?'var(--paper)':'currentColor'}" font-size="25">${x}</text><text x="${72+i*115}" y="150" text-anchor="middle">${i<n?'加 '+x*x:'未执行'}</text>`).join('')+`<text x="240" y="222" text-anchor="middle" font-size="24">total = ${total}</text>`),result:n===0?'循环开始前：total=0，变量 x 尚未由循环赋值。':`完成第 ${n} 次迭代：x=${n}，把 ${n}²=${n*n} 加入 total，得到 ${total}。${n===4?'循环结束后 x 仍为 4。':''}`,legend:'试着先心算下一步的 total，再拖动滑块。for 每次取一个列表元素，不会自动把整个列表一起计算。'};}},
 derivative:{icon:'∂',title:'从割线走向切线',description:'缩小两点的间距，观察平均变化率如何接近瞬时变化率。',controls:[['x','观察位置 x',-1.5,1.5,.1,.7],['h','两点间距 h',.01,1,.01,.7]],caption:'模型：f(x)=x²。h 保持为正，从右侧逼近；这个光滑函数的左右极限相同。',draw:v=>{let slope=2*v.x+v.h;return {svg:plot([{fn:x=>x*x,color:'var(--accent)'},{fn:x=>v.x*v.x+slope*(x-v.x),color:'var(--blue)',dash:true},{fn:x=>v.x*v.x+2*v.x*(x-v.x),color:'#bd7148'}],[-2,2.5],[-1,6],[{x:v.x,y:v.x*v.x},{x:v.x+v.h,y:(v.x+v.h)**2}]),result:`割线斜率 = 2x + h = ${slope.toFixed(3)}　·　切线斜率 = 2x = ${(2*v.x).toFixed(3)}。误差恰好为 h = ${v.h.toFixed(2)}。`,legend:'绿色：函数　蓝色虚线：割线　橙色：切线'};}} ,
 integral:{icon:'∫',title:'小矩形如何变成积分',description:'用中点矩形近似曲线下的面积，观察分割加密后的误差。',controls:[['n','矩形数量 n',2,60,1,8]],caption:'模型：在 [0,2] 上积分 x²，使用等宽中点法。面积非负；一般定积分是有向累积量。',draw:v=>{const n=Math.round(v.n),dx=2/n;let sum=0,bars='';for(let i=0;i<n;i++){const x=(i+.5)*dx,y=x*x;sum+=y*dx;bars+=`<rect x="${mapX(i*dx,[0,2])}" y="${mapY(y,[0,4.5])}" width="${386/n}" height="${mapY(0,[0,4.5])-mapY(y,[0,4.5])}" fill="var(--accent)" fill-opacity=".15" stroke="var(--accent)" stroke-width=".6"/>`;}return {svg:plot([{fn:x=>x*x,color:'var(--accent)'}],[0,2],[0,4.5],[],bars),result:`近似面积 ${sum.toFixed(6)}　·　精确积分 8/3 = ${(8/3).toFixed(6)}　·　误差 ${Math.abs(sum-8/3).toFixed(6)}`,legend:'每个矩形的高度取该小区间中点处的函数值。'};}} ,
 matrix:{icon:'⊞',title:'看见一个线性变换',description:'改变矩阵的四个元素，观察单位正方形和基向量如何变换。',controls:[['a','a：第一列的横坐标',-2,2,.1,1],['b','b：第二列的横坐标',-2,2,.1,.5],['c','c：第一列的纵坐标',-2,2,.1,.3],['d','d：第二列的纵坐标',-2,2,.1,1]],caption:'模型：二维线性映射 y=Ax，A=[[a,b],[c,d]]。行列式给出有向面积倍率。'},
 gradient:{icon:'∇',title:'梯度指向哪里',description:'移动曲面上的观察点，比较最陡上升方向与等高线。',controls:[['x','位置 x',-2,2,.1,1],['y','位置 y',-2,2,.1,.5]],caption:'模型：f(x,y)=x²+2y²，∇f=(2x,4y)。箭头缩放只为显示方向，不直接代表长度。'},
 carnot:{icon:'◒',title:'热机效率的上限',description:'改变高、低温热源的温度，观察卡诺效率和能量分配。',controls:[['hot','高温热源 Tₕ / K',450,1200,10,700],['cold','低温热源 T𝚌 / K',200,440,10,300]],caption:'模型：两个恒温热源之间的可逆热机，输入热量设为 1000 J。温度必须用 K；真实热机效率不超过此上限。',draw:v=>{const e=1-v.cold/v.hot,w=1000*e,q=1000-w;return {svg:barDiagram([['吸收热量',1000,'var(--blue)'],['输出功',w,'var(--accent)'],['排出热量',q,'#bd7148']],1000,'J'),result:`η = 1 − T𝚌/Tₕ = ${(100*e).toFixed(1)}%　·　W = ${w.toFixed(1)} J　·　Q𝚌 = ${q.toFixed(1)} J。`,legend:'每完成一个循环，系统内能变化为零：输入热量 = 输出功 + 排出热量。'};}} ,
 conduction:{icon:'↗',title:'平壁中的温度与热流',description:'调节厚度与导热系数，区分温度梯度和热流密度。',controls:[['k','导热系数 k / (W·m⁻¹·K⁻¹)',.1,10,.1,1.5],['L','墙厚 L / m',.02,.5,.01,.1],['hot','左侧温度 / °C',60,180,5,100],['cold','右侧温度 / °C',0,50,5,20]],caption:'模型：一维稳态、常导热系数、无内热源、两侧表面定温。不包含对流热阻。温差的 K 与 °C 数值相同。',draw:v=>{const q=v.k*(v.hot-v.cold)/v.L;return {svg:plot([{fn:x=>v.hot+(v.cold-v.hot)*x/v.L,color:'#bd7148'}],[0,v.L],[0,200]),result:`热流密度 q″ = k(T左 − T右)/L = ${q.toFixed(1)} W/m²　·　单位面积热阻 L/k = ${(v.L/v.k).toFixed(4)} m²·K/W。`,legend:'横轴：距离 x / m　纵轴：温度 / °C。固定表面温度时，增大 k 不改变温度直线，却增大热流。'};}} ,
 cooling:{icon:'τ',title:'温度如何随时间衰减',description:'改变换热系数与时间，理解指数冷却的时间常数。',controls:[['h','换热系数 h / (W·m⁻²·K⁻¹)',5,100,5,25],['t','观察时间 t / s',0,600,5,150]],caption:'模型：均匀温度的集总物体，m=0.1 kg，c=500 J/(kg·K)，A=0.01 m²，k=200 W/(m·K)，ρ=8000 kg/m³；环境20°C，初温100°C。Bi=hV/(Ak)<0.1 才适用。',draw:v=>{const tau=50/(v.h*.01),fn=t=>20+80*Math.exp(-t/tau),bi=v.h*(.1/8000)/(.01*200);return {svg:plot([{fn,color:'var(--accent)'}],[0,600],[0,110],[{x:v.t,y:fn(v.t)}]),result:`τ = ${tau.toFixed(1)} s　·　T(${v.t.toFixed(0)} s) = ${fn(v.t).toFixed(2)} °C　·　Bi = ${bi.toFixed(5)}，满足集总近似。`,legend:'横轴：时间 / s　纵轴：温度 / °C。经过一个时间常数，温差剩下初始温差的 e⁻¹。'};}} ,
 bernoulli:{icon:'≈',title:'管道变窄，流速怎样变化',description:'在理想水平流管中，把连续性与伯努利方程放在一起。',controls:[['ratio','出口面积 / 入口面积',.3,1.6,.05,.6],['v','入口速度 v₁ / (m/s)',.5,4,.1,2]],caption:'模型：水 ρ=1000 kg/m³；稳态、不可压、无黏、水平、同一流线、无泵或涡轮。忽略损失。p₁−p₂ 是压差，不是出口绝对压力。',draw:v=>{const v2=v.v/v.ratio,dp=.5*1000*(v2*v2-v.v*v.v),h=48*Math.sqrt(v.ratio);let svg=base(`<path d="M45 60H175L300 ${110-h}H438V${110+h}H300L175 160H45Z" fill="var(--blue)" fill-opacity=".1" stroke="var(--blue)" stroke-width="2"/><path d="M65 110H150M315 110H${Math.min(425,315+65/v.ratio)}" stroke="var(--accent)" stroke-width="3" marker-end="url(#arrow)"/><text x="60" y="205">入口 A₁</text><text x="315" y="205">出口 A₂</text>`);return {svg,result:`v₂ = v₁A₁/A₂ = ${v2.toFixed(3)} m/s　·　p₁−p₂ = ${(dp/1000).toFixed(3)} kPa。`,legend:'形状为概念示意，非严格几何比例。实际管路存在沿程和局部损失，压差还取决于泵、流量和边界条件。'};}} ,
 regression:{icon:'ŷ',title:'亲手拟合一条直线',description:'调节斜率与截距，让预测更接近观测点，观察均方误差。',controls:[['m','斜率 w',-1,3,.05,1],['b','截距 b',-2,4,.1,0]],caption:'模型：ŷ=wx+b；固定五组演示观测值。损失为所有样本残差平方的平均，不代表泛化误差。',draw:v=>{const pts=[{x:0,y:1},{x:1,y:2.1},{x:2,y:2.8},{x:3,y:4.2},{x:4,y:4.9}],mse=pts.reduce((s,p)=>s+(v.m*p.x+v.b-p.y)**2,0)/pts.length;let extra=pts.map(p=>`<path d="M${mapX(p.x,[-.5,4.5])} ${mapY(p.y,[-2,9])}V${mapY(v.m*p.x+v.b,[-2,9])}" stroke="#bd7148" stroke-width="2" stroke-dasharray="3 3"/>`).join('');return {svg:plot([{fn:x=>v.m*x+v.b,color:'var(--accent)'}],[-.5,4.5],[-2,9],pts,extra),result:`预测 ŷ = ${v.m.toFixed(2)}x + ${v.b.toFixed(2)}　·　训练均方误差 MSE = ${mse.toFixed(4)}。`,legend:'圆点为观测；虚线为残差。把训练误差压低，还需要验证集判断能否预测新数据。'};}} ,
 'gradient-descent':{icon:'↘',title:'梯度下降：步子多大合适',description:'在一个简单目标函数上，观察学习率导致的收敛、振荡和发散。',controls:[['rate','学习率 α',.05,1.15,.05,.3],['steps','迭代步数',0,14,1,5],['start','初始位置 w₀',-3,3,.25,2.5]],caption:'模型：J(w)=w²，更新 wₖ₊₁=(1−2α)wₖ。本例 0<α<1 收敛；其他损失函数的范围不同。',draw:v=>{const vals=[v.start];for(let i=0;i<Math.round(v.steps);i++)vals.push((1-2*v.rate)*vals.at(-1));const last=vals.at(-1),pts=vals.filter(x=>Math.abs(x)<=3.5).map(x=>({x,y:x*x}));return {svg:plot([{fn:x=>x*x,color:'var(--accent)'}],[-3.5,3.5],[0,12.5],pts),result:`第 ${Math.round(v.steps)} 步：w = ${last.toFixed(5)}，J = ${(last*last).toFixed(5)}。${v.start===0?'初值已在最小点，所有迭代保持 w=0。':Math.round(v.steps)===0?'尚未迭代，当前显示初值。':v.rate<.5?'本例逐步靠近最小值。':v.rate===.5?'本例一步到达最小值。':v.rate<1?'本例振荡着收敛。':v.rate===1?'本例在两侧等幅振荡。':'本例通常发散；超出坐标范围的点不绘制。'}`,legend:'点为各次迭代位置。收敛是这个二次模型的性质，不能据此保证任意神经网络达到全局最优。'};}}
};
// Original diagrams and calculations. Teaching references are linked in each lab;
// no remote scripts, images, model weights, or stochastic API calls are required.
const PI2=Math.PI*Math.PI, C={green:'var(--accent)',blue:'var(--blue)',orange:'#bd7148',purple:'#8c78bd'};
function heatState(b,c,Fo){
 const a=[.65,b,c],amplitudes=a.map((v,i)=>v*Math.exp(-((i+1)**2)*PI2*Fo));
 const theta=x=>x===0||x===1?0:amplitudes.reduce((s,v,i)=>s+v*Math.sin((i+1)*Math.PI*x),0);
 const gradient=x=>amplitudes.reduce((s,v,i)=>s+(i+1)*Math.PI*v*Math.cos((i+1)*Math.PI*x),0);
 const energy=amplitudes.reduce((s,v)=>s+v*v/2,0),initialEnergy=a.reduce((s,v)=>s+v*v/2,0);
 const heat=2/Math.PI*(amplitudes[0]+amplitudes[2]/3),initialHeat=2/Math.PI*(a[0]+a[2]/3);
 return {a,amplitudes,theta,gradient,energy,initialEnergy,heat,initialHeat,removedHeat:initialHeat-heat,
  energyRate:-amplitudes.reduce((s,v,i)=>s+(i+1)**2*PI2*v*v,0),heatRate:gradient(1)-gradient(0)};
}
const coolingConstants=Object.freeze({mc:180,A:.01,T0:80,Tinf:20,hTrue:18});
function coolingAt(h,t){return 20+60*Math.exp(-h*.01*t/180);}
function coolingSensitivity(h,t){return -60*.01*t/180*Math.exp(-h*.01*t/180);}
function coolingData(noise=0){return [0,100,300,600,1000,1800,3000].map((t,i)=>({x:t,y:coolingAt(18,t)+noise*[0,.5,-.7,.4,-.3,.6,-.2][i]}));}
function coolingSSE(h,noise=0){return coolingData(noise).reduce((s,p)=>s+(coolingAt(h,p.x)-p.y)**2,0);}
function designInformation(u,sigma=1,repeats=1){const t=1000*u,s=coolingSensitivity(18,t);return {t,sensitivity:s,information:repeats*s*s/(sigma*sigma),relative:u*u*Math.exp(2-2*u)};}
const proxyData=[{x:-1,y:.1},{x:-.5,y:.7},{x:0,y:.85},{x:.5,y:1.55},{x:1,y:1.65}];
function posterior(count=5,sigma=.3){
 const indices={2:[0,4],3:[0,2,4],4:[0,1,3,4],5:[0,1,2,3,4]}[Math.round(count)];
 const data=indices.map(i=>({...proxyData[i]})),w=1/(sigma*sigma);
 const a=.25+data.length*w,b=w*data.reduce((s,p)=>s+p.x,0),d=.25+w*data.reduce((s,p)=>s+p.x*p.x,0),det=a*d-b*b;
 const cov=[[d/det,-b/det],[-b/det,a/det]],rhs=[w*data.reduce((s,p)=>s+p.y,0),w*data.reduce((s,p)=>s+p.x*p.y,0)];
 return {data,sigma,cov,mean:cov.map(row=>row[0]*rhs[0]+row[1]*rhs[1])};
}
function predictBayes(model,x){const variance=model.cov[0][0]+2*x*model.cov[0][1]+x*x*model.cov[1][1];return {mean:model.mean[0]+x*model.mean[1],variance,observationVariance:variance+model.sigma**2};}
function physicsState(amplitude,rate,Fo){
 const exact=x=>Math.sin(Math.PI*x)*Math.exp(-PI2*Fo),candidate=x=>amplitude*Math.sin(Math.PI*x)*Math.exp(-rate*PI2*Fo);
 const residual=x=>(1-rate)*PI2*candidate(x);
 return {exact,candidate,residual,initialError:Math.abs(amplitude-1)/Math.SQRT2,boundaryError:0,
  residualNorm:Math.abs((1-rate)*PI2*amplitude*Math.exp(-rate*PI2*Fo))/Math.SQRT2,
  solutionError:Math.abs(amplitude*Math.exp(-rate*PI2*Fo)-Math.exp(-PI2*Fo))/Math.SQRT2};
}
function splitStudy(shift=1.5,noise=.2,seed=1){
 const offsets=[-1.5,-1,-.5,.5,1,1.5],eps=[-.3,.1,.2,-.2,-.1,.3];
 const rows=offsets.flatMap((b,run)=>eps.map((e,j)=>({id:run*6+j,run,x:j/5,y:j/5+shift*b+noise*e})));
 let state=Math.round(seed)>>>0;const random=()=>{state=(Math.imul(1664525,state)+1013904223)>>>0;return state/4294967296;};
 const rowTest=new Set();for(let run=0;run<6;run++){const order=[0,1,2,3,4,5];for(let j=5;j>0;j--){const k=Math.floor(random()*(j+1));[order[j],order[k]]=[order[k],order[j]];}order.slice(0,2).forEach(j=>rowTest.add(run*6+j));}
 function evaluate(isTest){
  const train=rows.filter(p=>!isTest(p)),test=rows.filter(isTest),offsets=new Map();
  for(let run=0;run<6;run++){const seen=train.filter(p=>p.run===run);if(seen.length)offsets.set(run,seen.reduce((s,p)=>s+p.y-p.x,0)/seen.length);}
  const predictions=test.map(p=>({...p,predicted:p.x+(offsets.get(p.run)||0)}));
  return {train,test,predictions,mse:predictions.reduce((s,p)=>s+(p.predicted-p.y)**2,0)/test.length};
 }
 return {rows,rowSplit:evaluate(p=>rowTest.has(p.id)),groupSplit:evaluate(p=>p.run===2||p.run===5)};
}
const LAB_MATH={heatState,coolingConstants,coolingAt,coolingSensitivity,coolingData,coolingSSE,designInformation,posterior,predictBayes,physicsState,splitStudy};
const heatSources=[['3Blue1Brown：热方程的图形含义','https://www.3blue1brown.com/lessons/pdes/'],['3Blue1Brown：傅里叶级数与模态叠加','https://www.3blue1brown.com/lessons/fourier-series/']];
Object.assign(LABS,{
 'heat-modes':{
  icon:'∿',title:'把温度拆成会衰减的波',description:'先看杆上的颜色，再看三条波怎样相加；细小的起伏为什么先消失？',
  controls:[['Fo','时间 Fo = αt/L²',0,.35,.0025,0,'只改变经过的时间；初始形状保持不变。'],['b','第二模态系数 a₂',-.15,.15,.01,.12,'蓝虚线：a₂ sin(2πξ)，正负控制左右偏热。'],['c','第三模态系数 a₃',0,.2,.01,.18,'橙虚线：a₃ sin(3πξ)，衰减速率是第一模态的 9 倍。']],
  caption:'一维均匀杆、常热扩散率、无内热源；ξ=x/L∈[0,1]，两端恒定20°C，T=20+80θ。a₁=0.65，a₂∈[−0.15,0.15]，a₃∈[0,0.2]。此范围保证初始0≤θ≤1；解析热方程解保持20≤T≤100°C。E=∫θ²dξ是平方泛函，不是物理内能；实际超额热量正比于H=∫θdξ，并通过两端散出。',
  animation:{key:'Fo',from:0,to:.35,duration:12000,label:'播放温度演化'},sources:heatSources,
  draw:v=>{
   const m=heatState(v.b,v.c,v.Fo),curves=[{fn:m.theta,color:C.green},...m.amplitudes.map((a,i)=>({fn:x=>a*Math.sin((i+1)*Math.PI*x),color:[C.purple,C.blue,C.orange][i],dash:true}))];
   let strip='';for(let i=0;i<96;i++){const theta=m.theta((i+.5)/96);strip+=`<rect x="${24+i*4.5}" y="18" width="4.6" height="32" fill="hsl(${220-205*theta} 65% 48%)"/>`;}
   for(let i=0;i<81;i++)strip+=`<rect x="${110+i*3.2}" y="81" width="3.3" height="12" fill="hsl(${220-205*i/80} 65% 48%)"/>`;
   strip+='<text x="24" y="71">20°C 定温端</text><text x="456" y="71" text-anchor="end">20°C 定温端</text><text x="103" y="94" text-anchor="end">20</text><text x="379" y="94">100°C</text>';
   const energyPlot=plot([{fn:t=>heatState(v.b,v.c,t).energy/m.initialEnergy,color:C.green}],[0,.35],[0,1.05],[{x:v.Fo,y:m.energy/m.initialEnergy}]);
   return {svg:base(strip,'杆上的温度与固定20至100摄氏度色标',110)+namedPlot('位置 ξ →；纵轴 θ。实线是三条模态的和。',plot(curves,[0,1],[-.22,1.05]))+namedPlot('时间 Fo →；纵轴 E(Fo)/E(0)。',energyPlot),result:`Fo=${v.Fo.toFixed(3)}；E/E₀=${(m.energy/m.initialEnergy).toFixed(4)}。剩余热量 H=${m.heat.toFixed(4)}，累计散出=${m.removedHeat.toFixed(4)}，二者之和=${m.initialHeat.toFixed(4)}。`,legend:'绿色实线：θ；紫、蓝、橙虚线：第1、2、3模态。色条固定20—100°C，不随时间重新缩放。两端与恒温热源交换热量，杆自身热量不守恒。'};
  }
 },
 'cooling-inverse':{
  icon:'ĥ',title:'从温度记录反推换热系数',description:'拖动 h，让冷却曲线穿过合成数据；再观察损失曲线与温度对 h 的灵敏度。',
  controls:[['h','候选 h / (W·m⁻²·K⁻¹)',5,45,.5,30,'绿色曲线中的指数衰减率为 hA/(mc)。'],['noise','固定扰动的幅度 / K',0,3,.1,0,'改变同一组合成扰动，不会生成新的随机样本。'],['probe','灵敏度观察时刻 / s',0,3000,25,1000,'比较轻微改变 h 后，这一时刻的温度有多敏感。']],
  caption:'集总冷却模型：已知 m=0.2 kg、c=900 J/(kg·K)，因此 mc=180 J/K；A=0.01 m²，T₀=80°C，T∞=20°C。只辨识一个恒定 h，并假设物体内部温度均匀、集总近似成立。数据由 h真=18 生成，固定扰动不是实测噪声；扰动为0时真值SSE=0。有扰动时，最小SSE位置未必等于真值。',
  animation:{key:'h',from:5,to:45,duration:14000,label:'扫描候选 h'},
  draw:v=>{const data=coolingData(v.noise),sse=coolingSSE(v.h,v.noise),max=Math.max(coolingSSE(5,v.noise),coolingSSE(45,v.noise))*1.05;
   const probe=`<path d="M${mapX(v.probe,[0,3000])} 217V${mapY(coolingAt(v.h,v.probe),[15,85])}" stroke="${C.orange}" stroke-dasharray="3 4"/><circle cx="${mapX(v.probe,[0,3000])}" cy="${mapY(coolingAt(v.h,v.probe),[15,85])}" r="6" fill="none" stroke="${C.orange}" stroke-width="2"/>`;
   return {svg:namedPlot('时间 t / s →；纵轴温度 / °C。蓝点为数据，橙圈为灵敏度观察时刻。',plot([{fn:t=>coolingAt(v.h-1,t),color:C.purple,dash:true},{fn:t=>coolingAt(v.h+1,t),color:C.purple,dash:true},{fn:t=>coolingAt(v.h,t),color:C.green}],[0,3000],[15,85],data,probe))+namedPlot('候选 h →；纵轴 SSE / K²。蓝点标出当前 h。',plot([{fn:h=>coolingSSE(h,v.noise),color:C.orange}],[5,45],[0,max],[{x:v.h,y:sse}])),result:`h=${v.h.toFixed(1)}，SSE=${sse.toFixed(3)} K²；τ=${(18000/v.h).toFixed(1)} s。在 t=${v.probe.toFixed(0)} s，∂T/∂h=${coolingSensitivity(v.h,v.probe).toFixed(4)} K/(W·m⁻²·K⁻¹)。`,legend:'绿色：候选曲线；紫虚线：把 h 分别增加、减少1后的曲线，仅显示参数扰动，不是置信带。曲线在橙圈附近分开得越明显，温度对h越敏感。SSE=Σ[T模型(tᵢ;h)−T数据,i]²，衡量这组数据的拟合误差；t=0时无法分辨h。'};}
 },
 'experiment-design':{
  icon:'◎',title:'什么时候测温更能辨识 h',description:'选择一次测量的时刻：只看温度变化大还不够，要看它对待辨识参数有多敏感。',
  controls:[['u','测量时刻 t/τ',0,6,.05,1,'标称 h=18，τ=1000 s；横轴用时间常数归一化。'],['sigma','单次温度噪声标准差 σ / K',.2,5,.1,1,'已知、独立、同方差的高斯测量误差。'],['repeats','独立重复测量次数 N',1,10,1,3,'只有相互独立时信息量才能相加。']],
  caption:'沿用已知 mc=180 J/K、A=0.01 m²、T₀=80°C、T∞=20°C 的单参数集总模型。h=18 是设计时使用的标称值，实际 h 尚未知。假设噪声独立、同方差且方差已知，无时间成本约束。t≈τ 最优仅对这一局部单参数设计成立；同时估计初温、环境温度或传感器滞后时，通常需要分散测时。连续采样的相关误差不能直接按N累加。',
  animation:{key:'u',from:0,to:6,duration:12000,label:'扫描测量时刻'},
  draw:v=>{const m=designInformation(v.u,v.sigma,Math.round(v.repeats)),bound=m.information>0?(1/Math.sqrt(m.information)).toFixed(3):'无有限下界';
   return {svg:namedPlot('时间 t/τ →；纵轴 I(t)/I(τ)。峰顶出现在1。',plot([{fn:u=>designInformation(u).relative,color:C.green}],[0,6],[0,1.08],[{x:v.u,y:m.relative}]))+namedPlot('时间 t / s →；纵轴温度 / °C。',plot([{fn:t=>coolingAt(18,t),color:C.blue}],[0,6000],[18,84],[{x:m.t,y:coolingAt(18,m.t)}])),result:`测量时刻=${m.t.toFixed(0)} s；相对信息=${(100*m.relative).toFixed(1)}%。N次总信息 I=${m.information.toFixed(4)} (W·m⁻²·K⁻¹)⁻²；局部无偏估计的标准差下界：${bound}${m.information>0?' W·m⁻²·K⁻¹':''}。`,legend:'绿色：平方灵敏度经归一化。I=N(∂T/∂h)²/σ²；下界1/√I是条件成立时的 Cramér–Rao 界，不是实际估计误差或一次实验的保证。'};}
 },
 'uncertainty-band':{
  icon:'±',title:'一条预测线，两种不确定性',description:'用贝叶斯线性代理区分“均值函数不确定”与“下一次观测还会波动”，观察远离数据时的变化。',
  controls:[['count','采用的合成观测数',2,5,1,5,'对称设计：2点用两端；3点加中心；4点用±0.5代替中心；5点全用。'],['sigma','假定已知的观测噪声 σ',.1,1,.05,.3,'这会改变似然权重与观测带，不重新生成数据。'],['x','查询位置 x',-3,3,.05,0,'所有训练数据在[−1,1]；区间外是在外推。']],
  caption:'无量纲演示：y=w₀+w₁x+ε；w~N(0,4I₂)，ε独立且服从N(0,σ²)，σ已知。固定数据仅用于演示。阴影为逐点约95%后验区间（均值±1.96标准差），不是整条曲线同时覆盖95%。此处是贝叶斯线性代理，不是已训练的神经网络或高斯过程；区间宽度不能保证模型失配、未知物理或分布外误差受到覆盖。',
  animation:{key:'x',from:-3,to:3,duration:10000,label:'沿预测区间观察'},
  sources:[['Toronto CSC411：Bayesian Regression（第23—27页）','https://www.cs.toronto.edu/~rsalakhu/CSC411/notes/lecture_Bayesian.pdf']],
  draw:v=>{const m=posterior(v.count,v.sigma),pred=x=>predictBayes(m,x),p=pred(v.x),xr=[-3,3],yr=[-6,8];
   const shade=band(pred,'observationVariance',xr,yr,C.orange,.15)+band(pred,'variance',xr,yr,C.blue,.3)+`<path d="M${mapX(v.x,xr)} ${mapY(p.mean-1.96*Math.sqrt(p.observationVariance),yr)}V${mapY(p.mean+1.96*Math.sqrt(p.observationVariance),yr)}" stroke="${C.orange}" stroke-width="3"/><path d="M${mapX(v.x,xr)} ${mapY(p.mean-1.96*Math.sqrt(p.variance),yr)}V${mapY(p.mean+1.96*Math.sqrt(p.variance),yr)}" stroke="${C.blue}" stroke-width="7"/>`;
   return {svg:namedPlot('横轴 x；纵轴 y。蓝点为数据，绿色线为后验均值。',plot([{fn:x=>pred(x).mean,color:C.green}],xr,yr,m.data,shade)),result:`x=${v.x.toFixed(2)}：预测均值=${p.mean.toFixed(3)}；函数值后验标准差=${Math.sqrt(p.variance).toFixed(3)}，新观测预测标准差=${Math.sqrt(p.observationVariance).toFixed(3)}。${Math.abs(v.x)>1?'当前查询位于训练区间之外。':'当前查询位于训练区间之内。'}`,legend:'内层蓝带：参数不确定性传播到函数值；外层橙带：再加新观测噪声。方差相加，标准差不直接相加。对本例对称设计，越远离数据中心，斜率不确定性带来的带宽越大。'};}
 },
 'physics-residual':{
  icon:'R',title:'方程残差为零，就答对了吗',description:'把一个“满足热方程却不满足初值”的候选解放到参考解旁边，分别检查三种约束。',
  controls:[['amplitude','候选初始幅值 c',0,1.5,.05,.6,'c 改变初值；即使 c≠1，也可能满足同一个 PDE。'],['rate','候选衰减率倍率 k',.2,1.8,.05,1,'k=1 才对应非零候选解的正确扩散速率。'],['Fo','观察时间 Fo',0,.2,.0025,.04,'比较当前时刻误差，不改变规定的初值。']],
  caption:'制造参考解 θ*=sin(πξ)e^(−π²Fo)，ξ∈[0,1]；θFo=θξξ，端点θ=0，规定初值sin(πξ)。候选 θ̂=c sin(πξ)e^(−kπ²Fo)。图中残差、初值误差和空间L²范数均由解析式计算，不是神经网络训练结果。零候选解 c=0 也满足PDE与边界，因此必须单独检查初值。',
  animation:{key:'Fo',from:0,to:.2,duration:10000,label:'播放候选与参考演化'},sources:heatSources,
  draw:v=>{const m=physicsState(v.amplitude,v.rate,v.Fo);return {svg:namedPlot('位置 ξ →；纵轴 θ。绿色参考，橙色虚线为候选。',plot([{fn:m.exact,color:C.green},{fn:m.candidate,color:C.orange,dash:true}],[0,1],[0,1.6]))+namedPlot('位置 ξ →；纵轴 PDE 残差 R=θ̂Fo−θ̂ξξ。',plot([{fn:m.residual,color:C.purple}],[0,1],[-13,13])),result:`当前PDE残差 ‖R‖₂=${m.residualNorm.toFixed(4)}；初值误差=${m.initialError.toFixed(4)}；边界误差=0；当前解误差=${m.solutionError.toFixed(4)}。${m.residualNorm<1e-12&&m.initialError>1e-8?'反例：PDE已满足，但初始条件不对。':''}`,legend:'分别检查方程、初值、边界；只盯一个损失项会漏掉约束。初值误差是Fo=0时的空间L²范数，不应随观察时间衰减。'};}
 },
 'data-split':{
  icon:'▦',title:'同一批实验，怎样拆分才公平',description:'每个方格是一条测量，同一行来自同一个run。比较混合拆分与整批留出后的误差。',
  controls:[['shift','run之间偏置的幅度',0,3,.1,1.5,'同一run共享偏置，测量点因此相关。'],['noise','固定点扰动的幅度',0,1,.05,.2,'固定扰动不是随机噪声分布的抽样。'],['seed','逐行切分方案编号',1,5,1,1,'固定种子、每run随机留出2点；结果可完全复现。']],
  caption:'确定性合成示例：6个run，每run6点，y=x+b_run+ε。模型已知基线x，只用训练数据估计各run的平均残差作为偏置；从未见过的run偏置设0。逐行切分每run留2点，按run切分完整留出run3与6；两者均24训练点/12测试点。目标是预测全新run。此结果不是实际实验性能，也不是对任何拆分策略都成立的误差定律。',
  animation:{key:'shift',from:0,to:3,duration:10000,label:'逐步增大批次差异'},
  draw:v=>{const m=splitStudy(v.shift,v.noise,v.seed),left=m.rowSplit,right=m.groupSplit;let grid='';
   for(const [s,offset,title] of [[left,24,'逐行随机'],[right,264,'按run隔离']]){const test=new Set(s.test.map(p=>p.id));grid+=`<text x="${offset+93}" y="23" text-anchor="middle">${title}</text>`;for(let run=0;run<6;run++){grid+=`<text x="${offset}" y="${57+run*28}" font-size="13">${run+1}</text>`;for(let j=0;j<6;j++){const held=test.has(run*6+j);grid+=`<rect x="${offset+20+j*27}" y="${39+run*28}" width="23" height="23" rx="3" fill="${held?C.orange:C.blue}"/><text x="${offset+31.5+j*27}" y="${55+run*28}" text-anchor="middle" fill="var(--paper)" font-size="13">${held?'验':'训'}</text>`;}}}
   grid+='<text x="240" y="237" text-anchor="middle" font-size="14">每行一个run；每格一个测量点</text>';
   const max=Math.max(.05,left.mse,right.mse)*1.2;
   return {svg:base(grid,'两种拆分的训练和测试成员，每行对应同一实验批次')+namedPlot('测试均方误差 MSE（响应单位²）；数值越小只说明对应测试任务更容易。',barDiagram([['逐行切分',left.mse,C.blue],['按run切分',right.mse,C.orange]],max,'',3)),result:`逐行测试 MSE=${left.mse.toFixed(5)}；新run测试 MSE=${right.mse.toFixed(5)}。逐行方案有6个run同时出现在训练与测试中；按run方案重叠为0。`,legend:'蓝格“训”：训练；橙格“验”：测试。同run的训练点透露了共享偏置。要评估新run，就应隔离run；若任务确实是在已知run内补测，逐行拆分回答的是另一问题。'};}
 }
});
function mapX(x,r){return 57+(x-r[0])/(r[1]-r[0])*386;}
function mapY(y,r){return 217-(y-r[0])/(r[1]-r[0])*194;}
let graphicSerial=0;
function escapeHTML(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));}
function base(s,label='根据当前参数计算的实验图形',height=260){
 const key='lab-graphic-'+(++graphicSerial);
 return `<svg viewBox="0 0 480 ${height}" class="lab-visual" role="img" aria-label="${escapeHTML(label)}"><title>${escapeHTML(label)}</title><defs><marker id="${key}-arrow" markerWidth="7" markerHeight="7" refX="6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="context-stroke"/></marker><clipPath id="${key}-clip"><rect x="56" y="22" width="388" height="196"/></clipPath></defs><g fill="currentColor" font-family="sans-serif" font-size="16">${s.replaceAll('url(#arrow)',`url(#${key}-arrow)`).replaceAll('url(#plot-clip)',`url(#${key}-clip)`)}</g></svg>`;
}
function fmt(n){if(Math.abs(n)<1e-8)return'0';return Math.abs(n)>=100?String(Math.round(n)):String(Number(n.toFixed(2)));}
function plot(curves,xr,yr,pts=[],extra=''){let s='';for(let i=0;i<=4;i++){const x=xr[0]+(xr[1]-xr[0])*i/4,y=yr[0]+(yr[1]-yr[0])*i/4,px=mapX(x,xr),py=mapY(y,yr);s+=`<path d="M${px} 23V217M57 ${py}H443" stroke="currentColor" opacity=".08"/><text x="${px}" y="246" text-anchor="middle">${fmt(x)}</text><text x="47" y="${py+5}" text-anchor="end">${fmt(y)}</text>`;}s+='<path d="M57 23V217H443" fill="none" stroke="currentColor" opacity=".4"/>';s+='<g clip-path="url(#plot-clip)">'+extra;curves.forEach(c=>{let d='';for(let i=0;i<=200;i++){const x=xr[0]+(xr[1]-xr[0])*i/200,y=c.fn(x);if(Number.isFinite(y))d+=(i?'L':'M')+mapX(x,xr).toFixed(2)+' '+mapY(y,yr).toFixed(2);}s+=`<path d="${d}" fill="none" stroke="${c.color}" stroke-width="2.6" ${c.dash?'stroke-dasharray="6 4"':''}/>`;});pts.forEach(p=>s+=`<circle cx="${mapX(p.x,xr)}" cy="${mapY(p.y,yr)}" r="4.5" fill="var(--blue)" stroke="var(--paper)" stroke-width="1.3"/>`);return base(s+'</g>');}
function barDiagram(rows,max,unit,precision=0){return base(rows.map(([label,n,color],i)=>`<text x="24" y="${36+i*75}">${label}</text><rect x="130" y="${15+i*75}" width="${n/max*215}" height="31" fill="${color}" rx="4"/><text x="355" y="${36+i*75}">${n.toFixed(precision)} ${unit}</text>`).join(''));}
function namedPlot(label,svg){return svg.replace('aria-label="根据当前参数计算的实验图形"',`aria-label="${escapeHTML(label)}"`).replace('<title>根据当前参数计算的实验图形</title>',`<title>${escapeHTML(label)}</title>`)+`<p class="lab-chart-label">${escapeHTML(label)}</p>`;}
function band(predict,key,xr,yr,color,opacity){const upper=[],lower=[];for(let i=0;i<=120;i++){const x=xr[0]+(xr[1]-xr[0])*i/120,p=predict(x),sd=1.96*Math.sqrt(p[key]);upper.push([mapX(x,xr),mapY(p.mean+sd,yr)]);lower.push([mapX(x,xr),mapY(p.mean-sd,yr)]);}return `<path d="M${upper.concat(lower.reverse()).map(p=>p.map(n=>n.toFixed(3)).join(' ')).join('L')}Z" fill="${color}" fill-opacity="${opacity}"/>`;}
// Square plot: identical pixels per coordinate unit preserve angles and areas.
function geometry(range,draw,label){
 const x=n=>57+(n-range[0])/(range[1]-range[0])*386,y=n=>409-(n-range[0])/(range[1]-range[0])*386;
 let s='';for(let n=Math.ceil(range[0]);n<=Math.floor(range[1]);n++){s+=`<path d="M${x(n)} 23V409M57 ${y(n)}H443" stroke="currentColor" opacity="${n===0?.35:.08}"/>`;if(n!==0)s+=`<text x="${x(n)}" y="431" text-anchor="middle">${n}</text><text x="47" y="${y(n)+5}" text-anchor="end">${n}</text>`;}
 return base(s+draw(x,y),label,450);
}
LABS.matrix.draw=v=>{const det=v.a*v.d-v.b*v.c;return {svg:geometry([-4.5,4.5],(x,y)=>{
 const polygon=points=>points.map(p=>`${x(p[0])},${y(p[1])}`).join(' ');
 return `<polygon points="${polygon([[0,0],[1,0],[1,1],[0,1]])}" fill="none" stroke="var(--muted)" stroke-dasharray="4 4"/><polygon points="${polygon([[0,0],[v.a,v.c],[v.a+v.b,v.c+v.d],[v.b,v.d]])}" fill="var(--accent)" fill-opacity=".17" stroke="var(--accent)" stroke-width="2"/><path d="M${x(0)} ${y(0)}L${x(v.a)} ${y(v.c)}" stroke="var(--blue)" stroke-width="4" marker-end="url(#arrow)"/><path d="M${x(0)} ${y(0)}L${x(v.b)} ${y(v.d)}" stroke="#bd7148" stroke-width="4" marker-end="url(#arrow)"/>`;
 },'等比例坐标中的单位正方形、变换后平行四边形与两个基向量'),result:`det(A) = ${det.toFixed(3)}　·　面积倍率 |det(A)| = ${Math.abs(det).toFixed(3)}。${Math.abs(det)<1e-8?'矩阵奇异：平面被压到线或点。':det<0?'变换反转了方向。':'变换保持方向。'}`,legend:'横、纵轴每个单位等长。蓝箭头：第一列；橙箭头：第二列；灰虚线：原单位正方形。两个像向量共线时面积为零。'};};
LABS.gradient.draw=v=>({svg:geometry([-3.4,3.4],(x,y)=>{
 let s='';const scale=386/6.8;for(const k of [.5,1,2,4,6,8])s+=`<ellipse cx="${x(0)}" cy="${y(0)}" rx="${Math.sqrt(k)*scale}" ry="${Math.sqrt(k/2)*scale}" fill="none" stroke="var(--accent)" opacity=".4"/>`;
 s+=`<circle cx="${x(v.x)}" cy="${y(v.y)}" r="4.5" fill="var(--blue)"/>`;if(v.x!==0||v.y!==0)s+=`<path d="M${x(v.x)} ${y(v.y)}L${x(v.x+.12*2*v.x)} ${y(v.y+.12*4*v.y)}" stroke="var(--blue)" stroke-width="3" marker-end="url(#arrow)"/>`;return s;
 },'等比例坐标中的椭圆等高线及与局部切线垂直的梯度'),result:`f = ${(v.x*v.x+2*v.y*v.y).toFixed(2)}　·　梯度 = (${(2*v.x).toFixed(2)}, ${(4*v.y).toFixed(2)})。在原点梯度为零。`,legend:'横、纵轴每个单位等长。绿色椭圆为等高线；蓝箭头为0.12倍梯度，可直接观察垂直关系。原点无非零最陡上升方向。'});

function guide(question,answer,steps){return {question,answer,steps:steps.map(([title,body,formula,preset])=>({title,body,formula,preset}))};}
const GUIDES={
 'python-loop':guide('做完两次迭代，total 是5还是9？','是5：第一次加1²，第二次加2²；total保留之前的累积值。',[
  ['看清一个元素','列表的第一项赋给x，累计量起初为0。','total ← 0 + 1²',{step:1}],['追踪累计量','第二轮增加4，而不是把累计量替换为4。','total ← 1 + 2² = 5',{step:2}],['核对循环结束','四次更新都执行后，总和是30；x仍保留最后的4。','Σ x² = 1 + 4 + 9 + 16',{step:4}]]),
 derivative:guide('固定x后，把h缩小10倍，割线斜率误差会怎样？','本例误差恰好是h，所以也缩小10倍；一般函数不一定有这个精确比例。',[
  ['看两点的差','蓝虚线穿过x与x+h两点，代表一段区间的平均变化率。','[f(x+h)−f(x)]/h = 2x+h',{x:.7,h:1}],['把间距缩小','函数曲线与橙切线不动，割线转向切线。','割线斜率 − 切线斜率 = h',{x:.7,h:.1}],['说出极限','只有取极限才得到导数；不能先令分母h=0。','lim(h→0) (2x+h) = 2x',{x:.7,h:.01}]]),
 integral:guide('增加中点矩形数，本例是从上方还是下方逼近？','x²是凸函数，等宽中点法在本例低估积分；其他函数不一定低估。',[
  ['一根柱代表一小段','每段宽2/n，高取中点处的x²；先看面积怎样累加。','Mₙ = Σ f(xᵢ*) Δx，Δx=2/n',{n:4}],['比较加密前后','把n翻倍，中点法误差在本例变为原来的四分之一。','8/3 − Mₙ = 2/(3n²)',{n:8}],['区分近似与极限','许多很窄的矩形看起来贴近曲线；精确值来自极限。','lim(n→∞) Mₙ = ∫₀²x²dx = 8/3',{n:60}]]),
 matrix:guide('两列相同，正方形会变成什么？','若相同的两列非零，正方形压成一条线段；若两列都为零，则压成一个点。两种情况的行列式均为0。',[
  ['跟踪两个方向','先从单位矩阵开始，蓝、橙箭头就是两个坐标方向。','Ae₁=(a,c)，Ae₂=(b,d)',{a:1,b:0,c:0,d:1}],['观察面积','让第二列向右倾斜，面积仍为1；面积与外形是不同信息。','det(A)=ad−bc',{a:1,b:1,c:0,d:1}],['检查退化','两列共线时，不再能区分原平面所有方向。','rank(A)<2 ⇔ det(A)=0',{a:1,b:2,c:1,d:2}]]),
 gradient:guide('在(1,1)处，最陡方向指向(1,1)还是(2,4)？','梯度是(2,4)。y项曲率较大，不能只看点到原点的方向。',[
  ['先读等高线','沿同一条椭圆移动，函数值不变。','x²+2y²=常数',{x:1,y:1}],['从变化率找方向','沿单位方向u的变化率是梯度与u的内积。','Dᵤf = ∇f·u；∇f=(2x,4y)',{x:1,y:1}],['检查零梯度','原点梯度为零，所有一阶方向导数都为0。','∇f(0,0)=(0,0)',{x:0,y:0}]]),
 carnot:guide('热源都升高100 K、温差保持不变，卡诺效率会不变吗？','不会；效率取决于绝对温度的比值，固定温差下同时升温会降低该上限。',[
  ['先核对能量账','输入1000 J，一部分作功，其余必须排给低温热源。','Qₕ=W+Q𝚌',{hot:600,cold:300}],['看温度比','把两端都升高100 K，效率由50%变为约42.9%。','η=1−T𝚌/Tₕ',{hot:700,cold:400}],['说出适用条件','这是两恒温热源间可逆循环的上限，不是实际机器的效率预测。','η实际 ≤ η卡诺',{hot:900,cold:300}]]),
 conduction:guide('固定两面温度与厚度，把k加倍，图中的温度斜率会加倍吗？','不会；温度斜率不变，热流密度加倍。温度分布与热流不是同一个量。',[
  ['读温度直线','左热右冷，温度梯度为负，向右热流为正。','q″=−k dT/dx',{k:1,L:.1,hot:100,cold:20}],['改变材料','相同温差和厚度，增加k使热流更大。','q″=k(T左−T右)/L',{k:2,L:.1,hot:100,cold:20}],['增加传热距离','厚度加倍会把热流减半；横轴范围也随厚度变化。','R″=L/k',{k:2,L:.2,hot:100,cold:20}]]),
 cooling:guide('经过一个时间常数后，温度还剩初温的1/e吗？','剩下的是相对环境的温差，不是摄氏温度本身。',[
  ['从初始状态出发','初温100°C，环境20°C，驱动冷却的温差是80 K。','θ=(T−T∞)/(T₀−T∞)',{h:25,t:0}],['观察一个时间常数','本组参数τ=200 s，此时温差剩80/e。','θ(τ)=e⁻¹',{h:25,t:200}],['增大换热能力','增大h缩短时间常数；本演示的Bi仍在集总近似范围内。','τ=mc/(hA)',{h:50,t:200}]]),
 bernoulli:guide('出口面积减半，流速是否只增加一半？','不可压稳态流的流量不变，面积减半使速度加倍。',[
  ['先用质量守恒','同一流管内入口出口体积流量相同。','A₁v₁=A₂v₂',{ratio:1,v:2}],['再看压力交换','水平无损模型中，速度增大对应静压降低。','p₁−p₂=ρ(v₂²−v₁²)/2',{ratio:.5,v:2}],['检查扩张方向','出口变宽时模型预测静压回升；实际还要扣除损失。','p₂>p₁，当v₂<v₁',{ratio:1.5,v:2}]]),
 regression:guide('只把训练MSE降到很小，就能证明对新实验预测准确吗？','不能。训练误差与独立验证误差回答不同问题，数据划分方式也很关键。',[
  ['看点与线的距离','橙虚线表示同一个x处预测值与观测值之差。','eᵢ=wxᵢ+b−yᵢ',{m:1,b:0}],['补偿截距','先平移整条线，让它靠近点群。','MSE=(1/n)Σeᵢ²',{m:1,b:1}],['分清拟合与预测','保持拟合结果，在另一批数据检验才涉及泛化。','训练集用于拟合；独立测试集用于评估',{m:1,b:1}]]),
 'gradient-descent':guide('学习率越大，一定越快到达最小点吗？','不一定。本例α>1通常发散；“更大一步”可能越过最低点越来越远。',[
  ['顺着负梯度走','J=w²的导数为2w，每步向其反方向移动。','wₖ₊₁=wₖ−α·2wₖ',{rate:.3,start:2.5,steps:5}],['看振荡但收敛','α=0.8时每步变号，但绝对值乘0.6。','|1−2α|<1 ⇒ wₖ→0',{rate:.8,start:2.5,steps:8}],['找到失稳原因','α=1.15时绝对值每步乘1.3，离最低点越来越远。','|1−2α|>1',{rate:1.15,start:2.5,steps:10}]]),
 'heat-modes':guide('哪条波会先变得看不见：一大拱还是三个小拱？','第三模态衰减最快：衰减指数中的频率要平方，所以它的速率是第一模态的9倍。',[
  ['只留一个形状','两端为零的正弦形状保持不变，随时间只缩小幅值。','θ₁=0.65 sin(πξ)e^(−π²Fo)',{b:0,c:0,Fo:0}],['把三条波相加','先在同一位置相加纵坐标，得到绿色温度曲线；不是把三条波首尾连接。','θ=Σₙ₌₁³ aₙ sin(nπξ)e^(−n²π²Fo)',{b:.12,c:.18,Fo:0}],['放走细小起伏','固定初始系数，播放时间；第三模态很快消失，第一模态留下更久。','衰减速率比：1∶4∶9',{b:.12,c:.18,Fo:.06}],['核对热量与平方泛函','边界允许散热。积分热方程得热量收支；分部积分得E严格衰减。','dH/dFo=θξ(1)−θξ(0)；dE/dFo=−2∫₀¹θξ²dξ',{b:.12,c:.18,Fo:.12}]]),
 'cooling-inverse':guide('刚开始测量的温度一样，能不能仅凭t=0的数据确定h？','不能。所有候选h都有相同的已知初温；需要后续时刻的温度变化。',[
  ['先看拟合偏快还是偏慢','h太大时模型降温过快，许多数据点落在曲线上方。','T(t;h)=20+60e^(−hAt/(mc))',{h:30,noise:0,probe:1000}],['让数据决定h','无扰动时把h调至18，所有点与模型一致，SSE为0。','SSE(h)=Σ[T(tᵢ;h)−yᵢ]²',{h:18,noise:0,probe:1000}],['读灵敏度','在t=0处灵敏度为0；到适当时刻才更容易区分邻近h。','∂T/∂h=−(At/mc)(T₀−T∞)e^(−hAt/mc)',{h:18,noise:0,probe:0}],['允许数据不完美','加固定扰动后，最佳拟合通常不再穿过每个点；低SSE也需模型假设支持。','已知mc与A时才能在本例单独辨识h',{h:18,noise:2,probe:1000}]]),
 'experiment-design':guide('为什么不是越晚测温，信息越多？','很晚时各候选曲线都接近环境温度，参数的微小变化几乎不再影响读数。',[
  ['初始时刻没有区分能力','已知初温与h无关，t=0的温度对h没有灵敏度。','∂T(0;h)/∂h=0',{u:0,sigma:1,repeats:3}],['选择最敏感的时刻','令u=t/τ，平方灵敏度与u²e^(−2u)成正比，导数在u=1由正变负。','d[u²e^(−2u)]/du=2u(1−u)e^(−2u)',{u:1,sigma:1,repeats:3}],['过晚会失去信息','温度越来越稳定，同时h也越来越难从测量中分辨。','I(t)/I(τ)=u²e^(2−2u)',{u:6,sigma:1,repeats:3}],['用独立重复降低不确定性','理想独立重复使信息乘N、下界除以√N；相关重复不满足此结论。','I=N(∂T/∂h)²/σ²',{u:1,sigma:1,repeats:9}]]),
 'uncertainty-band':guide('新观测的预测带能比函数均值的后验带更窄吗？','在本模型中不能：新观测额外带有独立噪声，方差增加σ²。',[
  ['先区分线与测量','绿色是后验均值函数；蓝色带描述w仍不确定造成的函数值变化。','φ=(1,x)ᵀ；Var[f(x)|D]=φᵀΣφ',{count:2,sigma:.3,x:0}],['加入观测噪声','下一次读数还会随机波动，橙色带因此更宽。','Var[y新|D]=φᵀΣφ+σ²',{count:5,sigma:.6,x:0}],['走到数据之外','斜率不确定性被x放大，外推带变宽；这没有计入线性模型本身可能错误。','Σ=(¼I+XᵀX/σ²)⁻¹',{count:5,sigma:.3,x:3}],['核对概率的条件','95%依赖先验、线性关系和噪声假设；不是外推安全保证。','μ=ΣXᵀy/σ²；逐点区间=φᵀμ±1.96√方差',{count:5,sigma:.3,x:1}]]),
 'physics-residual':guide('把参考解整体乘0.6，热方程还成立吗？初值呢？','线性齐次热方程仍成立，端点也仍为0；但初值从sin(πξ)变成0.6sin(πξ)，所以不是所求解。',[
  ['先确认一个已知答案','参考解满足方程、初值和边界三个部分。','θ*=sin(πξ)e^(−π²Fo)',{amplitude:1,rate:1,Fo:.04}],['制造会骗人的候选','只缩小幅值，PDE残差仍为0；初值误差不会消失。','R=(1−k)π²θ̂；当k=1，R=0',{amplitude:.6,rate:1,Fo:.04}],['检查全零捷径','全零解也让PDE与边界残差为0，但丢失了全部初始温度形状。','‖θ̂(·,0)−sin(πξ)‖₂=|c−1|/√2',{amplitude:0,rate:1,Fo:.04}],['再故意改错衰减率','此时初值正确而PDE错误。三类约束必须分别监测。','k≠1且c≠0 ⇒ R通常不为0',{amplitude:1,rate:.5,Fo:.04}]]),
 'data-split':guide('同一run的部分点进训练、其余点进测试，能评估全新run吗？','通常不能。在这个例子中，训练点透露了测试点共享的批次偏置，使逐行测试显得容易。',[
  ['先辨认独立单位','同一行共享b_run，六个点不是六次完全独立实验。','yᵣⱼ=xᵣⱼ+bᵣ+εᵣⱼ',{shift:0,noise:.2,seed:1}],['让批次差异显现','增加run间偏置，逐行训练仍能估计每个已见run的偏置。','已见run：b̂ᵣ=训练残差的均值',{shift:1.5,noise:.2,seed:1}],['隔离整个run','右图run3与6全部留出，预测器不能偷用这些run的观测估计偏置。','新run：本演示设b̂ᵣ=0',{shift:1.5,noise:.2,seed:2}],['把评估问题说准确','新run测试难并不证明所有模型都差；应改进能解释批次差异的特征，再做独立验证。','划分单位须与部署时的新数据单位一致',{shift:3,noise:.2,seed:3}]])
};
const OLD_ANIMATIONS={
 'python-loop':['step',0,4,8000,'逐步执行循环'],derivative:['h',1,.01,9000,'让割线靠近切线'],integral:['n',2,60,9000,'逐步加密分割'],matrix:['b',0,2,9000,'改变第二列的横坐标'],gradient:['x',-2,2,9000,'移动观察点'],carnot:['hot',450,1200,10000,'逐步升高热源温度'],conduction:['L',.02,.5,10000,'逐步增加墙厚'],cooling:['t',0,600,12000,'播放冷却过程'],bernoulli:['ratio',1.6,.3,10000,'逐步缩小出口'],regression:['b',0,2,9000,'上下移动拟合直线'],'gradient-descent':['steps',0,14,10000,'逐步迭代']
};
for(const [id,spec] of Object.entries(LABS)){spec.guide=GUIDES[id];if(OLD_ANIMATIONS[id]){const [key,from,to,duration,label]=OLD_ANIMATIONS[id];spec.animation={key,from,to,duration,label};}}
const mountedLabs=new WeakMap();let mountSerial=0;
function mountLab(el,id){
 if(typeof id!=='string'||!Object.prototype.hasOwnProperty.call(LABS,id))return;
 mountedLabs.get(el)?.();
 const spec=LABS[id],guide=spec.guide,values=Object.fromEntries(spec.controls.map(c=>[c[0],c[5]])),prefix='lab-control-'+(++mountSerial),doc=el.ownerDocument;
 let step=0,frame=null,playing=false,disposed=false,animationStart=null,animationFrom=0,lastDraw=null,observer;
 const raf=root.requestAnimationFrame?.bind(root)|| (fn=>root.setTimeout(()=>fn(Date.now()),32));
 const cancel=root.cancelAnimationFrame?.bind(root)||root.clearTimeout.bind(root);
 el.classList.add('research-lab');
 el.innerHTML=`<div class="eyebrow">INTERACTIVE · 动手试一试</div><h2>${spec.title}</h2><p>${spec.description}</p><details class="lab-prediction"><summary>先预测：${guide.question}</summary><p>${guide.answer}</p></details><div class="lab-chart"></div><div class="lab-controls">${spec.controls.map(c=>`<label for="${prefix}-${c[0]}"><span>${c[1]}</span><output data-value="${c[0]}" for="${prefix}-${c[0]}"></output><input id="${prefix}-${c[0]}" aria-label="${c[1]}" ${c[6]?`aria-describedby="${prefix}-${c[0]}-hint"`:''} data-param="${c[0]}" type="range" min="${c[2]}" max="${c[3]}" step="${c[4]}" value="${c[5]}">${c[6]?`<small id="${prefix}-${c[0]}-hint">${c[6]}</small>`:''}</label>`).join('')}</div><div class="lab-transport"><button type="button" class="secondary lab-play" aria-pressed="false">▶ ${spec.animation.label}</button><button type="button" class="secondary lab-reset">重置参数</button><span class="lab-play-state">手动播放；拖动控件即可暂停。</span></div><div class="lab-result" aria-live="polite" aria-atomic="true"></div><p class="lab-caption lab-legend"></p><section class="lab-story" aria-label="分步讲解"><div class="lab-step-header"><span class="lab-step-count" aria-live="polite" aria-atomic="true"></span><div><button type="button" class="secondary lab-prev" aria-label="上一步讲解">←</button><button type="button" class="secondary lab-next" aria-label="下一步讲解">→</button></div></div><h3 class="lab-step-title"></h3><p class="lab-step-body"></p><p class="lab-formula"></p><button type="button" class="secondary lab-preset">应用这一步的示例参数</button></section><p class="lab-caption lab-assumptions"><b>假设与适用范围：</b>${spec.caption}</p>${spec.sources?`<details class="lab-sources"><summary>教学参考与公式出处</summary><p>图形、数据和交互为本教材独立实现；参考讲解顺序，不复用原动画。外部参考需联网，本实验可离线运行。</p><ul>${spec.sources.map(([name,url])=>`<li><a href="${url}" target="_blank" rel="noopener noreferrer">${name}</a></li>`).join('')}</ul></details>`:''}`;
 const $=s=>el.querySelector(s),resultEl=$('.lab-result'),playButton=$('.lab-play'),playState=$('.lab-play-state');
 function update(){
  const result=spec.draw(values);$('.lab-chart').innerHTML=result.svg;resultEl.textContent=result.result;$('.lab-legend').textContent=result.legend;
  spec.controls.forEach(c=>{const digits=(String(c[4]).split('.')[1]||'').length;const shown=Number(values[c[0]].toFixed(digits));$(`[data-value="${c[0]}"]`).textContent=String(shown);const input=$(`[data-param="${c[0]}"]`);input.value=String(values[c[0]]);input.setAttribute('aria-valuetext',String(shown));});
 }
 function showStep(){const s=guide.steps[step];$('.lab-step-count').textContent=`步骤 ${step+1} / ${guide.steps.length}`;$('.lab-step-title').textContent=s.title;$('.lab-step-body').textContent=s.body;$('.lab-formula').textContent=s.formula;$('.lab-prev').disabled=step===0;$('.lab-next').disabled=step===guide.steps.length-1;}
 function stop(message='已暂停，可继续调节参数。'){playing=false;if(frame!==null)cancel(frame);frame=null;playButton.textContent='▶ '+spec.animation.label;playButton.setAttribute('aria-pressed','false');resultEl.setAttribute('aria-live','polite');playState.textContent=message;}
 function normalized(c,value){const n=Number(value);return Number.isFinite(n)?Math.max(c[2],Math.min(c[3],c[2]+Math.round((n-c[2])/c[4])*c[4])):c[5];}
 function tick(now){
  if(!playing||disposed)return;if(!el.isConnected||doc.hidden){stop('页面离开，播放已暂停。');return;}
  if(animationStart===null)animationStart=now;
  const a=spec.animation,c=spec.controls.find(c=>c[0]===a.key),fraction=Math.min(1,(now-animationStart)/a.duration);
  if(lastDraw===null||now-lastDraw>=50||fraction>=1){values[a.key]=normalized(c,animationFrom+(a.to-animationFrom)*fraction);update();lastDraw=now;}
  if(fraction>=1){stop('播放结束。再次播放将从起点开始。');return;}frame=raf(tick);
 }
 playButton.onclick=()=>{
  if(playing){stop();return;}const a=spec.animation;animationFrom=values[a.key];
  if((a.to>=a.from&&animationFrom>=a.to)||(a.to<a.from&&animationFrom<=a.to)){animationFrom=a.from;values[a.key]=a.from;update();}
  animationStart=null;lastDraw=null;playing=true;resultEl.setAttribute('aria-live','off');playButton.textContent='Ⅱ 暂停';playButton.setAttribute('aria-pressed','true');playState.textContent='正在播放；可随时暂停或逐步拖动。';frame=raf(tick);
 };
 el.querySelectorAll('[data-param]').forEach(input=>input.addEventListener('input',()=>{stop();const c=spec.controls.find(c=>c[0]===input.dataset.param);values[c[0]]=normalized(c,input.value);update();}));
 $('.lab-reset').onclick=()=>{stop('已恢复初始参数。');spec.controls.forEach(c=>values[c[0]]=c[5]);step=0;showStep();update();};
 $('.lab-prev').onclick=()=>{step=Math.max(0,step-1);showStep();};$('.lab-next').onclick=()=>{step=Math.min(guide.steps.length-1,step+1);showStep();};
 $('.lab-preset').onclick=()=>{stop('已应用当前步骤的示例参数。');const preset=guide.steps[step].preset;for(const c of spec.controls)if(Object.prototype.hasOwnProperty.call(preset,c[0]))values[c[0]]=normalized(c,preset[c[0]]);update();};
 function onVisibility(){if(doc.hidden&&playing)stop('页面不可见，播放已暂停。');}
 function dispose(){stop('实验已离开页面。');disposed=true;observer?.disconnect();doc.removeEventListener('visibilitychange',onVisibility);mountedLabs.delete(el);}
 doc.addEventListener('visibilitychange',onVisibility);
 if(root.MutationObserver&&doc.documentElement){observer=new root.MutationObserver(()=>{if(!el.isConnected)dispose();});observer.observe(doc.documentElement,{childList:true,subtree:true});}
 mountedLabs.set(el,dispose);showStep();update();
 if(root.matchMedia?.('(prefers-reduced-motion: reduce)').matches)playState.textContent='已遵循减少动态效果偏好：默认静止，也可手动逐步调节。';
 return dispose;
}
root.LABS=LABS;root.mountLab=mountLab;
root.LAB_MATH=LAB_MATH;
if(typeof module!=='undefined')module.exports={LABS,LAB_MATH,mountLab};
})(typeof window==='undefined'?globalThis:window);
