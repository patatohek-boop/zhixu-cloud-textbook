/* Dependency-free mathematical checks; add --dom for the shared mounting UI.
 * DOM checks require jsdom or ZHIXU_JSDOM_MODULE, and fail if it is unavailable.
 */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {FOUNDATION_MATH:M,LABS}=require('../site/assets/foundation-labs.js');
const ids=['foundation-energy','foundation-projection','foundation-mass'];
let checks=0,renderCases=0;
function check(name,fn){fn();checks++;console.log('PASS '+name);}
function near(actual,expected,tolerance=1e-10){assert.ok(Number.isFinite(actual)&&Number.isFinite(expected)&&Math.abs(actual-expected)<=tolerance,`${actual} != ${expected}`);}
const norm2=v=>v.reduce((s,x)=>s+x*x,0);

check('closed-system sign convention handles heat, work, zero and cancellation',()=>{
 for(const q of [-200,-80,0,120,200])for(const w of [-200,-50,0,50,200]){
  const m=M.energyAccount(q,w);near(m.delta,q-w);near(m.u1+m.w,m.u0+m.q);near(m.balanceError,0);
  near(m.heatContribution,q);near(m.workContribution,-w);
 }
 near(M.energyAccount(120,50).delta,70);near(M.energyAccount(-80,-50).delta,-30);
 near(M.energyAccount(0,-200).delta,200);near(M.energyAccount(-200,0).delta,-200);
 near(M.energyAccount(200,200).delta,0);near(M.energyAccount(0,0).delta,0);
 near(M.energyAccount(15,5,-100).u1,-90); // U's reference is arbitrary, not an absolute-temperature bound.
 assert.throws(()=>M.energyAccount(NaN,0),RangeError);assert.throws(()=>M.energyAccount(0,Infinity),RangeError);
});
check('projection reproduces analytic horizontal, vertical and oblique cases',()=>{
 for(const [v,u,p,c,d2] of [
  [[3,1],[1,1],[2,2],2,2],[[3,-2],[2,0],[3,0],1.5,4],
  [[-2,3],[0,-2],[0,3],-1.5,4],[[1,-1],[1,1],[0,0],0,2],
  [[0,0],[1,2],[0,0],0,0],[[2,-2],[-1,1],[2,-2],-2,0]
 ]){
  const m=M.projectLine(v,u,c);assert.equal(m.valid,true);near(m.coefficient,c);
  m.projection.forEach((x,i)=>near(x,p[i]));near(m.distanceSquared,d2);near(m.candidateDistanceSquared,d2);
 }
 const zero=M.projectLine([3,1],[0,0],1);assert.equal(zero.valid,false);assert.match(zero.reason,/不能.*直线/);assert.ok(!('coefficient' in zero));
 assert.throws(()=>M.projectLine([1],[1,0]),TypeError);assert.throws(()=>M.projectLine([NaN,0],[1,0]),RangeError);
});
check('projection residual is orthogonal; independent squared distances have the claimed unique minimum',()=>{
 for(const x of [-3,0,3])for(const y of [-3,0,3])for(const ux of [-2,-.5,0,.5,2])for(const uy of [-2,-.5,0,.5,2]){
  if(ux===0&&uy===0)continue;
  const v=[x,y],u=[ux,uy],m=M.projectLine(v,u);const den=ux*ux+uy*uy;
  near(m.coefficient,(x*ux+y*uy)/den);near(m.orthogonality,0);
  near(m.projection[0]+m.residual[0],x);near(m.projection[1]+m.residual[1],y);
  near(norm2(v),norm2(m.projection)+norm2(m.residual));
  for(const offset of [-3,-.25,0,.25,3]){
   const c=m.coefficient+offset,test=M.projectLine(v,u,c),independent=norm2([x-c*ux,y-c*uy]);
   near(test.candidateDistanceSquared,independent);
   near(independent,m.distanceSquared+offset*offset*den);
   near(test.excessDistanceSquared,offset*offset*den);
   assert.ok(independent+1e-10>=m.distanceSquared);
   if(offset!==0)assert.ok(independent>m.distanceSquared);
  }
 }
});
check('changing direction magnitude or sign preserves the line and its projection',()=>{
 const base=M.projectLine([3,-1],[1,2]);
 for(const scale of [-100,-2,-.5,1e-150,1e150]){
  const m=M.projectLine([3,-1],[scale,2*scale]);m.projection.forEach((x,i)=>near(x,base.projection[i]));
  near(m.coefficient*scale,base.coefficient);near(m.distanceSquared,base.distanceSquared);
 }
});
check('mass: constant-flow integral balance, nonnegativity and empty-stop boundary',()=>{
 for(const initial of [0,1,3,10,20])for(const inflow of [0,.5,2,4])for(const outflow of [0,.5,2,4])for(const t of [0,.25,.5,3,6,12]){
  const m=M.massBalance(initial,inflow,outflow,t);near(m.mass,initial+m.inflow-m.outflow);near(m.balanceError,0);
  assert.ok(m.mass>=0&&m.activeTime<=t&&m.inflow>=0&&m.outflow>=0);
  if(m.stopped){near(m.mass,0);near(m.actualInRate,0);near(m.actualOutRate,0);near(m.actualNetRate,0);near(m.activeTime,initial/(outflow-inflow));}
  else{near(m.mass,initial+(inflow-outflow)*t);near(m.actualNetRate,inflow-outflow);}
 }
 const before=M.massBalance(3,1,2,2.5),at=M.massBalance(3,1,2,3),after=M.massBalance(3,1,2,6);
 near(before.mass,.5);assert.equal(before.stopped,false);assert.equal(at.stopped,true);assert.equal(after.stopped,true);
 near(at.mass,0);near(after.mass,0);near(after.inflow,3);near(after.outflow,6);near(after.activeTime,3);
 near(M.massBalance(10,2,1,4).mass,14);near(M.massBalance(10,2,2,12).mass,10);
 for(const m of [M.massBalance(0,0,1,0),M.massBalance(0,1,2,12)])assert.equal(m.stopped,true);
 const noFlow=M.massBalance(0,0,0,12);assert.equal(noFlow.stopped,false);near(noFlow.mass,0);
 assert.throws(()=>M.massBalance(-1,0,0,0),RangeError);assert.throws(()=>M.massBalance(1,-1,0,0),RangeError);
 assert.throws(()=>M.massBalance(1,0,0,-1),RangeError);assert.throws(()=>M.massBalance(1,0,Infinity,1),RangeError);
});
check('mass slope agrees with net rate before stop and zero after stop',()=>{
 const h=1e-5;
 for(const [initial,inRate,outRate,t] of [[10,2,1,4],[10,2,2,4],[3,1,2,2],[3,1,2,6]]){
  const derivative=(M.massBalance(initial,inRate,outRate,t+h).mass-M.massBalance(initial,inRate,outRate,t-h).mass)/(2*h);
  near(derivative,M.massBalance(initial,inRate,outRate,t).actualNetRate,1e-9);
 }
});
check('all control boundary/default combinations render finite, accessible offline SVG',()=>{
 for(const id of ids){
  const lab=LABS[id];assert.ok(lab&&lab.title&&lab.caption&&lab.animation);assert.ok(lab.guide.steps.length>=4);
  const visit=(i,values)=>{
   if(i===lab.controls.length){
    const result=lab.draw(values);renderCases++;assert.ok(result.svg.startsWith('<svg'),id);
    assert.doesNotMatch(result.svg+result.result+result.legend,/NaN|Infinity|undefined/);
    assert.match(result.svg,/role="img"/);assert.match(result.svg,/<title>[^<]+<\/title>/);assert.match(result.svg,/aria-label="[^"<>]+"/);
    assert.match(result.svg,/viewBox="0 0 320 /);assert.doesNotMatch(result.svg,/<script|<foreignObject|<image|href=|onload=/i);
    if(id==='foundation-projection'){
     const x=result.svg.match(/data-unit-x="([^"]+)"/),y=result.svg.match(/data-unit-y="([^"]+)"/);assert.ok(x&&y);near(Number(x[1]),Number(y[1]));
    }
    return;
   }
   const c=lab.controls[i];for(const value of new Set([c[2],c[3],c[5]]))visit(i+1,{...values,[c[0]]:value});
  };
  visit(0,{});
  for(const step of lab.guide.steps){
   assert.ok(step.title&&step.body&&step.formula);
   for(const [key,value] of Object.entries(step.preset)){const c=lab.controls.find(c=>c[0]===key);assert.ok(c&&value>=c[2]&&value<=c[3],id+' preset '+key);near((value-c[2])/c[4],Math.round((value-c[2])/c[4]));}
   const out=lab.draw({...Object.fromEntries(lab.controls.map(c=>[c[0],c[5]])),...step.preset});assert.doesNotMatch(out.svg+out.result,/NaN|Infinity|undefined/);
  }
 }
});
check('teaching output states zero guards, signed contributions and the changed boundary after emptying',()=>{
 const zero=LABS['foundation-projection'].draw({x:3,y:1,ux:0,uy:0,c:0});assert.match(zero.result,/不能.*直线/);assert.doesNotMatch(zero.svg,/data-right-angle/);
 const exact=LABS['foundation-projection'].draw({x:2,y:2,ux:1,uy:1,c:2});assert.match(exact.result,/残差为零/);assert.doesNotMatch(exact.svg,/data-right-angle/);
 assert.match(LABS['foundation-projection'].draw({x:3,y:1,ux:1,uy:1,c:2}).svg,/data-right-angle/);
 const negativeWork=LABS['foundation-energy'].draw({q:0,w:-50});assert.match(negativeWork.result,/外界对系统做功/);assert.match(negativeWork.result,/\+50 J/);
 const drain=LABS['foundation-mass'].draw({initial:3,inRate:1,outRate:2,time:6});assert.match(drain.result,/累计流入 3 kg，累计流出 6 kg/);assert.match(drain.result,/两台泵都已停止/);
 const balanced=LABS['foundation-mass'].draw({initial:10,inRate:2,outRate:2,time:4});assert.match(balanced.result,/不证明.*其他量也处于稳态/);
});

async function domChecks(){
 const {JSDOM}=require(process.env.ZHIXU_JSDOM_MODULE||'jsdom');
 const dom=new JSDOM('<!doctype html><html><body></body></html>',{runScripts:'outside-only',pretendToBeVisual:true});
 const w=dom.window,d=w.document,frames=new Map();let nextFrame=0;
 w.requestAnimationFrame=fn=>{frames.set(++nextFrame,fn);return nextFrame;};w.cancelAnimationFrame=id=>frames.delete(id);w.matchMedia=()=>({matches:true});
 for(const file of ['labs.js','foundation-labs.js'])w.eval(fs.readFileSync(path.join(__dirname,'../site/assets',file),'utf8'));
 const cards=[];
 for(const id of ids){
  const el=d.createElement('section');d.body.append(el);w.mountLab(el,id);cards.push(el);const lab=w.LABS[id];
  assert.equal(el.querySelectorAll('input[type=range]').length,lab.controls.length);assert.equal(frames.size,0);
  assert.equal(el.querySelector('.lab-play').getAttribute('aria-pressed'),'false');assert.match(el.querySelector('.lab-play-state').textContent,/默认静止/);
  for(const input of el.querySelectorAll('[data-param]')){
   assert.ok(input.getAttribute('aria-label'));assert.ok(el.querySelector(`label[for="${input.id}"]`));assert.ok(el.querySelector(`output[for="${input.id}"]`));
   input.value=input.max;input.dispatchEvent(new w.Event('input'));assert.doesNotMatch(el.querySelector('.lab-result').textContent,/NaN|Infinity|undefined/);
  }
  el.querySelector('.lab-reset').click();for(const input of el.querySelectorAll('[data-param]'))assert.equal(input.value,input.defaultValue);
  for(let i=0;i<lab.guide.steps.length;i++){
   assert.match(el.querySelector('.lab-step-count').textContent,new RegExp(`步骤 ${i+1} / ${lab.guide.steps.length}`));
   el.querySelector('.lab-preset').click();assert.doesNotMatch(el.querySelector('.lab-result').textContent,/NaN|Infinity|undefined/);el.querySelector('.lab-next').click();
  }
  assert.equal(el.querySelector('.lab-next').disabled,true);el.querySelector('.lab-prev').click();assert.equal(el.querySelector('.lab-next').disabled,false);
  el.querySelector('.lab-reset').click();assert.equal(el.querySelector('.lab-prev').disabled,true);
 }
 check('all three mounts support accessible native sliders, explicit step presets and reset without autoplay',()=>{assert.equal(cards.length,3);assert.equal(frames.size,0);});
 check('multiple mounted instances use unique control IDs and named SVGs',()=>{
  const copy=d.createElement('section');d.body.append(copy);w.mountLab(copy,'foundation-projection');
  const all=[...d.querySelectorAll('[id]')].map(el=>el.id);assert.equal(new Set(all).size,all.length);
  for(const svg of d.querySelectorAll('svg'))assert.ok(svg.getAttribute('aria-label')&&svg.querySelector('title'));
  copy.remove();
 });
 const projection=cards[1];
 for(const key of ['ux','uy']){const input=projection.querySelector(`[data-param=${key}]`);input.value='0';input.dispatchEvent(new w.Event('input'));}
 assert.match(projection.querySelector('.lab-result').textContent,/不能.*直线/);
 const ux=projection.querySelector('[data-param=ux]');ux.value='1';ux.dispatchEvent(new w.Event('input'));assert.match(projection.querySelector('.lab-result').textContent,/最短距离/);
 check('zero-direction UI recovers after a nonzero direction is restored',()=>{assert.ok(projection.querySelector('svg'));});
 const advance=now=>{const pending=[...frames.values()];frames.clear();pending.forEach(fn=>fn(now));};
 for(let i=0;i<cards.length;i++){
  const el=cards[i],button=el.querySelector('.lab-play');button.click();assert.equal(frames.size,1);advance(0);advance(3000);
  assert.equal(button.getAttribute('aria-pressed'),'true');button.click();assert.equal(frames.size,0);
  button.click();el.querySelector('.lab-reset').click();assert.equal(frames.size,0);
  button.click();el.remove();await Promise.resolve();assert.equal(frames.size,0);
 }
 check('manual playback pauses and cancels on reset or removal in every new lab',()=>{assert.equal(frames.size,0);});
 dom.window.close();
}
const numericalChecks=checks;
if(process.argv.includes('--dom'))domChecks().then(()=>console.log(JSON.stringify({numerical:'passed',numericalChecks,renderCases,dom:'passed',domChecks:checks-numericalChecks,labs:ids.length}))).catch(error=>{console.error(error);process.exitCode=1;});
else console.log(JSON.stringify({numerical:'passed',numericalChecks,renderCases,dom:'not requested (use --dom)',labs:ids.length}));
