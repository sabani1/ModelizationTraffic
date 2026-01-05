function a = IDM_accel(s, v, dv, p)

s_star = p.s0 + v*p.T + v*dv/(2*sqrt(p.a*p.b));
a = p.a * (1 - (v/p.v0)^p.d - (s_star/s)^2);
