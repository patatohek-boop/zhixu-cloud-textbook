const {JSDOM,VirtualConsole}=require(process.env.ZHIXU_JSDOM_MODULE || 'jsdom');
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'../site');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const scripts=[...html.matchAll(/<script defer src="([^"]+)"/g)].map(x=>x[1]);
const hostile='</textarea><img src=x onerror="alert(1)"><script>alert(1)</script>';
function app(hash='',stored){
 const dom=new JSDOM(html,{url:'https://example.test/textbook/'+hash,runScripts:'outside-only',virtualConsole:new VirtualConsole()});
 const w=dom.window;w.scrollTo=()=>{};w.HTMLElement.prototype.scrollIntoView=()=>{};
 if(stored)w.localStorage.setItem('zhixu-learning-v1',JSON.stringify(stored));
 for(const file of scripts)w.eval(fs.readFileSync(path.join(root,file),'utf8'));
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
console.log(JSON.stringify({attack_payloads:attacks.length,lessons,formulas,notes:'escaped',invalid_routes:'handled',lab:'updated',quiz:'correct',status:'passed'},null,2));
