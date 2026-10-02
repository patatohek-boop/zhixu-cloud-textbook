/* Layered, accessible knowledge framework. Every lesson keeps its original ID.
   Required edges are curated; legacy prerequisite labels are reading suggestions. */
(function(root){
'use strict';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const lessonURL=n=>'#/course/'+n.course.id+'/'+n.id;
const mapURL=(c,id)=>'#/map/'+c+(id?'/'+id:'');
const stageSpecs=[
 {title:'先有工具',note:'三条工具线可以并行。需要哪种计算，就先补对应概念。',ids:['calculus','linear-algebra','python']},
 {title:'再解释物理过程',note:'能量守恒先抓住“多少”，流动与传热再解释“怎样变化”。',ids:['thermodynamics','fluid-mechanics','heat-transfer']},
 {title:'最后用数据建模',note:'先定义任务、隔离测试数据，再理解模型与误差。',ids:['machine-learning']}
];
const bridgeSpecs=[
 ['calculus','heat-transfer','变化率与累积 → 温度变化、热流与能量平衡'],
 ['thermodynamics','heat-transfer','能量守恒 → 建立传热问题的收支式'],
 ['fluid-mechanics','heat-transfer','流量与流态 → 理解流动带走的能量'],
 ['linear-algebra','machine-learning','向量与投影 → 最小二乘与模型参数'],
 ['calculus','machine-learning','导数与偏导 → 损失怎样随参数改变'],
 ['python','machine-learning','函数与数组 → 复现计算并检查数据']
];
function model(courses,guides=[]){
 const nodes=courses.flatMap(c=>c.chapters.map((l,index)=>({...l,course:c,index}))),byId=new Map(nodes.map(n=>[n.id,n])),byTitle=new Map(),guideById=new Map(guides.map(g=>[g.id,g]));
 nodes.forEach(n=>{if(!byTitle.has(n.title))byTitle.set(n.title,[]);byTitle.get(n.title).push(n);});
 const resolve=(text,n)=>byId.get(text)||byTitle.get(text)?.find(x=>x.course.id===n.course.id)||(byTitle.get(text)?.length===1?byTitle.get(text)[0]:null);
 nodes.forEach(n=>{
  const guide=guideById.get(n.id);n.guide=guide;n.tier=guide?.mainline?'mainline':n.level==='基础'?'foundation':'advanced';
  n.required=(guide?.required||[]).map(id=>byId.get(id)).filter(Boolean);
  const suggested=guide?guide.recommended:(n.prerequisites||[]).map(t=>resolve(t,n)?.id).filter(Boolean);
  n.recommended=[...new Set(suggested||[])].filter(id=>id!==n.id&&!n.required.some(r=>r.id===id)).map(id=>byId.get(id)).filter(Boolean);
  n.background=(n.prerequisites||[]).filter(t=>!resolve(t,n));
 });
 return {courses,nodes,byId,guideById};
}
const tierText={mainline:'先学这些',foundation:'补基础',advanced:'以后再学'};
function badge(n){return `<span class="map-badge ${n.tier}">${tierText[n.tier]}</span>`;}
function link(n,completed,kind='read'){return `<a href="${kind==='map'?mapURL(n.course.id,n.id):lessonURL(n)}" data-lesson-id="${esc(n.id)}">${esc(n.title)}${completed.includes(n.id)?'<span class="map-done"> · 已完成</span>':''}</a>`;}
function relationList(nodes,completed){return nodes.length?`<ul>${nodes.map(n=>`<li>${link(n,completed)} <span class="muted small">${esc(n.course.title)}</span></li>`).join('')}</ul>`:'<p class="muted small">这里没有另外列课文，先看看这节的学习目标。</p>';}
function dependencyFlow(m,n,completed){
 const after=m.nodes.filter(x=>x.required.some(r=>r.id===n.id));
 const start=n.required.length||n.recommended.length;
 return `<section class="dependency-flow" aria-label="这节前后怎么学"><h3>先学什么，学会后再去哪</h3><div class="dependency-lanes"><div class="dependency-inputs">${n.required.length?`<div class="dependency-source required"><b>要先会的基础</b>${relationList(n.required,completed)}<span class="edge-label">必须先会 →</span></div>`:''}${n.recommended.length?`<div class="dependency-source recommended"><b>按需补一补</b>${relationList(n.recommended,completed)}<span class="edge-label">建议补读 ⇢</span></div>`:''}${!start?'<p class="muted small">没有列出课内连接；不代表没有课外基础要求。</p>':''}</div><div class="dependency-current"><span class="small">你正在看</span><strong>${esc(n.title)}</strong><a class="text-link" href="${lessonURL(n)}">读这一节 →</a></div><div class="dependency-output"><span class="edge-label">学会这节后，再学 →</span>${after.length?relationList(after,completed):'<p class="muted small">这里还没列出后续课程；可回课程图继续选择。</p>'}</div></div><p class="small muted">线告诉你这些课怎么接起来。已经会的内容可以跳过，不熟的先补。实线框里的基础要先会，虚线框里的内容按需要看。</p></section>`;
}
function context(m,n,completed,{compact=false}={}){
 const next=m.nodes.filter(x=>x.required.some(r=>r.id===n.id));
 return `${compact?'<details class="knowledge-context compact"><summary>不会的地方，先补这些课</summary><div class="context-body">':'<section class="knowledge-context" aria-label="这节前后怎么学">'}<div class="section-heading"><h2>这节能帮你学什么？</h2>${badge(n)}</div>${n.guide?`<p>${esc(n.guide.why)}</p><p class="map-checkpoint"><b>学完能做什么：</b>${esc(n.guide.checkpoint)}</p>`:'<p class="muted small">先看看这节要学什么。有不熟悉的地方，再从相关课文补起；不用按目录把前面的课全学完。</p>'}<div class="relation-grid"><div class="relation required"><h3>需要先会什么</h3>${n.guide?relationList(n.required,completed):'<p class="muted small">这节还没单独整理必须先会的内容。下面列出的相关课文，可以按需要补读。</p>'}${n.guide&&!n.required.length?'<p class="small">可以直接开始。不用先把整门课学完。</p>':''}</div><div class="relation recommended"><h3>想不明白时，看看这些</h3>${relationList(n.recommended,completed)}${n.background.length?`<p class="small">课外还需要会：${n.background.map(esc).join('、')}</p>`:''}</div></div>${!compact&&next.length?`<div class="relation"><h3>学会后，再看这些</h3>${relationList(next,completed)}</div>`:''}<a class="text-link" href="${mapURL(n.course.id,n.id)}">在课程知识图中定位 →</a>${compact?'</div></details>':'</section>'}`;
}
function legend(){return '<div class="map-legend" aria-label="图例"><span class="map-badge mainline">先学这些</span><span class="map-badge foundation">补基础</span><span class="map-badge advanced">以后再学</span><p>实线框：这节要用到的基础，需要先会。虚线框：帮助理解的补充，有需要再看。目录排在前面，不代表每一节都得先读完。</p></div>';}
function overview(m,completed){return `<main class="page knowledge-page" id="main" tabindex="-1"><div class="eyebrow">KNOWLEDGE FRAMEWORK · 先看全貌</div><h1>先学常用的，卡住再补基础</h1><p class="lead">不用一次面对 ${m.nodes.length} 节。先选一门课，看它要解决什么问题，再把不熟悉的前置概念补回来。</p><a class="primary" href="#/path">打开起步学习路线 →</a>${legend()}<div class="map-stages">${stageSpecs.map((s,i)=>`<section class="map-stage"><div class="map-stage-heading"><span class="map-stage-number">${i+1}</span><div><h2>${s.title}</h2><p>${s.note}</p></div></div><div class="map-course-grid">${s.ids.map(id=>{const c=m.courses.find(c=>c.id===id),nodes=m.nodes.filter(n=>n.course.id===id);return `<a class="map-course-card" href="${mapURL(id)}"><span class="eyebrow">${esc(c.enTitle)}</span><h3>${esc(c.title)} →</h3><p>${esc(c.description)}</p><span class="small">${nodes.length} 节 · 建议先学 ${nodes.filter(n=>n.tier==='mainline').length} 节 · 已完成 ${nodes.filter(n=>completed.includes(n.id)).length}</span></a>`;}).join('')}</div></section>`).join('')}</div><section class="map-bridges"><h2>跨课程的联系</h2><p>下面是知识之间的联系，不是整门课都必须先修的要求。具体要先会什么，可以点开每一节查看。</p><ul>${bridgeSpecs.map(([a,b,why])=>`<li><a href="${mapURL(a)}">${esc(m.courses.find(c=>c.id===a).title)}</a><span aria-hidden="true"> → </span><a href="${mapURL(b)}">${esc(m.courses.find(c=>c.id===b).title)}</a><p>${why}</p></li>`).join('')}</ul></section></main>`;}
function courseMap(m,c,id,completed){
 const nodes=m.nodes.filter(n=>n.course.id===c.id),groups=[...new Set(nodes.map(n=>n.group))],selected=m.byId.get(id);if(id&&(!selected||selected.course.id!==c.id))return null;
 return `<main class="page knowledge-page" id="main" tabindex="-1"><div class="crumb"><a href="#/map">七门课程知识框架</a><span>/</span>${esc(c.title)}</div><h1>${esc(c.title)} · 知识图</h1><p class="lead">${esc(c.description)}</p><div class="map-actions"><a class="secondary" href="#/course/${c.id}">完整课文目录</a><a class="secondary" href="#/path/${c.id}">只看建议先学的课</a></div>${legend()}${selected?`<section class="map-selected"><div class="eyebrow">你正在看</div><h2>${esc(selected.title)}</h2><a class="primary" href="${lessonURL(selected)}">阅读这一节 →</a>${selected.guide?`<p class="map-selected-purpose">${esc(selected.guide.why)}</p><p class="map-checkpoint"><b>学完能做什么：</b>${esc(selected.guide.checkpoint)}</p>`:`<p class="map-selected-purpose">${esc(selected.summary)}</p><p class="small muted">这节还没单独整理必须先会的内容。下面是相关课文，按需要看就好。</p>`}${dependencyFlow(m,selected,completed)}${selected.background.length?`<p class="small">课外还需要会：${selected.background.map(esc).join('、')}</p>`:''}</section>`:''}<div class="map-filter"><label for="map-filter">显示知识点</label><select id="map-filter"><option value="all">全部 ${nodes.length} 节</option><option value="mainline">先学这些</option><option value="foundation">补基础</option><option value="advanced">以后再学</option></select><span id="map-count" role="status">显示 ${nodes.length} 节</span></div><p class="small muted">点击知识点，看看需要先会什么、卡住时补哪节；每个知识点都能直接进入课文。下面的课名都能点击，也能用键盘打开。</p><div class="topic-map">${groups.map((g,i)=>`<section class="topic-group" data-topic-group><header><span>${String(i+1).padStart(2,'0')}</span><h2>${esc(g.replace(/^\d+\s*·\s*/,''))}</h2></header><ol>${nodes.filter(n=>n.group===g).map(n=>`<li class="topic-node ${n.id===id?'selected':''}" data-tier="${n.tier}" data-node-id="${esc(n.id)}">${badge(n)}${link(n,completed,'map')}<p>${esc(n.guide?.why||n.summary)}</p><a class="map-read" href="${lessonURL(n)}">读课文 <span aria-hidden="true">↗</span></a></li>`).join('')}</ol></section>`).join('')}</div><p id="map-empty" hidden>这一分组没有对应知识点。可改为“全部”查看完整课程。</p></main>`;
}
function render(courses,guides,completed=[],courseId,lessonId){const m=model(courses,guides);if(!courseId)return overview(m,completed);const c=courses.find(c=>c.id===courseId);return c?courseMap(m,c,lessonId,completed):null;}
function lessonPanel(courses,guides,id,completed=[]){const m=model(courses,guides),n=m.byId.get(id);return n?context(m,n,completed,{compact:true}):'';}
function path(courses,guides,completed=[],courseId){
 const m=model(courses,guides),chosen=courses.find(c=>c.id===courseId);if(courseId&&!chosen)return null;const selected=chosen?[chosen]:stageSpecs.flatMap(s=>s.ids.map(id=>courses.find(c=>c.id===id))),anchors=m.nodes.filter(n=>n.tier==='mainline');
 return `<main class="page foundation-path" id="main" tabindex="-1"><div class="eyebrow">CORE LEARNING PATH · 本科起步</div><h1>少走弯路，先把最常用的学会</h1><p class="lead">先看图和具体问题，再跟算例动手算。暂时读不懂完整证明，可以先检查要先会的基础，之后再回来展开；“读完”不等于“掌握”。</p><div class="path-contract"><h2>每次学一小段，按这四步来</h2><ol><li><b>说清问题</b> · 这次要算什么？已知什么？</li><li><b>跟图写式子</b> · 每个符号是什么，单位是什么？</li><li><b>合上答案重做</b> · 解释每一步为什么成立</li><li><b>过关再往前</b> · 卡在哪里，就沿要先会的基础补哪里</li></ol><p>先用这 ${anchors.length} 节把常用基础接起来。做不出来就回头补，不用赶进度。考试要求和完整证明还要结合课程继续学，没有固定几天就能全会的保证。</p></div><nav class="map-course-tabs" aria-label="选择起步课程"><a href="#/path" ${!chosen?'aria-current="page"':''}>全部主线</a>${courses.map(c=>`<a href="#/path/${c.id}" ${chosen?.id===c.id?'aria-current="page"':''}>${esc(c.title)}</a>`).join('')}</nav>${selected.map(c=>{const nodes=m.nodes.filter(n=>n.course.id===c.id&&n.tier==='mainline');return `<section class="core-course"><div class="section-heading"><h2>${esc(c.title)}</h2><a class="text-link" href="${mapURL(c.id)}">全部课文怎么连起来 →</a></div><ol class="core-route">${nodes.map(n=>`<li><div class="core-route-head">${badge(n)}<span class="small">${completed.includes(n.id)?'✓ 已记录完成':'能自己做出来，再往下学'}</span></div><h3>${link(n,completed)}</h3><p>${esc(n.guide.why)}</p><p class="map-checkpoint"><b>试着自己做：</b>${esc(n.guide.checkpoint)}</p>${n.required.length?`<details><summary>卡住时，先补这 ${n.required.length} 个概念</summary>${relationList(n.required,completed)}</details>`:''}<a class="text-link" href="${lessonURL(n)}">开始读这一节 →</a></li>`).join('')}</ol></section>`;}).join('')}<section class="wide-note"><h2>基础打通后，再选专项</h2><p><a class="text-link" href="#/research">AI × 传热研究路线</a>　<a class="text-link" href="#/simulation">流动换热仿真路线</a>　<a class="text-link" href="#/map">七门课程知识框架</a></p></section></main>`;
}
function bind(doc){const select=doc.getElementById('map-filter');if(!select)return;select.addEventListener('change',()=>{let count=0;doc.querySelectorAll('[data-node-id]').forEach(el=>{el.hidden=select.value!=='all'&&el.dataset.tier!==select.value;if(!el.hidden)count++;});doc.querySelectorAll('[data-topic-group]').forEach(el=>el.hidden=![...el.querySelectorAll('[data-node-id]')].some(n=>!n.hidden));doc.getElementById('map-count').textContent='显示 '+count+' 节';doc.getElementById('map-empty').hidden=count!==0;});}
root.KnowledgeMap={model,render,path,lessonPanel,bind};
})(typeof window==='undefined'?globalThis:window);
