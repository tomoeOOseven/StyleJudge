#!/usr/bin/env python3
"""Reproduce every human-correlation number reported in the paper (Sec. 4.3, per-style table).

    python reproduce_paper_numbers.py

Reads manifest.csv (human ratings) and stylejudge_predictions.csv (student and teacher S_final),
both in this folder. Bootstrap intervals use the same procedure as score_metric.py
(2,000 paired resamples, seed 0).
"""
import os
import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from score_metric import corr_ci

HERE = os.path.dirname(os.path.abspath(__file__))
man = pd.read_csv(os.path.join(HERE, "manifest.csv"))
pred = pd.read_csv(os.path.join(HERE, "stylejudge_predictions.csv"))
df = man.merge(pred, on="row_id", how="inner")
assert len(df) == len(man) == 878, "manifest and predictions must cover all 878 rows"
S, T, H = "student_final_score", "teacher_final_score", "human_score"
seen, unseen = df[df.in_benchmark_728], df[~df.in_benchmark_728]

print("== Overall (Pearson r, Spearman rho, bootstrap 95% CI on Pearson)")
for name, d in [("seen_728", seen), ("unseen_150", unseen), ("all_878", df)]:
    for col in (S, T):
        r, rho, lo, hi = corr_ci(d[col].to_numpy(float), d[H].to_numpy(float))
        print(f"{name:11s} {col:20s} r={r:.3f} rho={rho:.3f} CI=[{lo:.3f}, {hi:.3f}]")

h, s, t = (seen[c].to_numpy(float) for c in (H, S, T))
idx = np.random.default_rng(0).integers(0, len(h), size=(2000, len(h)))
diff = [pearsonr(s[i], h[i])[0] - pearsonr(t[i], h[i])[0] for i in idx]
lo, hi = np.percentile(diff, [2.5, 97.5])
print(f"\nstudent - teacher on seen_728: 95% CI [{lo:.3f}, {hi:.3f}]")

print("\n== Per rater (seen_728, student)")
for r, g in seen.groupby("rater"):
    print(f"{r}: n={len(g)} r={pearsonr(g[S], g[H])[0]:.3f}")

print("\n== Per style (all 878)")
print(f"{'style':14s} {'n':>3s} {'human':>6s} {'student':>8s} {'r_stu':>6s} {'r_tea':>6s}")
for st, g in df.groupby("style"):
    print(f"{st:14s} {len(g):3d} {g[H].mean():6.2f} {g[S].mean():8.2f} "
          f"{pearsonr(g[S], g[H])[0]:6.3f} {pearsonr(g[T], g[H])[0]:6.3f}")

c = seen.copy()
for col in (H, S, T):
    c[col] = c[col] - c.groupby("style")[col].transform("mean")
print(f"\nwithin-style r on seen_728 (style means removed): student {pearsonr(c[S], c[H])[0]:.3f}, "
      f"teacher {pearsonr(c[T], c[H])[0]:.3f}")
