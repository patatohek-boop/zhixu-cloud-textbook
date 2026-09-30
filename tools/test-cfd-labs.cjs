const assert=require('node:assert/strict');
const {CFD_MATH:M,LABS}=require('../site/assets/cfd-labs.js');
assert.equal(Object.keys(LABS).length,21);
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
console.log('CFD labs: 4 models; 108 control combinations; analytic identities and failure cases passed.');
