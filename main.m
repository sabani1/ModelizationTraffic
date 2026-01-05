clear; clc;

Tmax = 60;          % total simulation time
dt   = 0.05;        % integration step

N = 10;             % vehicles in platoon
L = 5*ones(N,1);    % vehicle lengths

%% parameters 
par.v0 = 33.33;     % desired speed [m/s]
par.T  = 1.5;       % time gap
par.s0 = 2;         % minimum gap
par.a  = 1.4;       % max accel
par.b  = 2.0;       % comfortable decel
par.d  = 4;         % IDM exponent
par.c  = 0.99;      % coolness factor for ACC blending

% 0 = IDM, 1 = ACC
useACC = zeros(N,1);
useACC(2:10) = 1;   % make followers ACC for demonstration

%% Initial conditions
V0 = 25;            % initial speed of the entire platoon
x0 = zeros(2*N,1);

% initial positions so that s_i = equilibrium spacing at V0
S_eq = compute_equilibrium_spacing(V0,par);

x_lead = 0;
for i = 1:N
    x0(2*i-1) = x_lead - (i-1)*(S_eq + L(i));
    x0(2*i)   = V0;
end

%% Time integration
time = 0:dt:Tmax;
X = zeros(length(time),2*N);
X(1,:) = x0';

for k = 1:length(time)-1
    t = time(k);

    % leader speed profile
    v_lead = leader_velocity(t);

    % integrate one step with rk4 method
    X(k+1,:) = rk4_step(@(x) dynamics(x,N,L,par,useACC,v_lead), X(k,:), dt);
end

%% Plotting
positions = X(:,1:2:end);
velocities = X(:,2:2:end);

figure; hold on;
for i=1:N
    plot(time, positions(:,i));
end
title('Vehicle Trajectories (Space-Time)');
xlabel('Time [s]'); ylabel('Position [m]');

figure; hold on;
for i=1:N
    plot(time, velocities(:,i));
end
title('Velocities'); xlabel('Time [s]'); ylabel('v_i [m/s]');

figure; hold on;
for i=2:N
    s_i = positions(:,i-1) - positions(:,i) - L(i-1);
    plot(time, s_i);
end
title('Gaps s_i(t)'); xlabel('Time [s]'); ylabel('Gap [m]');
