"""Read-only HEOS 7.2.0 audit of existing textbook property records.

Run: python -B tools/recheck_thermal_heos.py
Optional isolated imports: --deps work/thermal-property-deps
Optional detailed result: --output work/thermal-heos-recheck.json
Optional compact result: --summary-output reviews/thermal-heos-result.json
Requires CoolProp==7.2.0 and NumPy on the normal Python import path or in
the explicitly supplied dependency directory. The script never installs
dependencies and never changes content or tables.
This reproduces equation-of-state models, not experimental measurements.
"""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import sys, json, math, hashlib, platform, argparse

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--deps', type=Path, help='Optional dependency directory; otherwise use the normal Python import path.')
parser.add_argument('--output', type=Path, help='Optional detailed JSON output. Without this option no detailed file is written.')
parser.add_argument('--summary-output', type=Path, help='Optional compact JSON output suitable for committing to reviews/.')
args = parser.parse_args()
if args.deps is not None:
    dependency_dir = args.deps.resolve()
    if not dependency_dir.is_dir():
        parser.error('--deps must name an existing directory')
    sys.path.insert(0, str(dependency_dir))
import CoolProp
from CoolProp.CoolProp import PropsSI
import numpy

assert CoolProp.__version__ == '7.2.0'
if args.deps is not None:
    assert Path(CoolProp.__file__).resolve().is_relative_to(dependency_dir), 'CoolProp must come from the explicitly selected directory'
DATA_FILE = ROOT / 'content/thermal-property-cases.json'
original_data = DATA_FILE.read_bytes()
saved = json.loads(original_data)
assert saved['version'] == CoolProp.__version__
assert saved['gitrevision'] == CoolProp.__gitrevision__
checks, states = [], []

def prop(output, a, x, b, y, fluid):
    return PropsSI(output, a, x, b, y, 'HEOS::' + fluid)

def state(label, fluid, a, x, b, y):
    raw = {key: prop(output, a, x, b, y, fluid) * scale + offset
           for key, output, scale, offset in [
               ('p_kPa', 'P', .001, 0), ('T_C', 'T', 1, -273.15),
               ('h_kJkg', 'H', .001, 0), ('s_kJkgK', 'S', .001, 0),
               ('quality', 'Q', 1, 0)]}
    raw['v_m3kg'] = 1 / prop('D', a, x, b, y, fluid)
    states.append({'label': label, 'backend': 'HEOS', 'fluid': fluid,
                   'inputs_SI': {a: x, b: y}, 'computed': raw})
    return raw

def compare(label, value, target, tolerance=None, category='saved_model'):
    # Saved full-precision values: a small numerical/platform allowance only.
    # Printed values: caller passes half the last displayed decimal unit.
    tolerance = max(abs(target) * 1e-10, 1e-12) if tolerance is None else tolerance
    delta = value - target
    checks.append({'label': label, 'category': category, 'computed': value,
                   'saved_or_printed': target, 'difference': delta,
                   'absolute_tolerance': tolerance,
                   'within_tolerance': abs(delta) <= tolerance})

def compare_record(label, computed, existing):
    for key, value in computed.items():
        if isinstance(value, (float, int)):
            compare(f'{label}.{key}', value, existing[key])

def printed(label, value, token, category='printed_model'):
    # Displayed decimal strings preserve their published precision.
    token = token.replace('−', '-')
    decimals = len(token.split('.')[1]) if '.' in token else 0
    compare(label, value, float(token), .5 * 10 ** (-decimals) + 1e-12, category)

# State inputs manually transcribed from the actual case statements in
# thermodynamics-04/15/19/21 and heat-transfer-30, checked against
# tools/verify_thermal_cases.py. Original reproduction script is not executed.
water = [state(f'water_lookup[{i}]', 'Water', 'P', 1e6, 'T', t + 273.15)
         for i, t in enumerate([260, 265, 270])]
for i, row in enumerate(water):
    compare_record(f'water_lookup[{i}]', row, saved['water_lookup'][i])
