# Inspiration feed content contract

This document is the canonical definition of what one published project must communicate and which data layer owns each value. The frontend, project types, JSON schema, validators, research notes, and generation skill must stay aligned with it.

## Product promise

Each project should let a Vibe Coding explorer who understands basic concepts such as frontend, backend, and APIs, but does not read code or know low-level technical internals, answer three questions after one read:

1. What does the original project let people do?
2. Why are its underlying capabilities useful for making another product?
3. What are three concrete, narrower products that could grow from it?

The page is an editorial interpretation of a repository, not a repository ranking, README translation, implementation tutorial, or build-plan generator.

## Record layers

### `repository` — refreshable GitHub facts

This layer is replaced by deterministic metadata refreshes:

- `githubId`
- `fullName`
- `name`
- `stars`
- `forks`
- `language`
- `pushedAt`
- `license`
- `state`
- `fetchedAt`

Store counts as integers and times as UTC ISO 8601 values. `pushedAt` must not be later than `fetchedAt`. The frontend is responsible for `57.5k` and `2 小时前` display formatting. A metadata refresh must not rewrite the other layers.

Published snapshots live in `src/data/repositories.json`; `src/data/repositories.ts` validates and exposes them to the frontend. Automated refreshes use the guarded workflow in [refresh-workflow.md](refresh-workflow.md).

Repository activity that merits deeper inspection passes to [research-refresh-workflow.md](research-refresh-workflow.md). Stage-seven source snapshots and semantic reviews are operational evidence under `outputs/`; they are not published record fields. A semantic review may keep the published copy or request a new draft, but it cannot directly mutate `editorial` or authorize publication.

### `editorial` — reviewed interpretation

Repository facts used inside these fields must come from GitHub or primary project documentation:

- factual statements inside `summary` and `audience`
- `features`
- `stack`

These fields are editorial inferences grounded in repository evidence:

- `hook`
- `meaning`
- `opportunity`
- `directions`

Record sources and research date in the research notes. Distinguish inference from documented behavior and use `未知` when a required fact cannot be verified.

### `visual` — persisted product configuration

- `generatorVersion`
- `seed`
- `accent`
- `foreground`
- `motif`
- `variant`

Visual configuration belongs to the inspiration-feed product. It is not a GitHub fact and a repository refresh must not change it.

## Field responsibilities

### Repository fields

| Field | Responsibility | Must not do |
| --- | --- | --- |
| `repository.githubId` | Keep GitHub's stable numeric identity across renames and transfers | Use the display slug as the only identity |
| `repository.fullName` | Store the current canonical `owner/repository` and derive the GitHub URL | Store an unofficial mirror |
| `repository.name` | Use the official project display name | Translate or embellish the name |
| `repository.stars` | Store the raw researched Star count | Store `12.3k` or use popularity as proof of quality |
| `repository.forks` | Store the raw researched Fork count | Store an abbreviation or treat forks as proven adoption |
| `repository.language` | Store the primary GitHub language | Describe the full stack |
| `repository.pushedAt` | Store the latest researched push timestamp | Store relative text or claim it is live without refreshing |
| `repository.license` | Store the verified license label or `未知` | Claim that source availability means unrestricted reuse |
| `repository.state` | Record active, archived, disabled, or unavailable | Hide a critical repository state |
| `repository.fetchedAt` | Record when this snapshot was collected | Present an old snapshot as current |

### Editorial project fields

| Field | Page role | Content responsibility | Must not do |
| --- | --- | --- | --- |
| `id` | Internal identity | Stable lowercase kebab-case project key | Carry editorial meaning |
| `editorial.hook` | Feed positioning | Express the repository's most distinctive product transformation | List features or repeat the summary |
| `editorial.summary` | Feed and detail introduction | Explain input or connection, core actions, several verified capabilities, and outcome | Discuss extension ideas or repeat the hook |
| `editorial.meaning` | Detail lead | Explain why the underlying capabilities are valuable for making new products | Restate the feature list |
| `editorial.audience` | Original-project information | Identify the original project's main users | Describe the audience of an extension direction |
| `editorial.features` | Original-project information | List 3–6 verified core capabilities | Include speculative or minor features |
| `editorial.stack` | Original-project information | List 1–8 important technologies that help explain reuse | Dump every dependency |
| `editorial.opportunity` | Opportunity section | Give 2–5 concrete bridges between existing capability, friction, and new product potential | Make generic claims such as “can add AI” |
| `editorial.directions` | Direction selection | Provide 3–5 distinct, evidence-based product directions | Become an implementation plan or category list |

