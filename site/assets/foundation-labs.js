/* Original, offline foundation models. Load after labs.js to extend its catalog. */
(function(root){
 'use strict';
 const LABS=root.LABS||(typeof require==='function'?require('./labs.js').LABS:null);
 if(!LABS)throw new Error('foundation-labs.js requires labs.js');
 const C={heat:'var(--blue)',energy:'var(--accent)',work:'#c47c48',trial:'#9b75b7'};
 const esc=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const fmt=n=>String(Number((Math.abs(n)<1e-10?0:n).toFixed(3)));
 const signed=n=>(n>0?'+':'')+fmt(n);
 const tuple=v=>'('+v.map(fmt).join(', ')+')';
 function finite(values){if(!values.every(Number.isFinite))throw new RangeError('Model inputs and outputs must be finite numbers');}

 // Heat into the closed system is positive; work done BY the system is positive.
 // KE and PE changes are zero. The chosen U reference does not determine T.
 function energyAccount(q,w,u0=500){
  finite([q,w,u0]);const delta=q-w,u1=u0+delta;finite([delta,u1]);
  return {q,w,u0,delta,u1,heatContribution:q,workContribution:-w,balanceError:u1-u0-(q-w)};
 }
 function projectLine(vector,direction,candidateCoefficient=0){
  if(!Array.isArray(vector)||!Array.isArray(direction)||vector.length!==2||direction.length!==2)throw new TypeError('Two 2D vectors are required');
  finite([...vector,...direction,candidateCoefficient]);
  const norm=Math.hypot(...direction);
  if(norm===0)return {valid:false,reason:'u=(0,0) 不能确定一条直线。span(0) 只有原点；投影系数公式不能除以 0。'};
  const normSquared=norm*norm,unit=direction.map(x=>x/norm),dot=vector[0]*direction[0]+vector[1]*direction[1];
  // Normalizing first avoids unnecessary cancellation in the projection itself.
  const along=vector[0]*unit[0]+vector[1]*unit[1],coefficient=along/norm;
  const projection=unit.map(x=>along*x),residual=vector.map((x,i)=>x-projection[i]);
  const candidate=direction.map(x=>candidateCoefficient*x),candidateResidual=vector.map((x,i)=>x-candidate[i]);
  const distance=Math.hypot(...residual),candidateDistance=Math.hypot(...candidateResidual);
  const distanceSquared=distance*distance,candidateDistanceSquared=candidateDistance*candidateDistance;
  const excessDistance=Math.abs(candidateCoefficient-coefficient)*norm,excessDistanceSquared=excessDistance*excessDistance;
  finite([normSquared,dot,coefficient,...projection,...residual,...candidate,distanceSquared,candidateDistanceSquared,excessDistanceSquared]);
  if(normSquared===0)throw new RangeError('Direction magnitude is outside the representable squared-norm range');
  return {valid:true,vector:[...vector],direction:[...direction],unit,dot,normSquared,coefficient,projection,residual,
   distance,distanceSquared,candidateCoefficient,candidate,candidateDistance,candidateDistanceSquared,
   orthogonality:residual[0]*direction[0]+residual[1]*direction[1],
   excessDistanceSquared};
 }
 // Ideal stock balance with imposed, constant nonnegative mass flow rates.
 // If the stock empties, BOTH pumps stop: subsequent cumulative flows are frozen.
 function massBalance(initial,inRate,outRate,time){
  finite([initial,inRate,outRate,time]);
  if([initial,inRate,outRate,time].some(x=>x<0))throw new RangeError('Mass, rates and time must be nonnegative');
  const netRate=inRate-outRate,emptyTime=netRate<0?initial/(-netRate):null;
  const stopped=emptyTime!==null&&time>=emptyTime,activeTime=stopped?emptyTime:time;
  const inflow=inRate*activeTime,outflow=outRate*activeTime,mass=stopped?0:Math.max(0,initial+netRate*activeTime);
  finite([activeTime,inflow,outflow,mass]);
  return {initial,inRate,outRate,time,netRate,emptyTime,stopped,activeTime,inflow,outflow,mass,
   delta:mass-initial,actualInRate:stopped?0:inRate,actualOutRate:stopped?0:outRate,
   actualNetRate:stopped?0:netRate,balanceError:mass-initial-(inflow-outflow)};
 }

 function svg(body,label,height,attributes=''){
  return `<svg xmlns="http://www.w3.org/2000/svg" class="lab-visual foundation-visual" viewBox="0 0 320 ${height}" preserveAspectRatio="xMidYMid meet" role="img" aria-label="${esc(label)}" ${attributes}><title>${esc(label)}</title><g fill="currentColor" font-family="sans-serif" font-size="18">${body}</g></svg>`;
 }
 const text=(x,y,s,anchor='start',size=18)=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}">${esc(s)}</text>`;
 function arrow(x1,y1,x2,y2,color,width=2.5,dash=false){
  const length=Math.hypot(x2-x1,y2-y1);if(length<.001)return '';
  const ux=(x2-x1)/length,uy=(y2-y1)/length,h=Math.min(8,length*.5),b=h*.5;
  return `<path d="M${x1} ${y1}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}" ${dash?'stroke-dasharray="5 4"':''}/><polygon points="${x2},${y2} ${x2-h*ux+b*uy},${y2-h*uy-b*ux} ${x2-h*ux-b*uy},${y2-h*uy+b*ux}" fill="${color}"/>`;
 }
 function mark(shape,x,y,color,size=5){
  if(shape==='circle')return `<circle cx="${x}" cy="${y}" r="${size}" fill="${color}" stroke="var(--paper)" stroke-width="1.5"/>`;
  if(shape==='square')return `<rect x="${x-size}" y="${y-size}" width="${size*2}" height="${size*2}" fill="none" stroke="${color}" stroke-width="2.5"/>`;
  return `<polygon points="${x},${y-size} ${x+size},${y} ${x},${y+size} ${x-size},${y}" fill="${color}" stroke="var(--paper)" stroke-width="1.5"/>`;
 }
 function energyGraphic(m){
  let body=text(160,30,'Q − W = ΔU','middle',23);
  const rows=[['热量 Q',m.q,C.heat,'circle'],['功的贡献 −W',-m.w,C.work,'square'],['内能变化 ΔU',m.delta,C.energy,'diamond']];
  rows.forEach(([label,value,color,shape],i)=>{
   const y=66+i*66,end=160+value*126/400;
   body+=mark(shape,20,y-6,color,5)+text(34,y,`${label}：${signed(value)} J`);
   body+=`<path d="M34 ${y+23}H286" stroke="currentColor" opacity=".2"/><rect x="${Math.min(160,end)}" y="${y+14}" width="${Math.max(.7,Math.abs(end-160))}" height="18" fill="${color}" fill-opacity=".65"/><path d="M160 ${y+8}V${y+38}" stroke="currentColor"/>`;
  });
  body+=text(34,249,'−400')+text(160,249,'0','middle')+text(286,249,'+400 J','end');
  body+='<rect x="18" y="270" width="284" height="83" rx="9" fill="none" stroke="currentColor" stroke-dasharray="6 4"/>';
  body+=text(160,295,'封闭系统：无质量流过边界','middle')+text(160,326,`U：${fmt(m.u0)} → ${fmt(m.u1)} J`,'middle',23);
  body+=text(18,383,'Q > 0：热量流入')+text(18,412,'W > 0：系统向外做功');
  return svg(body,`封闭系统能量账本。Q=${fmt(m.q)}焦耳，W=${fmt(m.w)}焦耳，内能变化=${fmt(m.delta)}焦耳。三个条形使用相同的有正负号刻度。`,434);
 }
 function projectionGraphic(m,v){
  const extent=m.valid?Math.max(4,...[v,m.projection,m.candidate].flat().map(Math.abs)):Math.max(4,...v.map(Math.abs));
  const range=Math.ceil(extent)+1,unit=120/range,X=x=>160+x*unit,Y=y=>166-y*unit;
  let body='';
  for(let i=-range;i<=range;i++)body+=`<path d="M${X(i)} 46V286M40 ${Y(i)}H280" stroke="currentColor" opacity=".08"/>`;
  body+='<path d="M40 166H280M160 46V286" stroke="currentColor" opacity=".5"/>';
  body+=text(297,172,'x','middle')+text(171,35,'y')+text(40,310,String(-range),'middle')+text(280,310,String(range),'middle')+text(24,53,String(range),'middle')+text(24,286,String(-range),'middle')+text(148,185,'0','end');
  if(m.valid){
   const [ux,uy]=m.unit,edge=range/Math.max(Math.abs(ux),Math.abs(uy));
   body+=`<path d="M${X(-edge*ux)} ${Y(-edge*uy)}L${X(edge*ux)} ${Y(edge*uy)}" stroke="currentColor" stroke-dasharray="7 5" stroke-width="2"/>`;
   body+=arrow(X(0),Y(0),X(m.projection[0]),Y(m.projection[1]),C.energy,4);
   body+=`<path d="M${X(m.projection[0])} ${Y(m.projection[1])}L${X(v[0])} ${Y(v[1])}" stroke="${C.work}" stroke-width="3" stroke-dasharray="5 4"/>`;
   if(m.distance>1e-9){
    const side=Math.min(.35,m.distance/2),r=m.residual.map(x=>x/m.distance),p=m.projection;
    const corner=[[p[0]+ux*side,p[1]+uy*side],[p[0]+(ux+r[0])*side,p[1]+(uy+r[1])*side],[p[0]+r[0]*side,p[1]+r[1]*side]];
    body+=`<polyline data-right-angle="true" points="${corner.map(p=>`${X(p[0])},${Y(p[1])}`).join(' ')}" fill="none" stroke="currentColor" stroke-width="1.8"/>`;
   }
   body+=mark('square',X(m.candidate[0]),Y(m.candidate[1]),C.trial,8);
  }
  body+=arrow(X(0),Y(0),X(v[0]),Y(v[1]),C.heat)+mark('circle',X(v[0]),Y(v[1]),C.heat,5);
  if(m.valid)body+=mark('diamond',X(m.projection[0]),Y(m.projection[1]),C.energy,6);
  body+=mark('circle',23,336,C.heat)+text(37,343,'圆点：v')+mark('diamond',179,336,C.energy)+text(193,343,'菱形：p');
  body+=mark('square',23,369,C.trial)+text(37,376,'方框：cu')+text(179,376,'虚线：r');
  body+=text(160,408,m.valid?'长虚线是直线 L = span(u)':'u = 0：直线尚未定义','middle');
  return svg(body,m.valid?`等比例坐标。向量v=${tuple(v)}，垂足p=${tuple(m.projection)}，虚线残差r=${tuple(m.residual)}，试探点cu=${tuple(m.candidate)}。`:'零方向向量不能定义直线；只显示原向量，不计算投影系数。',430,`data-unit-x="${unit}" data-unit-y="${unit}"`);
 }
 function massGraphic(m){
  let body=text(160,28,'累积 = 流入 − 流出','middle',23);
  body+=text(160,61,`进入：${fmt(m.actualInRate)} kg/s`,'middle')+arrow(160,68,160,93,C.heat);
  body+='<rect x="38" y="96" width="244" height="83" rx="9" fill="none" stroke="currentColor" stroke-width="2" stroke-dasharray="6 4"/>';
  body+=text(160,124,'控制体内的质量 m','middle')+text(160,158,`${fmt(m.mass)} kg`,'middle',26);
  body+=arrow(160,182,160,207,C.work)+text(160,231,`离开：${fmt(m.actualOutRate)} kg/s`,'middle');
  const X=t=>44+244*t/12,Y=mass=>390-114*mass/70;
  body+=text(44,263,'m / kg')+text(294,263,m.stopped?'空罐后停泵':'恒定流率阶段','end');
  for(const mass of [0,35,70])body+=`<path d="M44 ${Y(mass)}H288" stroke="currentColor" opacity=".15"/>`+text(35,Y(mass)+6,String(mass),'end');
  body+='<path d="M44 276V390H288" stroke="currentColor" fill="none"/>';
  const points=t=>[0,...(m.emptyTime!==null&&m.emptyTime>0&&m.emptyTime<t?[m.emptyTime]:[]),t].map(time=>`${X(time)},${Y(massBalance(m.initial,m.inRate,m.outRate,time).mass)}`).join(' ');
  body+=`<polyline points="${points(12)}" fill="none" stroke="currentColor" stroke-dasharray="5 4" opacity=".35" stroke-width="2"/><polyline points="${points(m.time)}" fill="none" stroke="${C.energy}" stroke-width="3"/>`+mark('circle',X(m.time),Y(m.mass),C.energy,5);
  body+=text(44,417,'0','middle')+text(166,417,'时间 t / s','middle')+text(288,417,'12','middle');
  return svg(body,`控制体质量随时间变化。当前${fmt(m.time)}秒，质量${fmt(m.mass)}千克，实际流入率${fmt(m.actualInRate)}千克每秒，流出率${fmt(m.actualOutRate)}千克每秒。${m.stopped?'质量已降为零，两台泵均停止。':''}`,438);
 }

 LABS['foundation-energy']={
  icon:'⇄',title:'给封闭系统记一本能量账',description:'先约定正负号，再把热量、功和内能变化逐项对齐。条形有共同刻度，负号意味着方向。',
  controls:[['q','热量 Q / J（流入为正）',-200,200,10,120],['w','功 W / J（对外做功为正）',-200,200,10,50]],
  caption:'封闭系统，无质量跨越边界；忽略宏观动能和重力势能的变化。只考虑热与功两类能量传递，采用 ΔU=Q−W。U₀=500 J 是选定参考下的初始内能；此账本没有状态方程，不能由图直接求温度。',
  animation:{key:'q',from:-200,to:200,duration:9000,label:'只改变热量 Q'},
  guide:{question:'吸热 120 J，同时向外做功 50 J，内能增加多少？',answer:'增加 70 J。热量流入贡献 +120 J，对外做功贡献 −50 J，净变化是 120−50=70 J。',steps:[
   {title:'先规定边界和正方向',body:'把系统圈起来：没有物质穿过边界。Q 是热量，W 是功，ΔU 是系统内能的变化；单位均为 J。本例不计动能和势能变化。',formula:'Q > 0 表示吸热；W > 0 表示系统对外做功',preset:{q:0,w:0}},
   {title:'只加热，先猜再看',body:'令 Q=120 J、W=0。热量全部表现为本模型的内能增加。条形向右表示正贡献，而不是空间中的运动方向。',formula:'ΔU = 120 − 0 = 120 J',preset:{q:120,w:0}},
   {title:'把对外做功扣掉',body:'保持吸热 120 J，改为对外做功 50 J。功本身为正，但对内能的贡献是 −W；不要把两个正数直接相加。',formula:'ΔU = 120 − 50 = 70 J',preset:{q:120,w:50}},
   {title:'反过来检查负号',body:'令系统放热 80 J，外界对系统做功 50 J，因此 Q=−80 J、W=−50 J。先判断哪项增加内能，再核对结果。',formula:'ΔU = −80 − (−50) = −30 J',preset:{q:-80,w:-50}}
  ]},
  draw:v=>{const m=energyAccount(v.q,v.w);return {svg:energyGraphic(m),result:`ΔU = Q − W = (${signed(m.q)}) − (${signed(m.w)}) = ${signed(m.delta)} J；U₁ = ${fmt(m.u1)} J。${m.q>0?'系统吸热':m.q<0?'系统放热':'没有净热量传递'}；${m.w>0?'系统对外做功':m.w<0?'外界对系统做功':'没有净功传递'}。`,legend:'圆点标记 Q，方框标记 −W，菱形标记 ΔU。右侧是正贡献，左侧是负贡献；所有能量条形都用 −400 至 +400 J 的相同刻度。'};}
 };
 LABS['foundation-projection']={
  icon:'⊥',title:'垂足为什么给出最小误差',description:'把一个向量投影到过原点的直线。用试探点与垂足比较，亲眼核对正交性和最小二乘。',
  controls:[['x','向量 v 的 x 分量',-3,3,.5,3],['y','向量 v 的 y 分量',-3,3,.5,1],['ux','方向 u 的 x 分量',-2,2,.5,1],['uy','方向 u 的 y 分量',-2,2,.5,1],['c','试探系数 c（方框位置 = cu）',-3,3,.25,0]],
  caption:'二维实向量，采用普通欧氏内积，直线 L={cu:c∈R} 通过原点。u 必须非零；坐标无量纲。两个坐标轴始终采用同一单位长度，并随点的范围一起缩放。试探滑块的范围有限，解析垂足仍在整条无限直线上求取。',
  animation:{key:'c',from:-3,to:3,duration:11000,label:'沿直线移动试探点'},
  guide:{question:'离 v 最近的直线上一点，会是“同样的 x 坐标”对应的点吗？',answer:'一般不是。欧氏距离的最小点是垂足 p，连接 p 与 v 的残差 r 与直线方向 u 垂直。只有特殊几何情形才与横坐标对齐。',steps:[
   {title:'看清三个不同的对象',body:'圆点是 v=(3,1)，直线方向 u=(1,1)，方框是可以改变的试探点 cu。先拖动 c，猜哪一点离圆点最近。',formula:'目标：在所有实数 c 中，使 ‖v−cu‖² 最小',preset:{x:3,y:1,ux:1,uy:1,c:0}},
   {title:'用点积算出垂足',body:'方向向量不必是单位向量，所以要除以 u·u。此处 v·u=4、u·u=2，得到 c*=2，垂足 p=(2,2)。将方框移到这里。',formula:'c* = (v·u)/(u·u)；p = c*u',preset:{x:3,y:1,ux:1,uy:1,c:2}},
   {title:'用勾股关系解释最小值',body:'残差 r=v−p=(1,−1)，满足 r·u=0。任意试探点比垂足多出一段沿直线的位移；两段垂直，所以距离平方只会增加。',formula:'‖v−cu‖² = ‖r‖² + (c−c*)²‖u‖² ≥ ‖r‖²',preset:{x:3,y:1,ux:1,uy:1,c:1}},
   {title:'检查公式的适用条件',body:'把 u 的两个分量都设为 0。此时没有直线方向，分母为 0，不能继续套用系数公式。把任意一个分量调成非零后再观察。',formula:'u ≠ 0 是投影到直线的必要前提',preset:{x:3,y:1,ux:0,uy:0,c:1}}
  ]},
  draw:v=>{const m=projectLine([v.x,v.y],[v.ux,v.uy],v.c);return {svg:projectionGraphic(m,[v.x,v.y]),result:m.valid?`v·u = ${fmt(m.dot)}；u·u = ${fmt(m.normSquared)}；c* = ${fmt(m.coefficient)}。垂足 p = ${tuple(m.projection)}，残差 r = ${tuple(m.residual)}，r·u = ${fmt(m.orthogonality)}。最短距离 ‖r‖ = ${fmt(m.distance)}，最小距离平方 = ${fmt(m.distanceSquared)}；当前 c=${fmt(v.c)} 的距离平方 = ${fmt(m.candidateDistanceSquared)}。${m.distance<1e-9?'残差为零：v 已在直线上，因此不画非零的直角标记。':''}`:m.reason,legend:'圆点与实线箭头表示 v；菱形表示垂足 p；空心方框表示试探点 cu；橙色短虚线表示残差 r。灰色长虚线表示整条直线；小方角表示垂直。重合的标记可叠在一起。'};}
 };
 LABS['foundation-mass']={
  icon:'⇥',title:'有流入流出，为什么还会累积',description:'从每秒流过多少质量，到一段时间后留下多少质量。守恒始终成立，稳态需要另外检查。',
  controls:[['initial','初始质量 m₀ / kg',1,20,1,10],['inRate','设定流入率 / (kg/s)',0,4,.5,2],['outRate','设定流出率 / (kg/s)',0,4,.5,1],['time','观察时间 t / s',0,12,.5,4]],
  caption:'固定控制体的理想质量账本，无质量源项。泵开启期间流入、流出质量流率恒定且非负；不解析压力、液位、容量限制或真实启动过程。若净流出使质量降至 0，则立即同时关闭两台泵，此后不再进出，防止负质量。图框只表示控制体边界，不表示容积。',
  animation:{key:'time',from:0,to:12,duration:11000,label:'观察质量随时间变化'},
  guide:{question:'只要质量守恒，流入率就一定等于流出率吗？',answer:'不一定。流入比流出多的部分会留在控制体内。只有质量不随时间变化时，才有流入率等于流出率；完整稳态还要求其他状态量也不随时间变化。',steps:[
   {title:'先分清质量与质量流率',body:'kg 表示有多少质量；kg/s 表示每秒流过多少质量。t=0 时还没有累计进出，控制体内有初始质量 10 kg。',formula:'质量变化 = 一段时间内流入的质量 − 流出的质量',preset:{initial:10,inRate:2,outRate:1,time:0}},
   {title:'流入多于流出，质量增加',body:'连续 4 s，每秒流入 2 kg、流出 1 kg。因此共流入 8 kg、流出 4 kg，留下的质量由 10 kg 增加到 14 kg。',formula:'m(t) = m₀ + (ṁ入−ṁ出)t = 10 + (2−1)×4',preset:{initial:10,inRate:2,outRate:1,time:4}},
   {title:'让质量稳态成为一个条件',body:'把两边都设为 2 kg/s，泵仍在运转，但质量不再变化。这里只证明质量不累积；温度、速度场等是否稳态还需要分别检查。',formula:'dm/dt = 0 ⇒ ṁ入 = ṁ出（本例无质量源）',preset:{initial:10,inRate:2,outRate:2,time:4}},
   {title:'排空之后不能继续减下去',body:'初始 3 kg、流入 1 kg/s、流出 2 kg/s，3 s 时排空。本模型立即关闭两台泵。观察到 6 s 时，累计量只按前 3 s 计算，质量仍为 0。',formula:'t空 = m₀/(ṁ出−ṁ入)；有效流动时间 = min(t,t空)',preset:{initial:3,inRate:1,outRate:2,time:6}}
  ]},
  draw:v=>{const m=massBalance(v.initial,v.inRate,v.outRate,v.time);const condition=m.stopped?`在 ${fmt(m.emptyTime)} s 排空后两台泵都已停止；实际流率均为 0，有效流动时间为 ${fmt(m.activeTime)} s。停泵改变了边界条件，不能继续套用原流率。`:m.netRate===0?'流入率等于流出率，因此质量不累积；这不证明温度、速度等其他量也处于稳态。':`dm/dt = ${signed(m.netRate)} kg/s，质量随时间变化；守恒并不要求稳态。`;return {svg:massGraphic(m),result:`t=${fmt(m.time)} s：累计流入 ${fmt(m.inflow)} kg，累计流出 ${fmt(m.outflow)} kg。Δm = ${fmt(m.mass)} − ${fmt(m.initial)} = ${signed(m.delta)} kg = ${fmt(m.inflow)} − ${fmt(m.outflow)}。${condition}`,legend:'箭头旁是此刻的实际流率（kg/s）；结果栏是已累计的质量（kg）。绿色实线画到当前时刻，圆点表示当前质量；灰色虚线显示同一模型到 12 s 的走势。'};}
 };
 root.FOUNDATION_MATH=Object.freeze({energyAccount,projectLine,massBalance});
 if(typeof module!=='undefined')module.exports={FOUNDATION_MATH:root.FOUNDATION_MATH,LABS};
})(typeof window==='undefined'?globalThis:window);
