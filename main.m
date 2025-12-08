clear;
clc;

%vehicle parameters for a car
v0 = 120; %desired speed
delta = 4; %free acceleration exponennt
T = 1.5; %desired time gap
s0 = 2; %jam distance
a = 1.4; %maximum acceleration
b = 2; %desired deceleration
c = 0.99; %coolness factor

%simulation parameters
T_total = 60; %simulation duration
N = 5; %number of vehicles in platoon

