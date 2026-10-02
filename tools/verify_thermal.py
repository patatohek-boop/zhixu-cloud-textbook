"""Independent numerical and coverage checks for the two thermal courses.

Run from any directory: python tools/verify_thermal.py
Uses only the Python standard library. These checks verify selected worked
examples and limiting cases; they do not validate empirical correlations.
"""
from pathlib import Path
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]
checks = 0


def check(condition, label):
    global checks
    if not condition:
        raise AssertionError(label)
    checks += 1


def close(actual, expected, label, rel=1e-6, abs_tol=1e-10):
    check(math.isclose(actual, expected, rel_tol=rel, abs_tol=abs_tol),
          f"{label}: {actual} != {expected}")


def simpson(fn, lower, upper, count=20000):
    step = (upper-lower)/count
    terms = fn(lower)+fn(upper)
    terms += 4*sum(fn(lower+i*step) for i in range(1, count, 2))
    terms += 2*sum(fn(lower+i*step) for i in range(2, count, 2))
    return terms*step/3


def check_coverage():
    for cid in ("thermodynamics", "heat-transfer"):
        folder = ROOT/"content"/cid
        course = json.loads((folder/"course.json").read_text(encoding="utf-8"))
        audit = json.loads((ROOT/"reviews/content-audit-2026-09"/f"{cid}.json")
                           .read_text(encoding="utf-8"))
        metadata = {}
        for name in course["lessons"]:
            content = (folder/name).read_text(encoding="utf-8")
            match = re.match(r"---json\s*(.*?)\n---\s*", content, re.S)
            check(match is not None, f"{name}: metadata")
            item = json.loads(match.group(1))
            check(item["id"] not in metadata, f"{name}: unique id")
            metadata[item["id"]] = item
            body = content[match.end():]
            check(not re.search(r"^`{4,}", body, re.M), f"{name}: three-backtick fences")
            check(not re.search(r"^## [^\n]+\n\s*## ", body, re.M), f"{name}: nonempty sections")
            for course_id, lesson_id in re.findall(r"#/course/([^/\s)]+)/([^\s)]+)", body):
                check((ROOT/"content"/course_id/f"{lesson_id}.md").exists(),
                      f"{name}: crosslink {lesson_id}")
        records = audit["records"]
        check(len({r["id"] for r in records}) == len(records), f"{cid}: unique audit records")
        check({r["id"] for r in records} == set(metadata), f"{cid}: audit completeness")
        for record in records:
            check(record["title"] == metadata[record["id"]]["title"],
                  f"{cid}: matching audit title {record['id']}")
        mapped = {item for entry in audit["coverage_map"] for item in entry["lesson_ids"]}
        check(mapped == set(metadata), f"{cid}: coverage map completeness")


def check_thermodynamics():
    # First law, sign convention, and the polytropic worked example.
    close(-20-(-100), 80, "rigid tank electric work")
    work = .287*50/(1-1.2)
    close(work, -71.75, "polytropic work")
    close(.718*50+work, -35.85, "polytropic rejected heat")
    # Finite-difference conservation in well-mixed adiabatic blowdown.
    gamma, cv, m, dm, initial_t = 1.4, 718, .8, 1e-6, 300
    energy = lambda mass: mass*cv*initial_t*mass**(gamma-1)
    derivative = (energy(m+dm)-energy(m-dm))/(2*dm)
    outlet_h = gamma*cv*initial_t*m**(gamma-1)
    close(derivative, outlet_h, "blowdown differential energy")
    close(300*.5**.4, 227.35748497656, "blowdown final temperature")
    close(400*.5**1.4, 151.57165665104, "blowdown final pressure")
    # Carnot composition and signed auxiliary-machine heat cancellation.
    close((400/800)*(300/400), 300/800, "reversible temperature ratios")
    qh, th, tl = 800, 600, 300
    ql = -qh*tl/th
    close(qh/th+ql/tl, 0, "reversible Clausius sum")
    check(qh/th-500/tl < 0, "irreversible cyclic Clausius sign")
    mixed_s = -8.314*(math.log(.5)+math.log(.5))
    close(mixed_s, 11.52565131835, "mixing entropy")
    close(300*mixed_s, 3457.695395505, "minimum separation work")
    # Mixture terminal temperatures depend on the energy boundary.
    capacity = (2*700, 1*1000)
    tf = (capacity[0]*300+capacity[1]*500)/sum(capacity)
    close(capacity[0]*(tf-300)+capacity[1]*(tf-500), 0,
          "closed mixture internal energy", abs_tol=1e-8)


