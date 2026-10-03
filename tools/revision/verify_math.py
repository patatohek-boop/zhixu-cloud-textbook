"""Independent equations/geometry and preservation checks for 2026-10-03 math additions.
Run: python tools/revision/verify_math.py [--root STAGED_OR_MERGED_ROOT]
Requires SymPy, mpmath. Does not use the author text's claimed verification strings.
"""
from pathlib import Path
import argparse,json,re,math,hashlib,xml.etree.ElementTree as ET
import sympy as s
import mpmath as mp
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[2]);p.add_argument('--output',type=Path)
a=p.parse_args();ROOT=a.root
# Nonempty source-line and canonical metadata hashes from b735293 (release-equivalent baseline).
BASE_HASHES={'calculus-02': {'source_nonempty_sha256': '22ea2d16b464b3e62ade77d66c4b9ff62c9795e2cbc78f7fe204b1780b497dbc', 'metadata_sha256': '8d676832ae91a8c7bbf3ad3c498e37d6cbd1c91186efe9b0c329adb74f78c63b'}, 'calculus-04': {'source_nonempty_sha256': 'e2a6634982e4a00cf73ec08c3dda5a1a88ed7f6f67b523c0e9d899e7827e207f', 'metadata_sha256': 'ecc5698bc4c6f8609927820655f42c01de6cdd74faa15dff4a2e3a7bccf56dac'}, 'linear-algebra-05': {'source_nonempty_sha256': '39f2f77188e5716f706cdbfb26b241283f1ed7c6b96b18000357b11454e2e9fc', 'metadata_sha256': '9d2df8aec5126110cf29e1044971894d5cb8e66081addf185843fb2090edf1a0'}, 'linear-algebra-06': {'source_nonempty_sha256': '8ba8d2221a8bf8643300238d5632fe04e7e616fee15284727a510a72a684464f', 'metadata_sha256': '1f2b6930c7997d889e496073a6a5209f4932dbd5cce1e7e3b928e275a76b0b28'}, 'calculus-15': {'source_nonempty_sha256': 'd2c171e92f65760cfdcd4a251ba0f514daf3af9f6f63468257cb86fe1050ff17', 'metadata_sha256': 'cf7efa6633b744d826c6bd62050015759a8d3d2da2fb4462e18d53dc92027004'}, 'calculus-17': {'source_nonempty_sha256': 'd04c310424dde2d76926b53488aea31a69e51529cb0335b766167f33a0c98e33', 'metadata_sha256': '7fa7e743cf06d391dcfa32bc84d8dc2dbf6b15e620afa46978390ba50bf0ee7f'}, 'calculus-27': {'source_nonempty_sha256': '6eee261ed3e1729996808cade1bd94078099b626dd32ef5c58a790e9dc8337ab', 'metadata_sha256': '71b442a7f6ad6aff63d6b2308229a2fc694b4a23da71550785547b04151fd340'}, 'linear-algebra-09': {'source_nonempty_sha256': 'd7ff837162bcb68415f359fc0b1b4a900b29df14bfae1e0c67ce56a7034b31bf', 'metadata_sha256': 'e009a7478725967d128565f9c9c49142c8a1f399486e77f5aae2b1329bcaaeed'}, 'calculus-25': {'source_nonempty_sha256': '430ae16ddf22a441ddc24ce5a99ffd638607e1d5049167c5502cd2157974e1d2', 'metadata_sha256': '8cc46d0097ade72072da2e5ebd2d1c5d63a0f4cab7bca9830d3c2617d6da7d63'}, 'calculus-05': {'source_nonempty_sha256': '00c1e313fd0cc503d1e3b53bfc9450888f1c1437bdfedd194eed8b431d1e380e', 'metadata_sha256': '7c2964c0762b5696cd7622e736598ba926450e29b71ab0b684b5901fd07a7f73'}, 'calculus-08': {'source_nonempty_sha256': '9b19b157d21d3efa5717640f31057230e37a7d73850fae2f6f6578041c59e722', 'metadata_sha256': 'ad217ac477140a24792fa6a3c882a304434dcf4e8d726d2305f68602349f47fd'}, 'calculus-12': {'source_nonempty_sha256': '787aef9801d1995055c3e237bc926477686fec4d4af4aa152692deff91207f4e', 'metadata_sha256': 'cdb2200ea0b6557396a05e3c38a7d37bd48ce0ec49396bfd91ba3aac092baff7'}, 'calculus-14': {'source_nonempty_sha256': '818897ff419d9be7350ea11f6eceeb35b8f243a7adef4edfef6c0478734c77e7', 'metadata_sha256': 'c72f870210f4cfeb02a8785c9d02bbd284d7b3069ce54aea9ec8a85670bf4d3d'}, 'calculus-19': {'source_nonempty_sha256': '1fc59d38b670450d3cad971e16fd4cf4601b2f35d1349adf5fd9f43a6ed1fb56', 'metadata_sha256': '8d2b275a5a98f2518b87edbff9cf33959a747b1618dbca98c8b04a16d87edd4f'}, 'calculus-22': {'source_nonempty_sha256': 'd5fe5e009d856ca2033630b1c0788f3dc35f99cbcde280be0db1147a5d30079c', 'metadata_sha256': '3ef1ed43ac8809165b0871edbc80c6f1e78f8f65392d4a7cbc76e9f98890ee26'}, 'calculus-24': {'source_nonempty_sha256': 'bde9f5beae1c24e539125dca2be0e2aa853de527cc8b4dcb86ff08e0b6f08e20', 'metadata_sha256': 'f3d47bd72ec44c550431c4c824b624b822792e16e4845bb7021e6bfaf956a0fc'}, 'linear-algebra-13': {'source_nonempty_sha256': '558b39d69321f71ca441701cf4af0118a8f23635233d5c654a5f54ce12e7b2ed', 'metadata_sha256': '9d3c720babebebdb2ff24d858c5b2d9ac4c59cabd127e1bf8391617336467653'}, 'linear-algebra-18': {'source_nonempty_sha256': 'b8d952f11701c748c3e9af1c56c3af59ada848d46bc33bdde9467f79cdbd5a19', 'metadata_sha256': '4c11ad97f43c0db196b1ce53196d9e1b462b1ead3a4eb387af1b49b93d8aed62'}}
checks=[]
def check(name,v):
    good=bool(v);checks.append({'check':name,'passed':good})
    if not good: raise AssertionError(name)
