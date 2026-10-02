"""Check the mathematics courses' sources, lesson links, KaTeX and worked results.

Run with Python 3 + SymPy and Node.js from the project root.
These checks corroborate examples and metadata; they are not automated theorem proofs.
"""
from pathlib import Path
import json
import re
import subprocess

import sympy as s

ROOT = Path(__file__).resolve().parents[1]
COURSES = ("calculus", "linear-algebra")
checks = []


def checked(label, condition):
    assert condition, label
    checks.append(label)


def equal(label, actual, expected):
    checked(label, s.simplify(actual - expected) == 0)


all_ids = set()
for path in (ROOT / "content").glob("*/*.md"):
    match = re.match(r"---json\s*\n(.*?)\n---\s*\n", path.read_text(encoding="utf-8"), re.S)
    if match:
        all_ids.add(json.loads(match[1])["id"])

lesson_total = 0
for course in COURSES:
    directory = ROOT / "content" / course
    manifest = json.loads((directory / "course.json").read_text(encoding="utf-8"))
    audit = json.loads((ROOT / "reviews/content-audit-2026-09" / (course + ".json")).read_text(encoding="utf-8"))
    records = {r["id"]: r for r in audit["records"]}
    checked(course + " unique audit records", len(records) == len(audit["records"]))
    ids = set()
    for filename in manifest["lessons"]:
        path = directory / filename
        text = path.read_text(encoding="utf-8")
        match = re.match(r"---json\s*\n(.*?)\n---\s*\n", text, re.S)
        assert match, str(path)
        meta = json.loads(match[1])
        lesson = meta["id"]
        checked(lesson + " unique ID", lesson not in ids)
        ids.add(lesson)
        lesson_total += 1
        checked(lesson + " audit title", records[lesson]["title"] == meta["title"])
        checked(lesson + " balanced details", text.count("<details>") == text.count("</details>"))
        checked(lesson + " code fences", len(re.findall(r"^```", text, re.M)) % 2 == 0)
        for target_course, target in re.findall(r"#/course/([a-z-]+)/([a-z-]+-\d+)", text):
            checked(lesson + " link " + target, target in all_ids and target.startswith(target_course + "-"))
        for pre in meta["prerequisites"]:
            if re.fullmatch(r"[a-z-]+-\d+", pre):
                checked(lesson + " prerequisite " + pre, pre in all_ids)
    mapped = {lesson for row in audit["coverage_map"] for lesson in row["lesson_ids"]}
    checked(course + " full audit coverage", ids == set(records) == mapped)
    checked(course + " manifest includes all files", set(manifest["lessons"]) == {p.name for p in directory.glob("*.md")})
    sources = {source["url"] for source in audit["sources"]}
    for row in audit["coverage_map"]:
        checked(course + " coverage topics are explicit", bool(row["reference_topics"]) and bool(row["knowledge_points"]))
        checked(course + " mapped sources exist", bool(row["source_urls"]) and set(row["source_urls"]) <= sources)

metadata_checks = len(checks)

# Independent symbolic checks of the expanded integration material.
x, y, u, v = s.symbols("x y u v", real=True)
a = s.symbols("a", positive=True)
equal("odd trig power antiderivative", s.diff(-s.cos(x)**3/3+s.cos(x)**5/5, x), s.sin(x)**3*s.cos(x)**2)
equal("even trig power integral", s.integrate(s.sin(x)**2*s.cos(x)**2, (x, 0, s.pi/2)), s.pi/16)
equal("completed-square rational antiderivative", s.diff(s.log(x*x+4*x+13)+s.atan((x+2)/3)/3, x), (2*x+5)/(x*x+4*x+13))
for m in range(2, 7):
    derivative = s.diff(x/(2*a*a*(m-1)*(x*x+a*a)**(m-1)), x)
    derivative += s.Rational(2*m-3, 2*(m-1))/a**2/(x*x+a*a)**(m-1)
    equal(f"repeated quadratic recurrence m={m}", derivative, 1/(x*x+a*a)**m)

def integral2(expr):
    return s.integrate(expr, (y, 0, 1), (x, 0, 2))

