function v = leader_velocity(t)
v0 = 25;
if t < 20
    v = v0;
elseif t < 23
    v = v0 - 2*(t-20);   % braking at -2 m/s^2
else
    v = min(v0, v0 - 6 + 1*(t-23));  % accelerate back
end