def eq(name,left,right): check(name,s.simplify(left-right)==0)
def mat(name,left,right):check(name,(left-right).applyfunc(s.simplify)==s.zeros(*left.shape))
x,t,u,v,r,z,th,eps=s.symbols('x t u v r z theta epsilon',real=True)
# M01: estimate constructed independently with exact endpoint upper bound.
for e in [s.Rational(1,10000),s.Rational(1,20),s.Rational(1,2),s.Integer(7)]:
 d=min(s.Integer(1),2*e)
 # Sup error over closed [2-d,2+d] is d/[2(2-d)], <= e. Open interval gives strict.
 check('M01 delta bound '+str(e),d/(2*(2-d))<=e)
 check('M01 avoid pole '+str(e),2-d>0)
eq('M01 rational error identity',1/x-s.Rational(1,2),(2-x)/(2*x))
for e in [s.Rational(3,100),s.Rational(1,10),s.Integer(9)]:
 d=min(1,e/3);check('square epsilon-delta bound '+str(e),3*d<=e)
# M02: chain and expanded polynomial.
q=5*(1+t/5)**3
eq('M02 chain rule',s.diff(q,t),3*(1+t/5)**2)
eq('M02 answer',s.diff(q,t).subs(t,5),12)
eq('M02 polynomial crosscheck',s.expand(q),5+3*t+s.Rational(3,5)*t*t+s.Rational(1,25)*t**3)
eq('starter cubic derivative',s.diff((1+2*x)**3,x).subs(x,1),54)
h=s.symbols('h',nonzero=True);eq('circle difference quotient',s.expand((s.pi*(2+h/10)**2-4*s.pi)/h),s.pi*(s.Rational(2,5)+h/100))
# M03/M04: solve independent systems, not just provided coefficients.
V=s.Matrix([[1,0],[0,1],[1,1]])
mat('M03 target',V*s.Matrix([3,2]),s.Matrix([3,2,5]))
check('M03 unreachable',V.row_join(s.Matrix([3,2,4])).rank()>V.rank())
check('M03 negative weight',list(V.gauss_jordan_solve(s.Matrix([-1,0,-1]))[0])==[-1,0])
B=s.Matrix([[1,1],[1,-1]]);C=B.row_join(s.Matrix([2,0]))
mat('M04 basis coordinates',B.inv()*s.Matrix([5,1]),s.Matrix([3,2]))
mat('M04 all coefficient family',C*s.Matrix([3-t,2-t,t]),s.Matrix([5,1]))
check('M04 rank and nullity',C.rank()==2 and len(C.nullspace())==1)
mat('M04 RREF',C.rref()[0],s.Matrix([[1,0,1],[0,1,1]]))
# M05: limits, full derivative signs, holes/horizontal.
f=x*x/(x-1)
eq('asymptote division',f,x+1+1/(x-1))
check('asymptote left infinity',s.limit(f,x,1,dir='-')==-s.oo)
check('asymptote right infinity',s.limit(f,x,1,dir='+')==s.oo)
for direction in [-s.oo,s.oo]: eq('asymptote error '+str(direction),s.limit(f-x-1,x,direction),0)
eq('asymptote first derivative',s.diff(f,x),x*(x-2)/(x-1)**2)
eq('asymptote second derivative',s.diff(f,x,2),2/(x-1)**3)
for point,sign in [(-1,1),(s.Rational(1,2),-1),(s.Rational(3,2),-1),(3,1)]:check('asymptote derivative sign '+str(point),s.sign(s.diff(f,x).subs(x,point))==sign)
eq('M05 hole limit',s.limit((x*x-1)/(x-1),x,1),2)
for direction in [-s.oo,s.oo]:
 eq('M05 reciprocal horizontal '+str(direction),s.limit(1/(x-1),x,direction),0)
 eq('M05 rational horizontal '+str(direction),s.limit((2*x*x+1)/(x*x+1),x,direction),2)
