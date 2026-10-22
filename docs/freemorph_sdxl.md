# FreeMorph: SD 2.1 baseline vs. SDXL adaptation

Graded intermediate supervision comes from an image-morphing pipeline adapted from
[FreeMorph](https://arxiv.org/abs/2411.01410). For every source→stylized pair, 8 interpolated frames are
generated between the source (frame 1) and the stylized target (frame 10).

The original SD 2.1 pipeline changes object shape and composition alongside style, which is unsuitable for
measuring style intensity independently of content drift. We re-target it to SDXL with dual text-encoder
conditioning (pooled CLIP-G and CLIP-L embeddings interpolated across frames) and a lower edit strength and
guidance scale, which prioritises semantic consistency over structural transformation.

## Settings

| Setting | SD 2.1 (original) | SDXL (ours) |
|---|---|---|
| Resolution | 768 px | 1024 px |
| Edit strength | 0.8 | 0.6 |
| Classifier-free guidance (CFG) scale | 7.5 | 6.5 |
| Denoising steps | 50 | 50 |
| Frame latents | spherical interpolation (slerp) | spherical interpolation (slerp) |
| Text / pooled embeddings | linear interpolation (lerp) | linear interpolation (lerp), dual encoder (CLIP-G + CLIP-L) |

With `t` the frame position in [0, 1]:

- latents: `z_t = slerp(z_A, z_B; t)`
- text and pooled embeddings: `e_t = (1 − t) · e_A + t · e_B`

The SD 2.1 and SDXL pipelines are compared qualitatively only; no quantitative ablation of the retargeting is reported.

## FreeMorph examples

![SD 2.1 example 1](../assets/figures/freemorph_sd21_ex1.png)
![SDXL-adapted example 1](../assets/figures/freemorph_sdxl_ex1.png)

*SD 2.1 FreeMorph example (top) and SDXL-adapted example (bottom); the rows show different input pairs.*

![SD 2.1 example 2](../assets/figures/freemorph_sd21_ex2.png)
![SDXL-adapted example 2](../assets/figures/freemorph_sdxl_ex2.png)

*SD 2.1 FreeMorph example (top) and SDXL-adapted example (bottom); the rows show different input pairs.*

The SDXL port, a fork of FreeMorph's `freemorph.py`, is available at [FreeMorph_sdxl](https://github.com/Lokesh-102214/FreeMorph_sdxl).
