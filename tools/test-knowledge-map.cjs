const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'..'),ctx={window:{}};vm.createContext(ctx);
for(const name of ['data.js','knowledge-map.js'])vm.runInContext(fs.readFileSync(path.join(root,'site/assets',name),'utf8'),ctx);
const {COURSES:courses,LEARNING_GUIDES:guides,KnowledgeMap:map}=ctx.window,m=map.model(courses,guides);
assert.equal(m.nodes.length,253);assert.equal(new Set(m.nodes.map(n=>n.id)).size,253);
assert.equal(guides.length,26,'The first enrichment pass covers exactly the enumerated 26 anchors');
assert.equal(m.nodes.filter(n=>n.tier==='mainline').length,26);
let required=0,recommended=0;
for(const n of m.nodes){
 assert.ok(['mainline','foundation','advanced'].includes(n.tier));
 for(const edge of n.required){required++;assert.ok(m.byId.has(edge.id));assert.notEqual(n.id,edge.id);assert.ok(!n.recommended.some(r=>r.id===edge.id));}
 for(const edge of n.recommended){recommended++;assert.ok(m.byId.has(edge.id));assert.notEqual(n.id,edge.id);}
 if(!n.guide)assert.equal(n.required.length,0,'Legacy previous-chapter suggestions must not become false required edges');
}
const linkPattern=/href="(#\/[^\"]+)"/g;
function links(html){for(const [,href]of html.matchAll(linkPattern)){const [kind,c,id]=href.slice(2).split('/');if(['map','course','path'].includes(kind)&&c){assert.ok(courses.some(x=>x.id===c),href);if(id)assert.equal(m.byId.get(id)?.course.id,c,href);}}}
for(const c of courses){
 const html=map.render(courses,guides,[],c.id);links(html);
 const ids=[...html.matchAll(/data-node-id="([^\"]+)"/g)].map(x=>x[1]);assert.equal(ids.length,c.chapters.length);assert.equal(new Set(ids).size,ids.length);
 for(const l of c.chapters){const local=map.render(courses,guides,[],c.id,l.id);links(local);assert.ok(local.includes('先学什么，学会后再去哪'));assert.ok(local.includes('必须先会')||!m.byId.get(l.id).required.length);}
 assert.equal(map.render(courses,guides,[],c.id,'__missing'),null);
}
links(map.render(courses,guides,[]));links(map.path(courses,guides,[]));
assert.equal(map.render(courses,guides,[],'__missing'),null);
const title=courses[0].chapters[0].title;courses[0].chapters[0].title='<img src=x onerror=alert(1)>';
const escaped=map.render(courses,guides,[],courses[0].id,courses[0].chapters[0].id);
assert.ok(escaped.includes('&lt;img'));assert.ok(!escaped.includes('<img src=x'));courses[0].chapters[0].title=title;
// Only static, local assets are added. No runtime fetch, CDN, or storage migration.
const source=fs.readFileSync(path.join(root,'site/assets/knowledge-map.js'),'utf8');assert.ok(!/\b(fetch|XMLHttpRequest|localStorage)\b/.test(source));
console.log(JSON.stringify({lessons:m.nodes.length,anchors:guides.length,required,recommended,links:'valid',legacy_edges:'suggestions',escaping:'passed'},null,2));
