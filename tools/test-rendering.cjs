const {JSDOM,VirtualConsole}=require(process.env.ZHIXU_JSDOM_MODULE || 'jsdom');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../site');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const scripts=[...html.matchAll(/<script defer src="([^"]+)"/g)].map(x=>x[1]);
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
assert.equal(d.querySelectorAll('#lesson-body figure img').length,1);
assert.equal(d.querySelectorAll('#lesson-body details').length,2);
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
 for(const s of [l.content,l.quiz.question,...l.quiz.options,l.quiz.explanation]){
  const fragment=JSDOM.fragment(w.ZHIXU.markdown(s));
  assert.equal(fragment.querySelectorAll('.math-error').length,0,l.id);
  formulas+=fragment.querySelectorAll('.katex').length;
 }
}
assert.equal(lessons,182);assert.equal(formulas,1265);
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
