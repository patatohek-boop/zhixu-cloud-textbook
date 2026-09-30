/* Independent physical identities, analytic reference cases, and DOM lifecycle.
 * No network, browser backend, datasets, random model weights, or test server.
 * Default: dependency-free numerical tests. Use --dom for jsdom checks;
 * set ZHIXU_JSDOM_MODULE if jsdom is not on NODE_PATH. DOM tests are not silently
 * skipped when requested; a missing dependency fails that run.
 */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const {LABS,LAB_MATH:M}=require('../site/assets/labs.js');
let checks=0;
function check(label,fn){fn();checks++;console.log('PASS '+label);}
function near(a,b,tol=1e-8){assert.ok(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=tol,`${a} != ${b} (tol ${tol})`);}
function integrate(fn,a,b,n=1000){const dx=(b-a)/n;let sum=fn(a)+fn(b);for(let i=1;i<n;i++)sum+=(i%2?4:2)*fn(a+i*dx);return sum*dx/3;}
const derivative=(f,x,h=1e-5)=>(f(x+h)-f(x-h))/(2*h);

check('all 11 original APIs and six new experiment IDs remain available',()=>{
 for(const id of ['python-loop','derivative','integral','matrix','gradient','carnot','conduction','cooling','bernoulli','regression','gradient-descent','heat-modes','cooling-inverse','experiment-design','uncertainty-band','physics-residual','data-split'])assert.ok(LABS[id],id);
 assert.equal(Object.keys(LABS).length,17);
 assert.match(LABS.derivative.draw({x:.7,h:.1}).result,/1\.500/);
 assert.match(LABS.cooling.draw({h:25,t:200}).result,/200\.0 s/);
});
check('heat: fixed boundary, bounded temperature and independently integrated energy',()=>{
 for(const b of [-.15,0,.15])for(const c of [0,.1,.2])for(const t of [0,.01,.1,.35]){
  const m=M.heatState(b,c,t);near(m.theta(0),0);near(m.theta(1),0);
  for(let i=0;i<=400;i++){const T=20+80*m.theta(i/400);assert.ok(T>=20-1e-10&&T<=100+1e-10);}
  near(integrate(x=>m.theta(x)**2,0,1),m.energy,1e-10);
  near(integrate(m.theta,0,1),m.heat,1e-10);
  assert.ok(m.energy<=m.initialEnergy+1e-14);
 }
});
check('heat: PDE and energy dissipation checked using differences and quadrature',()=>{
 const b=.12,c=.18,t=.07,m=M.heatState(b,c,t),dx=1e-4;
 for(const x of [.1,.25,.5,.8]){
  const dt=derivative(s=>M.heatState(b,c,s).theta(x),t,1e-6);
  const dxx=(m.theta(x+dx)-2*m.theta(x)+m.theta(x-dx))/(dx*dx);near(dt,dxx,2e-6);
 }
 const E=s=>integrate(x=>M.heatState(b,c,s).theta(x)**2,0,1,400);
 const dissipation=-2*integrate(x=>derivative(m.theta,x)**2,0,1,400);
 near(derivative(E,t,1e-6),dissipation,2e-7);near(m.energyRate,dissipation,2e-7);
});
check('heat: rod plus outward boundary heat obeys the heat balance',()=>{
 const b=-.15,c=.2,t=.16,dx=1e-6;
 // Boundary derivatives are approximated directly from temperatures, not from
 // the implementation's heatRate/removedHeat expressions.
 const outward=s=>{const f=M.heatState(b,c,s).theta;return (f(dx)-f(0))/dx-(f(1)-f(1-dx))/dx;};
 const emitted=integrate(outward,0,t,1200),H=s=>integrate(M.heatState(b,c,s).theta,0,1,1200);
 near(H(t)+emitted,H(0),2e-8);near(M.heatState(b,c,t).removedHeat,emitted,2e-8);
 assert.ok(emitted>0,'fixed-temperature ends must remove excess heat');
 const one=M.heatState(0,0,.1);near(one.amplitudes[0]/.65,Math.exp(-(Math.PI**2)*.1));
 const all=M.heatState(.1,.1,.03);near(Math.log(all.amplitudes[2]/.1)/Math.log(all.amplitudes[0]/.65),9);
});
check('cooling: new labs match the lesson baseline and inverse parameter truth',()=>{
 assert.deepEqual(M.coolingConstants,{mc:180,A:.01,T0:80,Tinf:20,hTrue:18});
 near(M.coolingAt(18,0),80);near(M.coolingAt(18,1000),20+60/Math.E);
 for(const p of M.coolingData(0).filter(p=>p.x>0)){
  const recovered=-180/(.01*p.x)*Math.log((p.y-20)/60);near(recovered,18,1e-10);
 }
 near(M.coolingSSE(18,0),0);assert.ok(M.coolingSSE(17.5,0)>0);assert.ok(M.coolingSSE(18.5,0)>0);
 near(M.coolingSSE(18,2),4*(.5**2+.7**2+.4**2+.3**2+.6**2+.2**2));
});
check('cooling: sensitivity and ODE checked by numerical perturbations',()=>{
 for(const h of [5,18,45])for(const t of [0,300,1000,3000]){
  near(derivative(q=>M.coolingAt(q,t),h),M.coolingSensitivity(h,t),3e-8);
  near(derivative(s=>M.coolingAt(h,s),t,.01),-h*.01/180*(M.coolingAt(h,t)-20),1e-10);
 }
});
check('design: one-parameter information peaks at tau with correct noise scaling',()=>{
 const peak=M.designInformation(1,1,1);near(peak.t,1000);near(peak.relative,1);
 near(M.designInformation(0).information,0);
 for(let i=0;i<=600;i++)assert.ok(M.designInformation(i/100).information<=peak.information+1e-12);
 assert.ok(M.designInformation(6).relative<.002);
 near(M.designInformation(1,2,1).information,peak.information/4);
 near(M.designInformation(1,1,9).information,9*peak.information);
 const fd=derivative(h=>M.coolingAt(h,1000),18);near(peak.information,fd*fd,2e-8);
});
check('Bayesian posterior satisfies normal equations and covariance inverse identity',()=>{
 for(const count of [2,3,4,5])for(const sigma of [.1,.3,1]){
  const m=M.posterior(count,sigma),[w0,w1]=m.mean;
  // Stationarity of negative log prior + log likelihood, independent of the
  // closed-form 2x2 inverse used by the implementation.
  near(w0/4+m.data.reduce((s,p)=>s+(w0+w1*p.x-p.y)/(sigma*sigma),0),0,2e-12);
  near(w1/4+m.data.reduce((s,p)=>s+p.x*(w0+w1*p.x-p.y)/(sigma*sigma),0),0,2e-12);
  const precision=[[.25,0],[0,.25]];
  for(const p of m.data){const phi=[1,p.x];for(let i=0;i<2;i++)for(let j=0;j<2;j++)precision[i][j]+=phi[i]*phi[j]/sigma**2;}
  for(let i=0;i<2;i++)for(let j=0;j<2;j++)near(precision[i][0]*m.cov[0][j]+precision[i][1]*m.cov[1][j],i===j?1:0);
  assert.ok(m.cov[0][0]>0&&m.cov[1][1]>0&&m.cov[0][0]*m.cov[1][1]>m.cov[0][1]**2);
 }
});
check('uncertainty: noise adds variance and extrapolation widens this model',()=>{
 for(const count of [2,3,4,5])for(const sigma of [.1,.3,1]){
  const m=M.posterior(count,sigma),p0=M.predictBayes(m,0),p3=M.predictBayes(m,3);
  near(p3.observationVariance-p3.variance,sigma*sigma);
  assert.ok(p3.variance>p0.variance);
  for(let x=-3;x<=3;x+=.25){const p=M.predictBayes(m,x);assert.ok(p.variance>0&&p.observationVariance>p.variance);}
 }
 for(const x of [-3,0,3])assert.ok(M.predictBayes(M.posterior(5,.3),x).variance<M.predictBayes(M.posterior(2,.3),x).variance);
});
check('physics residual: false initial conditions survive a zero PDE residual',()=>{
 for(const c of [0,.6,1,1.5]){
  const m=M.physicsState(c,1,.04);near(m.residualNorm,0);
  near(Math.sqrt(integrate(x=>(M.physicsState(c,1,0).candidate(x)-Math.sin(Math.PI*x))**2,0,1)),m.initialError);
  near(Math.sqrt(integrate(x=>(m.candidate(x)-m.exact(x))**2,0,1)),m.solutionError);
  if(c!==1)assert.ok(m.initialError>0&&m.solutionError>0);
 }
 const m=M.physicsState(1,.5,.04),dx=1e-4;
 for(const x of [.1,.4,.8]){
  const time=derivative(t=>M.physicsState(1,.5,t).candidate(x),.04,1e-6);
  const space=(m.candidate(x+dx)-2*m.candidate(x)+m.candidate(x-dx))/(dx*dx);
  near(time-space,m.residual(x),2e-6);
 }
});
check('data split: memberships and known noiseless errors expose run leakage',()=>{
 for(let seed=1;seed<=5;seed++)for(const shift of [0,1.5,3]){
  const m=M.splitStudy(shift,0,seed);assert.deepEqual(m,M.splitStudy(shift,0,seed));
  for(const split of [m.rowSplit,m.groupSplit]){
   assert.equal(split.train.length,24);assert.equal(split.test.length,12);
   const seen=new Set(split.train.map(p=>p.id));assert.ok(split.test.every(p=>!seen.has(p.id)));
  }
  const overlap=split=>new Set(split.test.map(p=>p.run).filter(run=>split.train.some(p=>p.run===run))).size;
  assert.equal(overlap(m.rowSplit),6);assert.equal(overlap(m.groupSplit),0);
  near(m.rowSplit.mse,0,1e-25);
  // The two held-out offsets are -0.5*shift and 1.5*shift. No learned run
  // offset is available: average squared error must be (0.25+2.25)/2 * shift².
  near(m.groupSplit.mse,1.25*shift*shift);
 }
 const m=M.splitStudy(1.5,.2,2);assert.ok(m.groupSplit.mse>100*m.rowSplit.mse);
});
check('every default, control boundary, and combination of extremes draws finite output',()=>{
 for(const [id,s] of Object.entries(LABS)){
  const defaults=Object.fromEntries(s.controls.map(c=>[c[0],c[5]]));
  const cases=[defaults];for(let mask=0;mask<2**s.controls.length;mask++)cases.push(Object.fromEntries(s.controls.map((c,i)=>[c[0],c[(mask>>i)&1?3:2]])));
  for(const values of cases){const r=s.draw(values);assert.ok(r.svg.startsWith('<svg'),id);assert.doesNotMatch(r.svg+r.result,/NaN|Infinity|undefined/,id);}
  assert.ok(s.guide.question&&s.guide.answer&&s.guide.steps.length>=3,id);
  for(const step of s.guide.steps)for(const [key,value] of Object.entries(step.preset)){const c=s.controls.find(c=>c[0]===key);assert.ok(c&&value>=c[2]&&value<=c[3],id+' '+key);}
 }
});

