"""
Swarm intelligence simulation for the coursework.

Part 1-2: Couzin et al. 2005 (Nature 433:513) "Effective leadership and
decision-making in animal groups on the move" -- 7-nearest-neighbour model
with information transmission, emergent leadership and majority consensus.

Part 3: engineering application -- multi-robot navigation through a narrow
passage, where only a small fraction of the robots knows where the door is.

Everything is vectorised with numpy; figures are written to ./figs.
"""

import json
import math
import os

import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Wedge, Rectangle, FancyArrow

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.join(HERE, "figs")
os.makedirs(FIGDIR, exist_ok=True)

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 9,
        "axes.titlesize": 10,
        "axes.labelsize": 9,
        "figure.dpi": 160,
        "savefig.dpi": 160,
        "axes.spines.top": False,
        "axes.spines.right": False,
    }
)

K = 7  # topological interaction number (7-nearest-neighbour model)
G = np.array([1.0, 0.0])  # the correct goal direction, +x
OMEGA = 0.4  # weight an informed individual puts on its own goal
KAPPA = 0.25  # angular error per step, radians


# --------------------------------------------------------------------------
# core model
# --------------------------------------------------------------------------
def step_decision(pos, vel, goal, informed, omega, kappa, v, radius, k=K, rng=None):
    """One update of the Couzin (2005) group model. Returns new pos/vel and leader mask.

    Leadership test.  Couzin et al. flag an individual as a decision maker when
    it is poorly connected -- i.e. it sits on the sparse flank of the group.
    A 7-nearest-neighbour graph cannot be tested by node degree (the degree of
    a k-NN graph is pinned near k whatever the density), so we use the metric
    instead: an individual leads when at least one of its k neighbours lies
    beyond the group's typical interaction distance.
    """
    n = len(pos)
    d2 = ((pos[:, None, :] - pos[None, :, :]) ** 2).sum(-1)
    np.fill_diagonal(d2, np.inf)
    part = np.argpartition(d2, k, axis=1)[:, :k]
    d2_sorted = np.take_along_axis(d2, part, axis=1)
    order = np.argsort(d2_sorted, axis=1)
    idx = np.take_along_axis(part, order, axis=1)
    knn_d = np.sqrt(np.take_along_axis(d2_sorted, order, axis=1))

    d_star = np.median(knn_d[:, -1])  # group's typical interaction distance
    is_leader = (knn_d > d_star).any(axis=1)

    # heading = mean heading of the k nearest neighbours
    m = vel[idx].mean(axis=1)
    m /= np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-12)

    # informed individuals balance their own goal against the local majority
    new = np.where(informed[:, None], omega * goal + (1.0 - omega) * m, m)
    new /= np.maximum(np.linalg.norm(new, axis=1, keepdims=True), 1e-12)

    ang = np.arctan2(new[:, 1], new[:, 0])
    ang = ang + rng.normal(0.0, kappa, size=n)  # angular error, radians
    vel = np.stack([np.cos(ang), np.sin(ang)], axis=1)
    pos = pos + v * vel

    # soft arena: push the group back when it leaves the foraging area
    out = np.linalg.norm(pos, axis=1) > radius
    if out.any():
        r = np.linalg.norm(pos[out], axis=1, keepdims=True)
        pos[out] = pos[out] * (radius / r)

    return pos, vel, is_leader


