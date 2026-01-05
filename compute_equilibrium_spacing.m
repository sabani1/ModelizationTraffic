function S = compute_equilibrium_spacing(V,par)
s_star = par.s0 + V*par.T;
S = s_star / sqrt(1 - (V/par.v0)^par.d);
