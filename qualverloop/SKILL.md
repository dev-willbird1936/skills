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

## Rules
- Review-only request: stop after Rate.
- Report only inspection or verification that happened.
- A score never replaces required checks, stricter category gates or independent review.
- Improve within authorized scope only; keep what works; no unrelated changes.

## Modes
- **Default:** review against purpose, audience and relevant quality criteria.
- **-Image (ImgVerLoop):** view the image itself; check brief fidelity, composition, legibility, artifacts, output properties, anything else relevant.
- **-Video (VidVerLoop):** watch natively if the model can, else `$watch`; check scene boundaries, continuity, motion, pacing, captions, audio, media properties, anything else relevant. Production changes follow the video policy.

## Loop
1. **Review:** what must the target achieve; judge current quality on the criteria that matter here (e.g. clarity, accuracy, usefulness, completeness, usability, craftsmanship).
2. **Rate:** each relevant dimension and overall **0.0–10.0**, with concrete reasons, strengths, weaknesses; judge what exists, not plans.
3. **Improve:** fix the highest-impact weaknesses.
4. **Repeat:** from 1 until threshold: caller's or workflow's, else overall **>7.5/10**, target **>8.0/10**. Blocked: explain why; never inflate scores or rerun unchanged work.

## Report
Initial and final ratings, key improvements, remaining weaknesses or blockers, result or its location.