def run_decision(n, p, omega=OMEGA, kappa=KAPPA, v=0.1, dt=1.0, T=400,
                 radius=None, k=K, seed=0, goal2=None, speed_ratio=1.0,
                 split=0.5):
    """Simulate one group.

    n            group size
    p            fraction of informed individuals
    goal2        if given, a second goal direction shared by a share of the
                 informed individuals (majority-consensus experiment)
    speed_ratio  extra speed of informed individuals (biological variant)
    """
    rng = np.random.default_rng(seed)
    if radius is None:
        radius = 2.0 * math.sqrt(n)

    pos = rng.normal(0, radius / 4, size=(n, 2))
    ang0 = rng.uniform(-np.pi, np.pi, size=n)
    vel = np.stack([np.cos(ang0), np.sin(ang0)], axis=1)

    nin = int(round(p * n))
    informed = np.zeros(n, dtype=bool)
    informed[:nin] = True
    rng.shuffle(informed)

    goal = np.tile(G, (n, 1))
    side = None
    if goal2 is not None:
        # the informed individuals are split into two camps: `split` of them
        # prefer the first goal, the rest prefer the second one
        idx = np.where(informed)[0]
        n1 = int(round(len(idx) * split))
        side = np.zeros(n, dtype=bool)  # True -> prefers the SECOND goal
        side[idx[n1:]] = True
        goal[side] = np.asarray(goal2, dtype=float)
        goal /= np.linalg.norm(goal, axis=1, keepdims=True)

    tail_dirs, tail_lead, tail_ph = [], [], []
    track = []
    for t in range(T):
        pos, vel, is_leader = step_decision(
            pos, vel, goal, informed, omega, kappa, v * dt, radius, k, rng
        )
        # informed individuals swim a little faster (the biological variant)
        if speed_ratio != 1.0:
            pos = pos + v * dt * vel * (speed_ratio - 1.0) * informed[:, None]
        if t % 5 == 0:
            track.append(pos.mean(axis=0).tolist())
        if t >= T * 0.5:  # measure on the second half only
            tail_dirs.append(vel.copy())
            tail_lead.append(is_leader.mean())
            tail_ph.append(np.linalg.norm(vel.mean(axis=0)))

    dirs = np.array(tail_dirs)
    mean_dir = dirs.mean(axis=(0, 1))
    polar = np.linalg.norm(dirs.mean(axis=0), axis=1).mean()
    leader_frac = float(np.mean(tail_lead))

    # decision: split the tail directions into the +x side and the other side
    if goal2 is None:
        correct = float(mean_dir[0] > 0)
    else:
        u1, u2 = G, np.asarray(goal2, float)
        u2 = u2 / np.linalg.norm(u2)
        s1, s2 = float(mean_dir @ u1), float(mean_dir @ u2)
        if side is None:
            correct = float(s1 > s2)
        else:
            correct = float(s1 > s2)  # 1.0 if first (larger) camp won

    return {
        "correct": correct,
        "mean_dir": mean_dir.tolist(),
        "polar": float(polar),
        "leader_frac": leader_frac,
        "pos": pos.tolist(),
        "track": track,
    }


# --------------------------------------------------------------------------
# Experiment A: accuracy vs informed fraction, several group sizes
# --------------------------------------------------------------------------
def exp_a(quick=False):
    sizes = [10, 50, 200] if quick else [10, 25, 50, 200]
    ps = [0, 0.02, 0.05, 0.1, 0.2, 0.4, 1.0] if quick else \
         [0, 0.01, 0.02, 0.03, 0.05, 0.08, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0]
    reps = 20 if quick else 60
    T = 300
    res = {}
    for n in sizes:
        acc, lead, polar = [], [], []
        for p in ps:
            rs = [run_decision(n, p, T=T, seed=1000 + 7 * int(p * 100) + r)
                  for r in range(reps)]
            acc.append(np.mean([r["correct"] for r in rs]))
            lead.append(np.mean([r["leader_frac"] for r in rs]))
            polar.append(np.mean([r["polar"] for r in rs]))
        res[n] = dict(p=list(map(float, ps)), acc=acc, lead=lead, polar=polar)
        print(f"[A] N={n:3d} done", flush=True)
    return res


# --------------------------------------------------------------------------
# Experiment B: majority consensus between two camps
# --------------------------------------------------------------------------
def exp_b(quick=False):
    """Majority consensus: two camps with competing goals, ω x split grid."""
    n = 100
    p = 0.3 if quick else 0.2
    reps = 15 if quick else 40
    splits = [0.5, 0.55, 0.6, 0.7, 0.8, 0.9] if quick else \
             [0.5, 0.55, 0.6, 0.65, 0.7, 0.8, 0.9]
    omegas = [0.2, 0.5, 0.8] if quick else [0.2, 0.4, 0.6, 0.8]
    g2 = [0.0, 1.0]
    grid = []
    for w in omegas:
        row = []
        for s in splits:
            acc = np.mean([run_decision(n, p, omega=w, T=300, goal2=g2, split=s,
                                        seed=900 + 31 * int(s * 100) + 7 * int(w * 10) + r)
                           ["correct"] for r in range(reps)])
            row.append(acc)
        grid.append(row)
        print(f"[B] omega={w}: " + " ".join(f"{s:.2f}:{a:.2f}"
              for s, a in zip(splits, row)), flush=True)
    return dict(omegas=omegas, splits=splits, grid=grid, p=p, n=n, reps=reps)


