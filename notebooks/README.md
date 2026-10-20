# Notebooks

Kaggle notebooks used to build the dataset and train StyleJudge. Paths inside refer to Kaggle input datasets;
see the main README for the dataset links.

| Notebook | Purpose |
|---|---|
| `01_sample_source_images.ipynb` | Sample and combine source images from the collections |
| `02_standardize_images.ipynb` | Keep square images and standardize to 1024×1024 (Lanczos) |
| `03_stylize_and_morph.ipynb` | FLUX.1-dev Kontext stylization with 12 style LoRAs, then FreeMorph-SDXL 8-frame morphing |
| `04a_teacher_rationales_batch1.ipynb` | Qwen2.5-VL-72B (AWQ, vLLM) structured rationales, batch 1 |
| `04b_teacher_rationales_batch2.ipynb` | Teacher rationales, batch 2 (checkpointed, resumable) |
| `05_sft_train.ipynb` | LoRA SFT of Qwen3.5-0.8B with the score-weighted loss (Unsloth) |
| `06_base_vs_adapter.ipynb` | Untuned base vs. SFT adapter on the unseen-style test set |
| `teacher_system_prompt.txt` | Teacher system prompt |
| `future_work/grpo.ipynb` | Exploratory GRPO fine-tuning; not part of the reported results |

Run order is the numeric prefix. FreeMorph-SDXL is described in [`../docs/freemorph_sdxl.md`](../docs/freemorph_sdxl.md).
