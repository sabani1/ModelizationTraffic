"""
config_enhenced_idm.py — Parameters for the enhanced IDM / ACC model (Python port)

Edit these values to run the enhanced-IDM simulator (`enhenced_idm.py`).
"""

# ----------------------------
# Enhanced-IDM / ACC parameters (cars)
# ----------------------------
P = {
    "v0": 33.33,    # desired speed (m/s)
    "T": 1.5,       # desired time headway (s)
    "s0": 2.0,      # minimum gap (m)
    "a": 1.4,       # maximum acceleration (m/s^2) -- named p.a in MATLAB
    "b": 2.0,       # comfortable deceleration (m/s^2)
    "d": 4,         # acceleration exponent (p.d in MATLAB)
    "L": 5.0,       # vehicle length (m)
}

# blending coefficient for ACC (0..1)
BLEND = {
    "c": 0.99,
}

# ----------------------------
# Simulation settings (same structure as other config files)
# ----------------------------
SIM = {
    "N": 10,
    "dt": 0.1,
    "T_sim": 200.0,
    "s_init": 80.0,
    "v_init": 30.0,
}

# Leader profile
LEADER = {
    "t_brake_start": 20.0,
    "t_brake_end": 22.0,
    "a_brake": -1.5,
    "a_cruise": 0.0,
    "v_min": 0.0,
    "v_max": None,
}

# Plot settings
PLOT = {
    "show_positions": True,
    "show_legend": True,
}
