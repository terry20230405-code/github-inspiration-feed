# apache/maka research notes

Research date: 2026-09-01
Repository: https://github.com/apache/maka
Research mode: new

## Snapshot

- Repository ID: 1251460378
- Repository full name: apache/maka
- Repository name: maka
- Stars at fetch time: 4391
- Forks at fetch time: 407
- Primary language: TypeScript
- Latest push at fetch time: 2026-09-01T14:58:14Z
- License: Apache License 2.0
- Default branch: main
- README SHA: 93d6154eb40cf2109a40a41e6eb820939c9522a1
- Latest release: 未知
- Repository state: active
- Fetched at: 2026-09-01T15:00:54Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/apache/maka — accessed 2026-09-01
- [S2] Official README — https://github.com/apache/maka/blob/main/README.md — accessed 2026-09-01

## Verified repository facts

- [F1] 仓库的 GitHub ID 是 1251460378，规范名是 apache/maka，显示名是 maka。 Sources: S1
- [F2] 仓库目前有 4391 个 stars、407 个 forks，主语言是 TypeScript。 Sources: S1
- [F3] 仓库未归档、未禁用、非 fork，默认分支是 main，许可证是 Apache-2.0。 Sources: S1
- [F4] README 将 Maka 定位为 local-first 的 AI agent workspace，并把 model messages、tool calls、tool results、permission decisions、termination events 记为 append-only log。 Sources: S2
- [F5] README 把 Desktop、TUI/CLI 和 Eval 列为入口，并说明它们共享 Runtime Host。 Sources: S2
- [F6] Desktop 基于 Electron + React，支持 streaming sessions、tool timelines、branching、search 和 recovery。 Sources: S2
- [F7] Agent Runtime 提供多模型连接、内置 Read/Write/Edit/Bash/Glob/Grep 工具，沙箱外操作需要批准，可中止运行，并能记录失败分类和可恢复执行记录。 Sources: S2
- [F8] Evaluation 支持声明式 multi-arm experiments、task×repetition×subject 展开、immutable attempts 和 result kernel。 Sources: S2
- [F9] 工作区数据默认保存在本地，模型连接可来自 cloud API、本地模型或兼容 gateway，首次使用需要在 Settings→Models 测试并选择默认模型。 Sources: S2
- [F10] 桌面 nightly 构建面向 developers and testers，且当前桌面主要支持 Apple Silicon Macs，Windows 仅 preview，Linux 还未支持。 Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | repository.githubId=1251460378 | F1 | verified |
| `repository.fullName` | repository.fullName=apache/maka | F1 | verified |
| `repository.name` | repository.name=maka | F1 | verified |
| `repository.stars` | repository.stars=4391 | F2 | verified |
| `repository.forks` | repository.forks=407 | F2 | verified |
| `repository.language` | repository.language=TypeScript | F2 | verified |
| `repository.pushedAt` | repository.pushedAt=2026-09-01T14:58:14Z | F2 | verified |
| `repository.license` | repository.license=Apache-2.0 | F3 | verified |
| `repository.state` | repository.state=active | F3 | verified |
| `editorial.hook` | editorial.hook=把 AI 代理做成可回放工作区 | F4, F5, F6, F7, F8, F9 | inferred |
| `editorial.summary` | editorial.summary=本地工作区、模型连接、权限设置、可回放记录和多入口工作流的完整产品画面 | F4, F5, F6, F7, F8, F9 | inferred |
| `editorial.meaning` | editorial.meaning=可追溯执行记录和共享 Runtime Host 适合作为可复用产品底座 | F4, F5, F6, F7, F8 | inferred |
| `editorial.audience` | editorial.audience=本地使用 AI agent 的开发者和测试者 | F10, F5, F6, F7, F9 | inferred |
| `editorial.features` | editorial.features=多入口共享 Runtime Host、append-only log、内置工具、沙箱审批、会话恢复、声明式评测 | F5, F6, F7, F8, F9 | verified |
| `editorial.stack` | editorial.stack=TypeScript、Electron、React、SQLite、Runtime Host、MCP | F2, F5, F6, F7, F8, F9 | verified |
| `editorial.opportunity` | editorial.opportunity=复盘台、权限审计台、实验对照台三种窄产品 | F4, F5, F6, F7, F8, F9 | inferred |

## Product inferences

