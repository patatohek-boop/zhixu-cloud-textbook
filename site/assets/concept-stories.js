/* Original, offline concept explanations. No third-party animation assets/runtime.
 * Contract: render(lessonId|storyId) -> markup; mount(section,id?) -> dispose().
 * The player never writes learning records, notes, URLs, or global key handlers.
 */
(function(root){
'use strict';
const foundation=root.FOUNDATION_MATH||(typeof require==='function'?require('./foundation-labs.js').FOUNDATION_MATH:null);
const C={a:'var(--accent)',b:'var(--blue)',o:'var(--story-orange)',p:'var(--story-purple)'};
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const fmt=(n,d=2)=>Number(n.toFixed(d)).toString();
function bounded(n,max){return Number.isFinite(Number(n))?Math.max(0,Math.min(max,Number(n))):0;}
function sample(values,position){const p=bounded(position,values.length-1),i=Math.floor(p),f=p-i;return values[i]+((values[i+1]??values[i])-values[i])*f;}
function stageOf(p,n){return Math.floor(bounded(p,n-1));}
const text=(x,y,s,anchor='start',size=18)=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}">${esc(s)}</text>`;
const line=(x1,y1,x2,y2,color='currentColor',extra='')=>`<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="2.5" ${extra}/>`;
function svg(body,label,height=280){return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 280 ${height}" role="img" aria-label="${esc(label)}"><title>${esc(label)}</title><g fill="currentColor" font-family="sans-serif" font-size="18">${body}</g></svg>`;}
function curve(fn,x0,x1,X,Y,n=60){return Array.from({length:n+1},(_,i)=>{const x=x0+(x1-x0)*i/n;return (i?'L':'M')+X(x)+','+Y(fn(x));}).join('');}
function metric(label,value){return `<div><dt>${esc(label)}</dt><dd>${esc(value)}</dd></div>`;}
function view(graph,metrics,note){return {graph,metrics:metrics.map(([k,v])=>metric(k,v)).join(''),note};}
const STEP_MS=6800,DWELL_MS=5000;
function snapPosition(p){const nearest=Math.round(p);return Math.abs(p-nearest)<1e-8?nearest:p;}
function phaseForPosition(position){const p=snapPosition(position),i=Math.floor(p),f=p-i;return i+(f>0?DWELL_MS/STEP_MS+(1-DWELL_MS/STEP_MS)*f:0);}
function playbackPosition(startPosition,elapsed,max,discrete=false){const phase=phaseForPosition(startPosition)+Math.max(0,elapsed)/STEP_MS,i=Math.floor(phase),f=phase-i,hold=DWELL_MS/STEP_MS;return bounded(discrete?i:snapPosition(i+Math.max(0,(f-hold)/(1-hold))),max);}

// The quantities below describe a gradually revealed ACCOUNT, not a transient.
function energyState(position){const p=bounded(position,4),workIn=sample([0,6,6,6,6],p),heatOut=sample([0,0,1.2,1.2,1.2],p),m=foundation.energyAccount(-heatOut,-workIn,0);return {...m,workIn,heatOut};}
function wallState(position){const p=bounded(position,4),k2=sample([.05,.05,.05,.1,.1],p),A=.5,L1=.01,L2=.02,k1=.2,R1=L1/(k1*A),R2=L2/(k2*A),rate=40/(R1+R2),drop1=rate*R1,drop2=rate*R2;return {A,L1,L2,k1,k2,R1,R2,rate,drop1,drop2,interfaceT:60-drop1};}
const coolingConstants=Object.freeze({r:.005,rho:7800,c:500,k:15,h:30,T0:80,Tinf:20});
function coolingState(position){const c=coolingConstants,tau=c.rho*c.c*c.r/(3*c.h),t=sample([0,.5,1,2,3],bounded(position,4))*tau,ratio=Math.exp(-t/tau),T=c.Tinf+(c.T0-c.Tinf)*ratio,V=4*Math.PI*c.r**3/3,A=4*Math.PI*c.r**2,capacity=c.rho*V*c.c,heatLeft=capacity*(T-c.Tinf),heatRemoved=capacity*(c.T0-T);return {...c,tau,t,ratio,T,V,A,capacity,heatLeft,heatRemoved,Bi:c.h*c.r/(3*c.k)};}
function massState(position){const t=sample([0,60,120,180,240,300],bounded(position,5)),m=foundation.massBalance(20,6/60,2/60,t);return {...m,height:m.mass/(1000*.2),rise:(m.mass-20)/(1000*.2),volumeLitres:m.mass};}
const training=Object.freeze([{x:1,y:2},{x:2,y:3},{x:3,y:5}].map(Object.freeze));
function regressionState(position){const p=bounded(position,4),w=sample([0,0,1.5,1.5,1.5],p),b=sample([0,10/3,1/3,1/3,1/3],p),residuals=training.map(d=>d.y-(w*d.x+b)),mse=residuals.reduce((s,r)=>s+r*r,0)/3;return {w,b,residuals,mse,residualSum:residuals.reduce((s,r)=>s+r,0),showModel:p>0,showNew:p>=4,newPrediction:4*w+b,newResidual:4-(4*w+b)};}
const pythonCode=['values = [18, 20, 22]','total = 0','count = 0','for value in values:','    if value >= 20:','        total = total + value','        count = count + 1','if count > 0:','    print(total / count)','else:','    print("没有达标读数")'];
const pythonFrames=[
 [3,null,0,0,null,'初始化完成','列表已准备好；total 与 count 都为 0。下一步才从列表取值。','尚未进入循环'],
 [4,18,0,0,null,'取出第一项','for 把 18 赋给 value；取值本身不会改动累计量。','value ← 18'],
 [5,18,0,0,null,'条件为假，跳过更新','18 < 20，所以两条缩进更深的更新都不执行。','18 ≥ 20 → False'],
 [4,20,0,0,null,'取出第二项','上一轮没有更新。现在 value 变为 20，累计量仍为 0。','value ← 20'],
 [5,20,0,0,null,'条件为真，进入分支','20 达到门槛。先更新 total，再更新 count。','20 ≥ 20 → True'],
 [6,20,20,0,null,'先更新总和','这一条赋值已经执行，计数那一条还没执行；这是语句之间的状态。','total ← 0 + 20 = 20'],
 [7,20,20,1,null,'再更新计数','第二轮结束：已处理的达标读数有 1 个，总和为 20。','count ← 0 + 1 = 1'],
 [4,22,20,1,null,'取出第三项','旧的累计量保留，只有 value 先换成 22。','value ← 22'],
 [5,22,20,1,null,'再次判断','22 达到门槛，接下来按顺序执行两条更新。','22 ≥ 20 → True'],
 [6,22,42,1,null,'把 22 加到总和','旧 total 是 20；不是把 total 直接替换成 22。','total ← 20 + 22 = 42'],
 [7,22,42,2,null,'第三轮结束','3 项都已处理；达标的 20、22 共 2 项，总和 42。','count ← 1 + 1 = 2'],
 [8,22,42,2,null,'循环后检查能否相除','列表取完，离开 for；count > 0 为真，才执行下一行。','2 > 0 → True'],
 [9,22,42,2,21,'输出达标平均值','输出 21.0。这个值是达标子集的平均，不是全部三项的平均。','42 / 2 = 21.0']
];
function pythonState(position){const index=Math.floor(bounded(position,pythonFrames.length-1)),[line,value,total,count,output,title,body,formula]=pythonFrames[index];return {index,line,value,total,count,output,title,body,formula};}
function step(title,body,formula){return {title,body,formula};}
const stories={
 'energy-account':{
  lessonId:'thermodynamics-05',title:'把输入、输出与储存对上账',kind:'讲解步骤',intro:'电加热送进 6 kJ，又向外散掉 1.2 kJ，里面多留下多少？先看方向，再逐项记账。',
  assumptions:'闭口系统；忽略整体动能、势能变化。取气体与电阻为系统，忽略电阻储能变化。热进入为正、系统向外作功为正。采用本节 20 s 工况的总量；播放顺序不表示先通电、后散热。',
  steps:[step('先定系统和正方向','刚性罐没有体积功，但电功仍可跨越边界。图中先从空账本开始。','ΔU = Q − W'),step('计入电功输入','本次过程输入电功 6.0 kJ，按本课约定 W = −6.0 kJ；内能账上记 −W。','−W = −(−6.0) = +6.0 kJ'),step('再扣除向外散热','同一过程中还散出 1.2 kJ。账本逐项显现，实际两种传递可以同时发生。','Q = −1.2 kJ'),step('核对留下多少','输入的能量一部分流出，剩余部分成为系统内能变化。','ΔU = −1.2 − (−6.0) = 4.8 kJ'),step('算温升，还要知道什么','守恒式先告诉我们内能增加了多少。要换算成温度升高多少，还需要气体质量、比热，以及适用的物性模型。','6.0 = 1.2 + 4.8 kJ')],state:energyState,
  draw:m=>{let b='<rect x="36" y="10" width="208" height="50" rx="8" fill="none" stroke="currentColor" stroke-dasharray="5 4"/>'+text(140,42,'气体＋电阻：闭口系统','middle',17);const bars=[['功输入 −W',m.workIn,C.b],['散热大小 −Q',m.heatOut,C.o],['内能变化 ΔU',m.delta,C.a]];bars.forEach(([name,value,color],i)=>{const y=88+i*64;b+=text(18,y,name,'start',17)+text(262,y,fmt(value)+' kJ','end',17)+`<rect x="18" y="${y+10}" width="244" height="16" rx="3" fill="currentColor" opacity=".08"/><rect x="18" y="${y+10}" width="${244*value/6}" height="16" rx="3" fill="${color}"/>`;});return view(svg(b,'能量账本：已计入功输入 '+fmt(m.workIn)+'，放热 '+fmt(m.heatOut)+'，内能变化 '+fmt(m.delta)+' 千焦',260),[['已计入 Q',fmt(m.q)+' kJ'],['已计入 W',fmt(m.w)+' kJ'],['账本 Q − W',fmt(m.delta)+' kJ']],'条长使用同一尺度：满格 6 kJ。显示的是已揭示的记账项，不是系统瞬时状态。');}
 },
 'wall-resistance':{
  lessonId:'heat-transfer-03',title:'温差怎样分给两层墙',kind:'讲解步骤',intro:'同样多的热每秒穿过两层墙，为什么保温层两端的温差更大？这里把“每秒传过多少热”叫热流率。',
  assumptions:'一维稳态、无内热源、常物性、理想接触，侧面绝热。两侧壁面为 60°C、20°C；导热面积 A=0.50 m²，第一层厚度 L₁=0.010 m，导热系数 k₁=0.20 W/(m·K)，第二层厚度 L₂=0.020 m。只改变第二层的导热系数 k₂；连续画面是一组稳态模型比较，不是墙的瞬态响应。',
  steps:[step('先读空间坐标','横轴是穿墙距离。先固定两端壁温，界面在 x = 0.010 m。','总温差 60 − 20 = 40 K'),step('相同的是热流率','k₂=0.050 时，R₂ 是 R₁ 的 8 倍，必须承担 8 倍温降。','R₁ = 0.10；R₂ = 0.80 K/W'),step('从左端重建界面温度','先算总热流，再减去第一层的温降；两段热流完全相同。','Q̇ = 40/0.90 = 44.44 W'),step('把第二层 k₂ 加倍','比较更易导热的墙：总阻减小，热流增加；第一层未变，却要承担更大的温降。','k₂：0.050 → 0.100 W/(m·K)'),step('核对新的稳态','现在两层温降为 8 K 和 32 K；比例为 1:4，不是各占一半。','Q̇ = 80 W；T界面 = 52°C')],state:wallState,
  draw:m=>{const X=x=>36+220*x/.03,Y=T=>206-145*(T-20)/40;let b=`<rect x="36" y="40" width="${220/3}" height="166" fill="${C.b}" opacity=".09"/><rect x="${X(.01)}" y="40" width="${440/3}" height="166" fill="${C.o}" opacity=".09"/>`;b+=line(36,206,260,206)+line(36,206,36,48)+line(X(.01),45,X(.01),206,'currentColor','stroke-dasharray="4 4" opacity=".3"');b+=`<polyline points="${X(0)},${Y(60)} ${X(.01)},${Y(m.interfaceT)} ${X(.03)},${Y(20)}" fill="none" stroke="${C.a}" stroke-width="3.5"/>`;[[0,60],[.01,m.interfaceT],[.03,20]].forEach(([x,T])=>b+=`<circle cx="${X(x)}" cy="${Y(T)}" r="4.5" fill="${C.a}"/>`);b+=text(17,27,'温度 / °C')+text(41,53,'60')+text(X(.01)+7,Y(m.interfaceT)-9,fmt(m.interfaceT), 'start',17)+text(256,196,'20','end')+text(36,230,'0','middle',16)+text(X(.01),230,'0.010','middle',16)+text(256,230,'0.030','end',16)+text(256,257,'位置 x / m','end',17);return view(svg(b,'稳态温度折线。界面 '+fmt(m.interfaceT)+' 摄氏度；同一热流率 '+fmt(m.rate)+' 瓦'),[['第一层温降',fmt(m.drop1)+' K'],['第二层温降',fmt(m.drop2)+' K'],['两层共同热流率',fmt(m.rate)+' W'],['当前 k₂',fmt(m.k2,3)+' W/(m·K)']],'横轴为真实厚度比例；界面左、右的温度连续。斜率变化由材料和热流共同决定。');}
 },
 'cooling-time':{
  lessonId:'heat-transfer-07',title:'冷却掉的是相对环境的温差',kind:'物理时间',intro:'小球起初是 80°C，房间始终是 20°C。过一会儿，它比房间还热多少？看球温与橙色温差线一起变化。',
  assumptions:'本节小球半径 r=5 mm；密度 ρ=7800 kg/m³，比热容 c=500 J/(kg·K)，导热系数 k=15 W/(m·K)，表面换热系数 h=30 W/(m²·K)。全表面对流、环境恒定 20°C、初温均匀 80°C，无内热源，忽略辐射、接触导热和物性变化。毕奥数 Bi=0.00333，采用集总近似；球内颜色均匀表示这一近似，不表示严格无温度梯度。',
  steps:[step('从 80°C 出发','初始温差是 60 K。环境线始终保持在 20°C。','τ = ρcr/(3h) = 216.7 s'),step('初期降得较快','初始温差大，对流散热率也大；温差条开始缩短。','T − 20 = 60 e^(−t/τ)'),step('经过一个时间常数','温差剩 60/e = 22.07 K，所以温度是 42.07°C。','T(τ) = 20 + 60/e'),step('越靠近环境，变化越慢','两倍时间常数后温差剩 e⁻²；降温速率持续减小。','dT/dt = −(T − 20)/τ'),step('靠近环境，不穿过去','三倍时间常数后约 22.99°C；模型只会渐近 20°C。','T(t) → 20°C，当 t → ∞')],state:coolingState,
  draw:m=>{const X=t=>38+220*t/(3*m.tau),Y=T=>232-136*(T-20)/60;let b=`<circle cx="49" cy="38" r="25" fill="hsl(${220-205*(m.T-20)/60} 58% 48%)" stroke="currentColor" stroke-width="1.5"/>`+text(91,32,'T = '+fmt(m.T)+'°C','start',21)+text(91,61,'温差 '+fmt(m.T-20)+' K','start',17);b+=text(38,82,'温度 / °C','start',16)+line(38,232,259,232,C.b,'stroke-dasharray="5 4"')+text(256,254,'环境 20°C','end',17)+line(38,232,38,90)+text(28,101,'80','end',16);b+=`<path d="${curve(t=>20+60*Math.exp(-t/m.tau),0,3*m.tau,X,Y)}" stroke="currentColor" opacity=".2" fill="none" stroke-width="2"/><path d="${curve(t=>20+60*Math.exp(-t/m.tau),0,m.t,X,Y)}" stroke="${C.a}" fill="none" stroke-width="3.5"/>`+line(X(m.t),232,X(m.t),Y(m.T),C.o)+`<circle cx="${X(m.t)}" cy="${Y(m.T)}" r="5" fill="${C.a}"/>`;b+=text(38,276,'0','middle',16)+text(X(m.tau),276,'τ','middle',16)+text(X(2*m.tau),276,'2τ','middle',16)+text(X(3*m.tau),276,'3τ','end',16)+text(140,302,'时间（τ = 216.7 s）','middle',17);return view(svg(b,'球温 '+fmt(m.T)+' 摄氏度，时间 '+fmt(m.t,1)+' 秒；温差比 '+fmt(m.ratio,3),318),[['模型物理时间',fmt(m.t,1)+' s'],['剩余温差比',fmt(m.ratio,3)],['降到环境温度前还会放出的能量',fmt(m.heatLeft)+' J'],['累计散出热量',fmt(m.heatRemoved)+' J']],'圆形是球体示意，非长度比例图；橙线表示此时温差。颜色只辅助区分温度，数值才是读数。');}
 },
 'control-volume':{
  lessonId:'fluid-mechanics-07',title:'流进减流出，留下的在哪里',kind:'物理时间',intro:'每分钟进来 6 L、出去 2 L，多出的 4 L 去哪了？它留在水箱里，让水面升高。',
  assumptions:'本节竖直水箱的横截面积 A=0.20 m²，高度不同时面积相同；水的密度 ρ=1000 kg/m³。给定恒定进水 6 L/min、出水 2 L/min，假设无泄漏、无溢流。为展示水面，另设初始水深 H=0.10 m（20 kg），只演示到 5 min。流率由外部维持，不是按水位自由出流。',
  steps:[step('先看固定控制体','虚线边界固定在水箱处。初始质量为 20 kg，水深 10 cm。','m = ρAH'),step('1 分钟后，多了 4 kg','6 kg 流入、2 kg 流出，剩下 4 kg；不能把流入量全当作新增量。','Δm = 6 − 2 = 4 kg'),step('区分流率与累计量','入口仍是 6 L/min；2 分钟累计流入已是 12 L。','ṁ入 = 0.100 kg/s'),step('水面持续升高','每分钟新增体积 4 L，除以水箱面积，水深每分钟增加 2 cm。','dH/dt = (Q入 − Q出)/A'),step('守恒不要求稳态','质量没有产生；只是边界内的存量不断增加，因此积累项不能删掉。','dm/dt = 0.0667 kg/s'),step('5 分钟后核对两本账','新增 20 kg，也就是新增 20 L；水深从 10 cm 升到 20 cm。','Δm = 30 − 10 = ρAΔH = 20 kg')],state:massState,
  draw:m=>{const base=213,height=164*m.mass/60,top=base-height;let b='<rect x="53" y="29" width="174" height="191" fill="none" stroke="currentColor" stroke-dasharray="5 5" opacity=".6"/>'+`<rect x="70" y="${top}" width="140" height="${height}" fill="${C.b}" opacity=".27"/>`+line(70,50,70,213)+line(70,213,210,213)+line(210,213,210,50)+line(70,top,210,top,C.b);b+=text(140,20,'固定控制体','middle')+text(140,97,fmt(m.mass)+' kg','middle',25)+text(140,129,'水深 '+fmt(m.height*100)+' cm','middle',18)+text(14,253,'流入 6 L/min','start',17)+text(266,279,'流出 2 L/min','end',17);b+=line(10,162,62,162,C.a)+`<polygon points="62,162 53,157 53,167" fill="${C.a}"/>`+line(218,186,270,186,C.o)+`<polygon points="270,186 261,181 261,191" fill="${C.o}"/>`;return view(svg(b,'水箱水深 '+fmt(m.height*100)+' 厘米，质量 '+fmt(m.mass)+' 千克。固定流率产生积累。',294),[['物理时间',fmt(m.time)+' s / '+fmt(m.time/60)+' min'],['累计流入',fmt(m.inflow)+' kg'],['累计流出',fmt(m.outflow)+' kg'],['新增水深',fmt(m.rise*100)+' cm']],'静止箭头只标流向，不是粒子轨迹；水深按同一竖直尺度绘制，水箱示意宽度不表达真实截面形状。');}
 },
 'python-loop':{
  lessonId:'python-06',title:'看清哪一行改了哪个变量',kind:'执行步骤',intro:'18、20、22 三个读数，只取不低于 20 的那些，平均是多少？跟着高亮行，看程序什么时候改总和、什么时候改个数。',
  assumptions:'固定整数列表 [18,20,22]，门槛为 20。这里模拟这段程序的确定执行轨迹，不是通用 Python 解释器；教学播放间隔不是运行耗时。初始化 3 行已完成，首帧停在进入循环之前。',
  steps:pythonFrames.map(f=>step(f[5],f[6],f[7])),state:pythonState,
  draw:m=>{const code=`<ol class="story-code" aria-label="Python 程序，当前第 ${m.line} 行">${pythonCode.map((s,i)=>`<li ${i+1===m.line?'class="is-current" aria-current="step"':''}><code>${esc(s)}</code>${i+1===m.line?'<span class="story-code-cue">当前</span>':''}</li>`).join('')}</ol>`;const tokens=svg([18,20,22].map((v,i)=>{const current=v===m.value,passed=m.count>(i===1?0:1)&&i>0;return `<rect x="${12+i*90}" y="12" width="76" height="46" rx="6" fill="${passed?C.a:'var(--soft)'}" fill-opacity="${passed?'.18':'1'}" stroke="${current?C.a:'var(--line)'}" stroke-width="${current?'3':'1'}"/>`+text(50+i*90,43,v,'middle',22)+text(50+i*90,82,i===0?(m.index>=2?'未达标':current?'本轮中':'待处理'):passed?'已完成':current?'本轮中':'待处理','middle',17);}).join(''),'列表元素及是否已完成累计',94);return view(tokens+code,[['刚执行/检查',`第 ${m.line} 行`],['value',m.value===null?'尚未赋值':String(m.value)],['total',String(m.total)],['count',String(m.count)],['输出',m.output===null?'尚无':m.output.toFixed(1)]],'每轮开始时，总和与个数对应此前已处理的达标数据。两条更新之间是语句中间态，不能当作整轮结束态。');}
 },
 'regression-fit':{
  lessonId:'machine-learning-07',title:'让线靠近数据，再固定模型试新数据',kind:'讲解步骤',intro:'三个点已经测到了，怎样用一条线猜下一个点？先看预测和观测差多少，这个差叫“残差”；再用新点检验。',
  assumptions:'本节无量纲教学训练点为 (1,2)、(2,3)、(3,5)；输入记为 x，观测值记为 y；直线的斜率为 w、截距为 b，预测值 ŷ=wx+b，残差 r=y−ŷ。移动路线是讲解用的候选模型比较，不声称是梯度下降。新点 (4,4) 只用于示例评价，不参与拟合；一个点不足以可靠估计泛化误差。',
  steps:[step('先看数据','三个点并不精确共线。一条直线会压缩它们的信息，也会留下误差。','观测 ≠ 模型'),step('先用平均值作常数预测','水平线 y=10/3 是不使用 x 的基线。虚线比较同一 x 上的预测与观测。','残差 rᵢ = yᵢ − ŷᵢ'),step('绕数据中心转到最小二乘线','保持直线经过均值点 (2,10/3)，改变斜率；到 w=3/2 时平方和最小。','w=3/2；b=1/3'),step('残差相抵，不代表误差为零','三个残差 1/6、−1/3、1/6 的和为 0，但平方和为 1/6。','训练 MSE = 1/18 ≈ 0.0556'),step('冻结模型，加入新观测','模型保持不变。在 x=4 预测 19/3，而新观测是 4，偏差仍可能很大。','新点 r = 4 − 19/3 = −7/3')],state:regressionState,
  draw:m=>{const X=x=>32+218*x/4.5,Y=y=>242-205*y/7;let b=line(32,242,264,242)+line(32,242,32,25)+text(18,19,'y','middle')+text(266,269,'x','end');for(const n of [1,2,3,4])b+=text(X(n),268,n,'middle',16);for(const n of [2,4,6])b+=text(24,Y(n)+6,n,'end',16);if(m.showModel){b+=`<path d="${curve(x=>m.w*x+m.b,0,4.2,X,Y)}" fill="none" stroke="${C.a}" stroke-width="3"/>`;training.forEach(p=>b+=line(X(p.x),Y(p.y),X(p.x),Y(m.w*p.x+m.b),C.o,'stroke-dasharray="4 3"'));}training.forEach(p=>b+=`<circle cx="${X(p.x)}" cy="${Y(p.y)}" r="5" fill="${C.b}"/>`);if(m.showNew)b+=line(X(4),Y(4),X(4),Y(m.newPrediction),C.p,'stroke-dasharray="4 3"')+`<circle cx="${X(4)}" cy="${Y(4)}" r="6" fill="var(--paper)" stroke="${C.p}" stroke-width="2.5"/>`+text(X(4)-10,Y(4)+23,'新点','end',17);return view(svg(b,'训练点固定，'+(m.showModel?'候选直线斜率 '+fmt(m.w)+'，截距 '+fmt(m.b)+', 训练均方误差 '+fmt(m.mse,4):'尚未显示模型')+(m.showNew?'。空心新点没有参与拟合。':''),284),m.showModel?[['当前预测',`ŷ = ${fmt(m.w,3)}x + ${fmt(m.b,3)}`],['训练 MSE',fmt(m.mse,4)],['训练残差和',fmt(m.residualSum,4)],...(m.showNew?[['新点残差',fmt(m.newResidual,4)]]:[])]:[['训练样本数','3'],['特征、输出单位','无量纲']],'实心点：训练观测；绿色实线：模型；虚线：同一 x 处的竖直残差。新点只在最后加入，模型不会随它改变。');}
 }
};
for(const story of Object.values(stories)){story.steps.forEach(Object.freeze);Object.freeze(story.steps);Object.freeze(story);}
Object.freeze(stories);
const lessonMap=Object.freeze(Object.fromEntries(Object.entries(stories).map(([id,s])=>[s.lessonId,id])));
function resolve(id){if(typeof id!=='string')return null;const key=Object.prototype.hasOwnProperty.call(stories,id)?id:lessonMap[id];return key&&Object.prototype.hasOwnProperty.call(stories,key)?key:null;}
// An in-between image needs an in-between explanation: milestone captions
// must never describe a different time or candidate model as the current one.
function transitionText(key,m){
 if(key==='wall-resistance')return step('换一种材料，重新比较两面墙',`第二层当前的导热系数是 ${fmt(m.k2,3)} W/(m·K)。每一幅画面都假设这面墙已经达到稳定状态，比较的是不同材料，不是升温、降温的过程。`,`Q̇ = 40 / (${fmt(m.R1)} + ${fmt(m.R2,3)}) = ${fmt(m.rate)} W；界面 ${fmt(m.interfaceT)}°C`);
 if(key==='cooling-time')return step('时间往前走，温差慢慢缩小',`现在过了 ${fmt(m.t,1)} s，球温为 ${fmt(m.T)}°C，比环境高 ${fmt(m.T-20)} K。温差越小，接下来降温就越慢。`,`t/τ = ${fmt(m.t/m.tau,3)}；T = 20 + 60e^(−${fmt(m.t/m.tau,3)}) = ${fmt(m.T)}°C`);
 if(key==='control-volume')return step('看看这段时间到底留下多少水',`现在过了 ${fmt(m.time)} s：流入 ${fmt(m.inflow)} kg，流出 ${fmt(m.outflow)} kg，因此多留下 ${fmt(m.delta)} kg。水面比起点高 ${fmt(m.rise*100)} cm。`,`m = 20 + ${fmt(m.inflow)} − ${fmt(m.outflow)} = ${fmt(m.mass)} kg`);
 if(key==='regression-fit')return step('点不动，换一条线试试看',`当前候选线的斜率是 ${fmt(m.w,3)}，截距是 ${fmt(m.b,3)}。虚线比较同一输入下，观测与预测差多少；平方后的平均值越小，说明这三个训练点拟合得越好。`,`ŷ = ${fmt(m.w,3)}x + ${fmt(m.b,3)}；训练 MSE = ${fmt(m.mse,4)}`);
 return null;
}
function getFrame(id,position=0){const key=resolve(id);if(!key)return null;const story=stories[key],p=snapPosition(bounded(position,story.steps.length-1)),index=key==='python-loop'?Math.floor(p):stageOf(p,story.steps.length),model=story.state(p),drawing=story.draw(model),transition=p%1!==0?transitionText(key,model):null;return {id:key,position:p,index,model,...(transition||story.steps[index]),...drawing,transition:!!transition};}
function render(id){const key=resolve(id);if(!key)return '';const s=stories[key],f=getFrame(key),max=s.steps.length-1;return `<section class="concept-story" data-story-id="${key}" data-concept-story="${key}" aria-label="${esc(s.title)}"><div class="story-eyebrow">可播放图解 · ${esc(s.kind)}</div><h2 class="story-title">${esc(s.title)}</h2><p class="story-intro">${esc(s.intro)}</p><p class="story-assumptions"><strong>先定模型：</strong>${esc(s.assumptions)}</p><div class="story-chart">${f.graph}</div><dl class="story-metrics">${f.metrics}</dl><p class="story-figure-note">${esc(f.note)}</p><div class="story-transport"><button type="button" class="secondary" data-story-action="play" aria-label="播放图解" aria-pressed="false">播放</button><button type="button" class="secondary" data-story-action="replay" aria-label="重看：回到起点并暂停">重看</button><button type="button" class="secondary" data-story-action="previous" aria-label="上一步图解" disabled>上一步</button><button type="button" class="secondary" data-story-action="next" aria-label="下一步图解">下一步</button></div><label class="story-progress-label"><span>手动选择${s.kind==='物理时间'?'时间节点':'步骤'}</span><input type="range" data-story-progress min="0" max="${max}" step="1" value="0" aria-label="图解步骤" aria-valuetext="第 1 步，共 ${max+1} 步"></label><p class="story-progress-text">${esc(s.kind)} · 1 / ${max+1}</p><div class="story-narration" aria-live="polite" aria-atomic="true"><p class="story-step-title"><strong>${esc(f.title)}</strong></p><p class="story-step-body">${esc(f.body)}</p><p class="story-formula">${esc(f.formula)}</p></div><p class="story-status" role="status">默认静止；可播放，也可逐步阅读。</p><details class="story-sources"><summary>图解方式与来源</summary><p>本图、代码与讲解为本教材独立创作。教学方式参考 <a href="https://www.3blue1brown.com/lessons/eola-preview/" target="_blank" rel="noopener noreferrer">3Blue1Brown 的视觉直觉讲解</a>与<a href="https://www.3blue1brown.com/lessons/pdes/" target="_blank" rel="noopener noreferrer">热方程的图形解释</a>：先看变化，再对应符号。本教材与其无隶属或合作关系，没有复用其动画素材。模型与数值对应本节示例；图解无需联网，参考链接需联网。</p></details></section>`;}

const mounted=new WeakMap();
function mount(el,id){
 if(!el||!el.ownerDocument)return ()=>{};
 mounted.get(el)?.();
 const host=el,key=resolve(id||el.dataset?.storyId||el.dataset?.conceptStory);if(!key)return ()=>{};
 // Accept either render()'s section itself or a caller-provided empty host.
 if(!el.matches?.('.concept-story')){el.innerHTML=render(key);el=el.querySelector('.concept-story');}
 else if(el.dataset.conceptStory!==key||!el.querySelector('[data-story-action="play"]')){
  const holder=el.ownerDocument.createElement('div');holder.innerHTML=render(key);const fresh=holder.firstElementChild;
  el.innerHTML=fresh.innerHTML;el.dataset.storyId=key;el.dataset.conceptStory=key;el.setAttribute('aria-label',fresh.getAttribute('aria-label'));
 }
 mounted.get(el)?.();
 const node=el,doc=node.ownerDocument,win=doc.defaultView||root,s=stories[key],max=s.steps.length-1;
 const $=sel=>node.querySelector(sel),play=$('[data-story-action="play"]'),range=$('[data-story-progress]'),narration=$('.story-narration'),status=$('.story-status');
 const raf=win.requestAnimationFrame?.bind(win)||(fn=>win.setTimeout(()=>fn(Date.now()),32));
 const caf=win.cancelAnimationFrame?.bind(win)||win.clearTimeout.bind(win);
 const mq=win.matchMedia?.('(prefers-reduced-motion: reduce)');
 let position=0,playing=false,disposed=false,handle=null,start=null,startPosition=0,lastPaint=-Infinity,lastIndex=-1,lastPosition=-1,reduced=!!mq?.matches,observer;
 const listeners=[];
 function listen(target,event,fn){target.addEventListener(event,fn);listeners.push(()=>target.removeEventListener(event,fn));}
 function draw(force=false){
  const f=getFrame(key,position);$('.story-chart').innerHTML=f.graph;$('.story-metrics').innerHTML=f.metrics;$('.story-figure-note').textContent=f.note;
  range.value=String(f.index);range.setAttribute('aria-valuetext',`第 ${f.index+1} 步，共 ${max+1} 步：${f.title}`);
  const physical=s.kind==='物理时间'?` · t = ${fmt(f.model.t??f.model.time,1)} s`:'';
  $('.story-progress-text').textContent=`${s.kind} · ${f.transition?`${f.index+1} → ${f.index+2}`:f.index+1} / ${max+1}${physical}`;
  $('[data-story-action="previous"]').disabled=position<=0;$('[data-story-action="next"]').disabled=position>=max;
  if(force||f.index!==lastIndex||f.transition){$('.story-step-title').textContent=f.title;$('.story-step-body').textContent=f.body;$('.story-formula').textContent=f.formula;lastIndex=f.index;}
  node.dataset.storyPosition=String(position);node.dataset.storyPlaying=String(playing);
 }
 function stop(message){playing=false;if(handle!==null)caf(handle);handle=null;start=null;play.textContent='播放';play.setAttribute('aria-label','播放图解');play.setAttribute('aria-pressed','false');narration.setAttribute('aria-live','polite');node.dataset.storyPlaying='false';if(message)status.textContent=message;}
 function tick(now){
  if(disposed||!playing)return;
  if(!node.isConnected){dispose();return;}
  if(doc.hidden){stop('页面不可见，已暂停。');return;}
  if(start===null)start=now;
  // Hold each complete explanation long enough to read before changing the model.
  const next=playbackPosition(startPosition,now-start,max,reduced||key==='python-loop'||key==='energy-account');
  position=next;
  if((now-lastPaint>=80||position>=max)&&position!==lastPosition){draw();lastPaint=now;lastPosition=position;}
  if(next>=max){position=max;draw(true);stop('图解结束；可重看或手动选择步骤。');return;}
  handle=raf(tick);
 }
 function onPlay(){if(disposed)return;if(playing){stop('已暂停；可继续播放或手动选择步骤。');return;}
  if(position>=max){position=0;draw(true);}playing=true;startPosition=position;start=null;lastPaint=-Infinity;play.textContent='暂停';play.setAttribute('aria-label','暂停图解');play.setAttribute('aria-pressed','true');narration.setAttribute('aria-live','off');status.textContent=reduced?'按完整步骤播放，已关闭中间过渡。':'正在播放；可随时暂停或逐步阅读。';node.dataset.storyPlaying='true';handle=raf(tick);
 }
 function go(next,message){if(disposed)return;stop(message);position=bounded(next,max);draw(true);}
 listen(play,'click',onPlay);
 listen($('[data-story-action="replay"]'),'click',()=>go(0,'已回到起点并暂停。'));
 listen($('[data-story-action="previous"]'),'click',()=>go(Math.ceil(position)-1,'已停在上一步。'));
 listen($('[data-story-action="next"]'),'click',()=>go(Math.floor(position)+1,'已停在下一步。'));
 listen(range,'input',()=>go(Number(range.value),'已暂停，手动选择步骤。'));
 listen(doc,'visibilitychange',()=>{if(doc.hidden)stop('页面不可见，已暂停。');});
 listen(win,'pagehide',()=>stop('页面已离开，播放暂停。'));
 const onMotion=e=>{reduced=!!e.matches;if(reduced){stop('已遵循减少动态效果偏好；请逐步阅读或手动播放完整步骤。');position=Math.floor(position);draw(true);}};
 if(mq?.addEventListener)listen(mq,'change',onMotion);else if(mq?.addListener){mq.addListener(onMotion);listeners.push(()=>mq.removeListener(onMotion));}
 function dispose(){if(disposed)return;stop();disposed=true;observer?.disconnect();listeners.splice(0).forEach(fn=>fn());mounted.delete(node);mounted.delete(host);}
 if(win.MutationObserver&&doc.documentElement){observer=new win.MutationObserver(()=>{if(!node.isConnected)dispose();});observer.observe(doc.documentElement,{childList:true,subtree:true});}
 mounted.set(node,dispose);mounted.set(host,dispose);draw(true);if(reduced)status.textContent='已遵循减少动态效果偏好：默认静止；手动播放时只切换完整步骤。';
 return dispose;
}
const api=Object.freeze({stories,lessonMap,sceneIds:Object.freeze(Object.keys(stories)),render,mount,getFrame,STEP_MS,DWELL_MS,math:Object.freeze({energyState,wallState,coolingState,coolingConstants,massState,regressionState,pythonState,training,phaseForPosition,playbackPosition})});
root.ConceptStories=api;
if(typeof module!=='undefined')module.exports=api;
})(typeof window==='undefined'?globalThis:window);
