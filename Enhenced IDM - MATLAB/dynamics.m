function dx = dynamics(x, t, N, L, par, useACC, v_lead)

dx = zeros(1, 2*N);

%% Leader acceleration from prescribed velocity
dt_eps = 1e-3;
v_lead_next = leader_velocity(t + dt_eps);
a_lead = (v_lead_next - v_lead) / dt_eps;

for i = 1:N
    xi = x(2*i-1);
    vi = x(2*i);

    % Position derivative
    dx(2*i-1) = vi;

    if i == 1
        % ================= LEADER =================
        dx(2*i-1) = v_lead;   % prescribed velocity
        dx(2*i)   = a_lead;   % prescribed acceleration

    else
        % ================= FOLLOWER =================
        xi_L = x(2*(i-1)-1);   % leader position
        vL   = x(2*(i-1));     % leader velocity

        s  = xi_L - xi - L(i-1);   % gap
        dv = vi - vL;              % relative speed

        % Approximate leader acceleration for CAH
        aL = a_lead;

        if useACC(i)
            a_idm = IDM_accel(s, vi, dv, par);
            a_cah = CAH_accel(s, vi, vL, aL, dv, par);
            a     = blend_ACC(a_idm, a_cah, par.c);
        else
            a = IDM_accel(s, vi, dv, par);
        end

        dx(2*i) = a;
    end
end
end
