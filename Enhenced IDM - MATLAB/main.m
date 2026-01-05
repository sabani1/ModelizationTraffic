clear; clc; close all;

%% Simulation parameters
Tmax = 60;
dt   = 0.05;
time = 0:dt:Tmax;

N = 10;
L = 5*ones(N,1);

%% Model parameters
par.v0 = 33.33;
par.T  = 1.5;
par.s0 = 2;
par.a  = 1.4;
par.b  = 2.0;
par.d  = 4;
par.c  = 0.99;

% ACC usage
useACC = zeros(N,1);
useACC(2:N) = 1;

%% Initial conditions (equilibrium)
V0 = 25;
x0 = zeros(2*N,1);

S_eq = compute_equilibrium_spacing(V0,par);

x_lead = 0;
for i = 1:N
    x0(2*i-1) = x_lead - (i-1)*(S_eq + L(max(i-1,1)));
    x0(2*i)   = V0;
end

%% Storage
X = zeros(length(time),2*N);
X(1,:) = x0';

%% Time integration
for k = 1:length(time)-1
    t = time(k);

    % leader velocity (prescribed)
    v_lead = leader_velocity(t);

    % integrate one RK4 step
    X(k+1,:) = rk4_step( ...
        @(x) dynamics(x,t,N,L,par,useACC,v_lead), ...
        X(k,:), dt);
end

%% Extract states
positions  = X(:,1:2:end);
velocities = X(:,2:2:end);

%% Plots
figure; hold on;
for i=1:N
    plot(time, velocities(:,i));
end
xlabel('Time [s]'); ylabel('Velocity [m/s]');
title('IDM with CAH - Velocities');


figure; hold on; 
for i = 1:N
    plot(time, positions(:,i), 'DisplayName', ['Vehicle ', num2str(i)]);
end
xlabel('Time [s]');
ylabel('Position [m]');
title('IDM with CAH - Positions of Vehicles');
legend show;
