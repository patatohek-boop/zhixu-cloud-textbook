/* Chapter tree and local prerequisite graph. Content IDs and storage remain unchanged. */
(function(root){
'use strict';
const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const href=(c,l)=>'#/course/'+c.id+(l?'/'+l.id:'');
const groups=c=>[...new Set(c.chapters.map(l=>l.group))];
function chapters(c,completed=[],active,open=false){
 return groups(c).map(g=>`<details class="tree-chapter" ${open||c.chapters.some(l=>l.id===active&&l.group===g)?'open':''}><summary>${esc(g)}</summary><ol>${c.chapters.filter(l=>l.group===g).map(l=>`<li><a class="${active===l.id?'current':''}" ${active===l.id?'aria-current="page"':''} href="${href(c,l)}"><span>${esc(l.title)}</span>${completed.includes(l.id)?'<span class="tick" aria-label="已完成">✓</span>':''}</a></li>`).join('')}</ol></details>`).join('');
}
function supplements(c){
 if(c.id==='machine-learning')return '<p class="tree-supplement"><a href="#/research">专题索引：AI、传热与实验 →</a></p>';
 if(c.id==='fluid-mechanics')return '<p class="tree-supplement"><a href="#/simulation">专题索引：流动换热仿真 →</a></p>';
 return '';
}
function tree(courses,state){
 const last=courses.flatMap(c=>c.chapters.map(l=>({c,l}))).find(x=>x.l.id===state.last);
 return `<main class="page textbook-index" id="main" tabindex="-1"><header class="index-heading"><p class="index-kicker">知序 · 理工云教材</p><h1>知识树</h1><p>按课程、章与知识点查阅。初次学习可依目录顺序阅读，正文中的链接用于查找前置概念。</p>${last?`<a class="resume-reading" href="${href(last.c,last.l)}">继续阅读：${esc(last.l.title)} →</a>`:''}</header><nav class="subject-links" aria-label="课程选择">${courses.map(c=>`<a href="${href(c)}">${esc(c.title)}</a>`).join('')}</nav><div class="textbook-tree" aria-label="全部课程知识树">${courses.map((c,i)=>`<section class="tree-course"><header><span class="tree-number">${String(i+1).padStart(2,'0')}</span><div><h2><a href="${href(c)}">${esc(c.title)}</a></h2><p>${esc(c.enTitle)} · ${c.chapters.length} 节</p></div><a class="tree-enter" href="${href(c)}" aria-label="进入${esc(c.title)}">→</a></header>${chapters(c,state.completed)}${supplements(c)}</section>`).join('')}</div><footer class="index-footer"><a href="#/labs">交互图解索引</a><a href="#/notebook">学习记录与备份</a><a href="#/review">修订记录</a><span>内容版本 ${esc(root.TEXTBOOK_VERSION?.version)}</span></footer></main>`;
}
function sidebar(c,completed,id){
 return `<aside class="sidebar" id="course-sidebar" aria-label="课程目录"><div class="sidebar-mobile-actions"><button class="secondary" data-close-sidebar>关闭目录 ×</button></div><a class="back" href="#/">← 全部课程</a><h2><a href="${href(c)}">${esc(c.title)}</a></h2><a class="sidebar-map-link" href="#/map/${esc(c.id)}${id?'/'+esc(id):''}">查看知识联系</a><nav class="sidebar-tree" aria-label="章与知识点">${chapters(c,completed,id,!id)}</nav>${supplements(c)}</aside>`;
}
function graph(courses,guides,completed,courseId,lessonId){
 const m=root.KnowledgeMap.model(courses,guides),c=courseId?courses.find(c=>c.id===courseId):courses[0];
 if(!c)return null;
 const n=lessonId?m.byId.get(lessonId):m.nodes.find(n=>n.course.id===c.id);
 if(!n||n.course.id!==c.id)return null;
 const before=[...n.required.map(x=>({n:x,kind:'先修'})),...n.recommended.filter(x=>!n.required.some(r=>r.id===x.id)).map(x=>({n:x,kind:'相关'}))];
 const after=m.nodes.filter(x=>x.required.some(r=>r.id===n.id)||x.recommended.some(r=>r.id===n.id));
 const node=(x,label)=>`<a class="relation-node" href="#/map/${x.course.id}/${x.id}"><small>${esc(label)} · ${esc(x.course.title)}</small><strong>${esc(x.title)}</strong></a>`;
 return `<main class="page relationship-page" id="main" tabindex="-1"><h1>知识联系</h1><p>选中一个知识点，查看课文中已记录的前置知识与后续联系。这里展示局部关系，完整学习范围见知识树。</p><nav class="subject-links" aria-label="课程选择">${courses.map(x=>`<a ${x.id===c.id?'aria-current="page"':''} href="#/map/${x.id}">${esc(x.title)}</a>`).join('')}</nav><div class="relation-selector"><label for="relation-select">${esc(c.title)}</label><select id="relation-select">${c.chapters.map(x=>`<option value="${esc(x.id)}" ${x.id===n.id?'selected':''}>${esc(x.title)}</option>`).join('')}</select></div><section class="relationship-diagram" aria-label="前置知识到当前知识再到后续知识"><div><h2>前置与相关知识</h2>${before.map(x=>node(x.n,x.kind)).join('')||'<p class="muted">未列出课内先修链接。</p>'}${n.background.length?`<p class="relation-background">其他基础：${n.background.map(esc).join('、')}</p>`:''}</div><div class="relation-center"><span class="relation-arrow" aria-hidden="true">→</span><div class="dependency-current"><small>当前知识点</small><h2>${esc(n.title)}</h2><a class="primary" href="${href(c,n)}">阅读正文 →</a></div><span class="relation-arrow" aria-hidden="true">→</span></div><div><h2>后续联系</h2>${after.map(x=>node(x,x.required.some(r=>r.id===n.id)?'以此为先修':'引用此节')).join('')||'<p class="muted">暂无课内后续链接，可回目录继续阅读。</p>'}</div></section><p class="small muted">“先修”来自已整理的学习依赖；“相关”来自课文元数据，用于补充阅读，不表示所有链接都必须先学。</p><p><a class="text-link" href="${href(c)}">${esc(c.title)}完整目录 →</a></p></main>`;
}
function bind(doc){const select=doc.getElementById('relation-select');if(select)select.onchange=()=>{const c=root.COURSES.find(c=>c.chapters.some(l=>l.id===select.value));if(c)root.location.hash='#/map/'+c.id+'/'+select.value;};}
root.TextbookNav={tree,chapters,sidebar,graph,bind,supplements};
})(typeof window==='undefined'?globalThis:window);