def check_heat_transfer():
    mu, latent, liquid, vapor, tension = 2.82e-4, 2.257e6, 958, .598, .0589
    boiling = mu*latent*math.sqrt(9.81*(liquid-vapor)/tension)*(4217*10/(.013*latent*1.75))**3
    chf = .131*vapor*latent*(tension*9.81*(liquid-vapor)/vapor**2)**.25
    close(boiling, 140791.55698, "Rohsenow substitution")
    close(chf, 1108850.77631, "CHF substitution")
    close(2*.06/10e-6, 12000, "bubble capillary pressure")
    # Condensation checks both the coefficient and the local latent balance.
    rho, rv, g, latent, conductivity, mu, height, dt = 1000, 1, 9.81, 2e6, .6, .001, .01, 10
    a = 4*mu*conductivity*dt/(rho*(rho-rv)*g*latent)
    delta = lambda x: (a*x)**.25
    gamma = lambda x: rho*(rho-rv)*g*delta(x)**3/(3*mu)
    x, dx = height/2, 1e-8
    energy = latent*(gamma(x+dx)-gamma(x-dx))/(2*dx)
    close(energy, conductivity*dt/delta(x), "condensation local mass-energy closure")
    average_h = 4*conductivity/(3*delta(height))
    close(average_h, 13523.94199497, "condensation average coefficient")
    close(average_h*height*dt, gamma(height)*latent, "condensation integrated closure")
    reynolds = 4*gamma(height)/mu
    close(reynolds, 2.70478839899, "condensation film Reynolds number")
    check(reynolds < 30 < reynolds*100**.75 < 1800,
          "height change exits smooth-film assumption")
    # A reciprocal direction-selective gray surface: alpha(theta)=epsilon(theta).
    # Normal illumination and hemispherical emission average different channels.
    directional = lambda angle: .2+.6*math.cos(angle)**2
    hemisphere = simpson(lambda angle: 2*directional(angle)*math.cos(angle)*math.sin(angle), 0, math.pi/2)
    close(hemisphere, .5, "gray directional hemispherical emissivity")
    close(directional(0), .8, "gray surface normal-incidence absorptivity")
    check(abs(directional(0)-hemisphere) > .29, "grayness alone does not match angular averages")
    isotropic_absorption = simpson(lambda angle: 2*directional(angle)*math.cos(angle)*math.sin(angle), 0, math.pi/2)
    close(isotropic_absorption, hemisphere, "isotropic blackbody angular compatibility")
    diffuse_gray = simpson(lambda angle: 2*.8*math.cos(angle)*math.sin(angle), 0, math.pi/2)
    close(diffuse_gray, .8, "diffuse-gray direction-independent limit")
    # Quadrature is independent of the series used in the lesson.
    spectrum = lambda z: z**3/math.expm1(z) if z else 0
    integral = simpson(spectrum, 0, 60)
    close(integral, math.pi**4/15, "Planck integral", rel=1e-9)
    hp, kb, light = 6.62607015e-34, 1.380649e-23, 299792458
    sigma = 2*math.pi**5*kb**4/(15*hp**3*light**2)
    close(sigma, 5.670374419e-8, "Stefan-Boltzmann constant", rel=1e-9)
    z = hp*light/(10e-6*kb*300)
    fraction = simpson(spectrum, z, 60)/integral
    close(fraction, .273229260146, "300 K shortwave fraction", rel=1e-8)
    close(sigma*300**4*fraction, 125.49428879, "300 K band power", rel=1e-8)
    root = 4.965114231744
    close(5*(1-math.exp(-root)), root, "Wien positive root", rel=1e-10)


if __name__ == "__main__":
    check_coverage()
    check_thermodynamics()
    check_heat_transfer()
    print(f"PASS: {checks} thermal content, coverage, and numerical checks.")
