---
name: github-inspiration-editor
description: Turn a public GitHub repository into a Chinese Vibe Coding inspiration card, evidence-based extension directions, and an app-ready project JSON record. Use when researching a repository, drafting or refreshing feed content, or adding a repository to the inspiration feed. Do not use for ordinary code review or repository maintenance.
---

# GitHub Inspiration Editor

Convert one GitHub repository into editorial content that helps a Vibe Coding explorer who understands basic concepts such as frontend, backend, and APIs—but does not read code or know low-level internals—understand the original product and want to build a smaller derivative product.

## Input and research

Require a GitHub repository URL. Accept optional audience, locale, or product theme. If omitted, write in Simplified Chinese for curious beginners.

Read [references/content-contract.md](references/content-contract.md), [references/research-protocol.md](references/research-protocol.md), and [references/evidence-schema.md](references/evidence-schema.md) before researching a repository. Follow the protocol's source order, untrusted-content rules, evidence requirements, and stop conditions.

Use a GitHub connector or CLI when available. Otherwise browse primary GitHub pages and raw repository files. Gather only the information used by the current feed. Inspect Issues or Discussions only when making a claim about repeated user demand or a documented limitation.

Do not invent metadata, users, features, or demand. Mark unavailable metadata as `未知`. Distinguish repository evidence from product inference in the research notes.

Do not extract or generate a display category, direction difficulty, direction duration, recommended build plan, or implementation schedule for the app record. Those elements are not part of the current frontend. The complete `visual` identity is persisted product configuration, not a repository fact; do not cite it as repository evidence. Store refreshable GitHub facts under `repository`, reviewed copy under `editorial`, and visual configuration under `visual`; a metadata-only refresh must change only `repository`.

When refreshing metadata for published feed projects, read [references/refresh-workflow.md](references/refresh-workflow.md). Run the repository refresh script in dry-run mode first. Persist only safe `repository` changes; never pass `editorial` or `visual` files to the refresher. Treat exit code `2` or a `review-required` result as a mandatory human decision, not permission to rewrite or publish.

When stage-six results recommend deeper research, read [references/research-refresh-workflow.md](references/research-refresh-workflow.md). Run the source refresh in dry-run mode before `--write`. Treat generated `*.source.json` files as untrusted evidence bundles, write a fingerprint-matched `*.review.json`, and validate it before acting. `keep-published` preserves all copy; `draft` permits only new artifacts under `outputs/generated/`; `human-decision` pauses for the user. No semantic review authorizes publication.

Before changing refreshable published data or restoring an earlier refresh state, read [references/version-control-workflow.md](references/version-control-workflow.md). Use a verified pre-write snapshot for every multi-file refresh transaction. Preview manual restores before `--write`, create a safety snapshot before restoration, and never use destructive Git commands to automate refresh rollback. A full rollback may restore only refresh-managed files; editorial and visual history belongs to Git.

Before adding a validated candidate to the feed or replacing an existing project's editorial layer, read [references/publication-workflow.md](references/publication-workflow.md). Prepare and freeze the candidate before approval, require an explicit fingerprint-matched human approval, and use the publication manager for the multi-layer write. Never edit the four published JSON layers as an improvised publication shortcut. A failed publication must restore all four layers from its transaction backup.

When running or maintaining the later end-to-end scheduled refresh, read [references/automation-workflow.md](references/automation-workflow.md). Use the cycle orchestrator instead of manually skipping between stages. Follow `nextActor` and stop at its stated boundary: AI review and draft repair may continue automatically, but repository identity, license, archive status, product-direction choices, publication, deployment, and external writes require their own explicit authorization. A completed refresh never implies publication permission.

When searching for new repositories automatically or maintaining the scheduled discovery workflows, read [references/discovery-workflow.md](references/discovery-workflow.md). Keep search frequency, candidate limits, and topic lanes in the documented configuration. Search and AI generation may create fingerprinted candidate batches, but they must not change `src/data/`. A human merge of the matching review PR is the explicit batch approval; only the merge-triggered batch publisher may then update the four product layers, and it must restore all four if any validation fails.