# --------------------------------------------------------------------------
# Experiment C: robots through a narrow passage
# --------------------------------------------------------------------------
def run_passage(n=40, p_informed=0.1, w_door=0.9, L=10.0, H=4.0,
                y_mid=2.0, steps=900, seed=0, informed_speed=1.0,
                noise=0.05, k=7, d_sep=0.45, omega=0.85, beta=0.6):
    """Robots must pass a wall with a single narrow door.

    Only `p_informed` of them know where the door is. Everyone uses the same
    three-zone rule set (repulsion / alignment / attraction) plus local wall
    avoidance; informed robots additionally have the door as their global goal.
    """
    rng = np.random.default_rng(seed)
    x_wall = L / 2.0
    d1 = max(0.0, y_mid - w_door / 2)
    d2 = y_mid + w_door / 2

    pos = np.stack([rng.uniform(0.5, x_wall - 1.5, n), rng.uniform(0.3, H - 0.3, n)], 1)
    ang = rng.uniform(-np.pi, np.pi, n)
    vel = np.stack([np.cos(ang), np.sin(ang)], 1)
    informed = np.zeros(n, bool)
    kk = max(1, int(round(p_informed * n))) if p_informed > 0 else 0
    informed[:kk] = True
    rng.shuffle(informed)

    arrived = np.zeros(n, bool)
    collisions = 0
    t_done = None
    t_first = None
    traj = []

    for t in range(steps):
        # --- perception: k nearest neighbours within a range -------------
        d2m = ((pos[:, None, :] - pos[None, :, :]) ** 2).sum(-1)
        np.fill_diagonal(d2m, np.inf)
        idx = np.argpartition(d2m, k, axis=1)[:, :k]
        rel = pos[idx] - pos[:, None, :]
        dist = np.linalg.norm(rel, axis=2)

        # separation: push away from close neighbours
        w = np.clip(1.0 - dist / d_sep, 0, 1)
        sep = -(rel * w[..., None]).sum(1)
        # alignment with neighbours
        ali = vel[idx].mean(1)
        # attraction to the local centroid
        cen = pos[idx].mean(1) - pos

        goal_dir = np.zeros((n, 2))
        # --- what an UNINFORMED robot is told to do --------------------
        # "stay in formation and drift forward".  It has no task knowledge at
        # all: no idea where the opening is.  Everything it does about the
        # wall is local collision avoidance.
        goal_dir[:, 0] = 0.20
        # --- what an INFORMED robot additionally knows ----------------
        # the position of the doorway (one global cue, no communication)
        goal_dir[informed, 0] = 1.0
        goal_dir[informed, 1] = (y_mid - pos[informed, 1]) * 0.5
        goal_dir /= np.maximum(np.linalg.norm(goal_dir, axis=1, keepdims=True), 1e-9)

        # Couzin's key asymmetry: an informed individual holds on to its own
        # goal, an uninformed one mostly defers to its neighbours.  Without
        # this difference a minority of "leaders" cannot move the group.
        w_goal = np.where(informed, 1.0, 0.22)
        w_ali = np.where(informed, 0.35, 1.0)
        acc = w_goal[:, None] * goal_dir
        acc += w_ali[:, None] * (ali / (np.linalg.norm(ali, axis=1, keepdims=True) + 1e-9))
        acc += 0.6 * sep / (np.linalg.norm(sep, axis=1, keepdims=True) + 1e-9)
        acc += 0.3 * (cen / (np.linalg.norm(cen, axis=1, keepdims=True) + 1e-9))
        acc /= np.maximum(np.linalg.norm(acc, axis=1, keepdims=True), 1e-9)

        # --- local wall avoidance (identical rule for every robot) -------
        # The sensing range SELF_PROBE is deliberately smaller than the
        # half-width of the doorway, so this purely local rule CANNOT discover
        # the opening.  Only the informed robots know where it is.
        SELF_PROBE = 0.4
        ahead = pos + vel * SELF_PROBE
        in_y = (ahead[:, 1] > d1 - 0.1) & (ahead[:, 1] < d2 + 0.1)
        blocked = (ahead[:, 0] > x_wall - 0.5) & in_y & (np.abs(ahead[:, 1] - y_mid) > w_door / 2 - 0.15)
        blocked &= vel[:, 0] > -0.1  # only when roughly moving into the wall
        if blocked.any():
            yb = pos[blocked, 1]
            up_open = ((yb + SELF_PROBE) > d1) & ((yb + SELF_PROBE) < d2)
            dn_open = ((yb - SELF_PROBE) > d1) & ((yb - SELF_PROBE) < d2)
            side = np.where(up_open, 1.0, np.where(dn_open, -1.0, 0.0))
            acc[blocked, 0] = 0.05
            acc[blocked, 1] = side * 0.9

        a = np.arctan2(acc[:, 1], acc[:, 0]) + rng.normal(0, noise, n)
        # finite turn rate
        turn = np.clip((a - ang + np.pi) % (2 * np.pi) - np.pi, -0.35, 0.35)
        ang = ang + turn
        vel = np.stack([np.cos(ang), np.sin(ang)], 1)

        speed = np.full(n, 0.05) * (informed_speed if informed_speed != 1.0 else 1.0)
        step_v = vel * speed[:, None]

        # hard wall constraint (robots cannot pass through the wall)
        newx = pos[:, 0] + step_v[:, 0]
        hit = (np.abs(newx - x_wall) < 0.2) & ((pos[:, 1] < d1) | (pos[:, 1] > d2))
        pos[hit] = np.stack([newx[hit], pos[hit, 1]], 1)
        pos[hit, 0] = x_wall - 0.2
        step_v[hit, 0] = 0.0
        rest = ~hit
        pos[rest] += step_v[rest]
        pos[:, 0] = np.clip(pos[:, 0], 0.15, L - 0.15)
        pos[:, 1] = np.clip(pos[:, 1], 0.15, H - 0.15)

        # collision bookkeeping
        dd = np.sqrt(d2m)
        collisions += int((dd < 0.25).sum() // 2)

        newly = (pos[:, 0] > x_wall + 0.8) & (~arrived)
        if t_first is None and newly.any():
            t_first = t
        arrived |= newly
        if t_done is None and arrived.all():
            t_done = t
        if t % 45 == 0:
            traj.append((t, pos.copy()))

    return dict(success=float(arrived.mean()), n_arrived=int(arrived.sum()),
                t_done=t_done, t_first=t_first, collisions=collisions, traj=traj,
                n_informed=int(informed.sum()))


def run_maze(n=30, p_informed=0.1, w_door=0.9, steps=1200, seed=0,
             informed_speed=1.0, noise=0.05, k=7, d_sep=0.6,
             d_goal=1.0, d_ali_u=1.0, d_goal_u=0.0, SPEED=0.07,
             SELF_PROBE=0.4, spread=True):
    """S-shaped corridor: two offset walls, each with one narrow doorway.

    Wall A (x=3.5) opens at y=0.9, wall B (x=6.8) opens at y=3.1.  A robot
    that only has local sensing can stumble through the first doorway, but it
    then runs into solid material in front of the second one.  Only robots
    that know both door positions steer diagonally and pull the swarm with
    them.  The avoidance rule is identical for every robot.
    """
    rng = np.random.default_rng(seed)
    walls = [(3.5, 1.2), (6.8, 2.9)]
    H = 4.0
    start_x, goal_x = 0.6, 9.6

    pos = np.stack([rng.uniform(0.4, 3.0, n), rng.uniform(0.3, H - 0.3, n)], 1)
    ang = rng.uniform(-np.pi, np.pi, n)
    vel = np.stack([np.cos(ang), np.sin(ang)], 1)
    informed = np.zeros(n, bool)
    kk = int(round(p_informed * n))
    if kk:
        informed[:kk] = True
    rng.shuffle(informed)

    # Waypoints only an informed robot knows.  Instead of everybody aiming at
    # the centre of a doorway, the informed robots are spread across its width
    # (spatial sorting, Couzin et al. 2002): they queue instead of jamming.
    half = w_door / 2.0
    slot = np.zeros(n)
    if kk:
        slot[informed] = (np.arange(kk) + 0.5) / kk
    if not spread:  # original design: everybody heads for the centre of the door
        slot[:] = 0.5
    offA = -half + slot * w_door
    offB = -half + ((slot + 0.5) % 1.0) * w_door
    target = np.zeros((n, 2))
    target[:, 0] = goal_x
    target[:, 1] = walls[1][1] + offB
    st0 = pos[:, 0] < walls[0][0]
    target[st0, 0] = walls[0][0] + 0.1
    target[st0, 1] = walls[0][1] + offA

    arrived = np.zeros(n, bool)
    collisions = 0
    t_done = t_first = None
    traj = []

    for t in range(steps):
        d2m = ((pos[:, None, :] - pos[None, :, :]) ** 2).sum(-1)
        np.fill_diagonal(d2m, np.inf)
        idx = np.argpartition(d2m, k, axis=1)[:, :k]
        rel = pos[idx] - pos[:, None, :]
        dist = np.linalg.norm(rel, axis=2)

        w = np.clip(1.0 - dist / d_sep, 0, 1)
        sep = -(rel * w[..., None]).sum(1)
        ali = vel[idx].mean(1)
        cen = pos[idx].mean(1) - pos

        goal_dir = np.tile([0.20, 0.0], (n, 1))  # uninformed: just drift forward
        gi = target - pos
        gi /= np.maximum(np.linalg.norm(gi, axis=1, keepdims=True), 1e-9)
        goal_dir[informed] = gi[informed]
        goal_dir /= np.maximum(np.linalg.norm(goal_dir, axis=1, keepdims=True), 1e-9)

        wg = np.where(informed, d_goal, d_goal_u)
        wa = np.where(informed, 0.35, d_ali_u)
        acc = wg[:, None] * goal_dir
        acc += wa[:, None] * (ali / (np.linalg.norm(ali, axis=1, keepdims=True) + 1e-9))
        acc += 0.6 * sep / (np.linalg.norm(sep, axis=1, keepdims=True) + 1e-9)
        acc += 0.3 * (cen / (np.linalg.norm(cen, axis=1, keepdims=True) + 1e-9))
        acc /= np.maximum(np.linalg.norm(acc, axis=1, keepdims=True), 1e-9)

        # --- identical local wall rule for everyone ---------------------
        for wx, wy in walls:
            d1, d2 = wy - half, wy + half
            ahead = pos + vel * SELF_PROBE
            in_y = (ahead[:, 1] > d1 - 0.1) & (ahead[:, 1] < d2 + 0.1)
            blk = (ahead[:, 0] > wx - 0.5) & in_y & (vel[:, 0] > -0.1)
            if blk.any():
                yb = pos[blk, 1]
                up = ((yb + SELF_PROBE) > d1) & ((yb + SELF_PROBE) < d2)
                dn = ((yb - SELF_PROBE) > d1) & ((yb - SELF_PROBE) < d2)
                side = np.where(up, 1.0, np.where(dn, -1.0, 0.0))
                acc[blk, 0] = 0.05
                acc[blk, 1] = side * 0.9

        a = np.arctan2(acc[:, 1], acc[:, 0]) + rng.normal(0, noise, n)
        turn = np.clip((a - ang + np.pi) % (2 * np.pi) - np.pi, -0.35, 0.35)
        ang += turn
        vel = np.stack([np.cos(ang), np.sin(ang)], 1)

        speed = np.full(n, SPEED) * np.where(informed, informed_speed, 1.0)
        step_v = vel * speed[:, None]
        newpos = pos + step_v

        # walls are solid: only the doorway lets a robot through
        for wx, wy in walls:
            d1, d2 = wy - half, wy + half
            cross = (np.abs(newpos[:, 0] - wx) < 0.2) & ((pos[:, 1] <= d1) | (pos[:, 1] >= d2))
            newpos[cross, 0] = wx - 0.2
        pos = newpos
        pos[:, 0] = np.clip(pos[:, 0], 0.15, 9.9)
        pos[:, 1] = np.clip(pos[:, 1], 0.15, H - 0.15)

        # waypoint stage advances as a robot passes each wall
        st0 = pos[:, 0] < walls[0][0]
        target[st0, 0] = walls[0][0] + 0.1
        target[st0, 1] = walls[0][1] + offA[st0]
        st1 = (~st0) & (pos[:, 0] < walls[1][0])
        target[st1, 0] = walls[1][0] + 0.1
        target[st1, 1] = walls[1][1] + offB[st1]
        rest = ~st0 & ~st1
        target[rest, 0] = goal_x
        target[rest, 1] = walls[1][1] + offB[rest]

        collisions += int((np.sqrt(d2m) < 0.25).sum() // 2)
        newly = (pos[:, 0] > goal_x - 0.2) & (~arrived)
        if t_first is None and newly.any():
            t_first = t
        arrived |= newly
        if t_done is None and arrived.all():
            t_done = t
        if t % 60 == 0:
            traj.append((t, pos.copy()))

    return dict(success=float(arrived.mean()), n_arrived=int(arrived.sum()),
                t_done=t_done, t_first=t_first, collisions=collisions,
                traj=traj, n_informed=int(informed.sum()), walls=walls,
                w_door=w_door, H=H)


def exp_maze(quick=False):
    """Four sub-experiments on the S-corridor benchmark."""
    reps = 5 if quick else 15
    out = {"p_scan": [], "size": [], "speed": [], "spread": []}

    def agg(cfg, label, bucket):
        rs = [run_maze(seed=400 + 13 * i, **cfg) for i in range(reps)]
        tf = [r["t_first"] for r in rs if r["t_first"] is not None]
        rec = dict(cfg, success=float(np.mean([r["success"] for r in rs])),
                   success_std=float(np.std([r["success"] for r in rs])),
                   collisions=float(np.mean([r["collisions"] for r in rs])),
                   t_first=float(np.mean(tf)) if tf else None,
                   reps=reps)
        out[bucket].append(rec)
        print(f"  {label}: success={rec['success']:.2f} "
              f"t_first={rec['t_first'] if tf else -1:.0f} "
              f"coll={rec['collisions']:.0f}", flush=True)

    print("[M1] informed fraction", flush=True)
    for p in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5, 1.0]:
        agg(dict(p_informed=p), f"p={p:.2f}", "p_scan")

    print("[M2] swarm size at fixed p", flush=True)
    for n in [20, 30, 45, 60]:
        agg(dict(p_informed=0.2, n=n), f"n={n}", "size")

    print("[M5] queueing vs. centre-seeking", flush=True)
    for p in [0.1, 0.3, 1.0]:
        agg(dict(p_informed=p, spread=False), f"p={p:.2f} centre", "spread")
        agg(dict(p_informed=p, spread=True), f"p={p:.2f} queue ", "spread")

    print("[M4] faster informed robots", flush=True)
    for s in [1.0, 1.3, 1.6]:
        agg(dict(p_informed=0.1, informed_speed=s), f"speed={s}", "speed")
    return out


def exp_c(quick=False):
    reps = 4 if quick else 12
    configs = [
        dict(p_informed=0.0, informed_speed=1.0),   # nobody knows the way
        dict(p_informed=0.1, informed_speed=1.0),   # original Couzin rule
        dict(p_informed=0.1, informed_speed=1.6),   # variant: informed are faster
        dict(p_informed=0.3, informed_speed=1.0),
        dict(p_informed=1.0, informed_speed=1.0),   # everyone knows
    ]
    out = []
    for cfg in configs:
        rs = [run_passage(seed=200 + 13 * i, **cfg) for i in range(reps)]
        out.append(dict(
            **cfg,
            success=float(np.mean([r["success"] for r in rs])),
            success_std=float(np.std([r["success"] for r in rs])),
            collisions=float(np.mean([r["collisions"] for r in rs])),
            t_done=float(np.mean([r["t_done"] for r in rs if r["t_done"]] or [np.nan])),
        ))
        print(f"[C] {cfg} -> success={out[-1]['success']:.2f}", flush=True)
    return out


# --------------------------------------------------------------------------
# figures
# --------------------------------------------------------------------------
def fig_zones():
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.3))

    ax = axes[0]
    ax.add_patch(Circle((0, 0), 1.0, color="#c6dbef", zorder=1))
    ax.add_patch(Circle((0, 0), 2.0, color="#9ecae1", zorder=1))
    ax.add_patch(Circle((0, 0), 3.0, color="#deebf7", zorder=1))
    # blind volume: a wedge directly behind the direction of travel
    ax.add_patch(Wedge((0, 0), 3.0, 140, 280, color="white", zorder=2))
    ax.add_patch(Circle((0, 0), 0.22, color="black", zorder=3))
    ax.add_patch(Wedge((0, 0), 0.55, -60, 60, color="#555555", zorder=4))
    for r, c in [(1.0, "#1f4e79"), (2.0, "#2e7d32"), (3.0, "#8e24aa")]:
        ax.add_patch(Circle((0, 0), r, fill=False, ec=c, lw=1.4, ls="--", zorder=5))
    ax.annotate("", xy=(2.9 * np.cos(np.pi / 6), 2.9 * np.sin(np.pi / 6)),
                xytext=(0.3 * np.cos(np.pi / 6), 0.3 * np.sin(np.pi / 6)),
                arrowprops=dict(arrowstyle="->", lw=1.5, color="k"), zorder=6)
    ax.text(2.45, 1.75, r"$v_i$", fontsize=10, zorder=6)
    ax.text(0.62, -0.52, "repulsion $d_r$", color="#1f4e79", fontsize=8, ha="left", zorder=6)
    ax.text(1.35, 0.62, "orientation $d_o$", color="#2e7d32", fontsize=8, ha="left", zorder=6)
    ax.text(1.95, 2.45, "attraction $d_a$", color="#8e24aa", fontsize=8, ha="left", zorder=6)
    ax.text(-1.15, 1.95, "blind\nvolume", fontsize=8, color="#555555", ha="left", zorder=6)
    ax.set_xlim(-3.4, 3.4); ax.set_ylim(-3.2, 3.4)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("a)  Couzin (2002) three-zone model", loc="left")

    ax = axes[1]
    pos = np.array([[0.0, 0.35],
                    [-1.15, 0.95], [-0.62, 1.30], [-0.95, 0.20],
                    [0.55, 1.10], [0.98, 0.55], [0.70, -0.35],
                    [1.55, 1.35], [1.62, -0.95], [-0.30, -1.05]])
    lab = ["$i$"] + [f"$j{k}$" for k in range(1, 10)]
    d = np.linalg.norm(pos[1:] - pos[0], axis=1)
    order = np.argsort(d)
    near = set(order[:7].tolist())
    far = [k for k in range(1, 10) if k not in near]
    for k in range(1, 10):
        col = "#d95f02" if k in near else "#bdbdbd"
        ax.plot([pos[0, 0], pos[k, 0]], [pos[0, 1], pos[k, 1]],
                color=col, lw=1.0, zorder=2, alpha=.75)
    ax.scatter(pos[:, 0], pos[:, 1], s=70, c=["black"] + ["#9ecae1"] * 9, zorder=3)
    for k in far:
        ax.scatter(*pos[k], s=110, facecolors="none", edgecolors="#999999", zorder=4)
    for r, t in zip(pos, lab):
        ax.annotate(t, r + 0.13, ha="center", fontsize=8.5, zorder=5)
    ax.text(0, -1.85, "individual $i$ senses its 7 nearest neighbours (orange links)\n"
                      "a neighbour lying beyond the group's typical interaction\n"
                      "distance means $i$ sits on the sparse flank $\\Rightarrow$  $i$ decides",
            ha="center", va="top", fontsize=8, color="#333333")
    ax.set_xlim(-2.1, 2.3); ax.set_ylim(-3.1, 1.9)
    ax.set_aspect("equal"); ax.axis("off")
    ax.set_title("b)  7-nearest-neighbour rule (Couzin 2005)", loc="left")
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig1_zones.png"), bbox_inches="tight")
    plt.close(fig)


