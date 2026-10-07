const assert=require('node:assert/strict');
const {CFD_MATH:M,LABS}=require('../site/assets/cfd-labs.js');
assert.equal(Object.keys(LABS).length,21);
// Independent integral-series ratio: (exp(z)-1)/z = sum z^j/(j+1)!.
// This oracle neither subtracts nearby exponentials nor uses the production branch.
function integralSeries(z){
 let total=1,term=1;
 for(let j=1;j<=600;j++){
  term*=z/(j+1);total+=term;
  if(term<=Number.EPSILON*total/4)return total;
 }
 throw new Error('Reference series did not converge');
}
let referenceChecks=0;
for(const pe of [0,Number.MIN_VALUE,1e-310,1e-17,1e-12,1e-8*(1-Number.EPSILON),1e-8,1e-8*(1+Number.EPSILON),1e-6,.1,1,5,10,60,100]){
 let previous=-1;
 for(const x of [0,1e-12,.01,.25,.5,.75,.99,1-Number.EPSILON/2,1]){
  const expected=x*integralSeries(pe*x)/integralSeries(pe),actual=M.exact(x,pe);
  assert.ok(Number.isFinite(actual)&&actual>=0&&actual<=1,`bounded exact x=${x}, Pe=${pe}`);
  assert.ok(Math.abs(actual-expected)<=2e-14*Math.abs(expected)+1e-320,`exact x=${x}, Pe=${pe}: ${actual} != ${expected}`);
  assert.ok(actual>=previous,`monotone exact Pe=${pe}`);previous=actual;referenceChecks++;
 }
 assert.equal(M.exact(0,pe),0);assert.equal(M.exact(1,pe),1);
}
for(const n of [10,20,40,80]){
 const coarse=M.transport(n,1e-6,'central').l2,fine=M.transport(n*2,1e-6,'central').l2;
 const order=Math.log2(coarse/fine);
 assert.ok(order>1.99&&order<2.01,`small-Pe convergence N=${n}: ${order}`);
}
for(const scheme of ['central','upwind']){
 for(const n of [5,20,80])for(const pe of [0,1,10,60]){
  const m=M.transport(n,pe,scheme);assert.ok(m.balance<1e-10);
  if(pe===0){assert.ok(m.l2<1e-13);m.flux.forEach(f=>assert.ok(Math.abs(f+1)<1e-12));}
  if(scheme==='upwind')assert.ok(m.bounded);
 }
 const a=M.transport(80,5,scheme).l2,b=M.transport(160,5,scheme).l2,p=Math.log2(a/b);
 assert.ok(scheme==='central'?p>1.99&&p<2.01:p>.95&&p<1.01);
}
assert.equal(M.transport(10,60,'central').bounded,false);
assert.throws(()=>M.transport(10,NaN,'upwind'));
const g=M.grid(100.25,101,104);assert.equal(g.p,2);assert.equal(g.ext,100);assert.equal(g.gci,.3125);
assert.equal(M.grid(1,1,1).valid,false);assert.equal(M.grid(1,2,1).valid,false);
assert.equal(M.wall(.1,1,10).yplus,1);assert.equal(M.wall(.1,1,10).height,20);
for(const k of [1,10,200])for(const h of [10,100,500])for(const rc of [0,.001,.005]){
 const m=M.resistance(k,h,rc);assert.ok(Math.abs(m.temperatures.at(-1)-300)<1e-10);assert.ok(Math.abs(m.drops.reduce((s,v)=>s+v,0)-30)<1e-10);
}
for(const [id,lab] of Object.entries(LABS).filter(([id])=>id.startsWith('cfd-'))){
 const visit=(i,values)=>{if(i===lab.controls.length){const out=lab.draw(values);assert.ok(!/NaN|Infinity|undefined/.test(out.svg+out.result+out.legend),id);assert.ok(out.svg.startsWith('<svg'));return;}const c=lab.controls[i];for(const value of [c[2],c[3],c[5]])visit(i+1,{...values,[c[0]]:value});};
 visit(0,{});assert.equal(lab.guide.steps.length,3);assert.ok(lab.animation.key);
}
console.log(`CFD exact: ${referenceChecks} independent reference checks passed.`);
console.log('CFD labs: 4 models; 108 control combinations; analytic identities and failure cases passed.');
// X-axis labels must preserve the actual tick values, not just avoid NaN.
// All grid slider values plus the quarter-position and log-wall axes are covered.
function xTicks(svg){return [...svg.matchAll(/<text x="[^"]+" y="286"[^>]*>([^<]+)<\/text>/g)].map(m=>Number(m[1]));}
function checkTicks(svg,expected){
 const labels=xTicks(svg);assert.equal(labels.length,5);assert.equal(new Set(labels).size,5);
 labels.forEach((n,i)=>assert.ok(Math.abs(n-expected[i])<1e-12,`${n} != tick ${expected[i]}`));
}
for(let hundredths=2;hundredths<=20;hundredths++){
 const h=hundredths/100;checkTicks(LABS['cfd-grid'].draw({h,order:2,noise:0}).svg,[0,h,2*h,3*h,4*h]);
}
checkTicks(LABS['cfd-upwind'].draw({pe:10,n:20,scheme:0}).svg,[0,.25,.5,.75,1]);
checkTicks(LABS['cfd-yplus'].draw({ut:.1,nu:15,y:150}).svg,[-2,-.625,.75,2.125,3.5]);
console.log('CFD axis regression: all 19 grid scales and both other numeric x axes retain five exact, distinct ticks.');
