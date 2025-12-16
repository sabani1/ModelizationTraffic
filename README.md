# IDM Platoon Simulation

A small, single-lane Intelligent Driver Model (IDM) platoon simulator.

This repository contains a compact Python implementation of the IDM used to simulate a leader vehicle performing a simple braking manoeuvre and a string of follower vehicles reacting according to the IDM law. The entire project consists of two files:

- `idm.py` — simulator and plotting utilities.
- `config.py` — editable scenario and model parameters.

## Requirements

- Python 3.8+ (should work on 3.7 in many environments)
- numpy
- matplotlib

Install dependencies with pip:

```bash
pip install numpy matplotlib
```

## Quick start

Run the simulation and show the default plots:

```bash
python idm.py
```

This runs the simulation using parameters in `config.py` and opens matplotlib figures showing speeds and (optionally) positions over time.

## Configuration (`config.py`)

Open `config.py` to change experiment settings without editing the simulator code.

- `IDM` (dict): model parameters for vehicles
	- `v0`: desired speed (m/s)
	- `T`: desired time headway (s)
	- `s0`: minimum gap (m)
	- `a_max`: maximum acceleration (m/s^2)
	- `b`: comfortable deceleration (m/s^2)
	- `delta`: acceleration exponent
	- `L`: vehicle length (m)

- `SIM` (dict): simulation settings
	- `N`: number of vehicles (vehicle 0 is the leader)
	- `dt`: timestep (s)
	- `T_sim`: total simulation time (s)
	- `s_init`: initial gap between vehicles (m)
	- `v_init`: initial speed for all vehicles (m/s)

- `LEADER` (dict): leader acceleration profile
	- `t_brake_start`, `t_brake_end`: braking time window (s)
	- `a_brake`: acceleration during braking (negative for braking)
	- `a_cruise`: acceleration outside braking window
	- `v_min`, `v_max`: optional speed clamps for leader

- `PLOT` (dict): plotting options
	- `show_positions`: whether to plot positions in addition to speeds
	- `show_legend`: show a legend on plots

The file contains a few commented example scenarios (mild brake, hard brake, collision test) you can uncomment or adapt.

## How it works (brief)

- `leader_acc(t_sec)` — returns the leader's acceleration at time `t_sec` according to the `LEADER` profile.
- `idm_acc(gap, v_i, dv)` — computes the IDM acceleration for a follower given the net gap (m), its speed `v_i` (m/s), and relative speed `dv = v_i - v_front`.
- `run_simulation()` — runs an explicit Euler integration of the leader and followers and returns `(time, x, v)` arrays.
- `plot_results(time, x, v)` — plots speeds and (optionally) positions versus time using matplotlib.

The simulator prints a collision message and stops early if a follower overlaps its leader (gap < 0).

## Examples

- Run the default scenario:

```bash
python idm.py
```

- To test a hard braking event, edit `LEADER['a_brake']` in `config.py` to a larger magnitude (e.g. `-3.0`) or change the braking window timings.

- To produce a collision test, reduce `SIM['s_init']` and/or `IDM['a_max']` as shown in the commented scenarios in `config.py`.

## Troubleshooting

- If matplotlib windows do not appear, make sure your Python environment supports GUI backends (on headless servers use an alternative backend or save figures using `plt.savefig`).
- If the simulation prints a `[COLLISION]` message, adjust initial gaps or IDM parameters to increase safety headways.

## Extending the project

- Add data export (CSV) for time series.
- Implement more realistic leader trajectories or external disturbances.
- Replace Euler integration with a higher-order integrator for improved numerical accuracy.

## License

This project is provided as-is for educational and experimental use. Feel free to adapt it for your work.