eq('M05 ordinary point',((2*x*x+1)/(x*x+1)).subs(x,1),s.Rational(3,2))
# M06: independent apart and derivative, coefficient system.
F=(4*x*x-2*x+2)/((x-1)**2*(x*x+1))
A,Bb,Cc,D=s.symbols('A B C D'); numerator=s.expand(A*(x-1)*(x*x+1)+Bb*(x*x+1)+(Cc*x+D)*(x-1)**2-(4*x*x-2*x+2))
sol=s.solve(s.Poly(numerator,x).all_coeffs(),[A,Bb,Cc,D]);check('M06 independent coefficients',sol=={A:1,Bb:2,Cc:-1,D:1})
eq('M06 independently apart',s.apart(F,x),1/(x-1)+2/(x-1)**2+(1-x)/(x*x+1))
primitive=s.log(s.Abs(x-1))-2/(x-1)-s.log(x*x+1)/2+s.atan(x)
# derivative of ln|x-1| is 1/(x-1), for both allowed real intervals.
eq('M06 primitive derivative',1/(x-1)+s.diff(primitive-s.log(s.Abs(x-1)),x),F)
for lo,hi in [(-2,0),(2,4)]:
 val=mp.quad(s.lambdify(x,F,'mpmath'),[lo,hi]);pf=s.lambdify(x,primitive,'mpmath');check('M06 numerical endpoint '+str(lo),abs(val-(pf(hi)-pf(lo)))<1e-12)
# M07 direct quadrature vs trig antiderivative.
g=s.sqrt(4-x*x);G=x*g/2+2*s.asin(x/2)
eq('M07 primitive derivative',s.diff(G,x),g)
eq('M07 exact integral',s.integrate(g,(x,0,1)),s.pi/3+s.sqrt(3)/2)
check('M07 numerical quadrature',abs(mp.quad(lambda y:mp.sqrt(4-y*y),[0,1])-(mp.pi/3+mp.sqrt(3)/2))<1e-12)
# M08: coefficients/radius and endpoint finite remainders; convergence arguments also need prose review.
n=s.symbols('n',integer=True,positive=True)
eq('M08 coefficient radius',s.limit((n+1)*3/n,n,s.oo),3)
for val in [s.Rational(-1,2),s.Rational(1,3)]:
 total=sum(val**k/s.Integer(k) for k in range(1,151));check('M08 interior independent sum '+str(val),abs(float(total+s.log(1-val)))<1e-14)
