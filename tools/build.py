"""Validate Markdown lessons, generate a self-contained static data bundle. Python >=3.10."""
import hashlib, json, pathlib, re, sys
from urllib.parse import urlparse
ROOT=pathlib.Path(__file__).resolve().parents[1]
ORDER=['calculus','linear-algebra','thermodynamics','heat-transfer','fluid-mechanics','python','machine-learning']
def build():
    courses=[]; ids=set(); count=0; char_count=0
    for course_id in ORDER:
        folder=ROOT/'content'/course_id
        if not (folder/'course.json').exists():
            if '--partial' in sys.argv: continue
            raise ValueError(f'Missing course: {course_id}')
        course=json.loads((folder/'course.json').read_text(encoding='utf-8'))
        chapter_files=course.pop('lessons'); chapters=[]
        for filename in chapter_files:
            text=(folder/filename).read_text(encoding='utf-8')
            assert text.startswith('---json\n'), f'Invalid front matter: {filename}'
            meta,content=text[8:].split('\n---\n',1)
            lesson=json.loads(meta); lesson['content']=content.strip()
            assert lesson['id'] not in ids, 'Duplicate ID: '+lesson['id']
            ids.add(lesson['id'])
            for field in ['title','group','minutes','level','tags','objectives','prerequisites','summary','quiz']:
                assert field in lesson, f'{filename}: missing {field}'
            assert len(lesson['content'])>500, f'Lesson is too short: {filename}'
            assert '<details>' in content and '<summary>' in content, f'Missing solved exercises: {filename}'
            assert content.count('```')%2==0, f'Unclosed code fence: {filename}'
            q=lesson['quiz']; assert len(q['options'])>=3 and 0<=q['answer']<len(q['options'])
            assert q['explanation'].strip(), f'Missing quiz explanation: {filename}'
            chapters.append(lesson); count+=1; char_count+=len(re.findall(r'[\u4e00-\u9fff]',content))
        course['chapters']=chapters; courses.append(course)
    # Keep the standalone research companion identical to the runnable lesson.
    research=next((l for c in courses for l in c['chapters'] if l['id']=='machine-learning-47'),None)
    if research:
        examples=re.findall(r'```python\s*\n(.*?)```',research['content'],re.S)
        assert len(examples)==1, 'Research companion needs exactly one complete source example'
        companion=ROOT/'examples/thermal-ai/cooling_research.py'
        assert companion.is_file() and companion.read_text(encoding='utf-8').strip()==examples[0].strip(), 'Research companion is out of sync with lesson 47'
    cfd=next((l for c in courses for l in c['chapters'] if l['id']=='fluid-mechanics-61'),None)
    if cfd:
        examples=re.findall(r'```python\s*\n(.*?)```',cfd['content'],re.S)
        assert len(examples)==1 and (ROOT/'examples/cfd/transport_fvm.py').read_text(encoding='utf-8').strip()==examples[0].strip(), 'CFD companion out of sync'
    version=json.loads((ROOT/'version.json').read_text(encoding='utf-8'))
    baseline=json.loads((ROOT/'reviews/baseline-1.0.json').read_text(encoding='utf-8'))
    assert set(baseline['lesson_ids']) <= ids, 'Existing lesson IDs must be preserved for learning records'
    reviews=[]
    lesson_course={l['id']:c['id'] for c in courses for l in c['chapters']}
    for course in courses:
        course_id=course['id']
        audit=json.loads((ROOT/'reviews'/version['review_directory']/(course_id+'.json')).read_text(encoding='utf-8'))
        assert audit['course_id']==course_id
        records={r['id']:r for r in audit['records']}
        expected={l['id'] for l in course['chapters']}
        assert len(records)==len(audit['records']) and set(records)==expected, f'{course_id}: audit must cover every lesson exactly once'
        for topic in audit['added_topics']:
            assert isinstance(topic,str) and topic.strip() or isinstance(topic,dict) and topic.get('id') in expected and all(isinstance(topic.get(k),str) and topic[k].strip() for k in ('title','reason')), f'{course_id}: invalid added topic'
        for source in audit['sources']:
            parsed=urlparse(source['url'])
            assert parsed.scheme=='https' and parsed.hostname and not parsed.username and not parsed.password, 'Audit source must be HTTPS without credentials'
        covered=set()
        for row in audit['coverage_map']:
            assert row['reference_topics'] and row['lesson_ids'], f'{course_id}: empty coverage mapping'
            assert set(row['lesson_ids']) <= expected, f'{course_id}: coverage mapping links to unknown lessons'
            covered.update(row['lesson_ids'])
        assert covered==expected, f'{course_id}: unmapped lessons: {expected-covered}'
        for lesson in course['chapters']:
            record=records[lesson['id']]
            assert record['title']==lesson['title'], f'{lesson["id"]}: audit title is stale'
            for field in ('checked_concepts','proofs','changes','remaining_limits'):
                assert isinstance(record[field],list) and all(isinstance(s,str) and s.strip() for s in record[field]), f'{lesson["id"]}: invalid {field}'
            assert record['checked_concepts'] and record['changes'], f'{lesson["id"]}: audit lacks substantive details'
            for prerequisite in lesson['prerequisites']:
                if re.fullmatch(r'[a-z]+(?:-[a-z]+)*-\d+',prerequisite):
                    assert prerequisite in ids, f'{lesson["id"]}: unknown prerequisite {prerequisite}'
            for linked_course, linked_lesson in re.findall(r'\]\(#/course/([a-z-]+)/([a-z-]+-\d+)\)',lesson['content']):
                assert lesson_course.get(linked_lesson)==linked_course, f'{lesson["id"]}: broken lesson link {linked_lesson}'
        audit['records']=[records[l['id']] for l in course['chapters']]
        reviews.append(audit)
    version.update(lessons=count,reviewed=sum(len(a['records']) for a in reviews),original_lessons=len(baseline['lesson_ids']),added_lessons=count-len(baseline['lesson_ids']))
    # Curated mainline guidance is maintained separately from stable lesson records.
    guides=[]
    for path in sorted((ROOT/'content').glob('learning-guides-*.json')):
        guides.extend(json.loads(path.read_text(encoding='utf-8')))
    assert len({g['id'] for g in guides})==len(guides), 'Duplicate learning guide'
    for g in guides:
        assert g['id'] in ids and isinstance(g.get('mainline'),bool), 'Invalid learning guide'
        assert all(isinstance(g.get(k),str) and g[k].strip() for k in ('why','checkpoint')), 'Missing learning outcome'
        for kind in ('required','recommended'):
            assert isinstance(g.get(kind),list) and set(g[kind])<=ids and g['id'] not in g[kind], 'Invalid learning relation'
        assert not set(g['required']) & set(g['recommended']), 'A relation cannot be required and recommended'
    edges={g['id']:g['required'] for g in guides}
    def visit(node,trail):
        assert node not in trail, 'Cyclic required learning relation: '+node
        for parent in edges.get(node,[]): visit(parent,trail|{node})
    for node in edges: visit(node,set())
    target=ROOT/'site/assets/data.js'; target.parent.mkdir(parents=True,exist_ok=True)
    bundle='/* Generated from content/ and reviews/ by tools/build.py. Do not edit. */\n'
    for name,value in [('COURSES',courses),('TEXTBOOK_VERSION',version),('CONTENT_REVIEW',reviews),('LEARNING_GUIDES',guides)]:
        bundle+='window.'+name+' = '+json.dumps(value,ensure_ascii=False,separators=(',',':'))+';\n'
    target.write_text(bundle,encoding='utf-8',newline='\n')
    stats={'version':version['version'],'courses':len(courses),'lessons':count,'reviewed_lessons':version['reviewed'],'added_lessons':version['added_lessons'],'chinese_characters':char_count,'course_counts':{c['id']:len(c['chapters']) for c in courses}}
    (ROOT/'site/assets/content-stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    # Content-addressed resource queries prevent mixing old reader code with new lessons.
    # Normalize text line endings so Windows and Linux builds produce identical HTML.
    entry=ROOT/'site/index.html'
    def version_asset(match):
        asset=ROOT/'site'/match.group(2)
        digest=hashlib.sha256(asset.read_bytes().replace(b'\r\n',b'\n')).hexdigest()[:12]
        return match.group(1)+match.group(2)+'?v='+digest+'"'
    html=re.sub(r'((?:src|href)=")(assets/[^"?]+\.(?:js|css))(?:\?v=[a-f0-9]+)?"',version_asset,entry.read_text(encoding='utf-8'))
    entry.write_text(html,encoding='utf-8',newline='\n')
    print(json.dumps(stats,ensure_ascii=True,indent=2))
if __name__=='__main__': build()
