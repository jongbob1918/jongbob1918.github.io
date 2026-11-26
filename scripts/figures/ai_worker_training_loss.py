"""Plot the latest GR00T runs from their exported training_metrics.jsonl files.

Usage: python3 scripts/figures/ai_worker_training_loss.py GRASPNET_JSONL CENTERPOSE_JSONL
The committed CSV contains 1,000-step means, not validation loss or task success.
"""
import csv
import json
from pathlib import Path
import sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from PIL import Image

ROOT = Path(__file__).resolve().parents[2]
CSV = ROOT / 'assets/data/ai-worker-training-loss.csv'
IMAGE = ROOT / 'assets/images/ai-worker-training-loss.webp'


def aggregate(path):
    rows = [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]
    samples = {int(row['step']): float(row['loss']) for row in rows if 'loss' in row}
    if sorted(samples) != list(range(10, 150001, 10)):
        raise ValueError('Expected loss records every 10 steps from 10 through 150,000')
    return [sum(samples[s] for s in range(end - 990, end + 1, 10)) / 100
            for end in range(1000, 150001, 1000)]


if len(sys.argv) == 3:
    graspnet, centerpose = map(aggregate, sys.argv[1:])
    CSV.parent.mkdir(parents=True, exist_ok=True)
    with CSV.open('w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['step_end', 'graspnet_mean_loss', 'centerpose_mean_loss'])
        writer.writerows((step, f'{g:.8f}', f'{c:.8f}')
                         for step, g, c in zip(range(1000, 150001, 1000), graspnet, centerpose))
elif len(sys.argv) != 1:
    raise SystemExit(__doc__)

with CSV.open() as file:
    rows = list(csv.DictReader(file))
steps = [int(row['step_end']) for row in rows]
plt.rcParams.update({'font.family': 'DejaVu Sans', 'font.size': 12})
fig, ax = plt.subplots(figsize=(11, 5.6), layout='constrained')
for key, label, color in [('graspnet_mean_loss', 'GraspNet · 310 demonstrations', '#2563eb'),
                           ('centerpose_mean_loss', 'CenterPose · 319 demonstrations', '#ea580c')]:
    values = [float(row[key]) for row in rows]
    ax.plot(steps, values, label=label, color=color, linewidth=2)
    print(f'{label}: last 10,000-step mean = {sum(values[-10:]) / 10:.6f}')
ax.set(title='GR00T N1.7 training loss', xlabel='Training step',
       ylabel='Training loss (1,000-step mean; log scale)', yscale='log', xlim=(0, 150000))
ax.set_xticks([0, 30000, 60000, 90000, 120000, 150000])
ax.xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:,.0f}'))
ax.grid(which='major', color='#e2e8f0')
ax.set_axisbelow(True)
ax.spines[['top', 'right']].set_visible(False)
ax.legend(frameon=False, loc='upper right')
from io import BytesIO
buffer = BytesIO()
fig.savefig(buffer, format='png', dpi=180, facecolor='white')
Image.open(buffer).convert('RGB').save(IMAGE, 'WEBP', quality=92)
plt.close(fig)
