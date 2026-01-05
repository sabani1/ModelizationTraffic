function a_cah = CAH_accel(s, v, vL, aL, dv, p)

% Constant-Acceleration Heuristic

if vL * v <= 0
    a_cah = p.a - (v * dv) / (2 * s);
    return;
end

discr = vL^2 + 2 * aL * s;

if discr < 0
    a_cah = -v^2 / (2 * s);
else
    a_cah = (vL^2 - v^2 + 2*aL*s) / (2*s);
end
