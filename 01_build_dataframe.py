from scipy.io import loadmat
import numpy as np
import pandas as pd

m = loadmat('Pupil_clean.mat', struct_as_record=False, squeeze_me=True)
S = m['S']

PROBE_LO, PROBE_HI = 6000, 7500 # post-probe window (samples = ms at 1kHz)

rows = []
for s in S:
    ep = s.epocs
    load= np.ravel(ep.Load).astype(float) # 1=low, 2=high
    perform = np.ravel(ep.Perform).astype(float) # 1/0/nan
    rtime= np.ravel(ep.Rtime).astype(float) # ms, nan if no response
    P= ep.Pupil # (160, 2): [diameter, timestamps]

    # this is per-trial max pupil in the post-probe window
    maxpup = np.full(P.shape[0], np.nan)
    for t in range(P.shape[0]):
        d = np.asarray(P[t, 0], dtype=float)
        if d.size == 8000:
            w = d[PROBE_LO:PROBE_HI]
            if np.any(~np.isnan(w)):
                maxpup[t] = np.nanmax(w)

    def frac_correct(mask):
        v = perform[mask]
        v = v[~np.isnan(v)]
        return np.mean(v) if v.size else np.nan

    rows.append(dict(
        group = str(s.Group),
        subject = float(np.ravel(s.Subject)[0]),
        perf_all = frac_correct(np.ones_like(load, bool)),
        perf_low = frac_correct(load == 1),
        perf_high = frac_correct(load == 2),
        rt_mean = np.nanmean(rtime),
        rt_sd = np.nanstd(rtime), # reaction-time variability
        maxpupil = np.nanmean(maxpup), # session mean of per-trial max
    ))

df = pd.DataFrame(rows)

# renaming groups to the labels from the paper
df['group'] = df['group'].map({'off-ADHD': 'ADHD', 'on-ADHD': 'mADHD', 'Ctrl': 'Control'})

df.to_csv('pupil_summary.csv', index=False)
print("Sessions:", len(df))
print(df['group'].value_counts())
print("\nPer-group means:")
print(df.groupby('group')[['perf_all','perf_low','perf_high','rt_sd','maxpupil']].mean().round(3))
