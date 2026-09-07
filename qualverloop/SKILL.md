---
name: qualverloop
description: Review the quality of something, rate it, improve it, and repeat. Supports -Image and -Video inspection modes. Run only when explicitly requested or required by a specialist workflow; preserve review-only scope.
---

# QualVerLoop

```text
$qualverloop <target>
$qualverloop -Image <image or project>
$qualverloop -Video <video or project>
```

## Modes

- **Default:** review anything against its purpose, intended audience, and relevant quality criteria.
- **-Image (ImgVerLoop):** view the actual image; check brief fidelity, composition, legibility, artifacts, and output properties or whatever else is relevant to the actual quality being measured.
- **-Video (VidVerLoop):** check for native video watching capability wihtin the current model, if not, use `$watch`; check scene boundaries, continuity, motion, pacing, captions, audio, and media properties or whatever else is relevant to the actual quality being measured. Follow the video policy for production changes.

## Loop

1. **Review:** understand what the target is meant to achieve. Examine its current quality using suitable criteria, such as clarity, accuracy, usefulness, completeness, usability, or craftsmanship. Choose only what matters to this target.
2. **Rate:** score relevant dimensions and overall quality **0.0–10.0**. Give concrete reasons, strengths, and weaknesses; judge what exists, not planned improvements.
3. **Improve:** address the weaknesses with the greatest impact on quality, within authorized scope. Preserve what already works; avoid unrelated changes.
4. **Repeat:** review the improved result, rate it again, and make further improvements until the requested quality is reached. Use caller/workflow thresholds; otherwise require overall **>7.5/10**, targeting **>8.0/10**. Preserve required checks, stricter category gates, and independent review; a score does not replace them.

For review-only requests, stop after rating. If meaningful improvement is blocked, explain why rather than inflating scores or repeating unchanged work. Do not claim inspection or verification that did not happen.

Return the initial and final ratings, key improvements, remaining weaknesses or blockers, and the result or its location when applicable.
