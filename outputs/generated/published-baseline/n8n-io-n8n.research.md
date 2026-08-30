# n8n-io/n8n research notes

Research date: 2026-08-30
Repository: https://github.com/n8n-io/n8n
Research mode: refresh

## Snapshot

- Repository ID: 193215554
- Default branch: master
- README SHA: 21909fae00cbad4f18af84d2948752445051a915
- Latest release: n8n@2.36.7
- Repository state: active
- Fetched at: 2026-08-27T11:05:43Z

## Sources

- [S1] Repository metadata evidence bundle — outputs/generated/research-refresh/n8n.source.json — generated 2026-08-27
- [S2] Official README — https://github.com/n8n-io/n8n/blob/master/README.md — accessed 2026-08-27
- [S3] Official release n8n@2.36.7 — https://github.com/n8n-io/n8n/releases/tag/n8n%402.36.7 — accessed 2026-08-27
- [S4] Official repository architecture guide — https://github.com/n8n-io/n8n/blob/master/AGENTS.md — accessed 2026-08-30
- [S5] Official root manifest — https://github.com/n8n-io/n8n/blob/master/package.json — accessed 2026-08-30

## Verified repository facts

- [F1] n8n is a platform for AI agents and workflow automation that combines a visual canvas with custom code. Sources: S1, S2
- [F2] The README documents self-hosted or cloud operation, multi-step logic and human approvals, JavaScript and Python code, and more than 1,500 integrations. Sources: S2
- [F3] The repository architecture uses a Vue 3 and TypeScript frontend and a Node.js and TypeScript backend. Sources: S4, S5
- [F4] At fetch time GitHub reported repository ID 193215554, 202,574 stars, 60,416 forks, active state, a latest push at 2026-08-27T11:03:20Z, and the Sustainable Use License. Sources: S1
- [F5] The release does not remove the visual workflow, integration, self-hosting, or code-extension model used by the page. Sources: S2, S3

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 193215554 | F4 | verified |
| `repository.fullName` | n8n-io/n8n | F1 | verified |
| `repository.name` | n8n | F1 | verified |
| `repository.stars` | 202574 at fetch time | F4 | verified |
| `repository.forks` | 60416 at fetch time | F4 | verified |
| `repository.language` | TypeScript | F3, F4 | verified |
| `repository.pushedAt` | 2026-08-27T11:03:20Z | F4 | verified |
| `repository.license` | Sustainable Use License | F4 | verified |
| `repository.state` | active | F4 | verified |
| `editorial.hook` | Visual connections make many tools work together | F1, F2, I1 | inferred |
| `editorial.summary` | A visual workflow connects services and code into multi-step automated results | F1, F2 | verified |
| `editorial.meaning` | Existing integrations and execution can be hidden behind focused product interfaces | F1, F2, I1 | inferred |
| `editorial.audience` | Technical teams, automation enthusiasts, and operators | F1, F2, I2 | inferred |
| `editorial.features` | Visual workflows, service integrations, self-hosting, and custom code | F1, F2 | verified |
| `editorial.stack` | Vue, TypeScript, Node.js | F3 | verified |
| `editorial.opportunity` | Fixed role-specific workflows can remove general automation configuration | F1, F2, I1 | inferred |

## Product inferences

- [I1] A derivative product can keep n8n's integrations and execution graph behind a domain-specific interface so the user sees familiar inputs and outcomes rather than nodes and credentials. Basis: F1, F2. Confidence: high
- [I2] Technical teams and operators are a plausible broad audience because the product exposes visual logic, code, integrations, deployment, and operational controls. Basis: F1, F2. Confidence: medium

## Direction rationale

### D1 — 创作者合作收件箱

- Reused capability: email integrations, multi-step logic, and scheduled or event-driven workflows. Evidence: F1, F2
- User, input, workflow, outcome: creator emails are classified, budget and dates are extracted, and a collaboration board with reminders is produced.
- Substantive difference: users see an inbox and project view rather than an automation graph.

### D2 — 小店评价雷达

- Reused capability: integrations, data transformation, workflow logic, and summaries. Evidence: F1, F2
- User, input, workflow, outcome: reviews from selected sources are grouped and turned into a daily set of concrete actions.
- Substantive difference: the workflow is fixed around local-shop feedback instead of open-ended automation building.

### D3 — 个人信息晨报

- Reused capability: scheduled execution, web or feed connections, and multi-step processing. Evidence: F1, F2
- User, input, workflow, outcome: a knowledge worker chooses sources; the system gathers and groups items and sends one morning summary.
- Substantive difference: subscription and reading are the interface, while the workflow editor remains hidden.

## Uncertainty

- Stars, forks, and push time are a snapshot from 2026-08-27T11:05:43Z, not live counters.
- The current summary names email, spreadsheets, databases, web services, and AI models as representative node categories; official evidence supports the broader integration claim, not a permanent guarantee for every named service.
- The three directions are proposals, not built-in n8n products.

## Localization decisions

- “Workflow” is rendered as “工作流”; “节点” is retained because Vibe Coding readers generally understand it once described as connectable blocks.
- Node.js remains in the stack because it identifies the backend runtime at an appropriate level.

## Refresh notes

- Stage-nine backfill records the current published copy and current official architecture evidence.
- The stage-seven review recommended keeping the published copy; publication remained unauthorized.