pump = state('water_pump_model', 'Water', 'P', 3e6, 'S', 649.2)
compare_record('water_pump_model', pump, saved['water_pump_model'])

low, high = 200000., 1000000.
sat = [state(f'r134a.saturated[{i}]', 'R134a', 'P', p, 'Q', q)
       for i, (p, q) in enumerate([(low, 0), (low, 1), (high, 0), (high, 1)])]
for i, row in enumerate(sat):
    compare_record(f'r134a.saturated[{i}]', row, saved['r134a']['saturated'][i])
s1 = state('r134a.states.one', 'R134a', 'P', low, 'T', sat[0]['T_C'] + 273.15 + 5)
s2s = state('r134a.states.two_s', 'R134a', 'P', high, 'S', s1['s_kJkgK'] * 1000)
h2 = s1['h_kJkg'] + (s2s['h_kJkg'] - s1['h_kJkg']) / .8
s2 = state('r134a.states.two', 'R134a', 'P', high, 'H', h2 * 1000)
s3 = state('r134a.states.three', 'R134a', 'P', high, 'T', sat[2]['T_C'] + 273.15 - 5)
s4 = state('r134a.states.four', 'R134a', 'P', low, 'H', s3['h_kJkg'] * 1000)
cycle = dict(one=s1, two_s=s2s, two=s2, three=s3, four=s4)
for key, row in cycle.items():
    compare_record('r134a.states.' + key, row, saved['r134a']['states'][key])
lookup = [state(f'r134a.lookup[{i}]', 'R134a', 'P', high, 'T', t + 273.15)
          for i, t in enumerate([50, 55, 60])]
for i, row in enumerate(lookup):
    compare_record(f'r134a.lookup[{i}]', row, saved['r134a']['lookup'][i])
qL, win = s1['h_kJkg'] - s4['h_kJkg'], s2['h_kJkg'] - s1['h_kJkg']
refrigeration = dict(qL=qL, win=win, qH=s2['h_kJkg']-s3['h_kJkg'], COP=qL/win)
compare_record('r134a.results', refrigeration, saved['r134a']['results'])

def air(T):
    values = {key: prop(output, 'T', T, 'P', 101325., 'Air')
              for key, output in [('rho', 'D'), ('mu', 'V'), ('k', 'L'),
                                  ('cp', 'C'), ('Pr', 'PRANDTL')]}
    states.append({'label': f'Air.{T:.12g}K', 'fluid': 'Air', 'backend': 'HEOS',
                   'inputs_SI': {'T': T, 'P': 101325.}, 'computed': values})
    return values

air_table = {}
for i, T in enumerate([300., 305., 310., 315., 333.15]):
    air_table[T] = air(T)
    compare_record(f'tube.properties[{i}]', air_table[T], saved['tube']['properties'][i])
inlet, surface = air(293.15), air_table[333.15]
massflow, area = inlet['rho'] * 2.0 * .12, 80 * math.pi * .02
Tout, iterations = 320., []
for i in range(8):
    Tb = (293.15 + Tout) / 2
    bulk = air(Tb)
    vmax = massflow / (bulk['rho'] * .04)
    Re = massflow * .02 / (.04 * bulk['mu'])
    Nu = .27 * Re ** .63 * bulk['Pr'] ** .36 * (bulk['Pr'] / surface['Pr']) ** .25
    h = Nu * bulk['k'] / .02
    ntu = h * area / (massflow * bulk['cp'])
    next_T = 333.15 - 40 * math.exp(-ntu)
    row = [Tout-273.15, Tb, Re, Nu, h, next_T-273.15]
    for j, value in enumerate(row):
        compare(f'tube.iterations[{i}][{j}]', value, saved['tube']['iterations'][i][j])
    iterations.append(row)
    Tout = next_T
