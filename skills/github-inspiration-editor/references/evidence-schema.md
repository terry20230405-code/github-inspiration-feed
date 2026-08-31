# Research evidence schema

Create `<owner>-<repo>.research.md` using the structure below. The research note is an audit trail for the versioned project record, not a second marketing article.

Use stable IDs so project claims and directions can refer back to evidence without copying long passages. Paraphrase sources and use only short excerpts when exact wording is necessary.

```markdown
# owner/repo research notes

Research date: YYYY-MM-DD
Repository: https://github.com/owner/repo
Research mode: new | refresh

## Snapshot

- Repository ID: number or 未知
- Repository full name: owner/repo
- Repository name: official name
- Stars at fetch time: raw integer
- Forks at fetch time: raw integer
- Primary language: language or 未知
- Latest push at fetch time: UTC ISO 8601 timestamp
- License: verified label or 未知
- Default branch: branch or 未知
- README SHA: sha or 未知
- Latest release: tag/date or 未知
- Repository state: active | archived | disabled | unavailable
- Fetched at: UTC ISO 8601 timestamp
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository — URL — accessed YYYY-MM-DD
- [S2] README — URL — accessed YYYY-MM-DD
- [S3] Official documentation — URL — accessed YYYY-MM-DD

## Verified repository facts

- [F1] Concise verified claim. Sources: S1, S2
- [F2] Concise verified claim. Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | ... | F1 | verified |
| `repository.fullName` | ... | F1 | verified |
| `repository.name` | ... | F1 | verified |
| `repository.stars` | raw integer at fetch time | F2 | verified |
| `repository.forks` | raw integer at fetch time | F2 | verified |
| `repository.language` | ... | F2 | verified |
| `repository.pushedAt` | UTC timestamp | F2 | verified |
| `repository.license` | ... | F3 | verified / unknown |
| `repository.state` | ... | F2 | verified |
| `editorial.hook` | ... | F4 | inferred |
| `editorial.summary` | ... | F4, F5 | verified |
| `editorial.meaning` | ... | F4, I1 | inferred |
| `editorial.audience` | ... | F6 or I2 | verified / inferred |
| `editorial.features` | ... | F4, F5 | verified |
| `editorial.stack` | ... | F7 | verified |
| `editorial.opportunity` | ... | F4, I1 | inferred |

## Product inferences

- [I1] Inference statement. Basis: F4, F5. Confidence: high | medium | low
- None.

## Direction rationale

### D1 — Direction name

- Reused capability: ...
- Evidence: F4, F5
- New audience and recurring problem: ...
- Input and visible outcome: ...
- Substantive difference: ...

Repeat for every direction in the project record.

## Uncertainty

- Clearly state missing, stale, or ambiguous information.
- None.

## Localization decisions

- Record consequential or uncertain terminology choices.
- None.

## Refresh notes

- For new research: `Initial research; no prior published snapshot.`
- For refreshes: list changed snapshot identifiers, affected fact IDs, and fields proposed for revision.
```

## Controlled values

- Page field status: `verified`, `inferred`, or `unknown`.
- Inference confidence: `high`, `medium`, or `low`.
- Research mode: `new` or `refresh`.
- Repository state: `active`, `archived`, `disabled`, or `unavailable`.

## Traceability rules

- Every repository fact uses an `F` ID and cites at least one defined `S` ID.
- Every factual repository or editorial field points to one or more `F` IDs.
- Every inference uses an `I` ID, cites its factual basis, and states confidence.
- Every direction has a `D` section and cites at least one verified capability.
- Dynamic metadata records `fetchedAt` and must not be described as live.
- `visual` needs no repository evidence because it is persisted product configuration. A capability-based motif choice is still not a repository field.
- Missing evidence is `unknown`; it is not a reason to invent a replacement claim.

For a published-project refresh, the stage-seven `*.source.json` and matching `*.review.json` are pre-research evidence, not replacements for this research note. If the review action is `draft`, copy only supported findings into a refreshed note using new or preserved stable `S`, `F`, and `I` IDs, list affected fields under Refresh notes, and keep unaffected claims intact. See [research-refresh-workflow.md](research-refresh-workflow.md).
