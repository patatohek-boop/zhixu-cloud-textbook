"""Independent analytic, convergence and conservation checks for the CFD course."""
import importlib.util
import json
import math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('transport',root/'examples/cfd/transport_fvm.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
for scheme in ('upwind','central'):
 for n in (5,20,80):
  pure=m.solve(n,0,scheme)
  assert pure['l2']<1e-13
  assert max(abs(f+1) for f in pure['flux'])<1e-12
  for pe in (1,10,60):
   out=m.solve(n,pe,scheme)
   assert out['max_cell_imbalance']<1e-10
   assert out['global_imbalance']<1e-10
   if scheme=='upwind':assert out['bounded']
 errors=[m.solve(n,5,scheme)['l2'] for n in (40,80,160)]
 order=math.log(errors[-2]/errors[-1],2)
 assert (1.99<order<2.01) if scheme=='central' else (.95<order<1.01)
assert not m.solve(10,60,'central')['bounded']
for args in ((1,5,'upwind'),(10,-1,'central'),(10,float('nan'),'upwind'),(10,2,'unknown')):
 try:m.solve(*args)
 except ValueError:pass
 else:raise AssertionError('Invalid input accepted')
# Independent Simpson integration checks the constant-flux pipe result.
def simpson(f,n=1000):
 return (f(0)+f(1)+sum((4 if i%2 else 2)*f(i/n) for i in range(1,n)))/(3*n)
offset=simpson(lambda s:4*(s*s-s**4/4-.75)*(1-s*s)*s)
assert abs(offset+11/24)<1e-10
nu=-2/offset
assert abs(nu-48/11)<1e-9
rho,u,d,L,cp,q=1000,.1,.01,5,4200,1000
mdot=rho*u*math.pi*d*d/4;Q=q*math.pi*d*L
assert abs(Q/(mdot*cp)-100/21)<1e-12
assert abs(32*.001*u*L/d**2-160)<1e-12
# Every new lesson and referenced local figure must exist; prerequisites audited by build.py.
for n in range(39,63):
 text=(root/f'content/fluid-mechanics/fluid-mechanics-{n}.md').read_text(encoding='utf-8')
 assert text.count('<details>')>=2
 import re
 for image in re.findall(r'!\[[^\]]*\]\((assets/[^)]+)\)',text):assert (root/'site'/image).is_file(),image
print(json.dumps({'cfd':'passed','lessons':24,'finite_volume':'conservation, pure diffusion, boundedness, failure cases, convergence','pipe_Nu':nu}))
