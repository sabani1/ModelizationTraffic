function dx = dynamics(x,N,L,p,useACC,v_lead)

dx = zeros(1, 2*N);    % must be ROW VECTOR

pos = x(1:2:end);
vel = x(2:2:end);

% Leader (i = 1)
dx(1) = vel(1);
dx(2) = (v_lead - vel(1));

% Followers
for i = 2:N

    s  = pos(i-1) - pos(i) - L(i-1);
    dv = vel(i)   - vel(i-1);
    aL = dx(2*(i-1));     % leader's acceleration

    if useACC(i)
        a_idm = IDM_accel(s, vel(i), dv, p);
        a_cah = CAH_accel(s, vel(i), vel(i-1), aL, dv, p);
        a     = blend_ACC(a_idm, a_cah, p.c);
    else
        a     = IDM_accel(s, vel(i), dv, p);
    end

    dx(2*i-1) = vel(i);
    dx(2*i)   = a;

end
