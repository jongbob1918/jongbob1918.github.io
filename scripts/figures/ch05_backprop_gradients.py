"""변수 색상과 접선으로 역전파를 설명하는 그림.

실행: PYTHONDONTWRITEBYTECODE=1 python3 scripts/figures/ch05_backprop_gradients.py
시각화 참고: https://www.3blue1brown.com/lessons/backpropagation-calculus/
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from ch05_sigmoid_animation import set_korean_font, sigmoid

OUT = Path(__file__).resolve().parents[2] / 'site/public/images/notes/easy-deep-learning-ch04'
BG, WHITE, MUTED = '#101318', '#f1f1ed', '#a8b0bd'
BLUE, GREEN, YELLOW, RED = '#67c5f5', '#83dba0', '#f6d56a', '#fa8282'
ORANGE = '#efa264'


def text(ax, x, y, s, size=16, color=WHITE, **kw):
    return ax.text(x, y, s, fontsize=size, color=color, ha='center', va='center', **kw)


def arrow(ax, x1, y1, x2, y2, color=MUTED):
    ax.annotate('', (x2, y2), (x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.7, mutation_scale=14))


def fraction(ax, x, y, numerator, denominator, top_color, bottom_color):
    text(ax, x, y+.25, numerator, 25, top_color)
    ax.plot([x-.42, x+.42], [y, y], color=WHITE, lw=1.2)
    text(ax, x, y-.27, denominator, 25, bottom_color)


def chain():
    # Mid-tone inks keep the transparent diagram legible on light and dark pages.
    ink, blue, green, gold, red = '#777777', '#2789ba', '#388d63', '#a57816', '#c55b60'
    fig, ax = plt.subplots(figsize=(10, 2.7), dpi=200)
    ax.set(xlim=(0, 12), ylim=(2.95, 6.05), aspect='equal')
    ax.axis('off')
    for x, y, label in [(1, 5.2, '$x_1$'), (1, 3.5, '$x_2$')]:
        ax.add_patch(Circle((x, y), .37, fill=False, ec=ink, lw=1.7))
        text(ax, x, y, label, 22, ink)
    # Weighted inputs meet at the sum; its output is the sigmoid input z.
    arrow(ax, 1.38, 5.1, 3.45, 4.48, blue)
    arrow(ax, 1.38, 3.62, 3.45, 4.22, blue)
    text(ax, 2.25, 5.1, '$w_1$', 24, blue)
    text(ax, 2.25, 3.6, '$w_2$', 24, blue)
    ax.add_patch(Circle((3.9, 4.35), .46, fill=False, ec=green, lw=2))
    text(ax, 3.9, 4.35, r'$\Sigma$', 25, green)
    text(ax, 3.9, 5.55, '$b$', 22, green)
    arrow(ax, 3.9, 5.25, 3.9, 4.85, green)
    arrow(ax, 4.38, 4.35, 5.52, 4.35, green)
    text(ax, 4.95, 4.72, '$z$', 26, green)
    # Sigmoid curve inside the activation node.
    ax.add_patch(Circle((6.15, 4.35), .58, fill=False, ec=gold, lw=2))
    t = np.linspace(-4, 4, 100)
    ax.plot(6.15+t*.105, 4.35+(sigmoid(t)-.5)*.65, color=gold, lw=2)
    text(ax, 6.15, 3.48, '시그모이드', 13, ink)
    arrow(ax, 6.76, 4.35, 8.35, 4.35, gold)
    text(ax, 7.55, 4.78, r'$p$', 25, gold)
    ax.add_patch(FancyBboxPatch((8.4, 3.8), 1.7, 1.1,
                               boxstyle='round,pad=0.04,rounding_size=0.08',
                               fill=False, ec=red, lw=1.8))
    text(ax, 9.25, 4.53, '손실 함수', 14, ink)
    text(ax, 9.25, 4.12, r'$L(p,y)$', 22, red)
    text(ax, 9.25, 5.65, '정답 $y$', 17, ink)
    arrow(ax, 9.25, 5.35, 9.25, 4.98, ink)
    arrow(ax, 10.17, 4.35, 11.45, 4.35, red)
    text(ax, 11, 4.77, '$L$', 26, red)
    fig.subplots_adjust(left=.02, right=.98, bottom=.02, top=.98)
    fig.savefig(OUT/'backprop-chain.png', transparent=True)
    plt.close(fig)


def gradients():
    # Compare loss-versus-z curves: tangent slopes are the actual backpropagated dL/dz.
    fig, axes = plt.subplots(3, 1, figsize=(8, 9), dpi=200, facecolor=BG)
    fig.subplots_adjust(left=.12, right=.96, top=.82, bottom=.09, hspace=.62)
    fig.text(.08, .955, '크게 틀렸는데도, 기울기는 작을 수 있습니다', color=WHITE, fontsize=20)
    fig.text(.08, .911, '정답 y = 1    ·    같은 점 z ≈ −4.60,  p = 0.01에서 비교', color=MUTED, fontsize=14)
    z = np.linspace(-7, 3, 900)
    p = sigmoid(z)
    z0 = np.log(.01/.99)
    curves = [p, (p-1)**2, np.logaddexp(0, -z)]
    values = [.01, .99**2, -np.log(.01)]
    slopes = [.0099, -2*.99*.0099, -.99]
    colors = [YELLOW, ORANGE, BLUE]
    labels = ['시그모이드', 'MSE', 'BCE']
    notes = ['확률이 거의 변하지 않음', '손실도 거의 변하지 않음', '손실이 뚜렷하게 줄어듦']
    for i, (ax, curve, val, slope, color) in enumerate(zip(axes, curves, values, slopes, colors)):
        ax.set_facecolor(BG)
        ax.plot(z, curve, color=color, lw=2.4)
        ax.axvline(z0, color=MUTED, lw=1, ls=(0, (3, 5)), alpha=.6)
        t = np.array([z0-1.35, z0+1.35])
        ax.plot(t, val+slope*(t-z0), color=WHITE, lw=2.3)
        ax.scatter([z0], [val], s=42, color=color, edgecolors=WHITE, zorder=5)
        ax.text(0, 1.15, labels[i], color=color, fontsize=18, transform=ax.transAxes)
        ax.text(.25, 1.15, notes[i], color=WHITE, fontsize=15, transform=ax.transAxes)
        derivative = r'$\partial p/\partial z$' if i == 0 else r'$\partial L/\partial z$'
        ax.text(.52 if i == 2 else .02, .67, derivative + f' = {slope:.4f}', color=WHITE, fontsize=15,
                transform=ax.transAxes, bbox=dict(fc=BG, ec='none', pad=3))
        ax.set(xlim=(-7, 3), xticks=[-6, -4, -2, 0, 2])
        ax.set_ylim([(-.08, 1.08), (-.4, 7.4), (-.4, 7.4)][i])
        ax.set_yticks([0, 1] if i == 0 else [0, 4, 7])
        ax.spines[['top', 'right']].set_visible(False)
        for side in ['left', 'bottom']:
            ax.spines[side].set_color('#727c8a')
        ax.tick_params(colors=MUTED, labelsize=11)
        ax.set_ylabel('확률 p' if i == 0 else '손실 L', color=MUTED, fontsize=12)
    axes[-1].set_xlabel('점수 z', color=MUTED, fontsize=13)
    fig.savefig(OUT/'backprop-gradients.png', facecolor=BG)
    plt.close(fig)


def render():
    set_korean_font()
    plt.rcParams['mathtext.fontset'] = 'cm'
    OUT.mkdir(parents=True, exist_ok=True)
    chain()
    gradients()


if __name__ == '__main__':
    render()
