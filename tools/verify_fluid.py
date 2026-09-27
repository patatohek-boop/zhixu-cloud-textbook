"""Independent numerical consistency checks for the revised fluid derivations.

Python standard library only. Finite differences, numerical quadrature and an
ODE shooting solution check the analytical examples by a different calculation.
These checks supplement the written derivations; they do not prove a theorem.
"""
import json
import math

checks = []
def close(name, actual, expected, tolerance=1e-7):
    assert abs(actual-expected) <= tolerance * max(1,abs(expected)), (name,actual,expected)
    checks.append(name)

def simpson(function, a, b, n=2000):
    step=(b-a)/n
    return step/3*(function(a)+function(b)+sum((4 if j%2 else 2)*function(a+j*step) for j in range(1,n)))

def derivative(function,x,h=1e-5):
    return (function(x+h)-function(x-h))/(2*h)

# A time-dependent density/velocity pair solves the continuity equation. Move
# both control-volume boundaries, and independently differentiate its inventory.
t=0.8
def mass(time):
    a,b=.2*time,1+.1*time
    return b-a+time*(b*b-a*a)/2
a,b=.2*t,1+.1*t
rho=lambda x:1+x*t
velocity=lambda x:-x*x/(2*rho(x))
out=rho(b)*(velocity(b)-.1)-rho(a)*(velocity(a)-.2)
close('07 moving-control-volume mass balance',derivative(mass,t)+out,0)

# Integrate the parabolic pipe profile rather than reusing its mean formula.
mu,radius,gradient,rho0=.001,.01,12,1000
profile=lambda r:gradient*(radius*radius-r*r)/(4*mu)
Q=simpson(lambda r:2*math.pi*r*profile(r),0,radius)
V=Q/(math.pi*radius**2)
close('12 Poiseuille mean velocity',V,gradient*radius**2/(8*mu))
Re=rho0*V*2*radius/mu
darcy=gradient*2*radius/(rho0*V*V/2)
close('13 Darcy laminar friction factor',darcy,64/Re)

# RK4 plus bisection solves the Blasius boundary-value problem, without using
# the chapter's wall-shear constant as an input.
def blasius(wall):
    value=[0.,0.,wall];step=.01
    def rhs(v): return [v[1],v[2],-.5*v[0]*v[2]]
    eta99=None
    for i in range(1200):
        previous=value[1]
        k1=rhs(value)
        k2=rhs([a+step*b/2 for a,b in zip(value,k1)])
        k3=rhs([a+step*b/2 for a,b in zip(value,k2)])
        k4=rhs([a+step*b for a,b in zip(value,k3)])
        value=[v+step*(a+2*b+2*c+d)/6 for v,a,b,c,d in zip(value,k1,k2,k3,k4)]
        if eta99 is None and previous<.99<=value[1]:
            eta99=step*(i+(.99-previous)/(value[1]-previous))
    return value[1],eta99
lo,hi=.30,.36
for _ in range(35):
    mid=(lo+hi)/2
    if blasius(mid)[0]>1:hi=mid
    else:lo=mid
wall=(lo+hi)/2
close('17 Blasius wall derivative',wall,.332057336,2e-8)
close('17 Blasius 99-percent thickness',blasius(wall)[1],4.91,.002)

# Rankine-Hugoniot relations must conserve all three fluxes and increase entropy.
gamma=1.4
for M in (1.01,1.5,2,3,6):
    p1=r1=1.;u1=M*math.sqrt(gamma)
    r2=(gamma+1)*M*M/((gamma-1)*M*M+2)
    p2=1+2*gamma*(M*M-1)/(gamma+1)
    u2=u1/r2
    close(f'22 shock mass M={M}',r2*u2,u1)
    close(f'22 shock momentum M={M}',p2+r2*u2*u2,p1+r1*u1*u1)
    cp=gamma/(gamma-1)
    close(f'22 shock energy M={M}',cp*p2/r2+u2*u2/2,cp+u1*u1/2)
    assert cp*math.log(p2/r2)-math.log(p2)>0
checks.append('22 shock entropy positive at five supersonic states')

# Check the Stokes sphere velocity and pressure in Cartesian coordinates using
# finite differences, avoiding reliance on spherical vector-Laplacian identities.
def stokes(point):
    x,y,z=point;r=math.sqrt(x*x+y*y+z*z)
    A=1-3/(4*r)-1/(4*r**3);B=-3/(4*r)+3/(4*r**3)
    return [B*z*x/(r*r),B*z*y/(r*r),A+B*z*z/(r*r)],-3*z/(2*r**3)
