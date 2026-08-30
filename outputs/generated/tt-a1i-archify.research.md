# tt-a1i/archify research notes

Research date: 2026-08-30
Repository: https://github.com/tt-a1i/archify
Research mode: new

## Snapshot

- Repository ID: 1211139949
- Default branch: main
- README SHA: 9edae19e987f493582e561bd9ab340b3e58939d3
- Latest release: v2.15.0
- Repository state: active
- Fetched at: 2026-08-30T04:10:02Z

## Sources

- [S1] GitHub repository metadata API — https://api.github.com/repos/tt-a1i/archify — accessed 2026-08-30
- [S2] Official README — https://github.com/tt-a1i/archify/blob/main/README.md — accessed 2026-08-30
- [S3] Packaged Archify Skill — https://github.com/tt-a1i/archify/blob/main/archify/SKILL.md — accessed 2026-08-30
- [S4] Archify package manifest — https://github.com/tt-a1i/archify/blob/main/archify/package.json — accessed 2026-08-30
- [S5] Official release v2.15.0 — https://github.com/tt-a1i/archify/releases/tag/v2.15.0 — accessed 2026-08-30

## Verified repository facts

- [F1] The canonical repository is tt-a1i/archify and the official product name is Archify. Sources: S1, S2
- [F2] Archify accepts a codebase or system description through an AI coding agent, represents the diagram as typed JSON, and deterministically generates a self-contained interactive HTML/SVG system map. Sources: S2, S3
- [F3] It supports architecture, workflow, sequence, data-flow, and lifecycle diagrams. Sources: S2, S3
- [F4] Generated diagrams support node search, authored upstream or downstream reach, exact-route tracing, guided stories, themes, and static or motion exports including PNG, SVG, WebM, and share cards. Sources: S2, S3
- [F5] Schema, layout, route, label, and final artifact checks gate delivery; a passing artifact replaces the previous output only after those checks complete. Sources: S2, S3
- [F6] The packaged renderer is a Node.js JavaScript module that produces HTML/SVG from JSON governed by schemas. Sources: S2, S3, S4
- [F7] The repository uses the MIT license and is neither archived, disabled, a fork, nor a mirror. Sources: S1, S4
- [F8] At fetch time GitHub reported repository ID 1211139949, 31,514 stars, 1,956 forks, JavaScript as the primary language, and a latest push at 2026-08-29T17:13:30Z. Sources: S1
- [F9] The latest stable release is v2.15.0; the main branch currently identifies itself as the v2.16.0 development line. Sources: S2, S4, S5

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 1211139949 | F8 | verified |
| `repository.fullName` | tt-a1i/archify | F1 | verified |
| `repository.name` | Archify | F1 | verified |
| `repository.stars` | 31514 at fetch time | F8 | verified |
| `repository.forks` | 1956 at fetch time | F8 | verified |
| `repository.language` | JavaScript | F6, F8 | verified |
| `repository.pushedAt` | 2026-08-29T17:13:30Z | F8 | verified |
| `repository.license` | MIT | F7 | verified |
| `repository.state` | active | F7 | verified |
| `editorial.hook` | Turn a complex system into an explorable map | F2, F4, I1 | inferred |
| `editorial.summary` | AI agent input, typed JSON, validated HTML/SVG generation, five diagram types, exploration, and export | F2, F3, F4, F5 | verified |
| `editorial.meaning` | The verified generation and delivery pipeline can support focused visual products | F2, F5, I1 | inferred |
| `editorial.audience` | Developers and technical teams that need to explain, review, or share systems | F2, F3, F4, I2 | inferred |
| `editorial.features` | Five diagram types, typed source, validation gates, path exploration, and exports | F2, F3, F4, F5 | verified |
| `editorial.stack` | Node.js, JavaScript, HTML/SVG, JSON Schema | F6 | verified |
| `editorial.opportunity` | Guided learning, privacy review, and incident narratives can reuse the verified visual pipeline | F2, F3, F4, F5, I1 | inferred |

## Product inferences

- [I1] Archify's typed inputs, multiple diagram modes, interaction, validation, and portable exports form a reusable visual communication pipeline; narrower products can replace technical authoring with guided domain-specific inputs. Basis: F2, F3, F4, F5. Confidence: high
- [I2] Developers and technical teams are the likely core audience because the official examples center on repository architecture, API sequences, system design, data flows, and review artifacts; the repository does not publish a formal audience segmentation. Basis: F2, F3, F4. Confidence: medium

## Direction rationale

### D1 — Vibe 项目导览图

- Reused capability: repository-based architecture mapping, source evidence, interactive nodes, and guided routes.
- Evidence: F2, F3, F4
- New audience and recurring problem: Vibe Coding creators can run their product but repeatedly struggle to explain how frontend, backend, APIs, and data connect.
- Input and visible outcome: a repository URL becomes an interactive system tour with basic terminology cards and one guided main path.
- Substantive difference: the workflow optimizes for beginner understanding and self-explanation rather than general technical diagram delivery.

### D2 — 家庭数字隐私地图

- Reused capability: data-flow diagrams, trust boundaries, route tracing, and portable interactive output.
- Evidence: F3, F4, F5
- New audience and recurring problem: families use connected cameras, speakers, phones, and cloud accounts without a clear view of where personal data travels.
- Input and visible outcome: a guided device-and-account questionnaire becomes a data-flow map plus a privacy review checklist.
- Substantive difference: non-technical household inputs and privacy decisions replace a technical diagram specification.

### D3 — 故障复盘故事板

- Reused capability: sequence and lifecycle diagrams, authored routes, guided stories, validation, and share exports.
- Evidence: F3, F4, F5
- New audience and recurring problem: small engineering teams repeatedly write long incident reports that do not clearly show the break, decisions, and recovery.
- Input and visible outcome: incident events, participants, and recovery actions become a playable failure-and-recovery path in a shareable page.
- Substantive difference: a time-based incident narrative and recovery outcome replace open-ended system-map authoring.

## Uncertainty

- Stars, forks, and push time are a snapshot fetched at 2026-08-30T04:10:02Z, not live values.
- The main branch is ahead of the latest stable release; page claims use capabilities documented on the current main branch and do not promise that every development feature exists in v2.15.0.
- The three extension directions are product proposals, not built-in Archify workflows.
- No Issues or Discussions were used to claim broad market demand.

## Localization decisions

- “Typed JSON IR” is expressed as “带类型的 JSON 图形来源” in the feature list; the summary keeps JSON because the target reader understands basic technical concepts.
- “Trust boundary” is rendered as “信任边界”; its practical role is explained through local devices, cloud services, and third parties.
- HTML/SVG remains named because it explains why the result is a portable interactive file rather than a hosted image.

## Refresh notes

- Initial research; no prior published snapshot.
