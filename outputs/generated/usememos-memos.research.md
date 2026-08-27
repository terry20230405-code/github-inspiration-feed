# usememos/memos research notes

Research date: 2026-08-27
Repository: https://github.com/usememos/memos
Research mode: refresh

## Snapshot

- Repository ID: 436297812
- Default branch: main
- README SHA: 未知（原始研究未记录）
- Latest release: 未知（原始研究未记录）
- Repository state: active
- Fetched at: 2026-08-27T08:53:31Z

## Sources

- [S1] Canonical repository — https://github.com/usememos/memos — accessed 2026-08-23
- [S2] README — https://github.com/usememos/memos/blob/main/README.md — accessed 2026-08-23
- [S3] Repository API metadata — https://api.github.com/repos/usememos/memos — accessed 2026-08-27

## Verified repository facts

- [F1] The official project name is Memos and its canonical repository is usememos/memos. Sources: S1
- [F2] The README describes Memos as an open-source, self-hosted, Markdown-native note-taking app for quick capture. Sources: S2
- [F3] Its documented core experience is a timeline-first interface without folder navigation. Sources: S2
- [F4] The project documents self-hosting without telemetry, deployment as a Go binary or Docker container, and SQLite, MySQL, or PostgreSQL storage. Sources: S2
- [F5] The documented web clipper saves pages, selected text, and images and supports review, visibility selection, and Markdown format customization. Sources: S2
- [F6] The README documents REST and gRPC APIs. Sources: S2
- [F7] At fetch time the GitHub API reported repository ID 436297812, 62,580 stars, 4,700 forks, Go as the primary language, MIT as the license, active state, and a latest push at 2026-08-26T15:43:13Z. Sources: S3

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 436297812 | F7 | verified |
| `repository.fullName` | usememos/memos | F1 | verified |
| `repository.name` | Memos | F1 | verified |
| `repository.stars` | 62580 at fetch time | F7 | verified |
| `repository.forks` | 4700 at fetch time | F7 | verified |
| `repository.language` | Go | F7 | verified |
| `repository.pushedAt` | 2026-08-26T15:43:13Z | F7 | verified |
| `repository.license` | MIT | F7 | verified |
| `repository.state` | active | F7 | verified |
| `editorial.hook` | Turn quick notes into a private personal timeline | F2, F3 | inferred |
| `editorial.summary` | Timeline-first Markdown capture, web clipping, self-hosting, and open APIs | F2, F3, F4, F5, F6 | verified |
| `editorial.meaning` | Fast capture, private storage, and APIs form a reusable base for focused recording products | F2, F3, F4, F6, I1 | inferred |
| `editorial.audience` | People who want quick capture and control of their data | F2, F4, I2 | inferred |
| `editorial.features` | Timeline capture, Markdown and web clipping, self-hosting, REST and gRPC APIs | F2, F3, F4, F5, F6 | verified |
| `editorial.stack` | Go, React, SQLite, Docker | F4, F7 | verified |
| `editorial.opportunity` | New inputs and review workflows can be built on the timeline and APIs | F3, F5, F6, I1 | inferred |

## Product inferences

- [I1] Voice capture, daily resurfacing, and family story presentation are new workflows rather than documented Memos features; they can reuse the timeline, private storage, clipping, and API capabilities. Basis: F3, F4, F5, F6. Confidence: medium
- [I2] The original audience includes people who value quick capture and data control; this is inferred from the product positioning and self-hosted, no-telemetry design. Basis: F2, F4. Confidence: medium

## Direction rationale

### D1 — 灵感语音收件箱

- Reused capability: timeline capture and REST API write path
- Evidence: F3, F6
- New audience and recurring problem: people who have ideas while walking or commuting but cannot type
- Input and visible outcome: spoken thought becomes a searchable text card
- Substantive difference: voice-first capture and confirmation replace the general text interface

### D2 — 创作素材回访器

- Reused capability: notes, web clipping, and timeline storage
- Evidence: F3, F5
- New audience and recurring problem: creators save material but rarely encounter it again
- Input and visible outcome: saved notes and clips become a small daily review queue
- Substantive difference: the product optimizes for resurfacing and reuse rather than open-ended note capture

### D3 — 家庭一句话日记

- Reused capability: private self-hosting and timeline organization
- Evidence: F3, F4
- New audience and recurring problem: family members rarely preserve the story behind everyday photos
- Input and visible outcome: one sentence and one photo per person become a shared weekly timeline
- Substantive difference: the workflow is structured, multi-person, and centered on family memory

## Uncertainty

- Dynamic stars, forks, and push time are a snapshot fetched at 2026-08-27T08:53:31Z and will become stale.
- The research still does not record the README SHA or latest release.
- No Issues-based demand claim was used in this draft.

## Localization decisions

- “Self-hosted” is rendered as “自托管”.
- “Timeline-first” is expressed as “时间线式” rather than translated word by word.

## Refresh notes

- Metadata-only refresh on 2026-08-27: recorded repository ID and fetch time, then updated stars from 62,451 to 62,580, forks from 4,683 to 4,700, and latest push from 2026-08-22 to 2026-08-26T15:43:13Z. Editorial claims were unchanged.
