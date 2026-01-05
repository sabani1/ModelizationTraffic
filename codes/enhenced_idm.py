import numpy as np
import matplotlib.pyplot as plt

from config_enhenced_idm import P, SIM, LEADER, PLOT, BLEND


def leader_acc(t_sec: float) -> float:
    if LEADER["t_brake_start"] <= t_sec <= LEADER["t_brake_end"]:
        return LEADER["a_brake"]
    return LEADER["a_cruise"]


def idm_acc_enh(s: float, v: float, dv: float, p: dict) -> float:
    """IDM acceleration (port of `IDM_accel.m`).

    s: gap (m), v: own speed (m/s), dv: v - v_lead (m/s)
    p: parameter dict (keys: v0, T, s0, a, b, d)
    """
    v0 = p["v0"]
    T = p["T"]
    s0 = p["s0"]
    a_max = p["a"]
    b = p["b"]
    d = p["d"]

    s_star = s0 + v * T + (v * dv) / (2.0 * np.sqrt(a_max * b))
    gap_eff = max(s, 0.1)
    return a_max * (1.0 - (v / v0) ** d - (s_star / gap_eff) ** 2)


def cah_accel(s: float, v: float, vL: float, aL: float, dv: float, p: dict) -> float:
    """Constant-Acceleration Heuristic (port of `CAH_accel.m`)."""
    if vL * v <= 0:
        return p["a"] - (v * dv) / (2 * s)

    discr = vL ** 2 + 2 * aL * s
    if discr < 0:
        return -v ** 2 / (2 * s)
    return (vL ** 2 - v ** 2 + 2 * aL * s) / (2 * s)


def blend_acc(a_idm: float, a_cah: float, c: float) -> float:
    """Blend IDM and CAH accelerations (port of `blend_ACC.m`)."""
    if a_idm > a_cah:
        return a_idm
    return (1 - c) * a_idm + c * a_cah


def run_simulation_enhanced():
    N = SIM["N"]
    dt = SIM["dt"]
    T_sim = SIM["T_sim"]
    steps = int(T_sim / dt)

    s_init = SIM["s_init"]
    v_init = SIM["v_init"]
    L = P["L"]

    v_min = LEADER["v_min"]
    v_max = LEADER["v_max"]

    # state arrays
    x = np.zeros((steps, N))
    v = np.zeros((steps, N))

    # initial conditions
    for i in range(N):
        x[0, i] = -i * (s_init + L)
        v[0, i] = v_init

    # integration
    for t in range(steps - 1):
        t_sec = t * dt

        # leader
        a_prev = 0.0
        a0 = leader_acc(t_sec)
        v0_next = v[t, 0] + a0 * dt
        if v_max is not None:
            v0_next = min(v0_next, v_max)
        v0_next = max(v0_next, v_min)
        x0_next = x[t, 0] + v0_next * dt

        v[t + 1, 0] = v0_next
        x[t + 1, 0] = x0_next

        # store last computed acceleration (for follower use)
        a_prev = a0

        # followers
        for i in range(1, N):
            gap = x[t, i - 1] - x[t, i] - L
            dv = v[t, i] - v[t, i - 1]

            a_idm = idm_acc_enh(gap, v[t, i], dv, P)
            a_cah = cah_accel(gap, v[t, i], v[t, i - 1], a_prev, dv, P)
            a_i = blend_acc(a_idm, a_cah, BLEND["c"])

            v_next = max(0.0, v[t, i] + a_i * dt)
            x_next = x[t, i] + v_next * dt

            gap_after = x[t, i - 1] - x_next - L
            if gap_after < 0:
                print(f"[COLLISION] t={t_sec:.2f}s between {i-1} and {i}, gap={gap_after:.2f} m")
                time = np.arange(steps) * dt
                return time[:t + 2], x[:t + 2], v[:t + 2]

            v[t + 1, i] = v_next
            x[t + 1, i] = x_next

            # update a_prev for the next follower
            a_prev = a_i

    time = np.arange(steps) * dt
    return time, x, v


def plot_results(time, x, v):
    N = v.shape[1]

    if PLOT["show_positions"]:
        fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
        for i in range(N):
            axs[0].plot(time, v[:, i], label=f"Vehicle {i+1}")
            axs[1].plot(time, x[:, i], label=f"Vehicle {i+1}")
        axs[0].set_ylabel("Speed (m/s)")
        axs[0].set_title("Enhanced IDM/ACC — speeds over time")
        axs[1].set_ylabel("Position (m)")
        axs[1].set_xlabel("Time (s)")
        axs[1].set_title("Enhanced IDM/ACC — positions over time")
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
        plt.title("Enhanced IDM/ACC — speeds over time")
        if PLOT["show_legend"]:
            plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    time, x, v = run_simulation_enhanced()
    plot_results(time, x, v)
