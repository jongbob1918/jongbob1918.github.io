"""퍼셉트론의 출력 영역 예시: z = 10x1 + x2 - 100."""
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from ch05_linear_classification import configure_font


def main():
    configure_font()
    fig, ax = plt.subplots(figsize=(7.2, 5.2), dpi=200)
    x = np.linspace(0, 10, 201)
    boundary = 100 - 10 * x
    ax.fill_between(x, boundary, 100, color='#e1edf5')
    ax.fill_between(x, 0, boundary, color='#fbeadb')
    ax.plot(x, boundary, color='#675084', lw=2.5)
    ax.text(1.3, 91, r'$x_2 = -\frac{w_1}{w_2}x_1 - \frac{b}{w_2}$', fontsize=14, color='#675084',
            bbox={'facecolor': 'white', 'edgecolor': 'none', 'alpha': .9})
    ax.set(xlim=(0, 10), ylim=(0, 100), xlabel='공부 시간 $x_1$ (시간)', ylabel='출석률 $x_2$ (%)')
    ax.spines[['top', 'right']].set_visible(False)
    ax.grid(color='white', alpha=.6)
    ax.set_axisbelow(True)
    fig.tight_layout()
    out = Path(__file__).resolve().parents[2] / 'site/public/images/notes/easy-deep-learning-ch04/perceptron-decision-regions.png'
    fig.savefig(out, facecolor='white')
    plt.close(fig)


if __name__ == '__main__':
    main()
