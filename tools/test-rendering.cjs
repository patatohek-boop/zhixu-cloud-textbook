const {JSDOM,VirtualConsole}=require(process.env.ZHIXU_JSDOM_MODULE || 'jsdom');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../site');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const scripts=[...html.matchAll(/<script defer src="([^"]+)"/g)].map(x=>x[1].split('?')[0]);
const hostile='</textarea><img src=x onerror="alert(1)"><script>alert(1)</script>';
function app(hash='',stored,android=false){
 const dom=new JSDOM(html,{url:(android?'https://appassets.androidplatform.net/assets/www/index.html':'https://example.test/textbook/')+hash,runScripts:'outside-only',virtualConsole:new VirtualConsole()});
 const w=dom.window;w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};
 if(stored)w.localStorage.setItem('zhixu-learning-v1',JSON.stringify(stored));
 for(const file of scripts){
  if(android&&file==='assets/app.js')w.eval(fs.readFileSync(path.join(root,'../android/web/android-adapter.js'),'utf8'));
  w.eval(fs.readFileSync(path.join(root,file),'utf8'));
 }
 return dom;
}
const dom=app('#/course/calculus/calculus-03',{notes:{'calculus-03':hostile},answers:{'calculus-03':null}}),w=dom.window,d=w.document;
assert.equal(d.querySelector('#note-text').value,hostile);
assert.equal(d.querySelectorAll('#my-notes img,#my-notes script').length,0);
assert.equal(d.querySelectorAll('.math-error').length,0);
assert.ok(d.querySelectorAll('#lesson-body .katex').length>10);
assert.ok(d.querySelectorAll('#lesson-body figure img').length>=1);
assert.ok(d.querySelectorAll('#lesson-body details').length>=2);
assert.ok(d.querySelectorAll('#mobile-toc-list [data-scroll]').length>3);
assert.ok(d.querySelector('.prereq a[href^="#/course/"]'));
const h=d.querySelector('[data-param=h]');h.value='.1';h.dispatchEvent(new w.Event('input'));
assert.match(d.querySelector('.lab-result').textContent,/1\.500/);
d.querySelector('[data-answer="2"]').click();assert.match(d.querySelector('#feedback').textContent,/回答正确/);
const attacks=[
 '<img src=x onerror=alert(1)>','<svg onload=alert(1)>',
 '<a href="javascript:alert(1)">run</a>','[run](javascript:alert%281%29)',
 '<iframe srcdoc="<script>alert(1)</script>"></iframe>',
 '<form action="https://example.invalid"><input name="notes"></form>',
 '<style>body{display:none}</style><object data="https://example.invalid"></object>',
 '<a title="$x$" href="javascript:alert(1)">link</a>',
 '$\\href{javascript:alert(1)}{click}$',
 '<svg><a xlink:href="javascript:alert(1)">x</a></svg>',
 '<math><mtext><table><mglyph><style><!--</style><img title="--><img src=x onerror=alert(1)>">',
 '<div id="__proto__"><a name="constructor">text</a></div>',
];
for(const payload of attacks){
 const fragment=JSDOM.fragment(w.ZHIXU.markdown(payload));
 assert.equal(fragment.querySelectorAll('script,style,iframe,object,embed,form,input,base,meta,link').length,0);
 for(const el of fragment.querySelectorAll('*'))for(const attr of el.attributes){
  assert.ok(!/^on/i.test(attr.name));
  if(/^(href|src|xlink:href)$/i.test(attr.name))assert.ok(!/^\s*(javascript|vbscript):/i.test(attr.value));
 }
}
let formulas=0,lessons=0;
for(const course of w.COURSES)for(const l of course.chapters){
 lessons++;
 const practice=(w.MASTERY_EXERCISES||[]).filter(e=>e.lessonId===l.id);
 for(const s of [l.content,l.quiz.question,...l.quiz.options,l.quiz.explanation,...practice.flatMap(e=>[e.prompt,e.solution,e.technique,e.pitfall,...e.checkpoints])]){
  const fragment=JSDOM.fragment(w.ZHIXU.markdown(s));
  assert.equal(fragment.querySelectorAll('.math-error').length,0,l.id);
  const textNodes=fragment.ownerDocument.createTreeWalker(fragment,4);
  let textNode;
  while((textNode=textNodes.nextNode())){
   if(textNode.parentElement?.closest('pre,code,.katex,math'))continue;
   assert.ok(!textNode.nodeValue.includes('**'),l.id+' has unparsed bold delimiters: '+textNode.nodeValue.trim());
  }
  formulas+=fragment.querySelectorAll('.katex').length;
 }
}
assert.equal(lessons,w.TEXTBOOK_VERSION.lessons);assert.ok(lessons>182);
assert.ok(formulas>1265,'The expanded textbook must retain and extend the original mathematical content');
assert.equal(w.TEXTBOOK_VERSION.version,JSON.parse(fs.readFileSync(path.join(root,'../version.json'),'utf8')).version);
w.location.hash='#/simulation';w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.equal(d.querySelectorAll('.simulation-stage').length,6);
assert.equal(d.querySelectorAll('.simulation-stage .research-lessons a').length,24);
assert.ok(d.querySelector('[data-nav=simulation]').classList.contains('active'));
for(const stage of w.SimulationGuide.stages)for(const id of stage.ids)assert.ok(w.ZHIXU.all.some(l=>l.id===id));
for(const id of ['cfd-upwind','cfd-yplus','cfd-grid','cfd-cht']){
 w.location.hash='#/labs/'+id;w.dispatchEvent(new w.HashChangeEvent('hashchange'));
 assert.ok(d.querySelector('.lab-chart svg'));
 const before=d.querySelector('.lab-result').textContent,input=d.querySelector('[data-param]');
 input.value=input.max;input.dispatchEvent(new w.Event('input'));
 assert.notEqual(d.querySelector('.lab-result').textContent,before);
 assert.ok(!/NaN|Infinity|undefined/.test(d.querySelector('.lab-result').textContent));
 d.querySelector('.lab-next').click();assert.match(d.querySelector('.lab-step-count').textContent,/2 \/ 3/);
 d.querySelector('.lab-preset').click();d.querySelector('.lab-reset').click();
 assert.equal(d.querySelector('.lab-result').textContent,before);
}
w.location.hash='#/course/fluid-mechanics/fluid-mechanics-04';w.dispatchEvent(new w.HashChangeEvent('hashchange'));
const conceptHeadings=[...d.querySelectorAll('#lesson-body h3')];
assert.ok(conceptHeadings.some(h=>h.textContent.includes('压力中心')));
assert.equal(d.querySelectorAll('#toc .toc-concept').length,conceptHeadings.length);
assert.equal(d.querySelectorAll('#mobile-toc-list .toc-concept').length,conceptHeadings.length);
assert.equal(new Set([...d.querySelectorAll('#lesson-body h2, #lesson-body h3')].map(h=>h.id)).size,d.querySelectorAll('#lesson-body h2, #lesson-body h3').length);
let scrolledTo;
w.HTMLElement.prototype.scrollIntoView=function(){scrolledTo=this.id;};
const conceptLink=d.querySelector('#mobile-toc-list .toc-concept');
conceptLink.click();
assert.equal(scrolledTo,conceptLink.dataset.scroll);
assert.equal(w.location.hash,'#/course/fluid-mechanics/fluid-mechanics-04','concept navigation must stay in the current lesson');
assert.match(d.getElementById(scrolledTo).textContent,/形心/);
w.HTMLElement.prototype.scrollIntoView=()=>{};
w.location.hash='#/review/fluid-mechanics/fluid-mechanics-30';w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.ok(d.querySelector('#review-fluid-mechanics-30').open);
assert.equal(d.querySelectorAll('.review-record').length,w.COURSES.find(c=>c.id==='fluid-mechanics').chapters.length);
assert.ok(d.querySelectorAll('.review-map a[href^="#/course/fluid-mechanics/"]').length>=35);
const audit=w.CONTENT_REVIEW.find(a=>a.course_id==='fluid-mechanics');audit.records[0].changes.push(hostile);
w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.equal(d.querySelectorAll('.review-page img,.review-page script').length,0);
assert.ok(d.querySelector('.review-record-body').textContent.includes(hostile));
audit.records[0].changes.pop();
for(const course of w.COURSES){
 w.location.hash='#/review/'+course.id;w.dispatchEvent(new w.HashChangeEvent('hashchange'));
 assert.equal(d.querySelectorAll('.review-record').length,course.chapters.length);
 assert.ok(!d.querySelector('#main').textContent.includes('[object Object]'),course.id+' added topics must be readable');
 const review=w.CONTENT_REVIEW.find(a=>a.course_id===course.id);
 for(const t of review.added_topics)assert.ok(d.querySelector('#main').textContent.includes(typeof t==='string'?t:t.title));
}
// The research route must resolve every prerequisite and preserve shared progress.
w.location.hash='#/research';w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.equal(d.querySelectorAll('.research-stage').length,6);
assert.ok(d.querySelector('[data-nav=research]').classList.contains('active'));
for(const stage of w.ResearchGuide.stages){
 for(const id of stage.ids)assert.ok(w.ZHIXU.all.some(l=>l.id===id),'Missing research prerequisite '+id);
 assert.ok(Object.hasOwn(w.LABS,stage.lab),'Missing research lab '+stage.lab);
}
for(const a of d.querySelectorAll('.research-lessons a')){
 const [,course,id]=a.getAttribute('href').split('/').slice(1);
 assert.ok(w.COURSES.some(c=>c.id===course&&c.chapters.some(l=>l.id===id)),'Broken research route '+a.href);
}
const record=w.ZHIXU.all.find(l=>l.id==='machine-learning-36');
const originalTitle=record.title;
const source=w.COURSES.find(c=>c.id==='machine-learning').chapters.find(l=>l.id===record.id);
source.title=hostile;w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.equal(d.querySelectorAll('.research-page img,.research-page script').length,0);
assert.ok(d.querySelector('.research-page').textContent.includes(hostile));
source.title=originalTitle;
const progress=JSON.parse(w.ZHIXU.exportBackup());progress.completed.push('machine-learning-36');
assert.equal(w.ZHIXU.importBackup(progress).ok,true);
assert.equal(d.querySelector('a[href="#/course/machine-learning/machine-learning-36"] .research-check').textContent,'✓');
assert.equal(d.querySelector('.research-hero .primary').getAttribute('href'),'#/course/machine-learning/machine-learning-37');
w.location.hash='#/notebook';w.dispatchEvent(new w.HashChangeEvent('hashchange'));
assert.equal(d.querySelectorAll('.saved-row img,.saved-row script').length,0);
assert.ok(d.querySelector('.saved-row').textContent.includes(hostile));
dom.window.close();
for(const id of ['__proto__','constructor','toString']){
 const invalid=app('#/labs/'+id);assert.ok(invalid.window.document.querySelector('.labs-index'));invalid.window.close();
}
for(const stored of [{answers:{'calculus-03':null},notes:[]},{answers:{'calculus-03':{choice:99}},font:{},completed:{}}]){
 const broken=app('#/course/calculus/calculus-03',stored);assert.ok(broken.window.document.querySelector('#lesson-body'));broken.window.close();
}

