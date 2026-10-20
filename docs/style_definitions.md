# Style definitions

The twelve styles and their three-marker definitions. These are the definitions raters were shown before
annotation (see [`annotation_protocol.md`](annotation_protocol.md)), and the same text is used as the
`STYLE MARKERS` line of the model prompt in both training and test. The markers were produced with web search and an LLM.

| Style | Markers |
|---|---|
| abstract | non-representational geometric forms, bold flat primary color blocks, and elimination of figurative elements. |
| acrylic | thick impasto surface texture, sharp-edged opaque brushwork, and high-saturation vivid colors. |
| charcoal | monochromatic grey tonal gradients, smudged dusty texture marks, and visible hatching lines. |
| cubist | simultaneous multiple-viewpoint planes, fractured interlocking geometric facets, and a muted palette. |
| expressive | raw emotionally distorted brushwork, unblended aggressive color strokes, and angular forms. |
| gouache | opaque chalky flat color areas, matte non-reflective finish, and clean sharp color edges. |
| impressionist | short broken dappled brushstrokes, chromatic color juxtaposition without blending, and soft atmospheric hazy edges. |
| minimalist | extreme negative white-space areas, a single dominant restrained color, and reductive simplified forms. |
| mosaic | discrete tile fragments with visible grout lines, angular hard-edge color segmentation, and tesserae patterns. |
| pencil | parallel graphite hatching lines, linear tonal gradation from light to dark, and visible paper grain texture. |
| pop_art | flat bold primary poster colors, Ben-Day halftone dot patterns, and thick black outline contour lines. |
| watercolor | transparent layered wash glazes, soft wet-edge bloom blending, and paper granulation in wash areas. |

Acrylic and Pop Art are held out entirely from training and used only as unseen test styles.
The inference code stores the same markers as three-part tuples in
[`inference/src/config.py`](../inference/src/config.py).
