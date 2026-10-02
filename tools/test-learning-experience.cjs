const {JSDOM,VirtualConsole}=require(process.env.ZHIXU_JSDOM_MODULE||'jsdom');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../site'),html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const scripts=[...html.matchAll(/<script defer src="([^"]+)"/g)].map(x=>x[1].split('?')[0]);
function app(hash,stored){const dom=new JSDOM(html,{url:'https://example.test/textbook/'+hash,runScripts:'outside-only',virtualConsole:new VirtualConsole()});const w=dom.window;w.scrollTo=()=>{};w.HTMLDialogElement.prototype.showModal=function(){this.open=true;};w.HTMLDialogElement.prototype.close=function(){this.open=false;this.dispatchEvent(new w.Event('close'));};w.HTMLElement.prototype.scrollIntoView=()=>{};w.matchMedia=()=>({matches:true,addEventListener(){},removeEventListener(){}});if(stored)w.localStorage.setItem('zhixu-learning-v1',JSON.stringify(stored));for(const s of scripts)w.eval(fs.readFileSync(path.join(root,s),'utf8'));return dom;}
const original={notes:{'calculus-03':'旧笔记 <&> 内容'},bookmarks:['calculus-03'],completed:['calculus-01'],answers:{'calculus-03':{choice:2,correct:true,at:'2026-10-02T00:00:00Z'}},font:20,theme:'dark',last:'calculus-03'};
const dom=app('#/course/calculus/calculus-03',original),w=dom.window,d=w.document;
function route(hash){w.location.hash=hash;w.dispatchEvent(new w.HashChangeEvent('hashchange'));}
assert.equal(d.querySelector('#note-text').value,original.notes['calculus-03']);assert.ok(d.body.classList.contains('dark'));
assert.equal(d.querySelector('#bookmark').getAttribute('aria-pressed'),'true');assert.equal(d.querySelector('#reading-depth').getAttribute('aria-expanded'),'false');
const depth=d.querySelector('#reading-depth');depth.click();assert.ok([...d.querySelectorAll('details.advanced-reading')].every(n=>n.open));depth.click();assert.ok([...d.querySelectorAll('details.advanced-reading')].every(n=>!n.open));
let printed=false;w.print=()=>{printed=true;assert.ok([...d.querySelectorAll('.prose details')].every(n=>n.open),'Print opens both proofs and solutions');};d.querySelector('#print').click();assert.ok(printed);d.querySelectorAll('.prose details').forEach(n=>n.open=false);
const advanced=d.querySelector('details.advanced-reading h2');const toc=[...d.querySelectorAll('#mobile-toc-list a')].find(a=>a.dataset.scroll===advanced.id);toc.click();assert.ok(advanced.closest('details').open);assert.equal(w.location.hash,'#/course/calculus/calculus-03');
const diagram=d.querySelector('#lesson-body figure a');diagram.click();assert.ok(w.FigureViewer.isOpen());const viewer=d.querySelector('#figure-dialog');const initialZoom=viewer.querySelector('#figure-zoom').textContent;viewer.querySelector('[data-figure-zoom=in]').click();assert.notEqual(viewer.querySelector('#figure-zoom').textContent,initialZoom);assert.ok(w.ZHIXU.handleBack());assert.ok(!w.FigureViewer.isOpen());assert.equal(w.location.hash,'#/course/calculus/calculus-03');
route('#/map');assert.equal(d.querySelectorAll('.map-course-card').length,7);
for(const course of w.COURSES){
 route('#/map/'+course.id);assert.equal(d.querySelectorAll('[data-node-id]').length,course.chapters.length);
 const filter=d.querySelector('#map-filter');for(const tier of ['mainline','foundation','advanced','all']){filter.value=tier;filter.dispatchEvent(new w.Event('change'));for(const n of d.querySelectorAll('[data-node-id]'))assert.equal(n.hidden,tier!=='all'&&n.dataset.tier!==tier);}
 for(const l of course.chapters){route('#/map/'+course.id+'/'+l.id);assert.ok(d.querySelector('.dependency-current').textContent.includes(l.title));}
}
route('#/path');assert.equal(d.querySelectorAll('.core-route>li').length,26);
for(const g of w.LEARNING_GUIDES){const c=w.COURSES.find(c=>c.chapters.some(l=>l.id===g.id));route('#/course/'+c.id+'/'+g.id);assert.ok(d.querySelector('.reader-setup'));assert.ok(d.querySelector('.knowledge-context.compact'));assert.equal(d.querySelectorAll('.math-error').length,0);assert.ok(d.querySelector('#lesson-body figure img'),'An anchor needs a meaningful visual '+g.id);assert.ok(d.querySelectorAll('#lesson-body details').length>=3);}
for(const [course,id,lab] of [['thermodynamics','thermodynamics-05','foundation-energy'],['linear-algebra','linear-algebra-10','foundation-projection'],['fluid-mechanics','fluid-mechanics-07','foundation-mass']]){route('#/course/'+course+'/'+id);assert.equal(d.querySelector('#interactive-lab').dataset.lab,lab);assert.ok(d.querySelector('#interactive-lab .lab-chart svg'));assert.ok(d.querySelector('#mobile-toc-list [data-scroll="interactive-lab"]'));}
for(const [lesson,id] of Object.entries(w.ConceptStories.lessonMap)){
 const c=w.COURSES.find(c=>c.chapters.some(l=>l.id===lesson));route('#/course/'+c.id+'/'+lesson);
 const story=d.querySelector('.concept-story');assert.ok(story,'Missing integrated story '+lesson);assert.ok(story.querySelector('svg'));assert.equal(story.querySelector('[data-story-action=play]').getAttribute('aria-pressed'),'false');
 const before=story.textContent;story.querySelector('[data-story-action=next]').click();assert.notEqual(story.textContent,before);story.querySelector('[data-story-action=replay]').click();assert.equal(story.querySelector('[data-story-action=play]').getAttribute('aria-pressed'),'false');
 const h=story.querySelector('h2');assert.ok(h,'A story needs a static h2 in the lesson outline');assert.ok(d.querySelector('#mobile-toc-list [data-scroll="'+h.id+'"]'));
 const old=story;route('#/map');assert.equal(old.isConnected,false);old.querySelector('[data-story-action=play]').click();assert.equal(old.querySelector('[data-story-action=play]').getAttribute('aria-pressed'),'false','Detached story listeners must be disposed');
}
route('#/course/calculus/calculus-03');assert.equal(d.querySelector('#note-text').value,original.notes['calculus-03']);const persisted=JSON.parse(w.localStorage.getItem('zhixu-learning-v1'));assert.equal(persisted.notes['calculus-03'],original.notes['calculus-03']);assert.ok(persisted.bookmarks.includes('calculus-03'));assert.ok(persisted.completed.includes('calculus-01'));
route('#/map/no-such-course');assert.match(d.querySelector('#main').textContent,/没有找到/);route('#/map/calculus/python-01');assert.match(d.querySelector('#main').textContent,/没有找到/);
dom.window.close();console.log('Learning experience DOM: 253 local map nodes, 26 anchors, filters, dependency flows, progressive disclosure, original records, 3 lab integrations, 6 disposed story integrations and invalid routes passed');
