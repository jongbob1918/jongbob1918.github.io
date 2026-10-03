"""Generate axis-only PNG figures for the GELU explanation.

Run: python3 scripts/figures/ch03_gelu.py
Requires matplotlib and numpy; uses the exact normal CDF via math.erf.
"""
from math import erf, sqrt
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


OUT = Path(__file__).resolve().parents[2] / "site/public/images/notes/linear-nonlinear-activations"
BLUE = "#2563eb"
ORANGE = "#e87924"
GRAY = "#94a3b8"


def cdf(x):
    return np.array([0.5 * (1 + erf(float(t) / sqrt(2))) for t in np.atleast_1d(x)])


def style(ax, ylabel):
    ax.set_xlabel(r"$x$", fontsize=14)
    ax.set_ylabel(ylabel, fontsize=14)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(alpha=0.16)
    ax.set_axisbelow(True)
    ax.tick_params(labelsize=11)


def save(fig, name):
    fig.tight_layout(pad=1.5)
    fig.savefig(OUT / name, dpi=180, facecolor="white")
    plt.close(fig)


def cumulative_probability():
    x = np.linspace(-4, 4, 1601)
    density = np.exp(-x**2 / 2) / sqrt(2 * np.pi)
    fig, axes = plt.subplots(2, 1, figsize=(6.4, 7.6))
    left, right = axes
    left.plot(x, density, color=BLUE, lw=2.5)
    left.fill_between(x, density, where=x <= 1, color=BLUE, alpha=0.25)
    left.vlines(1, 0, np.exp(-0.5) / sqrt(2 * np.pi), color=ORANGE, lw=2)
    left.set(xlim=(-4, 4), ylim=(0, 0.44), xticks=[-3, -1, 0, 1, 3])
    style(left, r"$\varphi(x)$")
    right.plot(x, cdf(x), color=BLUE, lw=2.5)
    probability = cdf([1])[0]
    right.vlines(1, 0, probability, color=ORANGE, ls="--", lw=1.5)
    right.hlines(probability, -4, 1, color=ORANGE, ls="--", lw=1.5)
    right.scatter([1], [probability], color=ORANGE, s=45, zorder=4)
    right.set(xlim=(-4, 4), ylim=(0, 1.04), xticks=[-3, -1, 0, 1, 3], yticks=[0, 0.5, probability, 1])
    right.set_yticklabels(["0", "0.5", "0.841", "1"])
    style(right, r"$\Phi(x)$")
    save(fig, "gelu-normal-cdf.png")


def gelu_region(name, limits, ylimits, highlight, point, reference):
    x = np.linspace(*limits, 1601)
    y = x * cdf(x)
    fig, ax = plt.subplots(figsize=(6.4, 3.8))
    ax.axhline(0, color=GRAY, lw=1)
    ax.axvline(0, color=GRAY, lw=1)
    if reference is not None:
        ax.plot(x, reference * x, color=GRAY, lw=2, ls="--")
    ax.plot(x, y, color=BLUE, alpha=0.35, lw=2)
    mask = (x >= highlight[0]) & (x <= highlight[1])
    ax.plot(x[mask], y[mask], color=BLUE, lw=3)
    value = point * cdf([point])[0]
    ax.vlines(point, min(0, value), max(0, value), color=ORANGE, lw=1.5, ls="--")
    ax.scatter([point], [value], color=ORANGE, s=48, zorder=5)
    ax.set(xlim=limits, ylim=ylimits)
    style(ax, r"$\mathrm{GELU}(x)$")
    save(fig, name)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cumulative_probability()
    gelu_region("gelu-positive.png", (-4, 4), (-0.4, 4.2), (2, 4), 3, 1)
    gelu_region("gelu-negative.png", (-4, 0), (-0.19, 0.025), (-4, -2), -3, None)
    gelu_region("gelu-near-zero.png", (-0.25, 0.25), (-0.13, 0.16), (-0.25, 0.25), 0, 0.5)


if __name__ == "__main__":
    main()