for point in ((2.,1.,3.),(1.5,-.7,.4)):
    h=.0005;u,p=stokes(point);div=0.;lap=[0.]*3;grad=[]
    for axis in range(3):
        plus=list(point);minus=list(point);plus[axis]+=h;minus[axis]-=h
        up,pp=stokes(plus);um,pm=stokes(minus)
        div+=(up[axis]-um[axis])/(2*h);grad.append((pp-pm)/(2*h))
        for j in range(3):lap[j]+=(up[j]-2*u[j]+um[j])/h**2
    close(f'31 sphere incompressibility {point}',div,0,1e-6)
    close(f'31 sphere Stokes residual {point}',max(abs(a-b) for a,b in zip(lap,grad)),0,2e-6)
close('31 sphere drag surface quadrature',simpson(lambda th:1.5*2*math.pi*math.sin(th),0,math.pi),6*math.pi)

def startup(y,t):return math.erfc(y/(2*math.sqrt(t)))
y,t=.8,.6;h=1e-4
ut=derivative(lambda time:startup(y,time),t)
uyy=(startup(y+h,t)-2*startup(y,t)+startup(y-h,t))/h**2
close('32 startup diffusion equation',ut,uyy,2e-7)
close('32 oscillating water penetration depth',math.sqrt(2e-6/(2*math.pi))*.001**-1,.56418958,1e-7)

b=(gamma-1)/2
def nu(M):
    return math.sqrt((gamma+1)/(gamma-1))*math.atan(math.sqrt((gamma-1)/(gamma+1)*(M*M-1)))-math.atan(math.sqrt(M*M-1))
for M in (1.1,2,4):
    close(f'33 Prandtl-Meyer antiderivative M={M}',derivative(nu,M),math.sqrt(M*M-1)/(M*(1+b*M*M)))
    T=lambda q:1/(1+b*q*q)
    p=lambda q:math.sqrt(T(q))/q
    entropy=lambda q:gamma/(gamma-1)*math.log(T(q))-math.log(p(q))
    close(f'33 Fanno entropy derivative M={M}',derivative(entropy,M),(1-M*M)/(M*(1+b*M*M)))
    T0=lambda q:q*q*(1+b*q*q)/(1+gamma*q*q)**2
    close(f'33 Rayleigh total-temperature derivative M={M}',derivative(lambda q:math.log(T0(q)),M),2*(1-M*M)/(M*(1+b*M*M)*(1+gamma*M*M)))
close('33 expansion angle example',(nu(3)-nu(2))*180/math.pi,23.37758593,1e-7)

g=9.81
for k in (.7,2.,7.):
    omega=lambda q:math.sqrt(g*q)
    close(f'34 deep gravity group velocity k={k}',derivative(omega,k),omega(k)/(2*k))
    omega=lambda q:math.sqrt(.072/1000*q**3)
    close(f'34 deep capillary group velocity k={k}',derivative(omega,k),1.5*omega(k)/k)
# New lecture-notes supplements: tensor contraction, boundary conditions,
# fluid kinetic energy and capillary/shear balances.
A=[[.4,3.,-.2],[1.,-.5,.7],[.3,-.1,.8]]
D=[[(A[i][j]+A[j][i])/2 for j in range(3)] for i in range(3)]
theta=sum(D[i][i] for i in range(3));mu,zeta=.2,.4
prime=[[D[i][j]-(theta/3 if i==j else 0) for j in range(3)] for i in range(3)]
tau=[[2*mu*prime[i][j]+(zeta*theta if i==j else 0) for j in range(3)] for i in range(3)]
close('36 tensor viscous dissipation identity',sum(tau[i][j]*A[i][j] for i in range(3) for j in range(3)),2*mu*sum(x*x for row in prime for x in row)+zeta*theta**2)
for angle in (.2,.8,2.):
    phi=lambda r:2*(r+.3**2/r)*math.cos(angle)
    close(f'37 cylinder no penetration {angle}',derivative(phi,.3,1e-6),0,1e-6)
for x in (-2.,.4,1.):
    phi=lambda y:math.log(x*x+(y-.7)**2)+math.log(x*x+(y+.7)**2)
    close(f'37 mirrored source normal velocity {x}',derivative(phi,0),0)
angular=simpson(lambda q:2*math.pi*(math.cos(q)**2+.25*math.sin(q)**2)*math.sin(q),0,math.pi)
radial=simpson(lambda s:s*s,0,1)
ma=1000*.1**3*angular*radial
close('37 sphere added mass via quadrature',ma,2*math.pi/3)
close('38 signed saddle capillary pressure',.03*(1/.002+1/(-.004)),7.5)
close('38 Marangoni flux via profile quadrature',simpson(lambda y:.2/.01*y,0,.0001),1e-7)
print(json.dumps({'status':'passed','checks':len(checks),'details':checks},ensure_ascii=True,indent=2))
