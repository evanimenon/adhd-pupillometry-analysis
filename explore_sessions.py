from scipy.io import loadmat
import numpy as np
import pandas as pd

print("Loading Pupil_clean.mat ...")
m = loadmat('Pupil_clean.mat', struct_as_record=False, squeeze_me=True)
S = m['S']
N = len(S)
pd.set_option('display.max_rows', 20)

def show(i):
    s = S[i]
    ep = s.epocs
    perf = np.ravel(ep.Perform).astype(float)
    rt = np.ravel(ep.Rtime).astype(float)
    df = pd.DataFrame({
        'Trial':   np.ravel(ep.Trial),
        'Load':    np.ravel(ep.Load),
        'Perform': perf,
        'Rtime':   rt,
    })
    print("\n" + "=" * 50)
    print(f"Session {i} of {N-1}   |   group = {s.Group}   |   subject = {s.Subject}")
    print("=" * 50)
    print(df)
    print(f"\nfraction correct: {np.nanmean(perf):.3f}    mean RT: {np.nanmean(rt):.0f} ms")

i = 0
show(i)
print("\n[Enter/n = next | p = prev | number = jump | q = quit]")

while True:
    cmd = input(f"\nsession {i} > ").strip().lower()
    if cmd in ('q', 'quit', 'exit'):
        break
    elif cmd in ('', 'n', 'next'):
        i = (i + 1) % N
        show(i)
    elif cmd in ('p', 'prev', 'previous'):
        i = (i - 1) % N
        show(i)
    elif cmd.isdigit():
        j = int(cmd)
        if 0 <= j < N:
            i = j
            show(i)
        else:
            print(f"  out of range (0 to {N-1})")
    else:
        print("  commands: Enter/n = next, p = prev, a number = jump, q = quit")
