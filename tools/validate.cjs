/* Validates all lesson mathematics and the numerical behavior of interactive labs. */
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm'),assert=require('node:assert/strict');
const root=path.resolve(__dirname,'..'),ctx={window:{}};
vm.runInNewContext(fs.readFileSync(path.join(root,'site/assets/data.js'),'utf8'),ctx);
const katex=require(path.join(root,'site/assets/vendor/katex/katex.min.js'));
const {LABS}=require(path.join(root,'site/assets/labs.js'));
let count=0,formulas=0,errors=[];
for(const course of ctx.window.COURSES)for(const l of course.chapters){
 count++;
 if(l.lab&&!LABS[l.lab])errors.push(`${l.id}: unknown lab ${l.lab}`);
 const inputs=[l.content,l.quiz.question,...l.quiz.options,l.quiz.explanation];
 for(let s of inputs){
  s=s.replace(/```[\s\S]*?```|`[^`\n]+`/g,'');
  for(const m of s.matchAll(/\$\$([\s\S]+?)\$\$|(?<!\\)\$([^$\n]+?)\$/g)){
   try{katex.renderToString(m[1]||m[2],{displayMode:!!m[1],throwOnError:true,strict:'ignore',trust:false});formulas++;}
   catch(e){errors.push(`${l.id}: ${m[0]} => ${e.message}`);}
  }
 }
 assert.equal((l.content.match(/<details>/g)||[]).length,(l.content.match(/<\/details>/g)||[]).length,`${l.id}: details mismatch`);
}
for(const [id,lab]of Object.entries(LABS)){
 const values=Object.fromEntries(lab.controls.map(c=>[c[0],c[5]]));
 for(const c of lab.controls)for(const v of [c[2],c[3],c[5]]){
  const result=lab.draw({...values,[c[0]]:v});
  assert.ok(!/NaN|Infinity|undefined/.test(result.svg+result.result),`${id}: nonfinite result`);
  assert.ok(result.svg.startsWith('<svg')&&result.result.length>10,`${id}: empty result`);
 }
}
assert.match(LABS.derivative.draw({x:1,h:.01}).result,/2\.010/);
assert.match(LABS.integral.draw({n:10}).result,/2\.660000/);
assert.match(LABS.matrix.draw({a:1,b:2,c:2,d:4}).result,/奇异/);
assert.match(LABS.carnot.draw({hot:600,cold:300}).result,/50\.0%/);
assert.match(LABS.conduction.draw({k:2,L:.1,hot:100,cold:20}).result,/1600\.0/);
assert.match(LABS.bernoulli.draw({v:2,ratio:.5}).result,/6\.000 kPa/);
assert.match(LABS['gradient-descent'].draw({rate:.5,start:3,steps:1}).result,/w = 0\.00000/);
const html=fs.readFileSync(path.join(root,'site/index.html'),'utf8');
for(const m of html.matchAll(/(?:src|href)="(assets\/[^"?#]+)"/g))assert.ok(fs.existsSync(path.join(root,'site',m[1])),`Missing asset ${m[1]}`);
if(errors.length){console.error(errors.join('\n'));process.exitCode=1;}
else console.log(JSON.stringify({lessons:count,renderedFormulas:formulas,labs:Object.keys(LABS).length,status:'passed'},null,2));
