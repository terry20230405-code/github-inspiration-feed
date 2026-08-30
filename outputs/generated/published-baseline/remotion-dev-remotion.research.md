# remotion-dev/remotion research notes

Research date: 2026-08-30
Repository: https://github.com/remotion-dev/remotion
Research mode: refresh

## Snapshot

- Repository ID: 274495425
- Default branch: main
- README SHA: 3eb05612d3c1322dcdf7e84cf75195a1d334e06c
- Latest release: v4.0.518
- Repository state: active
- Fetched at: 2026-08-27T11:05:43Z

## Sources

- [S1] Repository metadata evidence bundle — outputs/generated/research-refresh/remotion.source.json — generated 2026-08-27
- [S2] Official README — https://github.com/remotion-dev/remotion/blob/main/README.md — accessed 2026-08-27
- [S3] Official release v4.0.518 — https://github.com/remotion-dev/remotion/releases/tag/v4.0.518 — accessed 2026-08-27
- [S4] Official package manifest — https://github.com/remotion-dev/remotion/blob/main/package.json — accessed 2026-08-30
- [S5] Official renderer source — https://github.com/remotion-dev/remotion/blob/main/packages/renderer/src/render-media.ts — accessed 2026-08-30

## Verified repository facts

- [F1] The canonical repository is remotion-dev/remotion and the project describes itself as a framework for creating videos programmatically with React. Sources: S1, S2
- [F2] React code is the source of truth; users can connect data and use code to manage video composition. Sources: S2
- [F3] The README documents batch rendering on the user's own infrastructure and links server-side and client-side rendering paths. Sources: S2
- [F4] The repository is primarily TypeScript, uses React, and the renderer contains FFmpeg integration. Sources: S1, S4, S5
- [F5] At fetch time GitHub reported repository ID 274495425, 57,479 stars, 4,346 forks, active state, a latest push at 2026-08-27T11:04:01Z, and the Remotion License. Sources: S1
- [F6] The current release adds capabilities but does not remove the code-driven React video and rendering model used by the page. Sources: S2, S3

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 274495425 | F5 | verified |
| `repository.fullName` | remotion-dev/remotion | F1 | verified |
| `repository.name` | Remotion | F1 | verified |
| `repository.stars` | 57479 at fetch time | F5 | verified |
| `repository.forks` | 4346 at fetch time | F5 | verified |
| `repository.language` | TypeScript | F4, F5 | verified |
| `repository.pushedAt` | 2026-08-27T11:04:01Z | F5 | verified |
| `repository.license` | Remotion License | F5 | verified |
| `repository.state` | active | F5 | verified |
| `editorial.hook` | Video can be written like a web experience | F1, F2, I1 | inferred |
| `editorial.summary` | React components and code control video composition; templates can use data and render repeatedly | F1, F2, F3 | verified |
| `editorial.meaning` | Repeatable editing can become reusable automated products | F2, F3, I1 | inferred |
| `editorial.audience` | Developers and content teams needing repeatable or batch video generation | F2, F3, I2 | inferred |
| `editorial.features` | React video composition, precise code-controlled animation, server batch rendering | F1, F2, F3 | verified |
| `editorial.stack` | React, TypeScript, FFmpeg | F4 | verified |
| `editorial.opportunity` | Templates and focused interfaces can hide code for repeated content workflows | F2, F3, I1 | inferred |

## Product inferences

- [I1] A form or focused workflow can sit above Remotion templates so a non-programmer supplies content while the system reuses the same composition and rendering logic. Basis: F2, F3. Confidence: high
- [I2] Developers and content teams with many similar outputs are a plausible core audience because the official positioning emphasizes data connection, code reuse, and batch rendering. Basis: F2, F3. Confidence: medium

## Direction rationale

### D1 — 中文短视频工厂

- Reused capability: data-driven React templates and batch rendering. Evidence: F2, F3
- User, input, workflow, outcome: creators enter scripts, colors, and voice settings; the product applies vertical templates and produces captioned MP4 files.
- Substantive difference: a Chinese form-based content desk replaces direct framework programming.

### D2 — 文章转知识卡片视频

- Reused capability: reusable compositions and programmatic animation. Evidence: F1, F2
- User, input, workflow, outcome: educators paste an article, confirm a card outline, choose motion, and export a shareable knowledge video.
- Substantive difference: the workflow is constrained to explaining long-form knowledge rather than general video production.

### D3 — 商品视频生成器

- Reused capability: structured data input, reusable templates, and repeated rendering. Evidence: F2, F3
- User, input, workflow, outcome: sellers provide product images, price, and selling points; the product applies a promotion rhythm and exports a product video.
- Substantive difference: product fields and SKU repetition become the interface and workflow.

## Uncertainty

- Stars, forks, and push time are a snapshot from 2026-08-27T11:05:43Z, not live counters.
- “Per-frame” wording is an editorial explanation of code-controlled video composition, not a quoted README sentence.
- The three extension directions are product proposals, not existing Remotion features.

## Localization decisions

- “Programmatic video” is explained as “用代码精确控制视频” instead of using a more obscure literal translation.
- React and FFmpeg remain named because they help readers understand the reusable frontend composition and rendering layers.

## Refresh notes

- Stage-nine backfill records the current published copy without changing it.
- The stage-seven semantic review recommended keeping the published copy; publication was not authorized by that review.
