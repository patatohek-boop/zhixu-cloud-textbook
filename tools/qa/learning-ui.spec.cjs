const {test,expect}=require('@playwright/test');
// Capture-only cleanup: assertions and real viewport shots keep all actual app chrome.
const cleanCaptureChrome='.topbar,.skip{visibility:hidden!important}';
async function open(page,hash){
 await page.goto('/'+hash);
 await page.waitForFunction(hash=>{
  if(location.hash!==hash||!window.ZHIXU)return false;
  const [kind,course,id]=hash.slice(2).split('/');
  if(kind==='labs'&&course)return !!document.querySelector('[data-lab="'+course+'"] .lab-chart svg');
  if(kind==='course'&&id){const lesson=window.ZHIXU.all.find(l=>l.id===id);return window.ZHIXU.state.last===id&&document.querySelector('.article-head h1')?.textContent===lesson?.title;}
  if(kind==='map'&&course){const c=window.COURSES.find(c=>c.id===course);return !!document.querySelector('[data-node-id="'+(id||c?.chapters[0]?.id)+'"]')&&(!id||document.querySelector('.topic-node.selected')?.dataset.nodeId===id);}
  if(kind==='map')return document.querySelectorAll('.map-course-card').length===7;
  if(kind==='path')return document.querySelectorAll('.core-route>li').length===window.LEARNING_GUIDES.filter(g=>!course||g.id.startsWith(course+'-')).length;
  return !!document.querySelector('#main h1');
 },hash);
}
async function noOverflow(page,label){await page.evaluate(()=>document.fonts.ready);const result=await page.evaluate(()=>({width:innerWidth,html:document.documentElement.scrollWidth,body:document.body.scrollWidth}));expect(result.html,label).toBeLessThanOrEqual(result.width+1);expect(result.body,label).toBeLessThanOrEqual(result.width+1);}
async function wheelToEdge(page,region,direction,label){
 const state=()=>region.evaluate(el=>{const r=el.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2,hit=document.elementFromPoint(x,y);return {left:el.scrollLeft,max:el.scrollWidth-el.clientWidth,width:el.clientWidth,scrollWidth:el.scrollWidth,overflow:getComputedStyle(el).overflowX,box:{x:r.x,y:r.y,width:r.width,height:r.height},visible:r.top>=0&&r.bottom<=innerHeight,hitInside:!!hit&&(hit===el||el.contains(hit)),hit:hit?.tagName+'.'+hit?.className};});
 for(let pulse=0;pulse<4;pulse++){
  await region.scrollIntoViewIfNeeded();await region.hover();await page.evaluate(()=>new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve))));
  const before=await state();console.log(label+' pulse '+pulse+' '+JSON.stringify(before));expect(before.visible,label+' target is visible').toBe(true);expect(before.hitInside,label+' pointer hits the intended scroll region').toBe(true);
  await page.mouse.wheel(direction*1000,0);
  // Let native scrolling settle visually. This never assigns a scroll position.
  await region.evaluate(el=>new Promise(resolve=>{let last=el.scrollLeft,stable=0,frames=0;function tick(){const now=el.scrollLeft;stable=Math.abs(now-last)<.1?stable+1:0;last=now;if(stable>=3||++frames>=45)resolve();else requestAnimationFrame(tick);}requestAnimationFrame(tick);}));
  const after=await state();console.log(label+' observed '+JSON.stringify(after));if(direction>0?after.max-after.left<=1:after.left<=1)return;
 }
 const last=await state();expect(direction>0?last.max-last.left:last.left,label+' must reach the requested edge with real wheel input: '+JSON.stringify(last)).toBeLessThanOrEqual(1);
}
async function horizontalScroll(page,regions,label,required,capturePath){
 for(let i=0;i<await regions.count();i++){
  const region=regions.nth(i);const overflow=await region.evaluate(el=>el.scrollWidth>el.clientWidth+4);if(!overflow)continue;
  await region.scrollIntoViewIfNeeded();await region.hover();const before=await region.evaluate(el=>el.scrollLeft);
  console.log(label+' region '+i+' '+JSON.stringify(await region.evaluate(el=>({width:el.clientWidth,scrollWidth:el.scrollWidth,overflow:getComputedStyle(el).overflowX,childWidth:el.firstElementChild?.getBoundingClientRect().width}))));
  await wheelToEdge(page,region,1,label+' forward');await expect.poll(()=>region.evaluate(el=>el.scrollLeft),{message:label+' scrolls to reveal its right side'}).toBeGreaterThan(before);
  await expect.poll(()=>region.evaluate(el=>el.scrollWidth-el.clientWidth-el.scrollLeft),{message:label+' reaches the actual right edge'}).toBeLessThanOrEqual(1);
  if(await region.evaluate(el=>el.classList.contains('katex-display'))){
   const edges=await region.evaluate(el=>({container:el.getBoundingClientRect().right,formula:el.querySelector(':scope > .katex').getBoundingClientRect().right}));
   expect(edges.formula,label+' final symbols are in view').toBeLessThanOrEqual(edges.container+1);
  }
  if(capturePath)await region.screenshot({style:cleanCaptureChrome,path:capturePath});
  await wheelToEdge(page,region,-1,label+' backward');await expect.poll(()=>region.evaluate(el=>el.scrollLeft),{message:label+' returns to the left edge'}).toBeLessThanOrEqual(1);
  console.log(label+': real horizontal wheel reaches both ends passed');return;
 }
 expect(required,label+' should include an overflowing mobile region').toBe(false);
}
test('all routes, layered maps, lesson links and readable widths',async({page},info)=>{
 const capture=['width-390','width-1440'].includes(info.project.name);const errors=[];page.on('pageerror',e=>errors.push(e.message));await open(page,'#/map');
 const data=await page.evaluate(()=>({courses:COURSES.map(c=>({id:c.id,lessons:c.chapters.map(l=>l.id)})),guides:LEARNING_GUIDES.map(g=>g.id)}));
 await expect(page.locator('.map-course-card')).toHaveCount(7);await noOverflow(page,'global map');
 if(capture)await page.screenshot({path:info.outputPath('map-overview.png'),fullPage:true});
 for(const c of data.courses){await open(page,'#/map/'+c.id);await expect(page.locator('[data-node-id]')).toHaveCount(c.lessons.length);await noOverflow(page,c.id+' map');
  await page.locator('#map-filter').selectOption('mainline');const visible=await page.locator('[data-node-id]:visible').count();expect(visible).toBeGreaterThan(0);await page.locator('#map-filter').selectOption('all');
  for(const id of c.lessons.filter(id=>info.project.name==='width-320'||data.guides.includes(id))){await open(page,'#/course/'+c.id+'/'+id);await noOverflow(page,id);await expect(page.locator('.math-error')).toHaveCount(0);if(info.project.name==='width-320'){await page.locator('#lesson-body details').evaluateAll(xs=>xs.forEach(d=>d.open=true));await noOverflow(page,id+' all proofs and answers expanded');}}
 }
 await open(page,'#/map/calculus/calculus-03');await expect(page.locator('.dependency-current')).toContainText('导数');await noOverflow(page,'local dependency diagram');if(capture)await page.screenshot({path:info.outputPath('map-local-dependencies.png'),fullPage:true});if(capture)await page.locator('.map-selected').screenshot({style:cleanCaptureChrome,path:info.outputPath('map-selected-concept.png')});
 await open(page,'#/path');await expect(page.locator('.core-route>li')).toHaveCount(30);await noOverflow(page,'mainline path');
 await open(page,'#/course/calculus/calculus-03');if(capture)await page.screenshot({path:info.outputPath('reader-starter.png'),fullPage:false});
 await page.locator('#reading-depth').click();await expect(page.locator('details.advanced-reading')).toHaveAttribute('open','');await noOverflow(page,'expanded original proof');
 await page.evaluate(()=>{window.print=()=>{window.__printOpened=[...document.querySelectorAll('.prose details')].every(d=>d.open);};});await page.locator('#print').click();expect(await page.evaluate(()=>window.__printOpened)).toBe(true);
 const originalParagraph=page.locator('details.advanced-reading p').first();const oldFont=await originalParagraph.evaluate(el=>parseFloat(getComputedStyle(el).fontSize));await page.locator('#font-up').click();await page.locator('#font-up').click();expect(await originalParagraph.evaluate(el=>parseFloat(getComputedStyle(el).fontSize))).toBeGreaterThan(oldFont);await noOverflow(page,'larger reader font');
 await page.locator('#theme').click();await expect(page.locator('body')).toHaveClass(/dark/);await noOverflow(page,'dark reader');if(capture)await page.screenshot({path:info.outputPath('reader-dark.png'),fullPage:false});
 expect(errors).toEqual([]);
});
test('controls, retained learning state, repeated navigation and preloaded offline runtime',async({page,context},info)=>{
 const capture=['width-390','width-1440'].includes(info.project.name);const external=[];await context.route('**/*',route=>{const u=route.request().url();if(!u.startsWith('http://127.0.0.1:8767/')&&!u.startsWith('data:')){external.push(u);return route.abort();}return route.continue();});
 await open(page,'#/course/calculus/calculus-03');await page.locator('#note-text').fill('测试笔记：先写差商，再求极限');await page.locator('#bookmark').click();await page.locator('[data-answer="2"]').click();await page.locator('#complete').click();
 await open(page,'#/map/calculus/calculus-03');await expect(page.locator('.map-done').first()).toBeVisible();await page.goBack();await expect(page.locator('#note-text')).toHaveValue('测试笔记：先写差商，再求极限');
 await page.reload();await expect(page.locator('#note-text')).toHaveValue('测试笔记：先写差商，再求极限');await expect(page.locator('#bookmark')).toHaveAttribute('aria-pressed','true');await expect(page.locator('#feedback')).toContainText('回答正确');
 const targets=await page.locator('.article-tools button').evaluateAll(xs=>xs.map(x=>({id:x.id,h:x.getBoundingClientRect().height,w:x.getBoundingClientRect().width})));for(const t of targets){expect(t.h,t.id).toBeGreaterThanOrEqual(44);expect(t.w,t.id).toBeGreaterThanOrEqual(44);}
 for(const id of ['foundation-energy','foundation-projection','foundation-mass']){await open(page,'#/labs/'+id);await expect(page.locator('.lab-chart svg').first()).toBeVisible();const before=await page.locator('.lab-result').innerText();const input=page.locator('[data-param]').first();const direction=await input.evaluate(el=>Number(el.value)>=Number(el.max)?'ArrowLeft':'ArrowRight');await input.press(direction);await expect(page.locator('.lab-result')).not.toHaveText(before);await page.locator('.lab-next').click();await expect(page.locator('.lab-step-count')).toContainText('2 /');await page.locator('.lab-preset').click();await page.locator('.lab-reset').click();await expect(page.locator('.lab-result')).toHaveText(before);await noOverflow(page,id);if(capture)await page.locator('.lab-card').screenshot({style:cleanCaptureChrome,path:info.outputPath(id+'.png')});await page.locator('#theme').click();await noOverflow(page,id+' dark');if(capture)await page.locator('.lab-card').screenshot({style:cleanCaptureChrome,path:info.outputPath(id+'-dark.png')});await page.locator('#theme').click();}
 // This checks already-loaded JS/content only. Initial offline loads and every packaged image are checked by the Android bundle/emulator tests.
 await context.setOffline(true);await page.locator('.topbar a[data-nav="map"]').click();await expect(page.locator('.knowledge-page')).toBeVisible();await page.locator('.map-course-card[href="#/map/thermodynamics"]').click();await page.locator('[data-node-id="thermodynamics-05"] .map-read').click();await expect(page.locator('#lesson-body')).toContainText('能量');await expect(page.locator('.lab-chart svg').first()).toBeVisible();expect(external).toEqual([]);
});

