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

print("\n== Score counts (all 878 pairs; levels 1..10)")
for name, col in [("human", H), ("student", S), ("teacher", T)]:
    counts = df[col].value_counts().reindex(range(1, 11), fill_value=0).astype(int)
    print(f"{name:8s}" + "".join(f" {counts[score]:3d}" for score in range(1, 11)))

baseline_path = os.path.join(HERE, "baseline_metric_scores.csv")
zeroshot_path = os.path.join(HERE, "base_zeroshot_predictions.csv")
if os.path.exists(baseline_path) and os.path.exists(zeroshot_path):
    print("\n== Traditional metrics and untuned base (seen_728; missing scores skipped)")
    baseline = pd.read_csv(baseline_path)
    zeroshot = pd.read_csv(zeroshot_path)
    seen_ids = seen[["row_id", H]]
    evaluations = [
        ("Gram (negated, scaled)", baseline, "gram_negated_scaled"),
        ("LPIPS (negated, scaled)", baseline, "lpips_negated_scaled"),
        ("CLIP image similarity", baseline, "clip_scaled"),
        ("Untuned base (zero-shot)", zeroshot, "score"),
    ]
    for name, scores, score_col in evaluations:
        scored = seen_ids.merge(scores[["row_id", score_col]], on="row_id", how="left", validate="one_to_one")
        scored[score_col] = pd.to_numeric(scored[score_col], errors="coerce")
        scored = scored.dropna(subset=[score_col, H])
        r = pearsonr(scored[score_col], scored[H])[0]
        rho = spearmanr(scored[score_col], scored[H])[0]
        print(f"{name:26s} n={len(scored):3d} r={r:.3f} rho={rho:.3f}")