def fig_snapshots():
    """Group shape in the group's own frame + a compass showing the heading."""
    fig, axes = plt.subplots(1, 3, figsize=(7.2, 3.0))
    for ax, p in zip(axes, [0.0, 0.05, 0.3]):
        r = run_decision(60, p, T=250, seed=7)
        pos = np.array(r["pos"])
        rel = pos - pos.mean(0)
        ax.scatter(rel[:, 0], rel[:, 1], s=14, color="#3182bd", alpha=0.85, lw=0)
        mean = np.array(r["mean_dir"])
        a = np.degrees(np.arctan2(mean[1], mean[0]))
        lx = max(1.6, np.abs(rel[:, 0]).max() * 1.12)
        ly = max(1.6, np.abs(rel[:, 1]).max() * 1.12)
        ax.set_xlim(-lx, lx); ax.set_ylim(-ly, ly)
        # compass pinned to the top-right of the current data range
        rad = 0.20 * min(lx, ly)
        cx, cy = lx * 0.78, ly * 0.80
        ax.add_patch(Circle((cx, cy), rad, fill=False, ec="#c8ccd2", lw=0.8, zorder=5))
        ax.plot([cx - rad, cx + rad], [cy, cy], color="#d8dce1", lw=0.8, zorder=5)
        ax.annotate("", xy=(cx + 0.85 * rad * np.cos(a), cy + 0.85 * rad * np.sin(a)),
                    xytext=(cx, cy), zorder=6,
                    arrowprops=dict(arrowstyle="->", lw=1.6,
                                    color="#d94801" if abs(a) < 20 else "#8c949c"))
        ax.set_title(f"$p$ = {p:.2f}    heading error = {abs(a):.0f}°\n"
                     f"polar order = {r['polar']:.2f}", fontsize=9, loc="left")
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
    fig.suptitle("The decision model alone aligns the group's heading but does not hold its shape "
                 "(no separation/cohesion rules); compass = group heading, target = 0°",
                 y=1.06, fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig2_snapshots.png"), bbox_inches="tight")
    plt.close(fig)


def fig_accuracy(a):
    fig, axes = plt.subplots(1, 2, figsize=(7.2, 3.0))
    colors = plt.cm.viridis(np.linspace(0.1, 0.85, len(a)))
    for c, (n, d) in zip(colors, a.items()):
        axes[0].plot(d["p"], d["acc"], "-o", ms=3, color=c, label=f"$N$ = {n}")
    # right panel: informed fraction needed to reach 0.9 accuracy
    sizes, need = [], []
    for n, d in sorted(a.items()):
        ps, ac = d["p"], d["acc"]
        thr = None
        for i in range(1, len(ac)):
            if ac[i] >= 0.9 > ac[i - 1]:
                f = (0.9 - ac[i - 1]) / max(ac[i] - ac[i - 1], 1e-9)
                thr = ps[i - 1] + f * (ps[i] - ps[i - 1])
                break
        if thr is None and ac and ac[-1] >= 0.9:
            thr = ps[-1]
        if thr is not None:
            sizes.append(n)
            need.append(thr)
    axes[1].plot(sizes, [100 * x for x in need], "o-", color="#d94801")
    for x, y in zip(sizes, [100 * x for x in need]):
        axes[1].annotate(f"{y:.1f}%", (x, y), textcoords="offset points",
                         xytext=(0, 7), ha="center", fontsize=7.5, color="#d94801")
    axes[1].set_xscale("log")
    axes[1].set_xticks(sizes)
    axes[1].set_xticklabels([str(s) for s in sizes])
    axes[1].set_ylim(bottom=0)
    axes[1].set_xlabel("group size $N$")
    axes[1].set_ylabel("informed fraction needed for 90% accuracy (%)")
    axes[1].set_title("b)  bigger groups need fewer informed members", loc="left")
    axes[0].set_xlabel("fraction of informed individuals $p$")
    axes[0].set_ylabel("fraction of groups choosing the correct goal")
    axes[0].set_title("a)  decision accuracy saturates very early", loc="left")
    axes[0].set_ylim(-0.05, 1.05)
    axes[0].legend(frameon=False, fontsize=8, ncol=1)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig3_accuracy.png"), bbox_inches="tight")
    plt.close(fig)


def fig_consensus(b):
    grid = np.array(b["grid"])
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    im = ax.imshow(grid, vmin=0, vmax=1, cmap="RdYlGn", aspect="auto",
                   origin="lower")
    ax.set_xticks(range(len(b["splits"])))
    ax.set_xticklabels([f"{s:.2f}" for s in b["splits"]], fontsize=8)
    ax.set_yticks(range(len(b["omegas"])))
    ax.set_yticklabels([f"{w:.1f}" for w in b["omegas"]], fontsize=8)
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            ax.text(j, i, f"{grid[i, j]:.2f}", ha="center", va="center",
                    fontsize=7.5, color="black")
    ax.set_xlabel("share of informed robots in camp A")
    ax.set_ylabel("preference strength $\\omega$")
    ax.set_title(f"Majority camp wins ($N$={b['n']}, $p$={b['p']})", loc="left")
    cb = fig.colorbar(im, ax=ax, fraction=0.045)
    cb.set_label("win rate", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig4_consensus.png"), bbox_inches="tight")
    plt.close(fig)


def draw_maze(ax, walls, w_door=0.9, H=4.0):
    for wx, wy in walls:
        ax.add_patch(Rectangle((wx - 0.15, 0), 0.3, wy - w_door / 2, color="#636363"))
        ax.add_patch(Rectangle((wx - 0.15, wy + w_door / 2), 0.3, H - (wy + w_door / 2),
                               color="#636363"))
    ax.set_xlim(0, 10); ax.set_ylim(0, H)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_visible(False)


def fig_passage(m):
    fig = plt.figure(figsize=(7.2, 4.0))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.25], hspace=0.35, wspace=0.12)

    for col, (p, label) in enumerate([(0.0, "a)  0% informed"), (0.2, "b)  20% informed")]):
        ax = fig.add_subplot(gs[0, col])
        r = run_maze(seed=413, p_informed=p)
        for t, pos in r["traj"]:
            ax.scatter(pos[:, 0], pos[:, 1], s=7, color="#2171b5",
                       alpha=0.18 + 0.6 * (t / 1200.0), lw=0)
        draw_maze(ax, r["walls"], r["w_door"], r["H"])
        ax.set_title(f"{label}   $\\rightarrow$  {r['success'] * 100:.0f}% through",
                     loc="left", fontsize=8.5)

    ax = fig.add_subplot(gs[1, :])
    recs = m["p_scan"]
    ps = [r["p_informed"] for r in recs]
    ys = [r["success"] * 100 for r in recs]
    es = [r["success_std"] * 100 for r in recs]
    ax.errorbar(ps, ys, yerr=es, marker="o", ms=4.5, lw=1.5, color="#2171b5", capsize=3)
    ax.set_xlabel("fraction of robots that know the route")
    ax.set_ylabel("robots that reached the goal (%)")
    ax.set_ylim(0, 80)
    ax.set_title("c)  passage success rate, $N$=30, doorway 0.9 "
                 "(error bars = 1 s.d. over "
                 f"{recs[0].get('reps', '?')} runs)", loc="left", fontsize=8.5)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig5_passage.png"), bbox_inches="tight")
    plt.close(fig)