tube = dict(rho_in=inlet['rho'], mdot=massflow, As=area,
            rho_b=bulk['rho'], mu_b=bulk['mu'], k_b=bulk['k'], cp_b=bulk['cp'],
            Pr_b=bulk['Pr'], Pr_s=surface['Pr'], Vmax=vmax, Re=Re, Nu=Nu,
            h=h, NTU=ntu, Tout_C=Tout-273.15, Q_W=massflow*bulk['cp']*(Tout-293.15))
compare_record('tube', tube, saved['tube'])

# Cross-check NIST printed water rows; these are published IAPWS-95 table
# values, not independently measured data. Never test interpolated estimates
# as if they were exact EOS values at the interior state.
for i, values in [(0, ['2965.1', '6.9681', '0.23788']),
                  (2, ['2986.9', '7.0087', '0.24296'])]:
    for key, token in zip(['h_kJkg', 's_kJkgK', 'v_m3kg'], values):
        printed(f'thermodynamics-04.NIST.{water[i]["T_C"]}.{key}', water[i][key], token, 'printed_NIST')
for key, token in zip(['h_kJkg', 's_kJkgK', 'v_m3kg'], ['2976.053', '6.988545', '0.240426']):
    printed('thermodynamics-04.HEOS.265C.' + key, water[1][key], token)
printed('thermodynamics-04.Tsat_1MPa', prop('T','P',1e6,'Q',0,'Water')-273.15,'179.878','printed_NIST')
water_f = state('NIST.water.sat_liquid_10kPa', 'Water', 'P', 10000., 'Q', 0)
water_g = state('NIST.water.sat_vapor_10kPa', 'Water', 'P', 10000., 'Q', 1)
for name, row, vals in [('liquid', water_f, ['45.806','191.81','0.64920','0.00101027']),
                         ('vapor',water_g,['45.806','2583.9','8.1488','14.670'])]:
    for key, token in zip(['T_C','h_kJkg','s_kJkgK','v_m3kg'], vals):
        printed(f'thermodynamics-15.NIST.10kPa.{name}.{key}', row[key], token,'printed_NIST')
rankine3 = state('NIST.water.3MPa_400C','Water','P',3e6,'T',673.15)
for key, token in zip(['h_kJkg','s_kJkgK','v_m3kg'], ['3231.7','6.9234','0.099379']):
    printed('thermodynamics-15.NIST.3MPa_400C.'+key,rankine3[key],token,'printed_NIST')
printed('thermodynamics-15.Tsat_3MPa',prop('T','P',3e6,'Q',0,'Water')-273.15,'233.853','printed_NIST')
printed('thermodynamics-15.exact_pump_temperature',pump['T_C'],'45.9')
for t, value in saved['humid']['ps_kPa'].items():
    ps = prop('P','T',float(t)+273.15,'Q',0,'Water')/1000
    compare(f'thermodynamics-21.NIST.psat_{t}C_kPa',ps,value,5e-5+1e-12,'printed_NIST')

# Read the actual published Markdown table cells, preserving decimal precision.
def rows(path):
    return [[cell.strip().replace('−','-') for cell in line.strip().strip('|').split('|')]
            for line in (ROOT/path).read_text(encoding='utf-8').splitlines()
            if line.startswith('|')]
rrows = rows('content/thermodynamics/thermodynamics-19.md')
for pressure, liquid, vapor in [('0.200',sat[0],sat[1]),('1.000',sat[2],sat[3])]:
    row = next(r for r in rrows if r[0]==pressure and len(r)==6)
    for name, value, token in zip(['T','hf','hg','sf','sg'],
             [liquid['T_C'],liquid['h_kJkg'],vapor['h_kJkg'],liquid['s_kJkgK'],vapor['s_kJkgK']],row[1:]):
        printed(f'thermodynamics-19.sat.{pressure}.{name}',value,token)
for name, record in [('1',s1),('2s',s2s),('2',s2),('3',s3),('4',s4)]:
    row=next(r for r in rrows if r[0]==name and len(r)==6)
    for key,token in zip(['T_C','h_kJkg','s_kJkgK'],row[2:5]):
        printed(f'thermodynamics-19.state.{name}.{key}',record[key],token)
