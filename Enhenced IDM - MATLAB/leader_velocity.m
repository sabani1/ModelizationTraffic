function v = leader_velocity(t)

v0 = 25;

if t < 20
    v = v0;
elseif t < 22
    v = max(v0 - 6*(t-20), 0);   % strong braking
else
    v = v0 - 12;
end
end
