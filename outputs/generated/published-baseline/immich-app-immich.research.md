# immich-app/immich research notes

Research date: 2026-08-30
Repository: https://github.com/immich-app/immich
Research mode: refresh

## Snapshot

- Repository ID: 455229168
- Default branch: main
- README SHA: 02ae01857e52955e07cdb4d83a3d8f1d45e29e53
- Latest release: v3.1.0
- Repository state: active
- Fetched at: 2026-08-27T11:05:43Z

## Sources

- [S1] Repository metadata evidence bundle — outputs/generated/research-refresh/immich.source.json — generated 2026-08-27
- [S2] Official README — https://github.com/immich-app/immich/blob/main/README.md — accessed 2026-08-27
- [S3] Official release v3.1.0 — https://github.com/immich-app/immich/releases/tag/v3.1.0 — accessed 2026-08-27
- [S4] Official mobile README — https://github.com/immich-app/immich/blob/main/mobile/README.md — accessed 2026-08-30
- [S5] Official server manifest — https://github.com/immich-app/immich/blob/main/server/package.json — accessed 2026-08-30
- [S6] Official duplicates utility documentation — https://docs.immich.app/features/duplicates-utility/ — accessed 2026-08-30

## Verified repository facts

- [F1] Immich describes itself as a high-performance self-hosted photo and video management solution. Sources: S1, S2
- [F2] The official feature table includes automatic and background mobile backup, albums and shared albums, metadata and map views, global maps, and search by metadata, objects, faces, and CLIP. Sources: S2
- [F3] The mobile application is Flutter-based. Sources: S4
- [F4] The server manifest uses TypeScript and PostgreSQL client libraries. Sources: S5
- [F5] At fetch time GitHub reported repository ID 455229168, 112,773 stars, 6,738 forks, active state, a latest push at 2026-08-27T11:02:12Z, and the AGPL-3.0 license. Sources: S1
- [F6] Release v3.1.0 improves upload, archive, filtering, and administration flows without replacing the self-hosted photo-management model. Sources: S3
- [F7] Immich includes a machine-learning duplicates utility that groups visually similar assets for user review. Sources: S6

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 455229168 | F5 | verified |
| `repository.fullName` | immich-app/immich | F1 | verified |
| `repository.name` | Immich | F1 | verified |
| `repository.stars` | 112773 at fetch time | F5 | verified |
| `repository.forks` | 6738 at fetch time | F5 | verified |
| `repository.language` | TypeScript | F4, F5 | verified |
| `repository.pushedAt` | 2026-08-27T11:02:12Z | F5 | verified |
| `repository.license` | AGPL-3.0 | F5 | verified |
| `repository.state` | active | F5 | verified |
| `editorial.hook` | Private photos remain under the user's control | F1, I1 | inferred |
| `editorial.summary` | Mobile backup, private server storage, albums, maps, faces, search, duplicate review, sharing, and multi-device use | F1, F2, F7 | verified |
| `editorial.meaning` | Time, people, and place organization can support memory and travel experiences | F2, I1 | inferred |
| `editorial.audience` | Privacy-conscious photo users able to operate a home server | F1, I2 | inferred |
| `editorial.features` | Mobile backup, face and place discovery, shared albums | F2 | verified |
| `editorial.stack` | Flutter, TypeScript, PostgreSQL | F3, F4 | verified |
| `editorial.opportunity` | Photo metadata and self-hosting can support focused memory and cleanup workflows | F1, F2, I1 | inferred |

## Product inferences

- [I1] The combination of private storage and time, face, object, and location organization can support products centered on remembering, travel storytelling, and deliberate cleanup. Basis: F1, F2. Confidence: high
- [I2] Privacy-conscious home-server users are a reasonable audience description because self-hosting is central, but the repository does not publish a formal user profile. Basis: F1. Confidence: medium

## Direction rationale

### D1 — 家庭照片周报

- Reused capability: albums, sharing, time metadata, and self-hosted storage. Evidence: F1, F2
- User, input, workflow, outcome: family photos enter a shared album, the week is reviewed, and a private story page is produced.
- Substantive difference: the workflow emphasizes recurring family reflection rather than backup management.

### D2 — 旅行轨迹相册

- Reused capability: photo timestamps, metadata maps, and albums. Evidence: F2
- User, input, workflow, outcome: travelers choose a trip's photos; the product groups days, maps locations, and outputs a route-based story.
- Substantive difference: a single journey and its narrative become the primary unit.

### D3 — 隐私照片整理助手

- Reused capability: local/private photo access and object/search analysis. Evidence: F1, F2
- User, input, workflow, outcome: users scan selected photos, review duplicate, blurry, or sensitive candidates, and confirm cleanup.
- Substantive difference: the visible result is a reviewed cleanup decision, not another backup or album.

## Uncertainty

- Stars, forks, and push time are a snapshot from 2026-08-27T11:05:43Z, not live counters.
- Sensitive-document detection and blur detection are proposed direction capabilities, not existing verified Immich features.

## Localization decisions

- “Self-hosted” is rendered as “自托管” and explained through storage on the user's own server.
- CLIP is omitted from page copy because “按内容智能搜索” communicates the product capability at the reader's technical level.

## Refresh notes

- Stage-nine backfill added the official duplicates utility documentation, so the current duplicate-recognition claim remains evidence-backed.
- The baseline records the published text unchanged.
