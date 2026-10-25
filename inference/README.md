# StyleJudge inference

Inference code for the **Qwen3.5-0.8B + LoRA** StyleJudge student (teacher: Qwen2.5-VL-72B).
Given two exemplar source→stylized pairs and a query pair, the model returns Style Fidelity (SF),
Content Preservation (CP), Rendering Quality (RQ) and the composite score `S_final` (Eq. 1 of the paper).

On a single NVIDIA T4, StyleJudge scores a pair in 39 s (median over 900 pairs: the 878 rated pairs plus 22 unrated
ones) with 2.5 GB of peak GPU memory.

## Weights

The LoRA adapter is hosted on Hugging Face (not stored in this repo):
[GamerQuant/Qwen3.5_0.8b_10kbalanced_k2_lora16](https://huggingface.co/GamerQuant/Qwen3.5_0.8b_10kbalanced_k2_lora16)
(LoRA r=16, alpha=32, K=2 exemplar pairs). `src/model.py` downloads and loads it automatically.

## Setup

```bash
# from the repository root
cd inference
pip install -r requirements.txt
```

## Single evaluation

```bash
python infer_single.py \
    --style "acrylic" \
    --ex_a_src path/to/ex1_src.png --ex_a_dst path/to/ex1_dst.png \
    --ex_b_src path/to/ex2_src.png --ex_b_dst path/to/ex2_dst.png \
    --q_src path/to/query_src.png  --q_res path/to/query_result.png
```

## Batch evaluation (e.g. the released human-rated benchmark)

```bash
# 1. build an input CSV from the benchmark manifest (needs the image folders, see benchmark/README.md)
python ../benchmark/make_infer_csv.py --image_root /path/to/images --out infer_input.csv --subset 728

# 2. run the student
python infer_batch.py --csv_path infer_input.csv --output_path predictions.csv

# 3. score against the human ratings (pass pred_final_score as the metric)
python - <<'PY'
import pandas as pd
p = pd.read_csv("predictions.csv")
p[["row_id", "pred_final_score"]].rename(columns={"pred_final_score": "score"}).to_csv("scores.csv", index=False)
PY
python ../benchmark/score_metric.py scores.csv
```

Rows with unparseable model output are marked `parse_failed=True` and have a blank predicted score; the scoring
script ignores those missing scores.

The input CSV needs: `style`, `ex_a_src_path`, `ex_a_dst_path`, `ex_b_src_path`, `ex_b_dst_path`,
`q_src_path`, `q_res_path`, and optionally `final_score` (ground truth) and `row_id`.

## Layout

- `src/config.py` – system prompt, style-marker mapping, model parameters
- `src/model.py` – Unsloth model + adapter loading
- `src/prompt.py` – builds the multi-image style-marker prompt
- `src/evaluate.py` – generation and extraction of scores from the XML output
