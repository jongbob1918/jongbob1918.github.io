"""Generate the example-network figures for the backpropagation chapter.

The same network is drawn three times; later figures highlight the parts the
text is using (the path of one weight, the weights that share one delta).

Run: python3 scripts/figures/ch04_backprop_network.py
Requires matplotlib.
"""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Circle

for f in Path("/usr/share/fonts/truetype/nanum").glob("NanumGothic*.ttf"):
    font_manager.fontManager.addfont(str(f))
plt.rcParams["font.family"] = "NanumGothic"
plt.rcParams["mathtext.fontset"] = "dejavuserif"

OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/backpropagation"
BLUE = "#2563eb"
ORANGE = "#e87924"
GRAY = "#64748b"
LIGHT = "#cbd5e1"
R = 0.42

X = [(0.0, 0.9), (0.0, -0.9)]
H = [(4.4, 1.8), (4.4, 0.0), (4.4, -1.8)]
YHAT = (8.4, 0.0)


def line(ax, p, q, color, lw):
    ax.plot([p[0], q[0]], [p[1], q[1]], color=color, lw=lw, zorder=1)


def label(ax, p, q, text, t, color, size=12):
    x = p[0] + (q[0] - p[0]) * t
    y = p[1] + (q[1] - p[1]) * t
    ax.text(x, y, text, fontsize=size, color=color, ha="center", va="center",
            bbox=dict(fc="white", ec="none", pad=1.2), zorder=3)


def circle(ax, p, text, color, size=16):
    ax.add_patch(Circle(p, R, fc="white", ec=color, lw=2, zorder=2))
    ax.text(*p, text, fontsize=size, ha="center", va="center", color=color, zorder=4)


def relu_node(ax, p, name, color):
    ax.add_patch(Circle(p, R, fc="white", ec=color, lw=2, zorder=2))
    cx, cy = p
    s, base = 0.24, cy - 0.08
    ax.plot([cx - s - 0.04, cx + s + 0.04], [base, base], color=GRAY, lw=0.9, zorder=3)
    ax.plot([cx, cx], [base - 0.06, base + s + 0.06], color=GRAY, lw=0.9, zorder=3)
    ax.plot([cx - s, cx, cx + s], [base, base, base + s], color=color, lw=2.2, zorder=4)
    ax.text(cx, cy + R + 0.28, name, fontsize=15, ha="center", va="center", color=color)


def draw(name, hot_w=(), hot_v=(), hot_nodes=(), delta=None):
    """hot_w: (i, j) first-layer edges, hot_v: j second-layer edges, hot_nodes: j."""
    fig, ax = plt.subplots(figsize=(8.6, 5.0))
    ax.set_aspect("equal")
    ax.axis("off")

    for i, p in enumerate(X, 1):
        for j, q in enumerate(H, 1):
            hot = (i, j) in hot_w
            line(ax, p, q, ORANGE if hot else GRAY, 2.8 if hot else 1.4)
    for j, p in enumerate(H, 1):
        hot = j in hot_v
        line(ax, p, YHAT, ORANGE if hot else GRAY, 2.8 if hot else 1.4)

    for i, p in enumerate(X, 1):
        for j, q in enumerate(H, 1):
            hot = (i, j) in hot_w
            label(ax, p, q, rf"$w_{{{i}{j}}}$", 0.20, ORANGE if hot else GRAY)
    for j, p in enumerate(H, 1):
        hot = j in hot_v
        label(ax, p, YHAT, rf"$v_{j}$", 0.62, ORANGE if hot else GRAY)

    for i, p in enumerate(X, 1):
        circle(ax, p, rf"$x_{i}$", GRAY)
    for j, p in enumerate(H, 1):
        relu_node(ax, p, rf"$h_{j}$", ORANGE if j in hot_nodes else BLUE)
    circle(ax, YHAT, r"$\hat{y}$", ORANGE if hot_v else GRAY)
    if delta is not None:
        p = H[delta - 1]
        ax.text(p[0] + 0.95, p[1] + 0.3, rf"$\delta_{delta}$", fontsize=15,
                ha="center", va="center", color=ORANGE,
                bbox=dict(fc="white", ec="none", pad=1.2), zorder=5)

    head = dict(fontsize=13, ha="center", va="center", color="#334155")
    for x, t in ((0.0, "입력층"), (4.4, "은닉층"), (8.4, "출력층")):
        ax.text(x, 3.35, t, **head)

    ax.set_xlim(-0.8, 9.2)
    ax.set_ylim(-2.5, 3.8)
    fig.tight_layout(pad=0.5)
    fig.savefig(OUT / name, dpi=180, facecolor="white")
    plt.close(fig)


draw("example-network.png")
draw("path-w11.png", hot_w=[(1, 1)], hot_v=[1], hot_nodes=[1])
draw("shared-delta.png", hot_w=[(1, 1), (2, 1)], hot_nodes=[1], delta=1)