check('M08 right endpoint harmonic divergence',s.Sum(1/n,(n,1,s.oo)).doit()==s.oo)
check('M08 left endpoint not absolute',s.Sum(s.Abs((-1)**n/n),(n,1,s.oo)).doit()==s.oo)
# Generalized binomial coefficient recurrence for noninteger alpha, finite identities.
alpha=s.symbols('alpha')
for k in range(7):
 ck=s.prod(alpha-j for j in range(k))/s.factorial(k); cn=s.prod(alpha-j for j in range(k+1))/s.factorial(k+1)
 eq('binomial recurrence '+str(k),(k+1)*cn,(alpha-k)*ck)
# Log/arctan finite geometric remainder formulas.
for N in [0,1,4,9]:
 eq('log finite remainder '+str(N),1/(1+x)-sum((-x)**k for k in range(N+1)),(-x)**(N+1)/(1+x))
 eq('arctan finite remainder '+str(N),1/(1+x*x)-sum((-1)**k*x**(2*k) for k in range(N+1)),(-1)**(N+1)*x**(2*N+2)/(1+x*x))
# M09 exact quadrature and rigorous alternating bound.
Q=sum((-1)**k*s.Rational(1,2)**(2*k+1)/(s.factorial(k)*(2*k+1)) for k in range(4));bound=s.Rational(1,110592)
eq('M09 four terms',Q,s.Rational(1,2)-s.Rational(1,24)+s.Rational(1,320)-s.Rational(1,5376))
mp.mp.dps=50;I=mp.quad(lambda y:mp.exp(-y*y),[0,mp.mpf('.5')]);error=I-mp.mpf(str(s.N(Q,55)))
check('M09 direction and absolute bound',0<error<mp.mpf(str(s.N(bound,55)))<mp.mpf('1e-5'))
# M10 geometric bounds and independent horizontal/vertical integration.
eq('example volume cylindrical',s.integrate(2*s.pi*r*(4-r*r),(r,0,2)),8*s.pi)
eq('example volume slicing',s.integrate(s.pi*z,(z,0,4)),8*s.pi)
eq('M10 volume',s.integrate(2*s.pi*r*(3-r*r),(r,0,s.sqrt(3))),9*s.pi/2)
M=s.integrate(2*s.pi*r*s.integrate(z,(z,r*r,3)),(r,0,s.sqrt(3)))
eq('M10 cylindrical mass',M,9*s.pi)
eq('M10 horizontal mass',s.integrate(z*s.pi*z,(z,0,3)),M)
eq('M10 average density',M/(9*s.pi/2),2)
# M11 surface cross products, field pullbacks, flux and scalar surface area.
for c,sgn,expected in [(0,1,-s.pi/2),(2,-1,5*s.pi/2)]:
 R=s.Matrix([u,v,c+sgn*(u*u+v*v)]);normal=R.diff(u).cross(R.diff(v));mat('surface normal '+str(c),normal,s.Matrix([-2*sgn*u,-2*sgn*v,1]));fielddot=R.dot(normal)
 polar=s.simplify(fielddot.subs({u:r*s.cos(th),v:r*s.sin(th)}));flux=s.integrate(polar*r,(r,0,1),(th,0,2*s.pi));eq('surface upward flux '+str(c),flux,expected)
 eq('surface area '+str(c),s.integrate(2*s.pi*r*s.sqrt(1+4*r*r),(r,0,1)),s.pi*(5*s.sqrt(5)-1)/6)
# independent Gauss closure verification for curved surfaces (not used in worked derivation).
eq('example flux closed crosscheck',3*(s.pi/2)-2*s.pi,-s.pi/2)
eq('M11 flux closed crosscheck',3*(s.pi/2)+s.pi,5*s.pi/2)
# M12 direct characteristic polynomials, kernels, substitutions.
A=s.Matrix([[4,2],[1,3]]);J=s.Matrix([[2,1],[0,2]])
eq('M12 first polynomial',(t*s.eye(2)-A).det(),(t-5)*(t-2))
for lam,vec in [(5,s.Matrix([2,1])),(2,s.Matrix([1,-1]))]:
 mat('M12 eigenvector '+str(lam),A*vec,lam*vec);check('M12 nullspace dimension '+str(lam),len((A-lam*s.eye(2)).nullspace())==1)
