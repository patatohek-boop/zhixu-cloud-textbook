/* Validate local records and stage imports before a single durable write. */
(function(root){
'use strict';
const MAX_NOTE_CHARS=200000,MAX_STATE_CHARS=2000000;
const own=(value,key)=>Object.prototype.hasOwnProperty.call(value,key);
const record=value=>value!==null&&typeof value==='object'&&!Array.isArray(value);
function lessonMap(lessons){return new Map(lessons.map(lesson=>[lesson.id,lesson]));}
function validAnswer(answer,lesson){return record(answer)&&Number.isInteger(answer.choice)&&answer.choice>=0&&answer.choice<lesson.quiz.options.length;}
function copyAnswer(answer,lesson){return {choice:answer.choice,correct:answer.choice===lesson.quiz.answer,at:typeof answer.at==='string'?answer.at.slice(0,64):''};}
function normalize(raw,lessons){
 const input=record(raw)?raw:{},ids=lessonMap(lessons);
 const result={completed:[],bookmarks:[],notes:Object.create(null),answers:Object.create(null),last:null,theme:'light',font:18};
 for(const key of ['completed','bookmarks'])if(Array.isArray(input[key]))result[key]=[...new Set(input[key].filter(id=>typeof id==='string'&&ids.has(id)))];
 for(const [id,lesson]of ids){
  // Preserve existing plain-text notes in full, including older long notes.
  if(record(input.notes)&&own(input.notes,id)&&typeof input.notes[id]==='string')result.notes[id]=input.notes[id];
  if(record(input.answers)&&own(input.answers,id)&&validAnswer(input.answers[id],lesson))result.answers[id]=copyAnswer(input.answers[id],lesson);
 }
 if(typeof input.last==='string'&&ids.has(input.last))result.last=input.last;
 if(input.theme==='dark')result.theme='dark';
 const font=typeof input.font==='number'||typeof input.font==='string'?Number(input.font):NaN;
 if(Number.isFinite(font))result.font=Math.max(16,Math.min(22,font));
 return result;
}
function prepareImport(current,input,lessons){
 if(!record(input)||input.format!=='zhixu-learning'||input.version!==1||!Array.isArray(input.completed)||!Array.isArray(input.bookmarks)||!record(input.notes)||(own(input,'answers')&&!record(input.answers)))throw Error('这不是有效的知序学习备份');
 const ids=lessonMap(lessons),next=normalize(current,lessons);let merged=0;
 for(const key of ['completed','bookmarks']){
  if(input[key].some(id=>typeof id!=='string'))throw Error('备份中的课文编号格式无效');
  next[key]=[...new Set([...next[key],...input[key].filter(id=>ids.has(id))])];
 }
 for(const [id,value]of Object.entries(input.notes)){
  if(!ids.has(id))continue;
  if(typeof value!=='string'||value.length>MAX_NOTE_CHARS)throw Error('备份中的笔记格式无效或单篇超过 20 万字符');
  const before=next.notes[id]||'';
  if(!before)next.notes[id]=value;
  else if(value&&before!==value&&!before.includes(value)){
   const combined=before+'\n\n—— 从备份合并 ——\n'+value;
   if(combined.length>MAX_NOTE_CHARS)throw Error('合并后的单篇笔记超过 20 万字符，原记录未更改');
   next.notes[id]=combined;merged++;
  }
 }
 for(const [id,answer]of Object.entries(input.answers||{})){
  const lesson=ids.get(id);if(!lesson)continue;
  if(!validAnswer(answer,lesson))throw Error('备份中的答题记录格式无效');
  if(!own(next.answers,id))next.answers[id]=copyAnswer(answer,lesson);
 }
 const serialized=JSON.stringify(next);
 if(serialized.length>MAX_STATE_CHARS)throw Error('合并后记录过大，无法安全保存；原记录未更改');
 return {state:next,merged,serialized};
}
function commitImport(current,input,lessons,write){
 const prepared=prepareImport(current,input,lessons);
 try{write(prepared.serialized);}catch{throw Error('浏览器存储空间不足或不允许保存；导入未完成，原记录未更改');}
 return prepared;
}
function hasLab(labs,id){return typeof id==='string'&&record(labs)&&own(labs,id);}
const api={normalize,prepareImport,commitImport,hasLab,MAX_NOTE_CHARS,MAX_STATE_CHARS};
if(typeof module!=='undefined'&&module.exports)module.exports=api;
root.LearningState=api;
})(typeof window==='undefined'?globalThis:window);