### Direction fields

| Field | Page role | Content responsibility | Must not do |
| --- | --- | --- | --- |
| `id` | Internal identity | Stable lowercase kebab-case direction key | Carry display prose |
| `name` | Direction title | Name a small product a user could choose to build | Use a generic label such as “AI assistant” |
| `tagline` | Direction preview | State the input and visible outcome compactly | Repeat the name without adding meaning |
| `problem` | Selected-direction analysis | Describe a concrete recurring problem | Describe a broad market trend |
| `audience` | Selected-direction analysis | Name the specific people experiencing that problem | Use “everyone” or an undefined industry |
| `approach` | Selected-direction analysis | Explain the first complete workflow and what original capability it reuses | Expand into a day-by-day build plan |
| `difference` | Selected-direction analysis | State the substantive difference from the original project | Merely say it is simpler, mobile, translated, or AI-powered |
| `scope` | Minimum feature range | List 3–6 functions required for the smallest coherent experience | Add optional polish or future roadmap items |

### Visual fields

| Field | Responsibility | Must not do |
| --- | --- | --- |
| `visual.generatorVersion` | Pin the generation and rendering contract | Restyle old cards automatically after an algorithm upgrade |
| `visual.seed` | Preserve the repository identity string used for generation | Replace it during ordinary metadata refreshes or repository renames |
| `visual.accent` | Store the constrained product-generated theme color | Treat the repository logo color as mandatory or refresh it with GitHub facts |
| `visual.foreground` | Store readable black or white content color for the accent | Assume white is readable on every accent |
| `visual.motif` | Select one generic SVG graph family | Encode a repository name in a CSS selector |
| `visual.variant` | Reproduce the family's element count, position, weight, density, symmetry, and entry direction | Generate new random parameters on every render |

## Non-overlap rules

- `editorial.hook` attracts attention; `editorial.summary` builds the product mental model.
- `editorial.summary` describes the existing product; `editorial.meaning` explains reuse value.
- `editorial.meaning` states general reuse value; `editorial.opportunity` gives concrete supporting reasons.
- `editorial.opportunity` explains why directions are plausible; `editorial.directions` describes actual new products.
- Project audience describes original users; direction audience describes the narrower new users.
- Direction `approach` explains a complete workflow; `scope` lists only the minimum functions needed to support it.

## Explicitly excluded content

Do not add these fields or UI sections unless the product owner explicitly changes the content contract:

- Display category
- Direction difficulty
- Direction duration
- Recommended MVP section
- Day-by-day implementation plan
- Generated build button or build modal
- Monetization score, market size, or revenue ranking

Optional advice requested in a conversation may be given outside the app-ready project JSON, but it must not silently expand the published page schema.

## Page mapping

- **Feed:** `repository.name`, `repository.stars`, `repository.language`, the derived GitHub URL, `editorial.hook`, `editorial.summary`, the visual accent, and the first three directions' names and taglines.
- **Detail header:** `repository.name`, derived GitHub URL, `editorial.summary`, and the complete rendered visual identity.
- **Original project:** `repository.stars`, `repository.forks`, formatted `repository.pushedAt`, `repository.license`, `editorial.meaning`, `editorial.features`, `editorial.audience`, and `editorial.stack`.
- **Opportunity:** `editorial.opportunity`.
- **Directions:** every direction field.

## Change control

When the published record changes, update all of the following in the same task:

1. `src/App.tsx` and the generic `src/components/ProjectIdentity.tsx` renderer
2. Types and layer files under `src/data/`, including the machine-writable `repositories.json`, plus the composition layer `src/data.ts`; keep layer types read-only so UI code cannot accidentally rewrite source data
3. `references/content-contract.md`
4. `references/project-schema.md` and `references/evidence-schema.md`
5. `scripts/validate_project.py`, `scripts/validate_research.py`, and the guarded repository refresh workflow when repository fields change
6. Existing app data and generated drafts
7. `README.md` and `FRONTEND_HANDOFF.md`

Do not retain unused page fields “for later.” Operational identity and freshness fields are allowed only when they protect refresh correctness.
