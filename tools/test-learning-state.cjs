/* No dependencies: exercise input boundaries and transactional persistence. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const vm=require('node:vm');
const stateApi=require('../site/assets/learning-state.js');
const {LABS}=require('../site/assets/labs.js');
const lessons=Array.from({length:12},(_,i)=>({id:'lesson-'+i,quiz:{options:['a','b','c'],answer:1}}));
const backup=(extra={})=>({format:'zhixu-learning',version:1,completed:[],bookmarks:[],notes:{},answers:{},...extra});
let tests=0;
function check(name,test){test();tests++;console.log('PASS '+name);}

check('Normalize hostile keys and invalid local records',()=>{
 const raw=JSON.parse('{"__proto__":{"polluted":true},"completed":["lesson-0","lesson-0","constructor",null],"bookmarks":["lesson-1"],"notes":{"__proto__":"bad","lesson-0":"保留笔记","lesson-1":null},"answers":{"lesson-0":null,"lesson-1":{"choice":"1"},"lesson-2":{"choice":9},"lesson-3":{"choice":1,"correct":false}},"last":"constructor","theme":"dark","font":"999","unexpected":"remove"}');
 const result=stateApi.normalize(raw,lessons);
 assert.deepEqual(result.completed,['lesson-0']);assert.deepEqual(result.bookmarks,['lesson-1']);
 assert.equal(result.notes['lesson-0'],'保留笔记');assert.equal(result.notes['lesson-1'],undefined);
 assert.deepEqual(Object.keys(result.answers),['lesson-3']);assert.equal(result.answers['lesson-3'].correct,true);
 assert.equal(result.last,null);assert.equal(result.theme,'dark');assert.equal(result.font,22);
 assert.equal(result.unexpected,undefined);assert.equal(result.polluted,undefined);assert.equal({}.polluted,undefined);
 assert.equal(Object.getPrototypeOf(result.notes),null);
});
check('Array/null state fields cannot crash lesson or notebook readers',()=>{
 for(const invalid of [null,[],false,'invalid']){
  const result=stateApi.normalize({notes:invalid,answers:invalid,completed:invalid,bookmarks:invalid},lessons);
  assert.deepEqual(Object.keys(result.notes),[]);assert.deepEqual(Object.keys(result.answers),[]);
  assert.deepEqual(result.completed,[]);assert.deepEqual(result.bookmarks,[]);
 }
 assert.equal(stateApi.normalize(null,lessons).font,18);
});
check('Preserve existing notes, preferences, answers and merge distinct text',()=>{
 const current=stateApi.normalize({notes:{'lesson-0':'原笔记','lesson-1':'x'.repeat(200001)},completed:['lesson-0'],theme:'dark',font:20,answers:{'lesson-0':{choice:0,at:'old'}}},lessons);
 const before=JSON.stringify(current);let saved;
 const result=stateApi.commitImport(current,backup({completed:['lesson-1'],notes:{'lesson-0':'新笔记'},answers:{'lesson-0':{choice:1},'lesson-2':{choice:1,correct:false}}}),lessons,value=>{saved=value;});
 assert.equal(JSON.stringify(current),before);assert.equal(result.merged,1);
 assert.equal(result.state.notes['lesson-0'],'原笔记\n\n—— 从备份合并 ——\n新笔记');
 assert.equal(result.state.notes['lesson-1'].length,200001);
 assert.equal(result.state.answers['lesson-0'].choice,0);assert.equal(result.state.answers['lesson-2'].correct,true);
 assert.equal(result.state.theme,'dark');assert.equal(result.state.font,20);
 assert.deepEqual(JSON.parse(saved).completed,['lesson-0','lesson-1']);
});
check('Import rejects malformed values before writing and preserves the original',()=>{
 const current=stateApi.normalize({notes:{'lesson-0':'不能丢失'}},lessons),before=JSON.stringify(current);
 const invalid=[null,backup({notes:[]}),backup({answers:null}),backup({completed:[{}]}),backup({notes:{'lesson-0':null}}),backup({answers:{'lesson-0':null}}),backup({answers:{'lesson-0':{choice:'1'}}}),backup({notes:{'lesson-0':'x'.repeat(stateApi.MAX_NOTE_CHARS+1)}})];
 for(const value of invalid){let writes=0;assert.throws(()=>stateApi.commitImport(current,value,lessons,()=>writes++));assert.equal(writes,0);assert.equal(JSON.stringify(current),before);}
});
check('Oversized combined backup is rejected without replacing valid records',()=>{
 const current=stateApi.normalize({notes:{'lesson-0':'重要记录'}},lessons),before=JSON.stringify(current);
 const notes=Object.fromEntries(lessons.slice(1).map(lesson=>[lesson.id,'x'.repeat(190000)]));
 let writes=0;assert.throws(()=>stateApi.commitImport(current,backup({notes}),lessons,()=>writes++),/记录过大/);
 assert.equal(writes,0);assert.equal(JSON.stringify(current),before);
});
check('Quota failure cannot claim a successful import or modify in-memory records',()=>{
 const current=stateApi.normalize({notes:{'lesson-0':'旧记录'}},lessons),before=JSON.stringify(current);let durable=before;
 assert.throws(()=>stateApi.commitImport(current,backup({notes:{'lesson-0':'导入内容'}}),lessons,()=>{throw Error('QuotaExceededError');}),/导入未完成，原记录未更改/);
 assert.equal(JSON.stringify(current),before);assert.equal(durable,before);
});
check('Prototype property names and unknown routes are never mounted as labs',()=>{
 for(const id of ['__proto__','constructor','toString','hasOwnProperty','unknown','derivative\" onclick=alert(1)',null]){
  assert.equal(stateApi.hasLab(LABS,id),false);assert.doesNotThrow(()=>globalThis.mountLab({},id));
 }
 assert.equal(stateApi.hasLab(LABS,'derivative'),true);
 const app=fs.readFileSync(path.join(__dirname,'../site/assets/app.js'),'utf8');
 const source=app.slice(app.indexOf('function labsPage('),app.indexOf('\nfunction notebook('));
 const context={window:{LABS},hasLab:id=>stateApi.hasLab(LABS,id),all:[],footer:()=>'',esc:String};
 vm.runInNewContext(source,context);
 for(const id of ['__proto__','constructor','toString','unknown'])assert.doesNotMatch(context.labsPage(id),/data-lab=/);
 assert.match(context.labsPage('derivative'),/data-lab="derivative"/);
});
console.log(`Validated ${tests} learning-state and routing security boundaries.`);
