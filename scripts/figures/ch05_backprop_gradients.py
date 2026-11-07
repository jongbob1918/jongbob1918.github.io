"""변수 색상과 접선으로 역전파를 설명하는 그림.

실행: PYTHONDONTWRITEBYTECODE=1 python3 scripts/figures/ch05_backprop_gradients.py
시각화 참고: https://www.3blue1brown.com/lessons/backpropagation-calculus/
"""
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
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
    fig, ax = plt.subplots(figsize=(8, 6.1), dpi=200, facecolor=BG)
    ax.set(xlim=(0, 10), ylim=(0, 7.7)); ax.axis('off')
    text(ax, 5, 7.23, '가중치를 조금 바꾸면, 손실은 얼마나 바뀔까?', 19)
    xs = [1, 3.65, 6.3, 9]
    for x, symbol, label, color in zip(xs, ['$w_1$', '$z$', '$p$', '$L$'],
                                      ['가중치', '점수', '예측 확률', '손실'],
                                      [BLUE, GREEN, YELLOW, RED]):
        text(ax, x, 5.95, symbol, 36, color)
        text(ax, x, 5.25, label, 14, MUTED)
    for left, right in zip(xs[:-1], xs[1:]):
        arrow(ax, left+.48, 5.95, right-.48, 5.95)
    text(ax, 5, 4.45, r'$z=w_1x_1+w_2x_2+b\qquad p=\sigma(z)$', 19)
    text(ax, 5, 3.77, '입력과 나머지 가중치는 고정하고, 변화가 전달되는 길만 봅니다.', 13, MUTED)
    ax.plot([.6, 9.4], [3.25, 3.25], color='#343b46', lw=1)
    text(ax, 5, 2.85, '역전파  ·  오른쪽에서 구한 기울기를 차례로 곱합니다', 15)
    fraction(ax, 1, 1.7, r'$\partial L$', r'$\partial w_1$', RED, BLUE)
    text(ax, 2.12, 1.7, '$=$', 25)
    fraction(ax, 3.35, 1.7, r'$\partial z$', r'$\partial w_1$', GREEN, BLUE)
    text(ax, 4.65, 1.7, r'$\times$', 23)
    fraction(ax, 5.95, 1.7, r'$\partial p$', r'$\partial z$', YELLOW, GREEN)
    text(ax, 7.25, 1.7, r'$\times$', 23)
    fraction(ax, 8.65, 1.7, r'$\partial L$', r'$\partial p$', RED, YELLOW)
    for x, s in [(3.35, '가중치 → 점수'), (5.95, '점수 → 확률'), (8.65, '확률 → 손실')]:
        text(ax, x, .85, s, 13, MUTED)
    arrow(ax, 9.15, .33, 2.85, .33, WHITE)
    fig.subplots_adjust(left=.03, right=.97, bottom=.025, top=.98)
    fig.savefig(OUT/'backprop-chain.png', facecolor=BG)
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
