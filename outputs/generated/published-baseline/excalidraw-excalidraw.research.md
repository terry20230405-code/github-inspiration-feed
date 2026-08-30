# excalidraw/excalidraw research notes

Research date: 2026-08-30
Repository: https://github.com/excalidraw/excalidraw
Research mode: refresh

## Snapshot

- Repository ID: 231283452
- Default branch: master
- README SHA: 48b9d1de9fbb1c74406407e89e2471a01b1f28de
- Latest release: v0.18.1
- Repository state: active
- Fetched at: 2026-08-27T11:05:43Z

## Sources

- [S1] Repository metadata evidence bundle — outputs/generated/research-refresh/excalidraw.source.json — generated 2026-08-30
- [S2] Official README — https://github.com/excalidraw/excalidraw/blob/master/README.md — accessed 2026-08-30
- [S3] Official release v0.18.1 — https://github.com/excalidraw/excalidraw/releases/tag/v0.18.1 — accessed 2026-08-30
- [S4] Official package manifest — https://github.com/excalidraw/excalidraw/blob/master/package.json — accessed 2026-08-30
- [S5] Official editor source — https://github.com/excalidraw/excalidraw/blob/master/packages/excalidraw/components/App.tsx — accessed 2026-08-30

## Verified repository facts

- [F1] Excalidraw is an open-source virtual whiteboard with a hand-drawn style and an infinite canvas. Sources: S1, S2
- [F2] The editor supports shapes, arrows, free drawing, text, images, shape libraries, and exports to PNG, SVG, clipboard, and an open JSON scene format. Sources: S2
- [F3] Excalidraw.com supports real-time collaboration, end-to-end encryption, local-first autosave, and shareable links. Sources: S2
- [F4] The project uses React and TypeScript and renders its interactive scene through an HTML canvas. Sources: S4, S5
- [F5] At fetch time GitHub reported repository ID 231283452, 130,621 stars, 15,022 forks, active state, a latest push at 2026-08-27T01:44:31Z, and the MIT license. Sources: S1
- [F6] Release v0.18.1 is a security patch and does not replace the whiteboard product model. Sources: S3

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 231283452 | F5 | verified |
| `repository.fullName` | excalidraw/excalidraw | F1 | verified |
| `repository.name` | Excalidraw | F1 | verified |
| `repository.stars` | 130621 at fetch time | F5 | verified |
| `repository.forks` | 15022 at fetch time | F5 | verified |
| `repository.language` | TypeScript | F4, F5 | verified |
| `repository.pushedAt` | 2026-08-27T01:44:31Z | F5 | verified |
| `repository.license` | MIT | F5 | verified |
| `repository.state` | active | F5 | verified |
| `editorial.hook` | Hand-drawn interaction makes complex ideas easier to explain | F1, F2, I1 | inferred |
| `editorial.summary` | Infinite canvas, drawing elements, images, libraries, collaboration, links, and export | F1, F2, F3 | verified |
| `editorial.meaning` | Existing canvas, scene, export, and collaboration capabilities can support focused tools | F1, F2, F3, I1 | inferred |
| `editorial.audience` | Teams, teachers, and developers who need to express ideas quickly | F1, F2, F3, I2 | inferred |
| `editorial.features` | Infinite canvas, hand-drawn elements, real-time collaboration, export | F1, F2, F3 | verified |
| `editorial.stack` | React, TypeScript, Canvas | F4 | verified |
| `editorial.opportunity` | Structured templates can narrow the open canvas for specific workflows | F1, F2, I1 | inferred |

## Product inferences

- [I1] Because the canvas and scene mechanics already exist, a derivative product can focus on structured inputs, templates, and a narrower editing flow rather than rebuilding drawing technology. Basis: F1, F2, F3. Confidence: high
- [I2] Teachers, teams, and developers are plausible users of a collaborative diagramming component, but the repository does not publish a formal audience segmentation. Basis: F1, F2, F3. Confidence: medium

## Direction rationale

### D1 — 故事地图生成器

- Reused capability: cards, connectors, text, images, and scene export. Evidence: F2
- User, input, workflow, outcome: writers add characters, places, and events, connect them, and export a story relationship map.
- Substantive difference: a structured story workspace replaces the blank general-purpose canvas.

### D2 — 一页课件白板

- Reused capability: canvas composition, sharing, and visual export. Evidence: F1, F2, F3
- User, input, workflow, outcome: teachers arrange one concept in a lesson template, reveal elements in order, and present or share the page.
- Substantive difference: the product is organized around classroom explanation, not open drawing.

### D3 — 灵感随手画

- Reused capability: notes, arrows, images, and local-first canvas behavior. Evidence: F2, F3
- User, input, workflow, outcome: mobile users place a note, arrow, or photo with a reduced toolbar and save a quick visual thought.
- Substantive difference: single-hand capture and a deliberately reduced toolset change the workflow.

## Uncertainty

- Stars, forks, and push time are a snapshot from 2026-08-27T11:05:43Z, not live counters.
- The current page says “便签”; the README verifies text, shapes, and libraries, while this familiar term is an editorial grouping rather than a named core primitive.
- The extension directions are proposals and are not documented Excalidraw features.

## Localization decisions

- “Infinite canvas-based whiteboard” is expressed as “无限画布”.
- Canvas remains named in the stack because it explains the browser drawing surface without requiring low-level rendering knowledge.

## Refresh notes

- Stage-nine backfill created the missing source baseline and semantic review for Excalidraw.
- The review found no page-impacting change and did not authorize publication.
