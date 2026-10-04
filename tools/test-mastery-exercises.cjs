/* Verifies the exercise contract and optional live DOM without adding a grade schema. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),ctx={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'site/assets/data.js'),'utf8'),ctx);
const w=ctx.window,exercises=w.MASTERY_EXERCISES;
const review=JSON.parse(fs.readFileSync(path.join(root,'reviews/mastery-review-manifest.json'),'utf8'));
const amendmentPath=path.join(root,'reviews/report-revision-preservation.json');
const masteryAmendments=fs.existsSync(amendmentPath)?JSON.parse(fs.readFileSync(amendmentPath,'utf8')).mastery:[];
assert.ok(masteryAmendments.length<=1 && masteryAmendments.every(a=>a.scope==='computing'),'Only the reviewed floating-point prompt clarification is allowed');
const version=JSON.parse(fs.readFileSync(path.join(root,'version.json'),'utf8')).version;
assert.equal(w.TEXTBOOK_VERSION.version,version,'Generated exercises must use the current release version');
assert.ok(['1.5.0','1.6.0'].includes(version),'No exercise preservation contract for this version');
const sha=value=>require('node:crypto').createHash('sha256').update(value).digest('hex');
let readerPlan,masteryPlan;
const appliedChanges=new Set();
const approvedFields=new Set([
 'mastery-calculus-01-01:verification', 'mastery-linear-algebra-02-03:solution',
 'mastery-thermodynamics-01-01:prompt', 'mastery-thermodynamics-01-01:solution',
 'mastery-thermodynamics-07-01:prompt', 'mastery-thermodynamics-07-01:solution', 'mastery-thermodynamics-07-01:verification',
 'mastery-heat-transfer-01-02:prompt', 'mastery-heat-transfer-01-02:verification',
 'mastery-heat-transfer-01-03:prompt', 'mastery-heat-transfer-03-02:prompt',
 'mastery-heat-transfer-07-01:solution', 'mastery-heat-transfer-07-01:checkpoints'
]);
if(version==='1.6.0'){
 readerPlan=JSON.parse(fs.readFileSync(path.join(root,'reviews/reader-revision-1.6.0.json'),'utf8'));
 masteryPlan=JSON.parse(fs.readFileSync(path.join(root,'reviews/prepublication-mastery-dispositions-1.6.0.json'),'utf8'));
 const original=JSON.parse(fs.readFileSync(path.join(root,'reviews/reader-baseline-1.5.0.json'),'utf8'));
 assert.equal(readerPlan.status,'reviewed','Final exercise source snapshot must be reviewed');
 assert.equal(masteryPlan.schema,1);assert.equal(masteryPlan.version,'1.6.0');assert.equal(masteryPlan.baseline_version,'1.5.0');
 assert.equal(masteryPlan.baseline_commit,original.commit);assert.equal(masteryPlan.baseline_archive_sha256,original.archive_sha256);
 assert.deepEqual(masteryPlan.files.map(f=>f.scope).sort(),review.files.map(f=>f.scope).sort());
 assert.equal(masteryPlan.files.length,4);
}
for(const record of review.files){
 const sourcePath='content/mastery-exercises-'+record.scope+'.json';
 const source=fs.readFileSync(path.join(root,sourcePath));
 const amendment=masteryAmendments.find(a=>a.scope===record.scope);
 if(amendment){assert.equal(amendment.before_sha256,record.integrated_sha256);assert.ok(amendment.reason&&amendment.review);}
 const historicalHash=amendment?.after_sha256||record.integrated_sha256;
 if(version==='1.5.0'){
  assert.equal(sha(source),historicalHash,'Reviewed question/answer source changed: '+record.scope);
 }else{
  const entry=masteryPlan.files.find(f=>f.scope===record.scope);
  assert.equal(entry.path,sourcePath);assert.equal(entry.exercises,record.exercises);
  assert.equal(entry.baseline_sha256,historicalHash,'Original 1.5.0 exercise pin changed: '+record.scope);
  assert.equal(sha(Buffer.from(entry.baseline_utf8,'utf8')),historicalHash,'Stored baseline does not reproduce published bytes: '+record.scope);
  const expected=JSON.parse(entry.baseline_utf8);
  assert.equal(expected.length,record.exercises);assert.equal(new Set(expected.map(q=>q.id)).size,expected.length);
  for(const change of entry.changes){
   const key=change.id+':'+change.field;
   assert.ok(approvedFields.has(key)&&!appliedChanges.has(key),'Unexpected/duplicate exercise-field amendment: '+key);
   assert.ok(change.reason?.trim()&&change.review?.trim(),'Missing amendment reason or review');
   assert.ok(readerPlan.review_notes.includes(change.review)&&fs.existsSync(path.join(root,change.review)),'Missing approved exercise review');
   const question=expected.find(q=>q.id===change.id);
   assert.ok(question&&Object.hasOwn(question,change.field),'Amendment target must exist in the original question');
   assert.deepEqual(question[change.field],change.before,'Amendment does not match the original field: '+key);
   assert.notDeepEqual(change.before,change.after,'No-op amendment is not a reviewed change');
   question[change.field]=JSON.parse(JSON.stringify(change.after));appliedChanges.add(key);
  }
  assert.deepEqual(JSON.parse(source),expected,'Exercise content differs beyond the 13 approved field changes: '+record.scope);
  assert.equal(sha(source),entry.reviewed_sha256,'Exercise bytes differ from reviewed amendments: '+record.scope);
  const frozen=readerPlan.reviewed_files.filter(f=>f.path===sourcePath);assert.equal(frozen.length,1);
  assert.equal(sha(source),frozen[0].sha256,'Exercise bytes differ from the final 1.6.0 source snapshot: '+record.scope);
 }
 assert.equal(JSON.parse(source).length,record.exercises);
}
if(version==='1.6.0'){
 assert.deepEqual([...appliedChanges].sort(),[...approvedFields].sort(),'All 13 approved amendments must be applied exactly once');
 console.log('Mastery preservation: four original 1.5.0 byte-pinned files plus exactly 13 reviewed field changes equal all 78 current objects');
}
assert.equal(exercises.length,78,'All 78 reviewed exercises ship without replacing their identities');
const originalAnchors=JSON.parse(fs.readFileSync(path.join(root,'reviews/learning-original-content-baseline.json'),'utf8')).anchors.map(a=>a.id);
assert.equal(originalAnchors.length,26);
assert.deepEqual([...new Set(exercises.map(e=>e.lessonId))].sort(),originalAnchors.slice().sort());
assert.equal(new Set(exercises.map(e=>e.id)).size,exercises.length);
const levels=['基础理解','常规应用','综合提高'];
for(const guide of w.LEARNING_GUIDES.filter(g=>originalAnchors.includes(g.id))){const rows=exercises.filter(e=>e.lessonId===guide.id);assert.ok(rows.length>=3,guide.id);for(const level of levels)assert.ok(rows.some(e=>e.level===level),guide.id+' '+level);}
assert.ok(new Set(exercises.map(e=>e.type)).size>=10,'Practice must contain varied task types');
assert.equal(w.TEXTBOOK_VERSION.mastery_exercises,exercises.length);
for(const e of exercises){assert.ok(!Object.hasOwn(e,'verification'));assert.ok(e.checkpoints.length>=2,e.id);assert.ok(e.solution.length>70,e.id);}
if(process.argv.includes('--dom')){
 const {JSDOM,VirtualConsole}=require(process.env.ZHIXU_JSDOM_MODULE||'jsdom');
 const html=fs.readFileSync(path.join(root,'site/index.html'),'utf8');
 const dom=new JSDOM(html,{url:'https://example.test/textbook/#/path',runScripts:'outside-only',virtualConsole:new VirtualConsole()});
 const dw=dom.window,d=dw.document;dw.scrollTo=()=>{};dw.HTMLElement.prototype.scrollIntoView=()=>{};dw.matchMedia=()=>({matches:true});
 const original={notes:{'calculus-03':'原始笔记'},completed:['calculus-01'],bookmarks:['calculus-03'],answers:{'calculus-03':{choice:2,correct:true,at:'2026-10-02T00:00:00Z'}}};
 dw.localStorage.setItem('zhixu-learning-v1',JSON.stringify(original));
 for(const m of html.matchAll(/<script defer src="([^"]+)"/g))dw.eval(fs.readFileSync(path.join(root,'site',m[1].split('?')[0]),'utf8'));
 for(const guide of dw.LEARNING_GUIDES.filter(g=>originalAnchors.includes(g.id))){const course=dw.COURSES.find(c=>c.chapters.some(l=>l.id===guide.id));dw.location.hash='#/course/'+course.id+'/'+guide.id;dw.dispatchEvent(new dw.HashChangeEvent('hashchange'));
  const rows=dw.MASTERY_EXERCISES.filter(e=>e.lessonId===guide.id),cards=[...d.querySelectorAll('.mastery-card')];assert.equal(cards.length,rows.length,guide.id);
  assert.match(d.querySelector('.mastery-intro').textContent,/不会自动评分/);
  for(const card of cards){const answer=card.querySelector('details');assert.equal(answer.open,false);answer.querySelector('summary').click();assert.equal(answer.open,true);assert.ok(card.querySelector('.mastery-solution').textContent.trim().length>50);assert.ok(card.querySelectorAll('.mastery-checkpoints li').length>=2);answer.querySelector('summary').click();assert.equal(answer.open,false);}
  assert.equal(d.querySelectorAll('.math-error').length,0,guide.id);
  assert.equal(d.querySelectorAll('.mastery-card [data-answer],.mastery-card input').length,0,'Open ended answers must not masquerade as graded MCQ');
  const heading=d.querySelector('.mastery-practice h2');assert.ok(d.querySelector('#mobile-toc-list [data-scroll="'+heading.id+'"]'));
 }
 const saved=JSON.parse(dw.localStorage.getItem('zhixu-learning-v1'));assert.equal(saved.notes['calculus-03'],original.notes['calculus-03']);assert.ok(saved.completed.includes('calculus-01'));assert.ok(saved.bookmarks.includes('calculus-03'));assert.equal(saved.answers['calculus-03'].choice,2);assert.deepEqual(Object.keys(saved).sort(),Object.keys(dw.LearningState.normalize(original,dw.ZHIXU.all)).sort());
 dom.window.close();
}
console.log('Mastery exercises: '+exercises.length+' tasks across '+w.TEXTBOOK_VERSION.mastery_lessons+' lessons; 3 levels, diverse types, complete solutions and unchanged grade/progress schema passed');