def fig_variants(m):
    fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9))
    sp = m["speed"]
    w = [r["informed_speed"] for r in sp]
    ax = axes[0]
    ax.plot(w, [r["t_first"] for r in sp], "o-", color="#e6550d", label="first robot through")
    ax.plot(w, [r["success"] * 100 for r in sp], "s-", color="#2171b5", label="final success (%)")
    ax.set_xlabel("speed of the informed robots (relative)")
    ax.set_title("a) faster scouts start earlier, but do not raise the total",
                 loc="left", fontsize=8.5)
    ax.legend(frameon=False, fontsize=7.5)

    sz = m["size"]
    n = [r["n"] for r in sz]
    ax = axes[1]
    ax.plot(n, [r["t_first"] for r in sz], "o-", color="#e6550d", label="first through")
    ax2 = ax.twinx()
    ax2.plot(n, [r["collisions"] / 1000 for r in sz], "^-", color="#756bb1",
             label="contacts (x1000)")
    ax.set_xlabel("swarm size $N$   (20% informed in every case)")
    ax.set_ylabel("steps until the first robot gets through", color="#e6550d")
    ax2.set_ylabel("pairwise contacts (x1000)", color="#756bb1")
    ax.set_title("b) scale buys a faster start but costs congestion", loc="left",
                 fontsize=8.5)
    fig.tight_layout()
    fig.savefig(os.path.join(FIGDIR, "fig6_variants.png"), bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    import sys

    quick = "--quick" in sys.argv
    if not os.path.exists(os.path.join(HERE, "results.json")):
        fig_zones()
        fig_snapshots()
    a = exp_a(quick)
    b = exp_b(quick)
    m = exp_maze(quick)
    with open(os.path.join(HERE, "results.json"), "w") as f:
        json.dump(dict(a={str(k): v for k, v in a.items()}, b=b, m=m), f, indent=1)
    fig_accuracy(a)
    fig_consensus(b)
    fig_passage(m)
    fig_variants(m)
    print("ALL DONE")