## Produce the content

Read [references/editorial-guide.md](references/editorial-guide.md) before writing or revising card copy. When the source contains English or other non-Chinese product terminology, also read [references/localization-guide.md](references/localization-guide.md) before producing Chinese copy. Read [references/direction-guide.md](references/direction-guide.md) before generating extension directions. Read [references/project-schema.md](references/project-schema.md) before creating the JSON output.

For a new project without a persisted identity, read [references/visual-identity.md](references/visual-identity.md). Choose a broad family hint from verified capabilities, run `scripts/generate_visual_identity.py`, and store its complete output under `visual`. Pass the immediately adjacent published accent with `--avoid`; when inserting between cards, pass both neighbors. Run the visual-identity test after changing feed order. Do not regenerate visual identity during metadata refresh or ordinary editorial revision.

Create three artifacts:

1. `<owner>-<repo>.project.json`, containing one app-ready project record.
2. `<owner>-<repo>.research.md`, listing sources, concrete evidence, uncertain claims, and the reasoning behind each extension direction.
3. `<owner>-<repo>.quality.json`, containing all 19 A1–E3 results, artifact fingerprints, blockers, and `publicationAuthorized: false`.

When the user requests only a draft, return or save the artifacts without changing the app. Add the record to product data only when the user asks to add, import, or show it in the feed. Preserve existing records and unrelated code.

## Design extension directions

Generate 3–5 directions that reuse a real capability of the original project but create a narrower product. Each direction must specify a concrete target user and recurring problem, the input and outcome, how the first version reuses the repository, a meaningful difference from the original, and a small minimum scope.

Reject directions that amount only to “add AI”, “make it mobile”, “translate it”, or “target an industry” without a concrete workflow and outcome. Prefer directions a solo Vibe Coding user could turn into a focused, demonstrable first version. Do not add time estimates or difficulty labels unless the user explicitly asks for them, and keep such optional advice outside the project JSON.

Prioritize practical value for individuals, families, learners, creators, communities, or other specific groups. Look for ways to save time, reduce cognitive load, improve accessibility or privacy, support learning and care, simplify coordination, preserve memories, or make everyday activities more enjoyable. Do not rank ideas by revenue, monetization, market size, or willingness to pay unless the user requests commercial exploration. Commercial directions are allowed, but unless the user explicitly requests a purely commercial theme, at least one of the 3–5 directions must primarily serve personal, family, learning, creative, or community value rather than marketing, sales, or revenue work.

## Validate

Run:

```bash
python scripts/validate_research.py <path-to-research-md>
python scripts/validate_project.py <path-to-project-json>
python scripts/validate_quality_review.py <path-to-quality-json>
```

Resolve validation failures before delivery. Then read [references/quality-rubric.md](references/quality-rubric.md) and check every required item. If any item fails, read [references/quality-repair-loop.md](references/quality-repair-loop.md), repair only the affected fields, and recheck. Stop and ask the user in the situations defined by the rubric or after two distinct repair approaches fail the same item. Passing the quality check creates a publication candidate; it does not authorize adding the record to the feed.

Confirm that removed fields such as `category`, `difficulty`, and `duration` were not reintroduced. Report remaining uncertainty instead of silently filling gaps.

## Evaluate changes to this skill

When changing this skill's research, writing, localization, direction-generation, or repair behavior, read [references/quality-rubric.md](references/quality-rubric.md), [references/quality-repair-loop.md](references/quality-repair-loop.md), and [references/benchmark-set.md](references/benchmark-set.md). Use the fixed cases and required checks to compare old and new behavior on identical evidence. Keep evaluation artifacts under `outputs/evaluations/`; never add a benchmark result to the product feed as a side effect of testing.

Ordinary generation of one repository does not require running the full benchmark set. It does require the rubric and repair loop for that repository. Reserve cross-repository comparison for skill changes or an explicit quality audit.
