"""Independent analytic, convergence and conservation checks for the CFD course."""
import importlib.util
from decimal import Decimal, localcontext
import subprocess
import sys
import json
import math
from pathlib import Path
root=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('transport',root/'examples/cfd/transport_fvm.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

# Independent high-precision evaluation of the original exponential ratio.
# 400 decimal digits retain the difference even at the smallest positive float.
pe_values = (0., math.nextafter(0., 1.), 1e-310, 1e-17, 1e-12,
             math.nextafter(1e-8, 0.), 1e-8, math.nextafter(1e-8, 1.),
             1e-6, .1, 1., 5., 10., 60., 100.)
x_values = (0., 1e-12, .01, .25, .5, .75, .99, math.nextafter(1., 0.), 1.)
reference_checks = 0
with localcontext() as context:
 context.prec = 400
 for pe in pe_values:
  values = []
  for x in x_values:
   px, pp = Decimal.from_float(x), Decimal.from_float(pe)
   ref = float(px if pe == 0 else ((pp*px).exp()-1)/(pp.exp()-1))
   actual = m.exact(x, pe)
   assert math.isfinite(actual) and 0 <= actual <= 1, (x, pe, actual)
   assert math.isclose(actual, ref, rel_tol=2e-14, abs_tol=1e-320), (x, pe, actual, ref)
   values.append(actual)
   reference_checks += 1
  assert values[0] == 0 and values[-1] == 1, (pe, values)
  assert all(a <= b for a, b in zip(values, values[1:])), pe

# The formerly cancelled reference falsely distorted this near-diffusion study.
# Run the public CLI so JSON output/observed_order and embedded lesson code stay useful.
cli = subprocess.run([sys.executable, str(root/'examples/cfd/transport_fvm.py'),
                      '--pe', '1e-6', '--scheme', 'central', '--study'],
                     check=True, capture_output=True, text=True)
rows = [json.loads(line) for line in cli.stdout.splitlines()]
assert [row['cells'] for row in rows] == [10, 20, 40, 80, 160]
assert all(1.99 < row['observed_order'] < 2.01 for row in rows[1:]), rows
zero_cli = subprocess.run([sys.executable, str(root/'examples/cfd/transport_fvm.py'),
                           '--pe', '0', '--study'], check=True, capture_output=True, text=True)
assert all('observed_order' not in json.loads(line) for line in zero_cli.stdout.splitlines())
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
print(json.dumps({'cfd':'passed','lessons':24,'finite_volume':'conservation, pure diffusion, boundedness, failure cases, convergence, small-Pe CLI', 'exact_reference_checks':reference_checks,'pipe_Nu':nu}))