async function domChecks(){
 const {JSDOM}=require(process.env.ZHIXU_JSDOM_MODULE||'jsdom');
 const dom=new JSDOM('<!doctype html><html><body></body></html>',{runScripts:'outside-only',pretendToBeVisual:true}),w=dom.window,d=w.document;
 let nextFrame=0;const frames=new Map();
 w.requestAnimationFrame=fn=>{frames.set(++nextFrame,fn);return nextFrame;};w.cancelAnimationFrame=id=>frames.delete(id);
 w.matchMedia=()=>({matches:true});
 w.eval(fs.readFileSync(path.join(__dirname,'../site/assets/labs.js'),'utf8'));
 const cards=[];
 for(const id of Object.keys(w.LABS)){
  const el=d.createElement('section');d.body.append(el);w.mountLab(el,id);cards.push(el);
  const spec=w.LABS[id];assert.equal(el.querySelectorAll('[data-param]').length,spec.controls.length);
  assert.match(el.querySelector('.lab-play-state').textContent,/默认静止/);
  assert.equal(el.querySelector('.lab-play').getAttribute('aria-pressed'),'false');assert.equal(frames.size,0);
  for(const input of el.querySelectorAll('[data-param]')){
   assert.ok(d.getElementById(input.id));assert.ok(el.querySelector(`label[for="${input.id}"]`));
   input.value=input.max;input.dispatchEvent(new w.Event('input'));
   assert.doesNotMatch(el.querySelector('.lab-result').textContent,/NaN|Infinity|undefined/);
  }
  el.querySelector('.lab-reset').click();for(const input of el.querySelectorAll('[data-param]'))assert.equal(input.value,input.defaultValue,id);
  for(let i=0;i<spec.guide.steps.length;i++){el.querySelector('.lab-preset').click();assert.doesNotMatch(el.querySelector('.lab-result').textContent,/NaN|Infinity|undefined/);el.querySelector('.lab-next').click();}
  el.querySelector('.lab-reset').click();
 }
 check('all 17 DOM mounts support controls, guided presets, reduced-motion defaults and reset',()=>{assert.equal(cards.length,17);});
 check('all live SVG/input IDs and references are unique across a page',()=>{
  const ids=[...d.querySelectorAll('[id]')].map(el=>el.id);assert.equal(new Set(ids).size,ids.length);
  for(const el of d.querySelectorAll('[clip-path],[marker-end]'))for(const name of ['clip-path','marker-end']){const ref=el.getAttribute(name);if(ref){const match=ref.match(/^url\(#(.+)\)$/);assert.ok(match&&d.getElementById(match[1]),ref);}}
  for(const svg of d.querySelectorAll('svg'))assert.ok(svg.getAttribute('aria-label')&&svg.querySelector('title'));
 });
 check('matrix and gradient plots use equal length for both coordinate units',()=>{
  const unit=cards[3].querySelector('polygon').getAttribute('points').split(' ').map(p=>p.split(',').map(Number));
  near(Math.abs(unit[1][0]-unit[0][0]),Math.abs(unit[2][1]-unit[1][1]));
  const ellipse=cards[4].querySelector('ellipse');near(Number(ellipse.getAttribute('rx'))/Number(ellipse.getAttribute('ry')),Math.SQRT2);
  const arrow=cards[4].querySelector('path[marker-end]').getAttribute('d').match(/-?\d+(?:\.\d+)?/g).map(Number);
  // At the default point (1, 0.5), gradient=(2,2): a 45-degree arrow in an
  // equal-aspect plot must have equal horizontal and vertical pixel changes.
  near(Math.abs(arrow[2]-arrow[0]),Math.abs(arrow[3]-arrow[1]));
 });
 const el=cards[11],button=el.querySelector('.lab-play'),time=el.querySelector('[data-param=Fo]');
 const advance=now=>{const batch=[...frames.values()];frames.clear();batch.forEach(fn=>fn(now));};
 button.click();advance(0);advance(5000);assert.ok(Number(time.value)>0);button.click();assert.equal(frames.size,0);
 button.click();el.querySelector('.lab-reset').click();assert.equal(frames.size,0);assert.equal(time.value,time.defaultValue);
 button.click();el.remove();await Promise.resolve();assert.equal(frames.size,0);
 check('play/pause, reset and DOM removal cancel scheduled animation',()=>{assert.equal(button.getAttribute('aria-pressed'),'false');});
 const el2=cards[12];el2.querySelector('.lab-play').click();assert.equal(frames.size,1);
 Object.defineProperty(d,'hidden',{configurable:true,value:true});d.dispatchEvent(new w.Event('visibilitychange'));assert.equal(frames.size,0);
 check('hidden document stops playback',()=>{assert.equal(el2.querySelector('.lab-play').getAttribute('aria-pressed'),'false');});
 dom.window.close();
}
const numericalChecks=checks;
if(process.argv.includes('--dom'))domChecks().then(()=>console.log(JSON.stringify({numerical:'passed',numericalChecks,dom:'passed',domChecks:checks-numericalChecks,labs:Object.keys(LABS).length,network:'none'}))).catch(error=>{console.error(error);process.exitCode=1;});
else console.log(JSON.stringify({numerical:'passed',numericalChecks,dom:'not requested (use --dom)',labs:Object.keys(LABS).length,network:'none'}));
