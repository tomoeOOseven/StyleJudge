# Human study results

## Composition

| Set | Rows | Styles |
|---|---:|---|
| Benchmark (seen styles) | 728 | 10: pencil, expressive, cubist, mosaic, impressionist, charcoal, minimalist, abstract, gouache, watercolor |
| Unseen styles | 150 | Acrylic (75), Pop Art (75) |
| **All released ratings** | **878** | 12 |

882 ratings were collected and 4 empty rows were dropped. The 728 benchmark rows are the 750 scored seen-style
items minus 22 that failed at generation time and were excluded; all models are compared on the same 728.

Human score statistics, benchmark rows (computed from `benchmark/human_ratings.csv`):

Per style:

| Style | n | Mean score | SD |
|---|---:|---:|---:|
| pencil | 76 | 4.76 | 2.52 |
| expressive | 75 | 5.61 | 2.33 |
| mosaic | 74 | 5.15 | 2.36 |
| charcoal | 74 | 4.82 | 2.24 |
| impressionist | 74 | 5.08 | 2.36 |
| cubist | 74 | 5.27 | 2.63 |
| minimalist | 73 | 6.41 | 2.55 |
| abstract | 70 | 5.24 | 2.29 |
| gouache | 70 | 6.06 | 2.44 |
| watercolor | 68 | 5.47 | 2.37 |

Per rater:

| Rater | n | Mean score | SD |
|---|---:|---:|---:|
| R-A | 232 | 6.44 | 2.13 |
| R-J | 419 | 5.14 | 2.31 |
| R-S | 77 | 3.52 | 2.63 |

Raters differ noticeably in their score scale (R-S rates much lower on average), and each row was rated by one
person, so rater effects are not averaged out.

## Correlation with human ratings (reported in the paper)

Pearson r / Spearman ρ on the 728-pair benchmark:

| Metric | Pearson r | Spearman ρ |
|---|---:|---:|
| Gram-matrix style loss (negated, see below) | −0.404 | −0.394 |
| LPIPS | 0.041 | 0.049 |
| CLIP-Score | 0.168 | 0.178 |
| StyleJudge (SFT, 0.8B student) | 0.291 | 0.325 |
| StyleJudge (teacher, 72B) | 0.327 | 0.337 |

Bootstrap 95% confidence intervals (N = 728): student r ∈ [0.229, 0.354]; teacher r ∈ [0.265, 0.390];
difference (student − teacher) ∈ [−0.108, 0.032], so no significant difference is detected.

Per-rater student correlation (benchmark rows): R-J 0.333 (n=419), R-A 0.125 (n=232), R-S 0.109 (n=77),
positive for all three but modest.

**Unseen styles (Acrylic, Pop Art; 150 rows, exemplars and style markers still given).** Student r = 0.381
(95% CI [0.24, 0.51]), teacher r = 0.408. On all 878 rows: student 0.297, teacher 0.341. Query and training
pairs are disjoint.

### Gram-matrix convention

The Gram baseline is the VGG16 Gram-matrix distance between the query result and the exemplar target. It is
negated before 1–10 scaling, so a closer style match gets a higher score, which is the direction in which a
metric should rise with human ratings. It correlates at r = −0.404 (the raw loss correlates at +0.404), so on this
benchmark Gram loss is not a good metric for the task. Gram statistics measure feature divergence without
penalising semantic corruption, so this should not be read as a general claim about Gram loss.

### Human agreement

Inter-rater agreement r = 0.25 comes from the separate 2-rater pilot (n = 50 paired items; p = 0.08; Fisher 95%
CI [−0.03, 0.49], which includes zero). It is not a ceiling and not a same-set comparison, because the 728
benchmark rows are single-rated. We do not claim human parity. (The p = 0.18 in the pilot table belongs to the
zero-shot VLM-vs-human correlation, r = 0.19.)

### Zero-shot pilot

88 source-stylized pairs scored by Qwen2.5-VL-7B (ImgEdit-Judge weights); 50 had valid paired annotations from
two raters. VLM mean 5.86 ± 1.66, human mean 6.62 ± 1.95; Pearson r = 0.19 (p = 0.18), Spearman ρ = 0.11
(p = 0.46); the VLM under-estimated in 62% of cases (31/50). The pilot used two raters, one of whom also rated
the main benchmark.

## Reproducing

Score any metric on the same pairs with
[`benchmark/score_metric.py`](../benchmark/score_metric.py).
