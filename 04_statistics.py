import pandas as pd
import numpy as np
from scipy.stats import kruskal, mannwhitneyu, spearmanr

df = pd.read_csv('pupil_summary.csv')
g = {name: df[df.group == name] for name in ['ADHD', 'mADHD', 'Control']}

print("MAX PUPIL: group comparison")
h, p = kruskal(g['ADHD'].maxpupil, g['mADHD'].maxpupil, g['Control'].maxpupil)
print(f"Kruskal-Wallis across 3 groups: H={h:.3f}, p={p:.4f}")

# pairwise contrast
for a, b in [('ADHD','Control'), ('ADHD','mADHD'), ('mADHD','Control')]:
    u, pu = mannwhitneyu(g[a].maxpupil, g[b].maxpupil)
    print(f"  {a:8s} vs {b:8s}: Mann-Whitney U={u:.1f}, p={pu:.4f}")

print("\nPERFORMANCE: group comparison")
h, p = kruskal(g['ADHD'].perf_all, g['mADHD'].perf_all, g['Control'].perf_all)
print(f"Kruskal-Wallis across 3 groups: H={h:.3f}, p={p:.4f}")
for a, b in [('ADHD','Control'), ('ADHD','mADHD'), ('mADHD','Control')]:
    u, pu = mannwhitneyu(g[a].perf_all, g[b].perf_all)
    print(f"  {a:8s} vs {b:8s}: Mann-Whitney U={u:.1f}, p={pu:.4f}")

print("\nCORRELATIONS (all sessions)")
df['rt_sd_s'] = df.rt_sd / 1000
for xc, yc, lbl in [('rt_sd_s','maxpupil','pupil vs RT variability'),
                    ('maxpupil','perf_all','pupil vs performance'),
                    ('rt_sd_s','perf_all','performance vs RT variability')]:
    rho, pp = spearmanr(df[xc], df[yc])
    print(f"  {lbl:32s} rho={rho:+.3f}  p={pp:.2e}")