eq('M12 repeated polynomial',(t*s.eye(2)-J).det(),(t-2)**2)
check('M12 repeated geometric multiplicity',len((J-2*s.eye(2)).nullspace())==1)
mat('M12 repeated eigenvector',J*s.Matrix([1,0]),s.Matrix([2,0]))
# M13 Gram matrix eigenvectors, orthogonality and reconstruction, zero spaces.
A=s.Matrix([[3,1],[1,3],[0,0]]);B=s.Matrix([[1,1],[1,1],[0,0]])
V=s.Matrix([[1,1],[1,-1]])/s.sqrt(2);U=s.Matrix([[1/s.sqrt(2),1/s.sqrt(2),0],[1/s.sqrt(2),-1/s.sqrt(2),0],[0,0,1]])
mat('M13 V orthogonal',V.T*V,s.eye(2));mat('M13 U orthogonal',U.T*U,s.eye(3))
for name,matr,sigma in [('A',A,s.Matrix([[4,0],[0,2],[0,0]])),('B',B,s.Matrix([[2,0],[0,0],[0,0]]))]:
 mat('M13 reconstruct '+name,U*sigma*V.T,matr)
 mat('M13 Gram diagonal '+name,V.T*matr.T*matr*V,sigma.T*sigma)
 check('M13 actual dimensions '+name,matr.shape==(3,2) and U.shape==(3,3) and V.shape==(2,2))
mat('M13 input zero',B*V[:,1],s.zeros(3,1));mat('M13 left zero',B.T*U[:,1:],s.zeros(2,2))
check('M13 ranks',A.rank()==2 and B.rank()==1)
# M14 nonlinear solution and maximum interval boundary.
for y0,sol in [(s.Rational(1,4),1/(1+3*s.exp(-t))),(2,1/(1-s.exp(-t)/2))]:
 eq('logistic ODE '+str(y0),s.diff(sol,t),sol*(1-sol));eq('logistic initial '+str(y0),sol.subs(t,0),y0)
sol=1/(1-s.exp(-t)/2)
eq('M14 singular time',1-s.exp(-(-s.log(2)))/2,0)
check('M14 forward blowup boundary',s.limit(sol,t,-s.log(2),dir='+')==s.oo)
eq('M14 forward equilibrium',s.limit(sol,t,s.oo),1)
y1=2+s.Rational(1,10)*2*(1-2);eq('M14 Euler step',y1,s.Rational(9,5))
exact=float(sol.subs(t,s.Rational(1,10)));check('M14 numerical value',abs(exact-1.826213)<5e-7)
# Supremum repaired condition: old epsilon witness alone accepts u=1; upper-bound condition excludes it.
check('supremum counterexample witness',all(1-e<1<=1 for e in [1e-9,.1,1,100]))
check('supremum candidate excluded',not all(i<=1 for i in [0,1,2]))
# Source preservation, quiz metadata equality, 14 unique added identifiers.
# 1.5.0 retains its immutable pre-revision hashes. 1.6.0 uses the reviewed
# metadata/source mapping after authorized heading and reader restructuring.
version=json.loads((ROOT/'version.json').read_text(encoding='utf-8'))['version']
check('known preservation contract',version in ('1.5.0','1.6.0'))
reviewed={}
if version=='1.6.0':
 review=json.loads((ROOT/'reviews/reader-revision-1.6.0.json').read_text(encoding='utf-8'))
 check('1.6 reviewed source snapshot',review['version']=='1.6.0' and review['status']=='reviewed')
 reviewed={row['id']:row for row in review['lesson_mapping']}
 check('1.6 complete reviewed mapping',len(reviewed)==len(review['lesson_mapping'])==253)