// The native wrapper and webpage use the same synchronous, transactional backup API.
const backupDom=app('#/course/calculus/calculus-03'),bw=backupDom.window,bd=bw.document,api=bw.ZHIXU;
const note=bd.querySelector('#note-text');note.value='尚未等待自动保存的笔记';note.dispatchEvent(new bw.Event('input'));
const backup=api.exportBackup();assert.equal(typeof backup,'string');
const parsed=JSON.parse(backup);assert.equal(parsed.format,'zhixu-learning');assert.equal(parsed.version,1);
assert.equal(parsed.notes['calculus-03'],note.value);
assert.equal(JSON.parse(bw.localStorage.getItem('zhixu-learning-v1')).notes['calculus-03'],note.value);
const imported={...parsed,notes:{'calculus-03':hostile},completed:['calculus-03']};
const merged=api.importBackup(JSON.stringify(imported));assert.equal(merged.ok,true);assert.equal(merged.merged,1);
assert.equal(bd.querySelectorAll('#my-notes img,#my-notes script').length,0);
assert.ok(bd.querySelector('#note-text').value.includes(hostile));
assert.ok(api.state.completed.includes('calculus-03'));
assert.equal(api.importBackup(imported).merged,0,'reimport must not duplicate a merged note');
const liveBefore=JSON.stringify(api.state),storedBefore=bw.localStorage.getItem('zhixu-learning-v1');
for(const input of ['{bad',{},' '.repeat(10000001),{...parsed,notes:{'calculus-03':false}}]){
 assert.equal(api.importBackup(input).ok,false);
 assert.equal(JSON.stringify(api.state),liveBefore);assert.equal(bw.localStorage.getItem('zhixu-learning-v1'),storedBefore);
}
const setItem=bw.Storage.prototype.setItem;
bw.Storage.prototype.setItem=()=>{throw Error('quota exceeded');};
const failed=api.importBackup({...parsed,notes:{'calculus-03':'写入失败不应追加'}});
assert.equal(failed.ok,false);assert.match(failed.error,/原记录未更改/);
assert.equal(JSON.stringify(api.state),liveBefore);assert.equal(bw.localStorage.getItem('zhixu-learning-v1'),storedBefore);
assert.equal(api.flush(),false);
bw.Storage.prototype.setItem=setItem;assert.equal(api.flush(),true);
const searchDialog=bd.querySelector('#search-dialog');searchDialog.close=()=>searchDialog.removeAttribute('open');searchDialog.setAttribute('open','');
assert.equal(api.handleBack(),true);assert.equal(searchDialog.open,false);
bd.querySelector('#menu').click();assert.equal(api.handleBack(),true);assert.ok(!bd.querySelector('#course-sidebar').classList.contains('open'));
bd.querySelector('#focus').click();assert.equal(api.handleBack(),true);assert.ok(!bd.body.classList.contains('focus'));
assert.equal(api.handleBack(),false);
backupDom.window.close();