- [I1] append-only execution log 使这个项目天然适合做回放、分支、恢复和审计类产品，而不只是对话壳。 Basis: F4, F6, F7. Confidence: high
- [I2] Desktop、CLI 和 Eval 共用 Runtime Host，说明它更像一套可复用的执行底座，而不是单一入口应用。 Basis: F5, F8, F9. Confidence: high
- [I3] 因为连接来源可自带、工作区数据默认本地保存且桌面分发仍有平台限制，这个项目更适合做对隐私和控制边界敏感的产品。 Basis: F7, F9, F10. Confidence: medium

## Direction rationale

### D1 — 会话复盘台

- Reused capability: append-only execution log、search、branching、recovery
- Evidence: F4, F6, F7
- New audience and recurring problem: 面向经常要排查 AI agent 失败原因的个人开发者或支持人员；他们拿到的是一段已经结束的会话，需要看清工具调用、权限决策和终止点。
- Input and visible outcome: 原输入是新任务和模型连接；这里输入是既有会话日志，输出是可搜索、可分支的复盘结果。
- Original workflow: 在 Desktop、TUI/CLI 里连上模型后直接发起任务、运行工具并继续工作。
- New workflow: 打开历史会话→按时间线查看 messages、tool calls、tool results、permission decisions 和终止点→定位失败点→必要时分支出后续 turn。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做事后分析与追溯，不负责替用户完成原任务本身。
- Substantive difference: 原项目把会话当作继续做事的工作区，这个方向把同一份记录当作复盘材料。

### D2 — 权限审计台

- Reused capability: 模型连接、权限决策、sandbox boundary
- Evidence: F5, F7, F9
- New audience and recurring problem: 面向给团队配置 agent 连接和沙箱边界的平台或安全负责人；他们反复处理模型接入、权限放行和越界操作审批。
- Input and visible outcome: 原输入是工作任务；这里输入是 API、local-model 或 gateway 连接、sandbox 设置和批准规则，输出是可用的策略配置。
- Original workflow: 在工作区里开始任务，运行中再按需审批工具动作。
- New workflow: 测试连接→选择默认模型→设定哪些工具或越界动作要批准→保存并审计权限状态。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不面向日常做事的聊天界面，而是把模型、权限和 sandbox 当作独立治理对象。
- Substantive difference: 原项目以执行任务为中心，这个方向以配置和签核为中心。

### D3 — 实验对照台

- Reused capability: declarative multi-arm experiments、immutable per-cell attempts、result kernel
- Evidence: F5, F8
- New audience and recurring problem: 面向需要审查模型或 subject 结果的评测工程师和 QA 人员；他们每次改模型、改工具或改参数后，都要手工对照一组评测 cell，才能知道哪些结果真的变了。
- Input and visible outcome: 原输入是实验 spec 和要执行的 subjects；这里输入是已经跑完的实验结果，输出是可对照的差异和异常项。
- Original workflow: 编写声明式 spec→展开 task×repetition×subject cells→Runtime Host 跑 Maka subjects 和 external subjects→记录结果。
- New workflow: 打开一组已经完成的 multi-arm experiment→按 task、repetition、subject 和 cell 查看 attempts→对比 score、usage、duration、status、failure reason→标出异常项。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不负责执行评测，只负责阅读、比较和筛选评测结果。
- Substantive difference: 原项目负责把实验跑出来，这个方向只负责把已完成的结果看清楚并对照。

## Pairwise direction comparison

- 会话复盘台 vs 权限审计台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 会话复盘台看的是已经结束的对话记录，权限审计台看的是模型连接和 sandbox 规则；前者面向排查问题的人，后者面向治理配置的人。两者在输入、工作流、结果和用户上都不同。
- 会话复盘台 vs 实验对照台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 会话复盘台处理的是历史会话日志，实验对照台处理的是已经跑完的评测结果；前者输出失败定位线索，后者输出可对照的实验差异。两者在用户、输入、工作流和结果上都不同。
- 权限审计台 vs 实验对照台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 权限审计台围绕连接、模型和审批规则，实验对照台围绕 task×repetition×subject 的结果核对；一个输出可签核的治理配置，一个输出可读的评测差异。两者在用户、输入、工作流和结果上都不同。

## Uncertainty

- README 只明确 cloud API、local model 和 compatible gateway，没有给出完整兼容清单。

## Localization decisions

- 保留 Runtime Host、TUI、CLI、Eval、MCP、API、SQLite、Electron、React、tool calls、tool results、sandbox、branching、recovery 等技术词。
- 把 Turn 译为“回合”，把 Artifact 译为“产物”，其余句子按自然中文重写，不逐词翻译 README。

## Refresh notes

- Initial research; no prior published snapshot.