manifest=[{'id':id,'path':f'content/{id.rsplit("-",1)[0]}/{id}.md'} for id in BASE_HASHES]
newids=[]
for item in manifest:
 rel=item['path'];new=(ROOT/rel).read_text(encoding='utf-8');newids+=re.findall(r'##+ (?:桥梁自检|练习) (M\d+)',new)
 metadata_hash=hashlib.sha256(json.dumps(json.loads(new[8:].split('\n---\n',1)[0]),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
 if version=='1.6.0':
  row=reviewed[item['id']]
  check('reviewed lesson path '+item['id'],row['path']==rel)
  check('reviewed metadata unchanged '+item['id'],metadata_hash==row['after_metadata_sha256'])
  check('reviewed source unchanged '+item['id'],hashlib.sha256(new.encode()).hexdigest()==row['after_sha256'])
 else:
  check('metadata unchanged '+item['id'],metadata_hash==BASE_HASHES[item['id']]['metadata_sha256'])
  clean=re.sub(r'<!-- math-revision-20261003:[^\n]+:start -->\n.*?<!-- math-revision-20261003:[^\n]+:end -->\n','',new,flags=re.S)
  if item['id']=='calculus-25': clean=clean.replace(r'等价地，$u$ 是 $S$ 的上界，并且对每个 $\varepsilon>0$，都能找到 $s\in S$ 使 $u-\varepsilon<s\le u$。',r'等价地，每个 $\varepsilon>0$ 都能找到 $s\in S$ 使 $u-\varepsilon<s\le u$。')
  check('old text preserved '+item['id'],hashlib.sha256('\n'.join(l for l in clean.splitlines() if l.strip()).encode()).hexdigest()==BASE_HASHES[item['id']]['source_nonempty_sha256'])
 check('details balanced '+item['id'],len(re.findall(r'<details(?:\s[^>]*)?>',new))==new.count('</details>'))
check('exact 14 exercise identifiers',sorted(newids)==[f'M{i:02}' for i in range(1,15)])
# SVG coordinate audit from independent transform specifications.
ns={'s':'http://www.w3.org/2000/svg'}
geometry=[('math-rational-asymptotes.svg',80,-30,310,325,[(0,0),(2,4)]),('math-paraboloid-bounds.svg',250,-73,95,420,[(0,0),(1,1),(1,4),(2,4)]),('math-bridge-basis.svg',75,-75,145,350,[(0,0),(1,1),(1,-1),(3,3),(4,2)])]
for name,sx,sy,ox,oy,expected in geometry:
 tree=ET.parse(ROOT/'site/assets/diagrams'/name)
 dots=tree.findall('.//s:circle',ns);check('SVG dot count '+name,len(dots)==len(expected))
 actual=[]
 for dot in dots:
  xx=float(dot.attrib['data-x']);yy=float(dot.attrib['data-y']);actual.append((xx,yy))
  check('SVG point '+name+str((xx,yy)),abs(float(dot.attrib['cx'])-(ox+sx*xx))<.001 and abs(float(dot.attrib['cy'])-(oy+sy*yy))<.001)
 check('SVG expected mathematical points '+name,actual==expected)
 check('SVG accessible text '+name,tree.find('s:title',ns) is not None and tree.find('s:desc',ns) is not None)
 check('SVG readable type '+name,all(float(el.attrib.get('font-size',21))>=20 for el in tree.findall('.//s:text',ns)))
 if name=='math-rational-asymptotes.svg':
  branches=tree.findall('.//s:polyline',ns);check('SVG rational separate branches',len(branches)==2)
  for j,poly in enumerate(branches):
   for point in poly.attrib['points'].split():
    px,py=map(float,point.split(','));xx=(px-ox)/sx;yy=(py-oy)/sy
    check('SVG rational branch domain',xx<1 if j==0 else xx>1)
    check('SVG rational sampled curve',abs(yy-xx*xx/(xx-1))<.03) # 0.001px rounding is magnified near pole.
 if name=='math-paraboloid-bounds.svg':
  for point in tree.findall('.//s:polyline',ns)[0].attrib['points'].split():
   px,py=map(float,point.split(','));rr=(px-ox)/sx;zz=(py-oy)/sy;check('SVG paraboloid sampled curve',abs(zz-rr*rr)<2e-5)
summary={'assertions':len(checks),'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'checks':checks,'limits':['Exact symbolic/numerical checks supplement manual proof and pedagogical review; they do not machine-prove all theorems.','1.5.0 uses immutable nonempty-line/metadata hashes; 1.6.0 uses exact reviewed source and canonical metadata hashes for the same 18 lessons. Hashes identify the reviewed text and do not prove mathematical correctness.']}
if a.output:a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:summary[k] for k in ['assertions','passed','failed']}))
