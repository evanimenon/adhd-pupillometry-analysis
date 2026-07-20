import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('pupil_summary.csv')
order = ['ADHD', 'mADHD', 'Control']
colors = {'ADHD': '#1f77b4', 'mADHD': '#2ca02c', 'Control': '#d62728'}

fig, (axB, axC) = plt.subplots(1, 2, figsize=(11, 5))

# B: performance by group
for i, g in enumerate(order):
    v = df.loc[df.group == g, 'perf_all'].values
    x = np.random.normal(i, 0.05, len(v))
    axB.scatter(x, v, facecolors='none', edgecolors=colors[g], s=60, linewidths=1.5)
    axB.hlines(np.mean(v), i-0.25, i+0.25, colors=colors[g], linewidth=3)
axB.set_xticks(range(3)); axB.set_xticklabels(order)
axB.set_ylabel('Performance (fraction correct)')
axB.set_title('By group'); axB.set_ylim(0.3, 1.0)

# C: performance by group and load
for i, g in enumerate(order):
    sub = df[df.group == g]
    base = i * 2.5
    for _, r in sub.iterrows():
        axC.plot([base, base+1], [r.perf_high, r.perf_low],
                 color=colors[g], alpha=0.3, linewidth=0.8)
        axC.scatter([base, base+1], [r.perf_high, r.perf_low],
                    facecolors='none', edgecolors=colors[g], s=40, linewidths=1.2)
    axC.hlines(sub.perf_high.mean(), base-0.3, base+0.3, colors=colors[g], linewidth=3)
    axC.hlines(sub.perf_low.mean(),  base+0.7, base+1.3, colors=colors[g], linewidth=3)
axC.set_xticks([i*2.5 + 0.5 for i in range(3)]); axC.set_xticklabels(order)
axC.set_ylabel('Performance (fraction correct)')
axC.set_title('By group and cognitive load\n(left=high, right=low)')
axC.set_ylim(0.2, 1.0)

plt.tight_layout()
plt.savefig('figure1.png', dpi=150, bbox_inches='tight')
print("saved figure1.png")