mass = integral2(1+x)
cx, cy = integral2(x*(1+x))/mass, integral2(y*(1+x))/mass
equal("nonuniform lamina mass", mass, 4)
equal("nonuniform centroid x", cx, s.Rational(7, 6))
equal("nonuniform centroid y", cy, s.Rational(1, 2))
equal("nonuniform polar inertia", integral2((x*x+y*y)*(1+x)), 8)
equal("centroid inertia direct integral", integral2(((x-cx)**2+(y-cy)**2)*(1+x)), s.Rational(14, 9))
equal("nonlinear change of variables direct", s.integrate(y, (y, 0, 1+x), (x, 0, 1)), s.Rational(7, 6))
equal("nonlinear change of variables transformed", s.integrate((1+u)**2*v, (v, 0, 1), (u, 0, 1)), s.Rational(7, 6))
equal("inclined surface metric area", s.Matrix([1, 0, 1]).cross(s.Matrix([0, 1, 2])).norm(), s.sqrt(6))
c, h = s.symbols("c h", positive=True)
actual_cell = s.integrate(2*u*(1+u)*h, (u, c-h/2, c+h/2))
equal("small-cell volume relative error", (actual_cell-2*c*(1+c)*h**2)/h**2, h**2/6)

# Exact Jordan block invariants survive a nontrivial change of basis.
def block(n):
    return s.Matrix(n, n, lambda i, j: int(j == i+1))

J = s.diag(block(3), block(2), block(1))
S = s.eye(6)
S[0, 3], S[4, 1], S[5, 2] = 2, -1, 3
N = S*J*S.inv()
nullities = [6-(N**k).rank() for k in range(1, 5)]
checked("Jordan nullities and block reconstruction", nullities == [3, 5, 6, 6])
checked("Jordan minimal polynomial degree", N**3 == s.zeros(6) and N**2 != s.zeros(6))
checked("same eigenspace dimensions do not imply similarity", (s.diag(block(3), block(1))**2).rank() != (s.diag(block(2), block(2))**2).rank())
nilpotent = block(3)
remainder = (nilpotent+3*nilpotent**2)/2
checked("Jordan polynomial finite inverse", (2*s.eye(3)+nilpotent+3*nilpotent**2)*(s.eye(3)-remainder+remainder**2)/2 == s.eye(3))

H = s.diag(1, -2, 0)
K = s.diag(3, 2, 1).T * H * s.diag(3, 2, 1)
checked("congruence worked example", K == s.diag(9, -8, 0))
bad = s.diag(0, -1)
checked("nonnegative leading minors insufficient for PSD", bad[:1, :1].det() == 0 and bad.det() == 0 and bad[1, 1] < 0)
R = s.Matrix([[0, -1], [1, 0]])
Q = s.Matrix([[1, 1], [-s.I, s.I]])/s.sqrt(2)
checked("normal complex rotation eigensystem", Q.H*Q == s.eye(2) and Q.H*R*Q == s.diag(s.I, -s.I))
defective = s.Matrix([[1, 1], [0, 1]])
checked("defective matrix nonnormal", defective.H*defective != defective*defective.H)
A = s.Matrix([[1, 0], [0, 1], [1, 1]])
Ap = (A.T*A).inv()*A.T
free = s.Matrix([[1, 2, 3], [4, 5, 6]])
checked("all-left-inverse family example", (Ap+free*(s.eye(3)-A*Ap))*A == s.eye(2))
B = s.Matrix([[-1, 0, 1], [1, -1, 0], [0, 1, -1]])
checked("triangle cycle flow", B*s.ones(3, 1) == s.zeros(3, 1))
checked("grounded network potential", B*B.T*s.Matrix([s.Rational(1, 3), -s.Rational(1, 3), 0]) == s.Matrix([1, -1, 0]))

# 2026-10 audit regressions: independently reproduce the clarified edge cases.
# Thin QR with signed Householder-style diagonal, followed by the stated D fix.
Q0 = s.Matrix([[-1, 0], [0, 0], [0, 1]])
R0 = s.Matrix([[-2, 3], [0, 4]])
D = s.diag(*[s.sign(R0[i, i]) for i in range(R0.rows)])
Q, R = Q0*D, D*R0
checked("QR signed-diagonal normalization preserves product", Q*R == Q0*R0)
checked("QR normalization preserves thin orthogonality", Q.T*Q == s.eye(2))
checked("QR normalized diagonal positive", all(R[i, i] > 0 for i in range(2)))