test('concept stories are controllable, readable and disposed on navigation',async({page},info)=>{
 const capture=['width-320','width-390','width-1440'].includes(info.project.name);
 const lessons=['thermodynamics/thermodynamics-05','heat-transfer/heat-transfer-03','heat-transfer/heat-transfer-07','fluid-mechanics/fluid-mechanics-07','python/python-06','machine-learning/machine-learning-07'];
 for(const lesson of lessons){
  await open(page,'#/course/'+lesson);const story=page.locator('.concept-story');await expect(story.locator('svg').first()).toBeVisible();
  const play=story.locator('[data-story-action=play]');await expect(play).toHaveAttribute('aria-pressed','false');
  const before=await story.innerText();await story.locator('[data-story-action=next]').click();await expect(story).not.toHaveText(before);
  await story.locator('[data-story-progress]').press('End');await noOverflow(page,lesson+' story');const labels=await story.locator('svg text').evaluateAll(xs=>xs.map(el=>{const t=el.getScreenCTM();return parseFloat(getComputedStyle(el).fontSize)*Math.hypot(t.a,t.b);}));for(const size of labels)expect(size,lesson+' diagram label px').toBeGreaterThanOrEqual(14);
  const dimensions=await story.locator('button').evaluateAll(xs=>xs.map(x=>({h:x.getBoundingClientRect().height,w:x.getBoundingClientRect().width})));for(const size of dimensions){expect(size.h).toBeGreaterThanOrEqual(44);expect(size.w).toBeGreaterThanOrEqual(44);}
  const slug=lesson.replace('/','-');if(capture)await story.screenshot({style:cleanCaptureChrome,path:info.outputPath(slug+'-story.png')});if(capture){await story.locator('.story-chart').screenshot({style:cleanCaptureChrome,path:info.outputPath(slug+'-diagram.png')});await story.locator('.story-chart').scrollIntoViewIfNeeded();await page.screenshot({path:info.outputPath(slug+'-real-viewport.png'),fullPage:false});}
  await page.locator('#theme').click();await noOverflow(page,lesson+' story dark');if(capture&&info.project.name!=='width-320')await story.screenshot({style:cleanCaptureChrome,path:info.outputPath(slug+'-story-dark.png')});await page.locator('#theme').click();
  await story.locator('[data-story-action=replay]').click();await expect(play).toHaveAttribute('aria-pressed','false');
  // Reduced-motion mode allows explicit manual steps but must never start playing on navigation.
  await page.locator('.topbar a[data-nav="map"]').click();await expect(page.locator('.concept-story')).toHaveCount(0);
 }
});

