# Human-rated benchmark

878 human ratings of source→stylized query pairs, with the image paths needed to re-score them with any
automatic metric. 728 rows form the seen-style benchmark used for the paper's correlation analysis;
the other 150 are unseen-style rows (Acrylic, Pop Art).

## Files

| File | Description |
|---|---|
| `human_ratings.csv` | Raw ratings: `Row_ID, Row_Index, Style, Username, Score, Reasoning, Timestamp`. `Username` is a rater code (`R-J`, `R-A`, `R-S`). |
| `manifest.csv` | One row per `Row_ID`: style, split, benchmark flag, rater, human score, query pair id and frame, and image paths |
| `score_metric.py` | Scores your metric against the human ratings (Pearson, Spearman, bootstrap CI) |
| `make_infer_csv.py` | Converts the manifest into the CSV format used by `inference/infer_batch.py` |
| `stylejudge_predictions.csv` | Student and teacher S_final scores for all 878 benchmark rows |
| `reproduce_paper_numbers.py` | Reproduces the paper's correlation, per-rater, per-style and score-distribution numbers |

## Manifest columns

| Column | Meaning |
|---|---|
| `row_id` | UUID; joins to `Row_ID` in `human_ratings.csv` |
| `style` | Target style |
| `split` | `seen_10` (10 styles seen in training/validation) or `unseen_2` (Acrylic, Pop Art) |
| `in_benchmark_728` | `True` for the 728 seen-style benchmark rows |
| `rater` | Rater code |
| `human_score` | Rating, 1–10 (same as `Score`) |
| `query_pair_id`, `query_result_frame` | Pair folder number and morph-frame number (1 = source, 10 = fully stylized) of the query result |
| `query_source`, `query_result` | Query pair image paths |
| `exemplar_a_source`, `exemplar_a_target`, `exemplar_b_source`, `exemplar_b_target` | The two exemplar pairs shown to the rater |

All paths start with `input_dataset/` (for example `input_dataset/extracted-strips-part-2/pop_art/79/1.png`).
This is the directory containing the actual benchmark images, not a placeholder: each manifest path resolves to
an image file beneath it. Pass the parent directory of `input_dataset/` as `--image_root` to `make_infer_csv.py`.
The image datasets are linked from the main README; images are not stored in this repository.

## Scoring a metric

```bash
# predictions.csv: columns row_id, score  (higher = better stylization; use --negate for losses)
python score_metric.py predictions.csv
```

The script reports Pearson r and Spearman ρ with a bootstrap 95% CI on the 728 benchmark rows, the 150
unseen-style rows, and all 878 rows.

```bash
python score_metric.py stylejudge_predictions.csv --score_col student_final_score
python reproduce_paper_numbers.py
```

Items were sampled with roughly uniform teacher scores (100 per score level 1-9; 78 at level 6 after 22 items
were dropped before rating because the untuned model returned no score). Query results come from graded morph
strips (643) and from three further generation batches, including deliberately degraded outputs (235); the source
folder of each query is visible in its path.

## Annotation protocol

See [`docs/annotation_protocol.md`](../docs/annotation_protocol.md) for the rater methodology, briefing,
verbatim guideline and interface. Licensed CC BY 4.0 (see the main README).
