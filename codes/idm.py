import numpy as np
import matplotlib.pyplot as plt

from config import IDM, SIM, LEADER, PLOT


def leader_acc(t_sec: float) -> float:
    """Leader acceleration profile: constant acceleration inside a time window."""
    if LEADER["t_brake_start"] <= t_sec <= LEADER["t_brake_end"]:
        return LEADER["a_brake"]
    return LEADER["a_cruise"]


def idm_acc(gap: float, v_i: float, dv: float) -> float:
    """
    Intelligent Driver Model (IDM) acceleration.

    gap: net bumper-to-bumper distance to leader (m)
    v_i: current speed of this vehicle (m/s)
    dv: relative speed v_i - v_front (m/s), positive means closing in
    """
    v0 = IDM["v0"]
    T = IDM["T"]
    s0 = IDM["s0"]
    a_max = IDM["a_max"]
    b = IDM["b"]
    delta = IDM["delta"]

    # Desired dynamic gap
    s_star = s0 + v_i * T + (v_i * dv) / (2.0 * np.sqrt(a_max * b))

    # Numerical safety to avoid division by ~0
    gap_eff = max(gap, 0.1)

    # IDM acceleration law
    return a_max * (1.0 - (v_i / v0) ** delta - (s_star / gap_eff) ** 2)


def run_simulation():
    """Run the platoon simulation and return time, positions, and speeds."""
    N = SIM["N"]
    dt = SIM["dt"]
    T_sim = SIM["T_sim"]
    steps = int(T_sim / dt)

    s_init = SIM["s_init"]
    v_init = SIM["v_init"]
    L = IDM["L"]

    v_min = LEADER["v_min"]
    v_max = LEADER["v_max"]

    # State arrays
    x = np.zeros((steps, N))
    v = np.zeros((steps, N))

    # Initial conditions: vehicles in a line behind the leader
    for i in range(N):
        x[0, i] = -i * (s_init + L)
        v[0, i] = v_init

    # Euler integration
    for t in range(steps - 1):
        t_sec = t * dt

        # --- Leader (vehicle 0): imposed acceleration ---
        a0 = leader_acc(t_sec)

        v0_next = v[t, 0] + a0 * dt
        if v_max is not None:
            v0_next = min(v0_next, v_max)
        v0_next = max(v0_next, v_min)

        x0_next = x[t, 0] + v0_next * dt

        v[t + 1, 0] = v0_next
        x[t + 1, 0] = x0_next

        # --- Followers (vehicles 1..N-1): IDM ---
        for i in range(1, N):
            gap = x[t, i - 1] - x[t, i] - L
            dv = v[t, i] - v[t, i - 1]

            ai = idm_acc(gap, v[t, i], dv)

            v_next = max(0.0, v[t, i] + ai * dt)
            x_next = x[t, i] + v_next * dt

            gap_after = x[t, i - 1] - x_next - L
            if gap_after < 0:
                print(f"[COLLISION] t={t_sec:.2f}s between leader={i-1} and follower={i}, gap={gap_after:.2f} m")
                return time[:t+2], x[:t+2], v[:t+2]


            v[t + 1, i] = v_next
            x[t + 1, i] = x_next

    time = np.arange(steps) * dt
    return time, x, v


def plot_results(time, x, v):
    """Plot speed (and optionally position) vs time."""
    N = v.shape[1]

    if PLOT["show_positions"]:
        fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

        for i in range(N):
            axs[0].plot(time, v[:, i], label=f"Vehicle {i+1}")
            axs[1].plot(time, x[:, i], label=f"Vehicle {i+1}")

        axs[0].set_ylabel("Speed (m/s)")
        axs[0].set_title("IDM — speeds over time")

        axs[1].set_ylabel("Position (m)")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_title("IDM — positions over time")

        if PLOT["show_legend"]:
            axs[0].legend(loc="center left", bbox_to_anchor=(1, 0.5))
            axs[1].legend(loc="center left", bbox_to_anchor=(1, 0.5))

        fig.tight_layout()
        plt.show()

    else:
        plt.figure(figsize=(10, 4))
        for i in range(N):
            plt.plot(time, v[:, i], label=f"Vehicle {i+1}")
        plt.xlabel("Time (s)")
        plt.ylabel("Speed (m/s)")
        plt.title("IDM — speeds over time")
        if PLOT["show_legend"]:
            plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    time, x, v = run_simulation()
    plot_results(time, x, v)
