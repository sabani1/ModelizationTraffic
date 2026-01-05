function xnext = rk4_step(f,x,dt)

k1 = f(x);
k2 = f(x + 0.5*dt*k1);
k3 = f(x + 0.5*dt*k2);
k4 = f(x + dt*k3);

xnext = x + dt*(k1 + 2*k2 + 2*k3 + k4)/6;
end
