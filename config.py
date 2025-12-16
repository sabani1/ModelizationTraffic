"""
config.py — Parameters for a simple 1-lane IDM platoon simulation.
Edit this file to change the experiment without touching the simulator code.
"""

# ----------------------------
# IDM parameters (cars)
# ----------------------------
IDM = {
    "v0": 33.33,     # desired speed (m/s) ~120 km/h
    "T": 1.5,        # desired time headway (s)
    "s0": 2.0,       # minimum gap / jam distance (m)
    "a_max": 1.4,    # maximum acceleration (m/s^2)
    "b": 2.0,        # comfortable deceleration (m/s^2)
    "delta": 4,      # acceleration exponent
    "L": 5.0,        # vehicle length (m)
}

# ----------------------------
# Simulation settings
# ----------------------------
SIM = {
    "N": 10,         # number of vehicles (vehicle 0 is the leader)
    "dt": 0.1,       # time step (s)
    "T_sim": 120.0,  # total simulation time (s)
    "s_init": 25.0,  # initial gap between vehicles (m), excluding vehicle length
    "v_init": 30.0,  # initial speed for all vehicles (m/s)
}

# ----------------------------
# Leader profile (simple braking window)
# ----------------------------
LEADER = {
    "t_brake_start": 50.0,  # s
    "t_brake_end": 60.0,    # s
    "a_brake": -1.5,        # m/s^2 during braking window
    "a_cruise": 0.0,        # m/s^2 outside braking window
    "v_min": 0.0,           # m/s
    "v_max": None,          # m/s, set e.g. 50.0 to clamp; None = no clamp
}

# ----------------------------
# Plot settings
# ----------------------------
PLOT = {
    "show_positions": True,   # plot x(t) in addition to v(t)
    "show_legend": True,      # show legend (can get crowded for large N)
}


'''
----------------------------
Test A — “No event” (relaxation)
----------------------------
SIM = {
    "N": 10,
    "dt": 0.1,
    "T_sim": 60.0,
    "s_init": 25.0,
    "v_init": 30.0,
}


LEADER = {
    "t_brake_start": 9999.0,
    "t_brake_end": 10000.0,
    "a_brake": 0.0,
    "a_cruise": 0.0,
    "v_min": 0.0,
    "v_max": None,
}

----------------------------
Test B — “Mild brake”
----------------------------
LEADER = {
    "t_brake_start": 20.0,
    "t_brake_end": 25.0,
    "a_brake": -1.0,
    "a_cruise": 0.0,
    "v_min": 0.0,
    "v_max": None,
}

----------------------------
Test C — “Hard brake”
----------------------------
LEADER = {
    "t_brake_start": 20.0,
    "t_brake_end": 23.0,
    "a_brake": -3.0,
    "a_cruise": 0.0,
    "v_min": 0.0,
    "v_max": None,
}

'''
