#!/usr/bin/env python3
"""Score any automatic metric against the StyleJudge human-rating benchmark.

Usage:
    python score_metric.py predictions.csv [--score_col score] [--higher_is_better]

`predictions.csv` needs a `row_id` column (matching manifest.csv) and one numeric
score column (default name: `score`). Reports Pearson r and Spearman rho with a
bootstrap 95% CI on:
    * the 728-pair seen-style benchmark (in_benchmark_728 == True)
    * the 150 unseen-style rows (Acrylic, Pop Art)
    * all 878 rated rows

The sign of your metric is used as given. If your metric is a loss (lower = better),
negate it first, or pass --negate, so that a better stylization gets a higher score.
"""
import argparse, os
import numpy as np, pandas as pd
from scipy.stats import pearsonr, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))


def corr_ci(x, y, n_boot=2000, seed=0):
    rng = np.random.default_rng(seed)
    r = pearsonr(x, y)[0]
    rho = spearmanr(x, y)[0]
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    rs = [pearsonr(x[i], y[i])[0] for i in idx if x[i].std() > 0 and y[i].std() > 0]
    lo, hi = np.percentile(rs, [2.5, 97.5])
    return r, rho, lo, hi


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("predictions")
    ap.add_argument("--score_col", default="score")
    ap.add_argument("--negate", action="store_true", help="negate the metric (use for losses)")
    ap.add_argument("--manifest", default=os.path.join(HERE, "manifest.csv"))
    a = ap.parse_args()

    man = pd.read_csv(a.manifest)
    pred = pd.read_csv(a.predictions)
    if "row_id" not in pred or a.score_col not in pred:
        raise SystemExit(f"predictions must contain `row_id` and `{a.score_col}`")
    if pred.row_id.duplicated().any():
        raise SystemExit("duplicate row_id values in predictions")
    unknown = set(pred.row_id) - set(man.row_id)
    if unknown:
        raise SystemExit(f"{len(unknown)} row_id values not in manifest (e.g. {sorted(unknown)[:3]})")
    df = man.merge(pred[["row_id", a.score_col]], on="row_id", how="left")
    df["s"] = pd.to_numeric(df[a.score_col], errors="coerce") * (-1 if a.negate else 1)

    subsets = {
        "benchmark_728 (seen styles)": df[df.in_benchmark_728],
        "unseen_150 (acrylic, pop_art)": df[~df.in_benchmark_728],
        "all_878": df,
    }
    print(f"{'subset':32s} {'n':>5s} {'pearson':>8s} {'spearman':>9s}  95% CI (pearson, bootstrap)")
    for name, d in subsets.items():
        miss = d.s.isna().sum()
        d = d.dropna(subset=["s"])
        if len(d) < 10:
            print(f"{name:32s} {len(d):5d}  (too few predictions; {miss} missing)")
            continue
        r, rho, lo, hi = corr_ci(d.s.to_numpy(float), d.human_score.to_numpy(float))
        note = f"  [{miss} missing]" if miss else ""
        print(f"{name:32s} {len(d):5d} {r:8.3f} {rho:9.3f}  [{lo:.3f}, {hi:.3f}]{note}")


if __name__ == "__main__":
    main()
