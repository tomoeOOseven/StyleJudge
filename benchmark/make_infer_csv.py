#!/usr/bin/env python3
"""Convert manifest.csv into the CSV format expected by inference/infer_batch.py.

    python make_infer_csv.py --image_root /path/to/images --out infer_input.csv [--subset 728|unseen|all]

Manifest paths start with `input_dataset/`, the directory containing the actual benchmark images.
`--image_root` is the parent directory that contains that folder. See the README in this folder.
"""
import argparse, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--image_root", required=True)
ap.add_argument("--out", default="infer_input.csv")
ap.add_argument("--subset", choices=["728", "unseen", "all"], default="728")
ap.add_argument("--manifest", default=os.path.join(HERE, "manifest.csv"))
a = ap.parse_args()

m = pd.read_csv(a.manifest)
if a.subset == "728":
    m = m[m.in_benchmark_728]
elif a.subset == "unseen":
    m = m[~m.in_benchmark_728]
j = lambda c: m[c].map(lambda p: os.path.join(a.image_root, p))
out = pd.DataFrame({
    "row_id": m.row_id, "style": m["style"],
    "ex_a_src_path": j("exemplar_a_source"), "ex_a_dst_path": j("exemplar_a_target"),
    "ex_b_src_path": j("exemplar_b_source"), "ex_b_dst_path": j("exemplar_b_target"),
    "q_src_path": j("query_source"), "q_res_path": j("query_result"),
    "final_score": m.human_score,
})
out.to_csv(a.out, index=False)
print(f"wrote {len(out)} rows to {a.out}")
