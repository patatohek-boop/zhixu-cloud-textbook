"""Execute the actual lesson analyzer on normal, rejected and overflow inputs."""
from pathlib import Path
import contextlib
import io
import json
import re

def verify():
    lesson = (Path(__file__).resolve().parents[1] / 'content/python/python-25.md').read_text(encoding='utf-8')
    namespace = {'__name__': 'lesson_under_test'}
    with contextlib.redirect_stdout(io.StringIO()):
        for code in re.findall(r'```python\n(.*?)```', lesson, re.S):
            exec(compile(code, 'python-25.md', 'exec'), namespace)
    analyze = namespace['analyze']
    normal = analyze('sensor,temp_c\nA,20\nA,22\nB,24\nB,invalid\n')
    assert normal['summary'] == [{'sensor': 'A', 'count': 2, 'mean_c': 21.0}, {'sensor': 'B', 'count': 1, 'mean_c': 24.0}]
    assert len(normal['errors']) == 1
    huge = analyze('sensor,temp_c\nA,1e308\nA,1e308\n')
    assert huge['summary'][0]['mean_c'] == 1e308 and not huge['errors']
    json.dumps(huge, allow_nan=False)
    rejected = analyze('sensor,temp_c\nA,nan\nA,inf\nA,-274\n,20\nA,20,extra\n')
    assert rejected['summary'] == [] and len(rejected['errors']) == 5
    assert analyze('sensor,temp_c\n') == {'summary': [], 'errors': []}
    try:
        analyze('temp_c,sensor\n20,A\n')
    except ValueError:
        pass
    else:
        raise AssertionError('Wrong header accepted')
    return 6

if __name__ == '__main__':
    print(f'Audit regressions: {verify()} input scenarios passed.')
