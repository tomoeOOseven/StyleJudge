# Stylized Image Dataset Generation using FLUX.1-dev Kontext

[![Model](https://img.shields.io/badge/Model-FLUX.1--dev_Kontext-orange.svg)](https://huggingface.co/collections/fal/kontext-dev-loras)

This repository outlines the methodology, base content collection, and generation pipeline for creating our stylized image dataset. We leverage the FLUX.1-dev Kontext diffusion model paired with specialized LoRA adapters to perform high-quality style transfer across multiple visual domains.

---

## 1. Dataset Description

### Base Content Collection
Source images were aggregated from seven complementary collections to ensure broad content diversity (links in [`dataset_sources.md`](dataset_sources.md)).

| Source | Size / Attributes | Rationale |
| :--- | :--- | :--- |
| **HQ-50K** | 50,000 images, avg. 2.5M px, high texture frequency. | Balanced semantic coverage across indoor, outdoor, and artificial visual domains with strong texture detail. |
| **LAION-2B (squarish 1024px)** | Large-scale general pool. | General-purpose 1024×1024 content. |
| **OmniConsistency** | 3D, Chibi, Illustration classes. | Ensures the evaluator handles non-photorealistic starting domains. |
| **Pexels** | High-res macro photography. | Fills domain gaps: macro subjects, botanical close-ups. |
| **iNaturalist** | Fish, birds, insects. | Macro subjects used to handle class imbalance. |
| **LHQ-1024** | 90K images, 1024² res. | Natural and urban landscapes with diverse atmospheric and spatial variation. |
| **Unsplash** | Landscape photography. | Landscape scenes and atmospheric variation. |

**Source Dataset Distribution** *Share of the curated pool contributed by each source collection (HQ-50K 47.4%, OmniConsistency 27.0%, others 25.5%).* ![Dataset Distribution](../assets/figures/dataset_source_distribution.png)

---

## 2. Dataset Generation Pipeline

### Stylized Target Generation via LoRA Adapters
Stylized target images were generated using the **FLUX.1-dev Kontext** diffusion model combined with twelve style-specific LoRA adapters sourced from the [HuggingFace fal/kontext-dev-loras collection](https://huggingface.co/collections/fal/kontext-dev-loras).

### Low-Rank Adaptation (LoRA)
LoRA is a parameter-efficient fine-tuning technique that inserts trainable low-rank matrices into frozen pre-trained layers. For a weight matrix $W_0 \in \mathbb{R}^{d \times k}$, the update is reparameterized as:

$$W = W_0 + \Delta W = W_0 + BA, \quad B \in \mathbb{R}^{d \times r},\; A \in \mathbb{R}^{r \times k},\; r \ll \min(d, k)$$

This allows lightweight style specialization without full retraining and enables rapid adapter swapping during dataset construction.

**LoRA architecture.** Low-rank decomposition matrices $B$ and $A$ are inserted into selected transformer layers. Only the adapter parameters ($\Delta W = BA$) are trained; the base weights $W_0$ remain frozen. For an overview, see [IBM Research's LoRA explanation](https://www.ibm.com/think/topics/lora).

### Style Adapters Used

| # | Adapter Name | Primary Visual Signature |
|:---|:---|:---|
| 1 | `Abstract-Art-Kontext-Dev-LoRA` | Non-representational geometry, flat primary blocks |
| 2 | `Acrylic-Art-Kontext-Dev-LoRA` | Impasto texture, opaque brushwork, saturated color |
| 3 | `Charcoal-Art-Kontext-Dev-LoRA` | Monochromatic gradients, smudged dusty hatching |
| 4 | `Cubist-Art-Kontext-Dev-LoRA` | Multi-viewpoint facets, muted ochre–brown palette |
| 5 | `Expressive-Art-Kontext-Dev-LoRA` | Raw distorted brushwork, unblended aggressive strokes |
| 6 | `Gouache-Art-Kontext-Dev-LoRA` | Opaque chalky flats, matte finish, sharp color edges |
| 7 | `Impressionist-Art-Kontext-Dev-LoRA`| Broken dappled strokes, chromatic juxtaposition |
| 8 | `Minimalist-Art-Kontext-Dev-LoRA` | Extreme negative space, single restrained color |
| 9 | `Mosaic-Art-Kontext-Dev-LoRA` | Discrete tile fragments, visible grout lines |
| 10 | `Pencil-Drawing-Kontext-Dev-LoRA` | Graphite hatching, paper grain, tonal gradation |
| 11 | `Pop-Art-Kontext-Dev-LoRA` | Ben-Day halftone dots, thick black outlines |
| 12 | `Watercolor-Art-Kontext-Dev-LoRA` | Transparent wash glazes, wet-edge bloom |

### Style Transfer Examples

Source → stylized pairs for all 12 adapters are shown in Figure 1 of the paper.


# Stylized Image Dataset Generation & Rationales

[![Dataset Link](https://img.shields.io/badge/Dataset-Kaggle-blue.svg)](https://www.kaggle.com/datasets/yatishjuneja/style-rationale-final)
[![Model](https://img.shields.io/badge/Model-FLUX.1--dev_Kontext-orange.svg)](https://huggingface.co/collections/fal/kontext-dev-loras)
[![Rationale Generator](https://img.shields.io/badge/Rationale_Generator-Qwen2.5--VL--72B-purple.svg)](#)

This repository outlines the methodology, base content collection, and generation pipeline for creating our stylized image dataset and accompanying evaluations. We leverage the FLUX.1-dev Kontext diffusion model paired with specialized LoRA adapters to perform high-quality style transfer, and utilize large vision-language models for generating structured reasoning traces.

---

## 1. Choice of Rationale Generator

> **Why Qwen2.5-VL-72B-Instruct?**
>
> We used **Qwen2.5-VL-72B-Instruct** as the sole rationale generator: strong published benchmarks on visual question answering, multimodal reasoning and instruction following, and open availability at this scale, so it can be run locally at the volume the dataset requires without per-call API cost. Its rationales are the supervised targets for the compact Qwen3.5-0.8B student.

---

## 2. Style Rationale Dataset

The generated reasoning traces and scoring metrics evaluating the style transfers are publicly available on Kaggle.

* **Dataset Link:** [Style Rationale Final (Kaggle)](https://www.kaggle.com/datasets/yatishjuneja/style-rationale-final)

### Directory Structure

The dataset comprises multiple CSV files spanning different batches and generation iterations:

```text
style_rationale_remaining/
├── style_rationale_dataset Part1.csv
├── style_rationale_dataset.csv
├── style_rationale_dataset_(110)_v2.csv
└── style_rationale_dataset_(117)_v2.csv
```
# Extracted Morph Strips Dataset (FreeMorph SDXL)

[![Dataset Part 1](https://img.shields.io/badge/Kaggle-Extracted_Strips_Part_1_(10GB)-blue.svg?logo=kaggle)](https://www.kaggle.com/datasets/somanshu7527/extracted-strips-part-1)
[![Dataset Part 2](https://img.shields.io/badge/Kaggle-Extracted_Strips_Part_2_(12GB)-blue.svg?logo=kaggle)](https://www.kaggle.com/datasets/somanshu7527/extracted-strips-part-2)

This dataset contains a large-scale collection of step-by-step image morphing sequences generated using **FreeMorphs SDXL**. It captures the continuous visual transition between a base source image and its fully stylized counterpart across 12 distinct artistic domains.

## 📊 Dataset Overview

Due to the high resolution and volume of the generated images, the collection is split across two Kaggle repositories totaling **22 GB** of data. 

Every single data point represents a complete visual transformation sequence stored in an isolated folder. 

* **Total Images per Sequence:** 10 images per folder.
* **Sequence Composition:** * `Image 1`: The original source image.
    * `Images 2-9`: The intermediate FreeMorph SDXL transitional morphs.
    * `Image 10`: The final stylized target image.

## 📂 Dataset Volumes

The 12 total artistic styles are divided evenly across the two dataset parts.

### [Part 1](https://www.kaggle.com/datasets/somanshu7527/extracted-strips-part-1)
* **Size:** ~10 GB
* **Contents:** Covers the first **6 distinct artistic styles**.
* **Focus:** Core visual styles and their respective morphological transitions.

### [Part 2](https://www.kaggle.com/datasets/somanshu7527/extracted-strips-part-2)
* **Size:** ~12 GB
* **Contents:** Covers the remaining **6 distinct artistic styles**.
* **Focus:** Completes the 12-style collection, maintaining the identical 10-image sequence structure.

## 🗂️ Directory Structure

Inside each dataset part, the files are organized hierarchically by style and then by a unique identifier for the specific image pair. 

```text
extracted-strips-part-*/
├── style_name_1/
│   ├── 001/
│   │   ├── 1.png   <-- (Original Source Image)
│   │   ├── 2.png   <-- (Morph step 1)
│   │   ├── 3.png   <-- (Morph step 2)
│   │   ├── ...
│   │   ├── 9.png   <-- (Morph step 8)
│   │   └── 10.png  <-- (Final Stylized Image)
│   ├── 002/
│   │   ├── 1.png
│   │   └── ...
├── style_name_2/
...
```

For users who prefer to download the full dataset at once or outside of the Kaggle environment, the complete 22 GB collection is mirrored on Google Drive.
[📁 Datasets (Google Drive)](https://drive.google.com/drive/folders/1hzk80mSjpXRNwI5kUuDLyTcYRblOymeB)