test('every new diagram can be enlarged to readable labels without leaving the lesson',async({page},info)=>{
 const fs=require('node:fs'),path=require('node:path'),capture=['width-320','width-390','width-1440'].includes(info.project.name);
 await open(page,'#/path');const guides=await page.evaluate(()=>LEARNING_GUIDES.filter(g=>MASTERY_EXERCISES.some(e=>e.lessonId===g.id)).map(g=>({id:g.id,course:ZHIXU.all.find(l=>l.id===g.id).course.id})));
 for(const guide of guides){
  const hash='#/course/'+guide.course+'/'+guide.id;await open(page,hash);const image=page.locator('#lesson-body figure img[src*="learn-"]').first();await expect(image).toBeVisible();const src=await image.getAttribute('src');
  const svg=fs.readFileSync(path.resolve(__dirname,'../../site',src),'utf8'),box=svg.match(/viewBox="([^"]+)"/)[1].trim().split(/\s+/).map(Number),fonts=[...svg.matchAll(/font-size\s*(?:=|:)\s*["']?(\d+(?:\.\d+)?)/g)].map(m=>Number(m[1]));expect(fonts.length,src).toBeGreaterThan(0);
  const minFont=Math.min(...fonts);const link=image.locator('..');await expect(link).toHaveAttribute('aria-haspopup','dialog');await image.click();await expect(page.locator('#figure-dialog')).toBeVisible();
  const enlarged=page.locator('.figure-enlarged');const actual=await enlarged.boundingBox();expect(minFont*actual.width/box[2],src+' enlarged minimum label px').toBeGreaterThanOrEqual(14);
  const before=await page.locator('#figure-zoom').textContent();await page.getByRole('button',{name:'放大图片',exact:true}).click();await expect(page.locator('#figure-zoom')).not.toHaveText(before);await noOverflow(page,guide.id+' figure viewer');
  if(capture&&guide.id==='python-20')await page.screenshot({path:info.outputPath('readable-diagram-viewer.png'),fullPage:false});
  await page.getByRole('button',{name:'关闭大图',exact:true}).click();await expect(page.locator('#figure-dialog')).not.toBeVisible();await expect(link).toBeFocused();expect(new URL(page.url()).hash).toBe(hash);if(guide.id==='python-20'){await link.press('Enter');await expect(page.locator('#figure-dialog')).toBeVisible();await page.keyboard.press('Escape');await expect(page.locator('#figure-dialog')).not.toBeVisible();await expect(link).toBeFocused();}
 }
});