for t, record in zip(['50','55','60'],lookup):
    row=next(r for r in rrows if r[0]==t and len(r)==3)
    for key,token in zip(['h_kJkg','s_kJkgK'],row[1:]):
        printed(f'thermodynamics-19.lookup.{t}.{key}',record[key],token)
arows=rows('content/heat-transfer/heat-transfer-30.md')
for t in [305.,310.,333.15]:
    row=next(r for r in arows if r[0].split('（')[0]==f'{t:g}')
    for key,token in zip(['rho','mu','k','cp','Pr'],row[1:]):
        if key=='mu':
            coefficient=token.strip('$').split('\\times')[0]
            printed(f'heat-transfer-30.Air.{t}.mu_scaled_1e5',air_table[t][key]*1e5,coefficient)
        else:
            printed(f'heat-transfer-30.Air.{t}.{key}',air_table[t][key],token)
for name,value,token in [('Nu',Nu,'66.5321'),('h_Wm2K',h,'89.9642'),
                         ('Tout_C',Tout-273.15,'51.5419'),('Q_kW',tube['Q_W']/1000,'9.1801')]:
    printed('heat-transfer-30.final.'+name,value,token)
printed('thermodynamics-19.COP',refrigeration['COP'],'3.4580')

# Approximation differences are reported, not forced into rounding tolerance.
observations = {
    'water_265C_HEOS_minus_printed_linear_interpolation': {
        key: water[1][key]-target for key,target in
        [('h_kJkg',2976.0),('s_kJkgK',6.9884),('v_m3kg',.24042)]},
    'ideal_pump_HEOS_minus_incompressible_table_h_kJkg':pump['h_kJkg']-(191.81+.00101027*2990),
    'interpretation':'EOS recomputation, table rounding, interpolation, and constant-property approximations are distinct. No experimental validation is claimed.'}
assert DATA_FILE.read_bytes() == original_data, 'Audit must never mutate the saved table'
failed = [c for c in checks if not c['within_tolerance']]
result = {'status':'failed' if failed else 'passed','utc':datetime.now(timezone.utc).isoformat(),
          'python_version':platform.python_version(),'numpy_version':numpy.__version__,
          'dependency_mode':'explicit-directory' if args.deps is not None else 'python-import-path',
          'dependency_note':'Dependencies are only imported; this audit does not install or modify them.',
          'coolprop_version':CoolProp.__version__,'gitrevision':CoolProp.__gitrevision__,
          'backend':'HEOS',
          'reference_state':'CoolProp 7.2.0 unchanged default','saved_table_sha256':hashlib.sha256(original_data).hexdigest(),
          'source_cases':['thermodynamics-04','thermodynamics-15','thermodynamics-19','thermodynamics-21','heat-transfer-30'],
          'check_count':len(checks),'categories':dict(Counter(c['category'] for c in checks)),
          'failed_checks':failed,'checks':checks,'queried_states':states,
          'refrigeration':refrigeration,'tube':tube,'approximation_differences':observations}
summary = {key: value for key, value in result.items() if key not in ['checks', 'queried_states']}
summary['state_record_count'] = len(states)
summary['count_note'] = 'Counts are scalar comparisons, including repeated states and iteration values, not independent experiments.'
summary['tolerance_policy'] = {
    'saved_model':'max(abs(saved) * 1e-10, 1e-12)',
    'printed_values':'Half of the last displayed decimal unit plus 1e-12 floating-point allowance.'}
summary['largest_tolerance_fraction_by_category'] = {}
for category in summary['categories']:
    rows_in_category = [c for c in checks if c['category'] == category]
    worst = max(rows_in_category, key=lambda c: abs(c['difference']) / c['absolute_tolerance'])
    summary['largest_tolerance_fraction_by_category'][category] = dict(
        worst, tolerance_fraction=abs(worst['difference']) / worst['absolute_tolerance'])
for path, payload in [(args.output, result), (args.summary_output, summary)]:
    if path is not None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(summary, ensure_ascii=False, indent=2))
sys.exit(bool(failed))
