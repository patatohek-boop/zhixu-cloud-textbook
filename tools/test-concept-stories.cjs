/* Offline deterministic concept + lifecycle checks. No browser socket required.
 * node tools/test-concept-stories.cjs [--dom]
 * ZHIXU_JSDOM_MODULE may point at an existing jsdom installation.
 */
'use strict';
const assert=require('node:assert/strict'),fs=require('node:fs'),path=require('node:path');
const C=require('../site/assets/concept-stories.js'),M=C.math;
const atPosition=p=>M.phaseForPosition(p)*C.STEP_MS;
let checks=0,renderCases=0;
function check(name,fn){fn();checks++;console.log('PASS '+name);}
function near(a,b,tol=1e-9){assert.ok(Number.isFinite(a)&&Number.isFinite(b)&&Math.abs(a-b)<=tol,`${a} != ${b}`);}
function finiteTree(o){for(const value of Object.values(o)){if(typeof value==='number')assert.ok(Number.isFinite(value));else if(value&&typeof value==='object')finiteTree(value);}}
check('six original scene/lesson mappings are unique and the render contract is stable',()=>{
 assert.equal(C.sceneIds.length,6);assert.equal(Object.keys(C.lessonMap).length,6);
 for(const id of C.sceneIds){const s=C.stories[id];assert.equal(C.lessonMap[s.lessonId],id);assert.equal(C.render(id),C.render(s.lessonId));assert.match(C.render(id),new RegExp(`data-story-id="${id}"`));assert.match(C.render(id),/<h2 class="story-title">/);assert.match(C.render(id),/<svg/);assert.ok(s.assumptions.length>40);assert.ok(s.steps.length>=5);}
 for(const bad of [null,'missing','constructor','__proto__','toString',{},undefined]){assert.equal(C.render(bad),'');assert.equal(C.getFrame(bad),null);}
});
check('closed-system account keeps work input negative and conserves every revealed amount',()=>{
 for(let p=0;p<=4;p+=.03125){const m=M.energyState(p);near(m.q,-m.heatOut);near(m.w,-m.workIn);near(m.delta,m.q-m.w);near(m.workIn,m.heatOut+m.delta);near(m.balanceError,0);assert.ok(m.delta>=0);}
 const final=M.energyState(4);near(final.q,-1.2);near(final.w,-6);near(final.delta,4.8);assert.match(C.stories['energy-account'].assumptions,/不表示先通电、后散热/);
});
check('steady wall states conserve common heat rate with actual thickness and k units',()=>{
 for(let p=0;p<=4;p+=.03125){const m=M.wallState(p);near(m.R1,.1);near(m.R2,m.L2/(m.A*m.k2));near(m.rate,40/(m.R1+m.R2));near(m.drop1/m.R1,m.rate);near(m.drop2/m.R2,m.rate);near(m.drop1+m.drop2,40);near(m.interfaceT-m.drop2,20);assert.ok(m.interfaceT>=52&&m.interfaceT<=56);}
 near(M.wallState(0).rate,400/9);near(M.wallState(0).interfaceT,500/9);near(M.wallState(4).rate,80);near(M.wallState(4).interfaceT,52);
});
check('sphere cooling reproduces lesson geometry, Bi, tau, exponential and energy balance',()=>{
 const start=M.coolingState(0);near(start.T,80);near(start.Bi,1/300);near(start.tau,650/3);near(start.V/start.A,.005/3);near(start.capacity,start.rho*start.V*start.c);
 let previous=Infinity;
 for(let p=0;p<=4;p+=.03125){const m=M.coolingState(p);near(m.T,20+60*Math.exp(-m.t/m.tau));near(m.ratio,(m.T-20)/60);near(m.heatLeft+m.heatRemoved,start.capacity*60);assert.ok(m.T>20&&m.T<=previous);previous=m.T;}
 const atTau=M.coolingState(2);near(atTau.t,atTau.tau);near(atTau.ratio,1/Math.E);near(atTau.T,20+60/Math.E);
 // Independent ODE finite difference with physical seconds, not animation time.
 const a=M.coolingState(2-1e-5),b=M.coolingState(2+1e-5);near((b.T-a.T)/(b.t-a.t),-(atTau.T-20)/atTau.tau,3e-7);
});
check('control-volume states match constant-flow mass and water-level balances',()=>{
 for(let p=0;p<=5;p+=.03125){const m=M.massState(p);near(m.mass,20+m.inflow-m.outflow);near(m.inflow,.1*m.time);near(m.outflow,m.time/30);near(m.rise,m.time/3000);near(m.height,m.mass/200);near(m.balanceError,0);assert.equal(m.stopped,false);}
 const end=M.massState(5);near(end.time,300);near(end.mass,40);near(end.inflow,30);near(end.outflow,10);near(end.rise,.1);
});
check('Python trace exposes exact current line, skipped updates, intermediate states and output',()=>{
 const expected=[[3,null,0,0,null],[4,18,0,0,null],[5,18,0,0,null],[4,20,0,0,null],[5,20,0,0,null],[6,20,20,0,null],[7,20,20,1,null],[4,22,20,1,null],[5,22,20,1,null],[6,22,42,1,null],[7,22,42,2,null],[8,22,42,2,null],[9,22,42,2,21]];
 expected.forEach((want,i)=>{const s=M.pythonState(i);assert.deepEqual([s.line,s.value,s.total,s.count,s.output],want);assert.deepEqual(M.pythonState(i+.99),M.pythonState(i));});
 assert.equal(M.pythonState(1000).output,21);assert.equal(M.pythonState(-1).value,null);
});
check('regression uses observation-minus-prediction residuals and freezes fit before new data',()=>{
 const baseline=M.regressionState(1),fit=M.regressionState(2),end=M.regressionState(4);near(baseline.w,0);near(baseline.b,10/3);near(fit.w,1.5);near(fit.b,1/3);near(fit.mse,1/18);near(fit.residualSum,0);fit.residuals.forEach((r,i)=>near(r,[1/6,-1/3,1/6][i]));
 let old=baseline.mse;for(let p=1;p<=2;p+=.03125){const m=M.regressionState(p);near(2*m.w+m.b,10/3);assert.ok(m.mse<=old+1e-10);old=m.mse;}
 for(let p=2;p<=4;p+=.03125){const m=M.regressionState(p);near(m.w,fit.w);near(m.b,fit.b);near(m.mse,fit.mse);}
 near(end.newPrediction,19/3);near(end.newResidual,-7/3);assert.equal(M.regressionState(3.99).showNew,false);assert.equal(end.showNew,true);
});
check('intermediate captions report the current physical or candidate state, not the next milestone',()=>{
 const wall=C.getFrame('wall-resistance',2.5);assert.equal(wall.transition,true);assert.match(wall.formula,/63\.16 W/);assert.match(wall.body,/0\.075 W/);assert.doesNotMatch(wall.formula,/44\.44 W/);
 const cooling=C.getFrame('cooling-time',2.5);assert.equal(cooling.transition,true);assert.match(cooling.body,/325 s/);assert.match(cooling.body,/33\.39°C/);assert.doesNotMatch(cooling.body,/42\.07/);
 const mass=C.getFrame('control-volume',1.5);assert.equal(mass.transition,true);assert.match(mass.body,/90 s/);assert.match(mass.body,/多留下 6 kg/);assert.match(mass.formula,/26 kg/);
 const fit=C.getFrame('regression-fit',1.5);assert.equal(fit.transition,true);assert.match(fit.body,/斜率是 0\.75/);assert.match(fit.formula,/1\.833/);
 for(const id of ['wall-resistance','cooling-time','control-volume','regression-fit'])for(let i=0;i<C.stories[id].steps.length;i++)assert.equal(C.getFrame(id,i).transition,false);
});
check('playback dwells at readable milestones, interpolates afterwards and resumes without jumping',()=>{
 near(M.playbackPosition(0,C.DWELL_MS-1,4),0);near(M.playbackPosition(0,C.DWELL_MS,4),0);near(M.playbackPosition(0,C.STEP_MS,4),1);near(M.playbackPosition(0,C.STEP_MS+C.DWELL_MS-1,4),1);
 near(M.playbackPosition(0,atPosition(1.5),4),1.5);near(M.playbackPosition(1.5,0,4),1.5);near(M.playbackPosition(1.5,(C.STEP_MS-C.DWELL_MS)*.25,4),1.75);near(M.playbackPosition(0,atPosition(1.5),4,true),1);
 for(const id of C.sceneIds){const f=C.getFrame(id,.999999999);assert.equal(f.position,1);assert.equal(f.index,1);assert.equal(f.transition,false);}
});
check('all complete and fractional states render finite named visuals without external assets',()=>{
 for(const id of C.sceneIds){const max=C.stories[id].steps.length-1;for(let p=0;p<=max;p+=.125){const f=C.getFrame(id,p);finiteTree(f.model);assert.ok(f.title&&f.body&&f.formula);assert.match(f.graph,/<svg[^>]*role="img"[^>]*aria-label=/);assert.match(f.graph,/<title>/);assert.doesNotMatch(f.graph+f.metrics,/NaN|Infinity|undefined|<script|<image|<animate|onload=/);renderCases++;}
 for(const p of [NaN,Infinity,-Infinity,-1,1000]){const f=C.getFrame(id,p);finiteTree(f.model);assert.ok(f.position>=0&&f.position<=max);}}
 const code=fs.readFileSync(path.join(__dirname,'../site/assets/concept-stories.js'),'utf8');assert.doesNotMatch(code,/\b(?:fetch|XMLHttpRequest|localStorage|sessionStorage|eval)\s*[.(]/);
});
async function domChecks(){
 const {JSDOM}=require(process.env.ZHIXU_JSDOM_MODULE||'jsdom');
 function app(reduced=false){const dom=new JSDOM('<!doctype html><html><body><textarea id="notes"></textarea></body></html>',{pretendToBeVisual:true,runScripts:'outside-only'}),w=dom.window,d=w.document,frames=new Map(),motionListeners=new Set();let id=0;
  w.requestAnimationFrame=fn=>{frames.set(++id,fn);return id;};w.cancelAnimationFrame=k=>frames.delete(k);const mq={matches:reduced,addEventListener:(_,fn)=>motionListeners.add(fn),removeEventListener:(_,fn)=>motionListeners.delete(fn)};w.matchMedia=()=>mq;
  for(const f of ['labs.js','foundation-labs.js','concept-stories.js'])w.eval(fs.readFileSync(path.join(__dirname,'../site/assets',f),'utf8'));
  return {dom,w,d,frames,motionListeners,mq,advance:now=>{const fns=[...frames.values()];frames.clear();fns.forEach(fn=>fn(now));},add:(id,host=false)=>{const el=d.createElement(host?'div':'section');d.body.append(el);if(host){const dispose=w.ConceptStories.mount(el,id);return {el:el.firstElementChild,host:el,dispose};}el.innerHTML=w.ConceptStories.render(id);const node=el.firstElementChild;const dispose=w.ConceptStories.mount(node,id);return {el:node,host:el,dispose};}};
 }
 const a=app();
 for(const id of C.sceneIds){const {el,dispose}=a.add(id),q=s=>el.querySelector(s),max=C.stories[id].steps.length-1;
  assert.equal(a.frames.size,0);assert.equal(q('[data-story-action=play]').getAttribute('aria-pressed'),'false');assert.equal(el.dataset.storyPosition,'0');assert.ok(q('h2'));assert.ok(q('svg title'));assert.ok(q('[data-story-progress]').closest('label'));
  for(let i=1;i<=max;i++){q('[data-story-action=next]').click();assert.equal(+el.dataset.storyPosition,i);assert.equal(q('[data-story-progress]').value,String(i));}
  assert.equal(q('[data-story-action=next]').disabled,true);q('[data-story-action=previous]').click();assert.equal(+el.dataset.storyPosition,max-1);q('[data-story-action=replay]').click();assert.equal(+el.dataset.storyPosition,0);assert.equal(q('[data-story-action=previous]').disabled,true);
  q('[data-story-action=play]').click();assert.equal(a.frames.size,1);a.advance(0);a.advance(atPosition(1.5));const pos=+el.dataset.storyPosition;assert.ok(pos>0&&pos<max);if(['python-loop','energy-account'].includes(id))assert.ok(Number.isInteger(pos));else assert.equal(pos,1.5);
  q('[data-story-action=play]').click();assert.equal(a.frames.size,0);a.advance(100000);assert.equal(+el.dataset.storyPosition,pos);
  const range=q('[data-story-progress]');range.value='1';range.dispatchEvent(new a.w.Event('input'));assert.equal(+el.dataset.storyPosition,1);assert.equal(a.frames.size,0);
  q('[data-story-action=play]').click();q('[data-story-action=replay]').click();assert.equal(a.frames.size,0);assert.equal(+el.dataset.storyPosition,0);assert.equal(q('[data-story-action=play]').getAttribute('aria-pressed'),'false');
  q('[data-story-action=play]').click();a.advance(0);a.advance(C.STEP_MS*max+1);assert.equal(+el.dataset.storyPosition,max);assert.equal(a.frames.size,0);assert.match(q('.story-status').textContent,/结束/);
  dispose();dispose();q('[data-story-action=play]').click();assert.equal(a.frames.size,0);el.parentElement.remove();
 }
 check('all six DOM players have accessible manual controls, deterministic playback, pause, end and paused replay',()=>assert.equal(a.frames.size,0));
 const repeated=a.add('cooling-time',true);repeated.el.querySelector('[data-story-action=play]').click();assert.equal(a.frames.size,1);const nextDispose=a.w.ConceptStories.mount(repeated.host,'cooling-time');assert.equal(a.frames.size,0);assert.equal(a.motionListeners.size,1);nextDispose();assert.equal(a.motionListeners.size,0);repeated.host.remove();
 check('repeated mounting disposes old host/section timers and media listeners immediately',()=>assert.equal(a.frames.size,0));
 const swapped=a.add('cooling-time');swapped.el.querySelector('[data-story-action=play]').click();const swapDispose=a.w.ConceptStories.mount(swapped.el,'control-volume');assert.equal(a.frames.size,0);assert.equal(swapped.el.dataset.storyId,'control-volume');assert.equal(swapped.el.querySelectorAll('.concept-story').length,0);assert.match(swapped.el.querySelector('.story-title').textContent,/流进减流出/);swapDispose();swapped.host.remove();
 check('reusing a story section with a different ID resets it without nested stories or leaked timers',()=>assert.equal(a.frames.size,0));
 const removed=a.add('control-volume');removed.el.querySelector('[data-story-action=play]').click();removed.host.remove();await Promise.resolve();assert.equal(a.frames.size,0);assert.equal(a.motionListeners.size,0);
 check('DOM removal cancels playback and disposes listeners',()=>assert.equal(a.frames.size,0));
 const caption=a.add('cooling-time');caption.el.querySelector('[data-story-action=play]').click();a.advance(0);a.advance(atPosition(2.5));assert.match(caption.el.querySelector('.story-step-body').textContent,/325 s/);a.advance(atPosition(2.75));assert.match(caption.el.querySelector('.story-step-body').textContent,/379\.2 s/);assert.equal(caption.el.querySelector('[data-story-progress]').value,'2');assert.match(caption.el.querySelector('[data-story-progress]').getAttribute('aria-valuetext'),/第 3 步/);caption.dispose();
 check('fractional DOM captions update within the same step and slider values match accessibility text',()=>assert.equal(a.frames.size,0));
 const visibility=a.add('cooling-time');visibility.el.querySelector('[data-story-action=play]').click();Object.defineProperty(a.d,'hidden',{configurable:true,value:true});a.d.dispatchEvent(new a.w.Event('visibilitychange'));assert.equal(a.frames.size,0);Object.defineProperty(a.d,'hidden',{configurable:true,value:false});a.d.dispatchEvent(new a.w.Event('visibilitychange'));assert.equal(a.frames.size,0);visibility.el.querySelector('[data-story-action=play]').click();a.w.dispatchEvent(new a.w.Event('pagehide'));assert.equal(a.frames.size,0);visibility.dispose();
 check('hidden page and pagehide pause without automatic resumption',()=>assert.equal(a.frames.size,0));
 const preference=a.add('wall-resistance');preference.el.querySelector('[data-story-action=play]').click();a.advance(0);a.advance(atPosition(1.25));assert.equal(+preference.el.dataset.storyPosition,1.25);for(const fn of a.motionListeners)fn({matches:true});assert.equal(a.frames.size,0);assert.equal(+preference.el.dataset.storyPosition,1);preference.dispose();
 check('changing reduced-motion preference cancels an active interpolation and shows a whole step',()=>assert.equal(a.frames.size,0));
 const reduced=app(true);for(const id of C.sceneIds){const {el,dispose}=reduced.add(id);assert.equal(reduced.frames.size,0);assert.match(el.querySelector('.story-status').textContent,/默认静止/);el.querySelector('[data-story-action=play]').click();reduced.advance(0);reduced.advance(atPosition(1.5));assert.equal(+el.dataset.storyPosition,1);el.querySelector('[data-story-action=replay]').click();assert.equal(reduced.frames.size,0);assert.equal(+el.dataset.storyPosition,0);dispose();}
 check('reduced motion starts static and only explicitly plays whole semantic states',()=>assert.equal(reduced.frames.size,0));
 // Verify input and callbacks outside the widget remain untouched during playback.
 const note=a.d.getElementById('notes');let noteEvents=0;note.addEventListener('input',()=>noteEvents++);const active=a.add('cooling-time');active.el.querySelector('[data-story-action=play]').click();note.value='保留我的笔记';note.dispatchEvent(new a.w.Event('input'));a.advance(0);a.advance(1000);assert.equal(note.value,'保留我的笔记');assert.equal(noteEvents,1);active.dispose();
 check('story updates leave unrelated note inputs/listeners intact',()=>assert.equal(noteEvents,1));
 for(const id of C.sceneIds){for(let i=0;i<C.stories[id].steps.length;i++){const f=C.getFrame(id,i),fragment=a.d.createElement('div');fragment.innerHTML=f.graph;const raw=fragment.querySelector('svg').outerHTML,parsed=new a.w.DOMParser().parseFromString(raw,'image/svg+xml');assert.equal(parsed.querySelector('parsererror'),null);if(id==='python-loop')assert.equal(fragment.querySelectorAll('[aria-current=step]').length,1);}}
 check('every integer-frame SVG is well-formed and Python has one current code line',()=>{});
 a.dom.window.close();reduced.dom.window.close();
}
const numericalChecks=checks;
if(process.argv.includes('--dom'))domChecks().then(()=>console.log(JSON.stringify({models:'passed',numericalChecks,renderCases,dom:'passed',domChecks:checks-numericalChecks,scenes:6}))).catch(e=>{console.error(e);process.exitCode=1;});
else console.log(JSON.stringify({models:'passed',numericalChecks,renderCases,dom:'not requested',scenes:6}));
