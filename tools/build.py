"""Validate Markdown lessons, generate a self-contained static data bundle. Python >=3.10."""
import json, pathlib, re, sys
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
    target=ROOT/'site/assets/data.js'; target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text('/* Generated from content/ by tools/build.py. Do not edit. */\nwindow.COURSES = '+json.dumps(courses,ensure_ascii=False,separators=(',',':'))+';\n',encoding='utf-8')
    stats={'courses':len(courses),'lessons':count,'chinese_characters':char_count,'course_counts':{c['id']:len(c['chapters']) for c in courses}}
    (ROOT/'site/assets/content-stats.json').write_text(json.dumps(stats,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(stats,ensure_ascii=True,indent=2))
if __name__=='__main__': build()