test('tiered practice reveals verified solutions without automatic grading',async({page},info)=>{
 const capture=['width-320','width-390','width-1440'].includes(info.project.name);await open(page,'#/path');
 const guides=await page.evaluate(()=>LEARNING_GUIDES.filter(g=>MASTERY_EXERCISES.some(e=>e.lessonId===g.id)).map(g=>({id:g.id,course:ZHIXU.all.find(l=>l.id===g.id).course.id})));
 for(const guide of guides){
  await open(page,'#/course/'+guide.course+'/'+guide.id);const practice=page.locator('.mastery-practice');await expect(practice).toBeVisible();await expect(practice.locator('.mastery-card')).toHaveCount(3);await expect(practice.locator('.mastery-intro')).toContainText('不会自动评分');
  const first=practice.locator('.mastery-answer').first();await expect(first).not.toHaveAttribute('open','');await first.locator('summary').click();await expect(first).toHaveAttribute('open','');await expect(first.locator('.mastery-solution')).toBeVisible();await first.locator('summary').click();await expect(first).not.toHaveAttribute('open','');
  await practice.locator('details').evaluateAll(xs=>xs.forEach(d=>d.open=true));await noOverflow(page,guide.id+' exercise solutions');await expect(page.locator('.math-error')).toHaveCount(0);await expect(practice.locator('[data-answer],input')).toHaveCount(0);
  if(guide.id==='fluid-mechanics-01'||guide.id==='python-07'){
   const kind=guide.id==='fluid-mechanics-01'?'.katex-display':'pre';
   await horizontalScroll(page,practice.locator(kind),guide.id+' '+info.project.name,['width-320','width-390'].includes(info.project.name),capture?info.outputPath(guide.id+'-horizontally-scrolled.png'):null);
  }
  if(guide.id==='python-07'){
   const spacing=await practice.locator('pre').evaluateAll(xs=>xs.map(pre=>{const code=pre.querySelector('code'),button=pre.querySelector('.copy-code'),walker=document.createTreeWalker(code,NodeFilter.SHOW_TEXT);const first=walker.nextNode();const range=document.createRange();range.setStart(first,0);range.setEnd(first,1);return {firstLine:range.getBoundingClientRect().top,buttonBottom:button.getBoundingClientRect().bottom};}));
   for(const box of spacing)expect(box.firstLine,'Copy control leaves the first code line unobstructed').toBeGreaterThanOrEqual(box.buttonBottom+4);
  }
  if(capture&&['calculus-03','fluid-mechanics-01','python-07','machine-learning-07'].includes(guide.id)){
   const card=practice.locator('.mastery-card').last();await card.screenshot({style:cleanCaptureChrome,path:info.outputPath(guide.id+'-mastery.png')});await card.locator('summary').scrollIntoViewIfNeeded();await page.screenshot({path:info.outputPath(guide.id+'-mastery-real-viewport.png'),fullPage:false});
  }
 }
 await open(page,'#/course/calculus/calculus-03');const summary=page.locator('.mastery-answer summary').first();await summary.focus();await summary.press('Enter');await expect(page.locator('.mastery-answer').first()).toHaveAttribute('open','');await summary.press('Enter');await expect(page.locator('.mastery-answer').first()).not.toHaveAttribute('open','');
 await page.locator('.mastery-answer').first().evaluate(d=>d.open=true);const solutionParagraph=page.locator('.mastery-solution p').first();const initialSize=await solutionParagraph.evaluate(el=>parseFloat(getComputedStyle(el).fontSize));await page.locator('#font-up').click();await page.locator('#font-up').click();expect(await solutionParagraph.evaluate(el=>parseFloat(getComputedStyle(el).fontSize))).toBeGreaterThan(initialSize);await noOverflow(page,'enlarged practice solution font');
 await page.locator('#theme').click();await page.locator('.mastery-answer').evaluateAll(xs=>xs.forEach(d=>d.open=true));await noOverflow(page,'dark practice');if(capture)await page.locator('.mastery-card').first().screenshot({style:cleanCaptureChrome,path:info.outputPath('mastery-dark.png')});
});

