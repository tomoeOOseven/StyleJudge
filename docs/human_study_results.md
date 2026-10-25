# Human study results

## Composition

| Set | Rows | Styles |
|---|---:|---|
| Benchmark (seen styles) | 728 | 10: pencil, expressive, cubist, mosaic, impressionist, charcoal, minimalist, abstract, gouache, watercolor |
| Unseen styles | 150 | Acrylic (75), Pop Art (75) |
| **All released ratings** | **878** | 12 |

The three raters were project-team members with no formal art training. Each worked alone on a separate part of the
data, so each pair was single-rated. 882 ratings were collected and 4 empty rows were dropped. The 878 released pairs
(728 seen-style, 150 unseen-style) were sampled with roughly uniform teacher scores: 100 per teacher-score level 1-9,
except 78 at level 6, because 22 sampled items at that level were not rated. All models are compared on the same
728 seen-style pairs.

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

Raters differ noticeably in their score scale (R-S rates much lower on average), and each pair was single-rated,
so rater effects are not averaged out.

## Correlation with human ratings (reported in the paper)

Pearson r / Spearman ρ on the 728-pair benchmark:

| Metric | Pearson r | Spearman ρ |
|---|---:|---:|
| Gram-matrix style loss (negated) | 0.041 | 0.049 |
| LPIPS (negated) | −0.404 | −0.394 |
| CLIP image similarity | 0.168 | 0.178 |
| Untuned base (0.8B, zero-shot)* | 0.019 | 0.017 |
| StyleJudge (SFT, 0.8B student) | 0.291 | 0.325 |
| StyleJudge (teacher, 72B) | 0.327 | 0.337 |

\* Scored on the 711 of 728 pairs for which it returned a parseable score.

The untuned base model is uncorrelated with human ratings zero-shot (r = 0.019 on the 711 pairs it scores), so the
gain comes from fine-tuning.

Bootstrap 95% confidence intervals (N = 728): student r ∈ [0.225, 0.351]; teacher r ∈ [0.258, 0.389];
difference (student − teacher) ∈ [−0.112, 0.037], so no significant difference is detected.

Per-rater student correlation (benchmark rows): R-J 0.333 (n=419), R-A 0.124 (n=232), R-S 0.109 (n=77),
positive for all three but modest.

**Unseen styles (Acrylic, Pop Art; 150 rows, exemplars and style markers still given).** Student r = 0.381
(95% CI [0.24, 0.51]), teacher r = 0.408. On all 878 rows: student 0.297, teacher 0.341. Query and training
pairs are disjoint.

### Traditional metrics

Gram: mean squared difference between Gram matrices of ImageNet-pretrained VGG16 features (layers 3, 8, 15, 22)
of the query result and exemplar A's stylized image. LPIPS (VGG) between the query source and its result.
CLIP image similarity: cosine similarity of CLIP ViT-B/32 image embeddings of the query result and exemplar A's
stylized image. Images are resized to 256×256 (Lanczos). Gram and LPIPS are negated; all three are min-max scaled
to 1–10 over the benchmark pairs and rounded.

### Baseline interpretation

LPIPS (source vs. result) is negatively correlated: its distance grows with stylization strength along the morph
strips (Spearman rho = 0.66 with frame index), which raters reward. Gram-matrix loss is essentially uncorrelated
(r = 0.041). An unsigned stylization-strength proxy such as raw LPIPS distance (r = 0.405) is therefore a strong
baseline on this benchmark, because most queries come from graded morph strips.

### Human agreement

Inter-rater agreement r = 0.25 comes from the separate 2-rater pilot (n = 50 paired items; p = 0.08; Fisher 95%
CI [−0.03, 0.49], which includes zero). It is not a ceiling and not a same-set comparison, because the 728
benchmark rows are single-rated. We do not claim human parity. (The p = 0.18 in the pilot table belongs to the
zero-shot VLM-vs-human correlation, r = 0.19.)

### Zero-shot pilot

88 source-stylized pairs scored by Qwen2.5-VL-7B (ImgEdit-Judge weights); 50 had valid paired annotations from
two raters. VLM mean 5.86 ± 1.66, human mean 6.62 ± 1.95; Pearson r = 0.19 (p = 0.18), Spearman ρ = 0.11
(p = 0.46); the VLM under-estimated in 62% of cases (31/50). The separate pilot used two project-team members, one of whom also
rated the main benchmark.

## Reproducing

Score any metric on the same pairs with
[`benchmark/score_metric.py`](../benchmark/score_metric.py).