const androidDom=app('#/notebook',undefined,true),aw=androidDom.window,ad=aw.document;
assert.equal(aw.ZhixuAndroid.isApp,true);assert.match(ad.querySelector('#main').textContent,/与网站不自动同步/);
let webpageHandlerRan=false;ad.querySelector('#export').onclick=()=>{webpageHandlerRan=true;};
const exportEvent=new aw.MouseEvent('click',{bubbles:true,cancelable:true});ad.querySelector('#export').dispatchEvent(exportEvent);
assert.equal(exportEvent.defaultPrevented,true);assert.equal(webpageHandlerRan,false);
aw.ZhixuAndroid.notify(hostile);assert.equal(ad.querySelector('#toast').textContent,hostile);assert.equal(ad.querySelectorAll('#toast img,#toast script').length,0);
aw.location.hash='#/about';aw.dispatchEvent(new aw.HashChangeEvent('hashchange'));
assert.match(ad.querySelector('#main').textContent,/安装包内置的教材版本/);
assert.match(ad.querySelector('#main').textContent,/独立本地存储/);
assert.ok(!ad.querySelector('#main').textContent.includes('其他项目共享本地存储边界'));
androidDom.window.close();
console.log(JSON.stringify({attack_payloads:attacks.length,lessons,formulas,notes:'escaped',invalid_routes:'handled',lab:'updated',quiz:'correct',backup_api:'transactional',android_adapter:'isolated',back_handler:'passed',status:'passed'},null,2));