test('report revision examples, continuation path and diagrams remain readable',async({page},info)=>{
 const fs=require('node:fs'),path=require('node:path');
 const revision=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../../reviews/report-revision-2026-10-03.json'),'utf8'));
 const capture=['width-390','width-1440'].includes(info.project.name);
 await open(page,'#/path');await expect(page.locator('.core-continuation')).toContainText('本科核心续学');
 await expect(page.locator('.core-continuation .relation')).toHaveCount(6);await noOverflow(page,'undergraduate continuation');
 if(capture){await page.locator('.core-continuation h2').scrollIntoViewIfNeeded();await page.screenshot({path:info.outputPath('report-core-continuation.png'),fullPage:false});}
 const continuationCourses=await page.evaluate(()=>COURSES.map(c=>c.id));for(const course of continuationCourses){await open(page,'#/path/'+course);expect(await page.locator('.core-continuation .relation').count(),course+' has follow-on core work').toBeGreaterThan(0);await noOverflow(page,course+' continuation');}
 for(const entry of revision.visual_checks){
  const hash='#/course/'+entry.course+'/'+entry.id;await open(page,hash);
  await page.locator('#lesson-body details.advanced-reading').evaluateAll(xs=>xs.forEach(d=>d.open=true));
  const heading=page.locator('#lesson-body h2,#lesson-body h3').filter({hasText:entry.heading}).first();
  await expect(heading,entry.id+' reviewed section').toHaveCount(1);await heading.scrollIntoViewIfNeeded();
  await expect(page.locator('.math-error')).toHaveCount(0);await noOverflow(page,entry.id+' reviewed section');
  if(capture)await page.screenshot({path:info.outputPath('report-'+entry.id+'.png'),fullPage:false});
  // Also inspect the complete worked/variant answer at the narrowest width.
  await page.locator('#lesson-body details').evaluateAll(xs=>xs.forEach(d=>d.open=true));await noOverflow(page,entry.id+' revised answers');
  for(const src of entry.diagrams||[]){
   const image=page.locator('#lesson-body figure img').filter({visible:true}).and(page.locator('img[src="'+src+'"]')).first();
   await expect(image).toBeVisible();expect(await image.evaluate(el=>el.complete&&el.naturalWidth>0),src).toBe(true);
   const anchor=image.locator('..');await expect(anchor).toHaveAttribute('aria-haspopup','dialog');await image.click();
   await expect(page.locator('#figure-dialog')).toBeVisible();await noOverflow(page,src+' figure dialog');
   const svg=fs.readFileSync(path.resolve(__dirname,'../../site',src),'utf8');
   const box=svg.match(/viewBox="([^"]+)"/)[1].trim().split(/\s+/).map(Number);
   const fonts=[...svg.matchAll(/font-size\s*(?:=|:)\s*["']?(\d+(?:\.\d+)?)/g)].map(m=>Number(m[1]));
   expect(fonts.length,src+' declares readable label sizes').toBeGreaterThan(0);
   let actual=await page.locator('.figure-enlarged').boundingBox();
   for(let clicks=0;Math.min(...fonts)*actual.width/box[2]<14&&clicks<6;clicks++){await page.getByRole('button',{name:'放大图片',exact:true}).click();actual=await page.locator('.figure-enlarged').boundingBox();}
   expect(Math.min(...fonts)*actual.width/box[2],src+' labels are readable using the provided zoom controls').toBeGreaterThanOrEqual(14);
   if(capture)await page.screenshot({path:info.outputPath('report-figure-'+path.basename(src,'.svg')+'.png'),fullPage:false});
   await page.getByRole('button',{name:'关闭大图',exact:true}).click();await expect(page.locator('#figure-dialog')).not.toBeVisible();expect(new URL(page.url()).hash).toBe(hash);
  }
 }
});
