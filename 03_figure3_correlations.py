import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import spearmanr

df = pd.read_csv('pupil_summary.csv')
order = ['ADHD', 'mADHD', 'Control']
colors = {'ADHD': '#2a9d8f', 'mADHD': '#e9c46a', 'Control': '#264653'}

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': '#666666',
    'axes.titlesize': 12,
})

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

def scatter_panel(ax, xcol, ycol, xlabel, ylabel):
    for g in order:
        sub = df[df.group == g]
        ax.scatter(sub[xcol], sub[ycol], facecolors=colors[g],
                   edgecolors='white', s=65, linewidths=0.8,
                   alpha=0.8, label=g, zorder=3)
    x = df[xcol].values; y = df[ycol].values
    ok = ~(np.isnan(x) | np.isnan(y))
    rho, p = spearmanr(x[ok], y[ok])
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    ax.set_title(f'ρ = {rho:.2f},  p = {p:.1e}   (n = {ok.sum()})')
    ax.grid(alpha=0.15, zorder=0)

df['rt_sd_s'] = df['rt_sd'] / 1000.0

scatter_panel(axes[0], 'rt_sd_s', 'maxpupil',
              'σ Reaction time (s)', 'Max pupil diameter (z-score)')
scatter_panel(axes[1], 'maxpupil', 'perf_all',
              'Max pupil diameter (z-score)', 'Performance (fraction correct)')
scatter_panel(axes[2], 'rt_sd_s', 'perf_all',
              'σ Reaction time (s)', 'Performance (fraction correct)')

axes[0].legend(frameon=False)
plt.tight_layout()
plt.savefig('figure3.png', dpi=200, bbox_inches='tight')
print("saved figure3.png")

for xc, yc, lbl in [('rt_sd_s','maxpupil','pupil vs RT variability'),
                    ('maxpupil','perf_all','pupil vs performance'),
                    ('rt_sd_s','perf_all','performance vs RT variability')]:
    x = df[xc].values; y = df[yc].values
    ok = ~(np.isnan(x) | np.isnan(y))
    rho, p = spearmanr(x[ok], y[ok])
    print(f"{lbl:35s} rho={rho:+.3f}  p={p:.2e}")