# Wide A has a zero-padded right singular direction that the row space of B may use.
A = s.Matrix([[3, 0, 0], [0, 2, 0]])
P = s.diag(0, 0, 1)
weights = [(P*s.eye(3)[:, i]).dot(P*s.eye(3)[:, i]) for i in range(3)]
checked("wide-matrix full right-basis weight sum", sum(weights) == P.rank() == 1)
checked("wide-matrix thin weight sum need not equal rank", sum(weights[:2]) == 0)
checked("wide-matrix zero-padded energy identity", (A*P).norm()**2 == sum(v*w for v, w in zip([9, 4, 0], weights)))

# Polynomial Jordan powers must include k=0 and lambda=0 without negative powers.
for size in (1, 2, 4):
 for eigenvalue in (0, s.Rational(1, 2), -2):
  nilpotent = block(size)
  J = eigenvalue*s.eye(size)+nilpotent
  for power in range(size+2):
   expansion = s.zeros(size)
   for j in range(min(power, size-1)+1):
    scalar = 1 if power == j else eigenvalue**(power-j)
    expansion += s.binomial(power, j)*scalar*nilpotent**j
   checked(f"Jordan polynomial power r={size}, lambda={eigenvalue}, k={power}", expansion == J**power)

# Nonlinear inverse: the Jacobian inverse is evaluated at the preimage, not x.
H = s.Matrix([s.exp(x), y+x*x])
Hinv = s.Matrix([s.log(u), v-s.log(u)**2])
preimage_jacobian = H.jacobian([x, y]).subs({x: s.log(u), y: v-s.log(u)**2})
checked("inverse Jacobian evaluated at preimage", s.simplify(Hinv.jacobian([u, v])-preimage_jacobian.inv()) == s.zeros(2))
checked("inverse Jacobian evaluation point matters", Hinv.jacobian([u, v]).subs({u: s.E, v: 1}) != H.jacobian([x, y]).subs({x: s.E, y: 1}).inv())

# Render directly from editable source, not possibly stale site/assets/data.js.
node_code = r'''
const fs=require('node:fs'), path=require('node:path');
const root=process.argv[1];
const katex=require(path.join(root,'site/assets/vendor/katex/katex.min.js'));
let formulas=0,errors=[];
for(const course of ['calculus','linear-algebra']) {
 const dir=path.join(root,'content',course);
 const manifest=JSON.parse(fs.readFileSync(path.join(dir,'course.json'),'utf8'));
 for(const file of manifest.lessons) {
  const text=fs.readFileSync(path.join(dir,file),'utf8');
  const m=text.match(/^---json\s*\n([\s\S]*?)\n---\s*\n/);
  const meta=JSON.parse(m[1]);
  const input=[text.slice(m[0].length),meta.quiz.question,...meta.quiz.options,meta.quiz.explanation].join('\n');
  const clean=input.replace(/```[\s\S]*?```|`[^`\n]+`/g,'');
  for(const match of clean.matchAll(/\$\$([\s\S]+?)\$\$|(?<!\\)\$([^$\n]+?)\$/g)) {
   try {katex.renderToString(match[1]||match[2], {displayMode:!!match[1],throwOnError:true,strict:'ignore',trust:false}); formulas++;}
   catch(e) {errors.push(meta.id+': '+e.message);}
  }
 }
}
if(errors.length) {console.error(errors.join('\n'));process.exit(1);}
console.log(JSON.stringify({formulas,status:'passed'}));
'''
render = subprocess.run(["node", "-e", node_code, str(ROOT)], capture_output=True, text=True, encoding="utf-8", check=True)
print(json.dumps({"status": "passed", "lessons": lesson_total, "checks": len(checks), "metadataChecks": metadata_checks, "mathematicalChecks": len(checks)-metadata_checks, "katex": json.loads(render.stdout), "limits": "Symbolic and numerical checks validate examples, not every theorem proof."}, ensure_ascii=False, indent=2))
