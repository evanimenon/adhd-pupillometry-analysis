import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('pupil_summary.csv')
order = ['ADHD', 'mADHD', 'Control']

colors = {'ADHD': '#2a9d8f', 'mADHD': '#e9c46a', 'Control': '#264653'}

plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'axes.spines.top': False,
    'axes.spines.right': False,
    'axes.edgecolor': '#666666',
    'axes.titlesize': 13,
    'axes.titleweight': 'medium',
})

fig, (axB, axC) = plt.subplots(1, 2, figsize=(11, 5))

# B: performance by group
for i, g in enumerate(order):
    v = df.loc[df.group == g, 'perf_all'].values
    x = np.random.normal(i, 0.06, len(v))
    axB.scatter(x, v, facecolors=colors[g], edgecolors='white',
                s=70, linewidths=1.0, alpha=0.75, zorder=3)
    axB.hlines(np.mean(v), i-0.28, i+0.28, colors=colors[g],
               linewidth=4, zorder=4)
axB.set_xticks(range(3)); axB.set_xticklabels(order)
axB.set_ylabel('Performance (fraction correct)')
axB.set_title('Accuracy by group')
axB.set_ylim(0.3, 1.0)
axB.grid(axis='y', alpha=0.15, zorder=0)

# C: performance by group and load
for i, g in enumerate(order):
    sub = df[df.group == g]
    base = i * 2.5
    for _, r in sub.iterrows():
        axC.plot([base, base+1], [r.perf_high, r.perf_low],
                 color=colors[g], alpha=0.25, linewidth=1.0, zorder=2)
        axC.scatter([base, base+1], [r.perf_high, r.perf_low],
                    facecolors=colors[g], edgecolors='white',
                    s=45, linewidths=0.8, alpha=0.75, zorder=3)
    axC.hlines(sub.perf_high.mean(), base-0.3, base+0.3,
               colors=colors[g], linewidth=4, zorder=4)
    axC.hlines(sub.perf_low.mean(), base+0.7, base+1.3,
               colors=colors[g], linewidth=4, zorder=4)
axC.set_xticks([i*2.5 + 0.5 for i in range(3)]); axC.set_xticklabels(order)
axC.set_ylabel('Performance (fraction correct)')
axC.set_title('Accuracy by group and cognitive load\n(left = high load, right = low load)')
axC.set_ylim(0.2, 1.0)
axC.grid(axis='y', alpha=0.15, zorder=0)

plt.tight_layout()
plt.savefig('figure1.png', dpi=200, bbox_inches='tight')
print("saved figure1.png")