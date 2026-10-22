# hhyqhh/inno-agent research notes

Research date: 2026-09-04
Repository: https://github.com/hhyqhh/inno-agent
Research mode: new

## Snapshot

- Repository ID: 1252294823
- Repository full name: hhyqhh/inno-agent
- Repository name: inno-agent
- Stars at fetch time: 1082
- Forks at fetch time: 205
- Primary language: TypeScript
- Latest push at fetch time: 2026-09-04T04:22:43Z
- License: MIT License
- Default branch: main
- README SHA: 56f3e38391e8656fcf5427fcfeace15e89a7d05a
- Latest release: v0.5.4 / 2026-09-03T16:09:41Z
- Repository state: active
- Fetched at: 2026-09-04T05:44:09Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/hhyqhh/inno-agent — accessed 2026-09-04
- [S2] Official README — https://github.com/hhyqhh/inno-agent/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/hhyqhh/inno-agent/releases/tag/v0.5.4 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/hhyqhh/inno-agent/blob/main/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] 仓库是 hhyqhh/inno-agent，GitHub 数字 ID 为 1252294823，主语言是 TypeScript，Stars 为 1082，Forks 为 205，默认分支为 main，仓库未归档、未禁用、不是 fork。 Sources: S1
- [F2] GitHub 元数据记录的最新推送时间是 2026-09-04T04:22:43Z。 Sources: S1
- [F3] 官方 LICENSE 文件与 GitHub 检测到的许可证都指向 MIT License。 Sources: S1, S4
- [F4] README 将项目定义为一个开源 personal learning agent，包含分层记忆、主动调度器、个人 IM 通道和 Practice Lab，并说明它建立在 Pi SDK 上且不修改 kernel。 Sources: S2
- [F5] README 把记忆拆成 L1 learner profile、L2 native wiki knowledge base 和 L3 session records with cross-conversation retrieval。 Sources: S2
- [F6] README 说明它同时提供 Electron 桌面端、React 19 + Tailwind 4 的 Web UI、基于 Node HTTP server 和 SSE 的后端，以及 terminal CLI。 Sources: S2
- [F7] README 列出 Feishu / WeChat 通道、带 xterm.js over WebSocket 的 Practice Lab、Simple Mode presets、skill system + content hub、conversation branch editing、pluggable providers、i18n/themes 和 session replay showcase。 Sources: S2
- [F8] README 明确写出它是 personal agent，且只有一个进程、一个 active agent session，不提供 multi-user concurrency、auth model 或 tenant isolation。 Sources: S2
- [F9] 最新发布 v0.5.4 增加了 agent trace timeline and replay、rich streaming Markdown、interactive artifacts 和相关 UX 修复。 Sources: S3

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | repository.githubId 为 1252294823 | F1 | verified |
| `repository.fullName` | repository.fullName 为 hhyqhh/inno-agent | F1 | verified |
| `repository.name` | repository.name 为 inno-agent | F1 | verified |
| `repository.stars` | repository.stars 为 1082 | F1 | verified |
| `repository.forks` | repository.forks 为 205 | F1 | verified |
| `repository.language` | repository.language 为 TypeScript | F1 | verified |
| `repository.pushedAt` | repository.pushedAt 为 2026-09-04T04:22:43Z | F2 | verified |
| `repository.license` | repository.license 为 MIT License | F3 | verified |
| `repository.state` | repository.state 为 active | F1 | verified |
| `editorial.hook` | hook 依据个人学习代理、分层记忆、IM 通道和 Practice Lab 的组合来写成一句自然中文 | F4, F5, F6, F7 | inferred |
| `editorial.summary` | summary 说明输入连接、核心动作、可见结果和三态运行形态 | F4, F5, F6, F7, F9 | verified |
| `editorial.meaning` | meaning 解释分层记忆和显式工具化如何便于拆出更窄的学习产品 | F4, F5, F7, F8 | inferred |
| `editorial.audience` | audience 是单人学习者 / personal learning 的主要用户 | F4, F8 | verified |
| `editorial.features` | features 列出三层记忆、调度、IM、Practice Lab、三种形态和回放能力 | F5, F7, F9 | verified |
| `editorial.stack` | stack 选取 TypeScript、Electron、React 19、Tailwind 4、SSE、WebSocket、SQLite、Pi SDK | F4, F5, F6, F7 | verified |
| `editorial.opportunity` | opportunity 从分层记忆、调度、IM、Practice Lab 和 replay 推出窄产品桥梁 | F5, F7, F8, F9 | inferred |

## Product inferences

- [I1] 这个仓库更适合被理解成面向单人学习的持续陪练系统，而不是通用编程代理或多人平台。 Basis: F4, F5, F7, F8. Confidence: high
- [I2] L1/L2/L3 分层记忆、scheduler、IM 通道和 Practice Lab 共同构成了一条可复用的学习闭环。 Basis: F5, F7. Confidence: high
- [I3] session replay 和 trace timeline 让学习过程可以被审阅、导出并改造成回放型产品。 Basis: F7, F9. Confidence: medium
- [I4] 仓库明确拒绝多用户并发和横向扩展，因此更适合做个人场景的产品，而不是团队协作平台。 Basis: F8. Confidence: high

## Direction rationale

### D1 — 错题复盘教练

- Reused capability: 复用三层记忆、自然语言调度、个人 IM 通道和 Practice Lab。
- Evidence: F4, F5, F7, F8
- New audience and recurring problem: 面向备考或自学时总在同一类题上反复失手的人；他们的问题不是缺少一次答案，而是错题、讲解和薄弱点分散，过几天就难以继续复盘。
- Input and visible outcome: 原项目主要接收学习对话、文件和练习过程，输出长期记忆和陪伴式支持；新方向接收错题照片、解析和标记，输出薄弱点清单、复习提醒和再练题记录。
- Original workflow: 单人学习者在对话中提出问题，系统用三层记忆、IM 通道和 Practice Lab 持续陪伴学习。
- New workflow: 用户上传错题和讲解后，系统把错因写入 L1/L2，按 scheduler 生成复习节点，再通过 IM 通道推送提醒并在 Practice Lab 里安排再练。
- Materially changed axes: input, workflow, outcome
- Product form: end-user-product
- Product boundary: 产品边界是“错题诊断 + 复习推进”的个人复盘工具，不是通用聊天助手，也不是课程内容管理平台。
- Substantive difference: 原项目是单人学习者的持续陪伴；这个方向把输入收窄为错题和标注，把核心工作流改成薄弱点诊断、复习排程和再练习，最终交付可追踪的错题复盘流程，而不是通用学习对话。

### D2 — 讲义整理助手

- Reused capability: 复用 L2 native wiki、文件摄取、混合检索和 Web 端展示。
- Evidence: F4, F5, F6, F7
- New audience and recurring problem: 面向课程助教、家教或知识型创作者；他们手里有 PDF、PPT、图片和零散讲义，但很难把资料整理成稳定可查、可复用的课程知识页。
- Input and visible outcome: 原项目接收学习过程中的对话和记录，输出长期记忆与练习支持；新方向接收课件、讲义和参考资料，输出结构化知识页、引用式问答和主题检索。
- Original workflow: 单人学习者在使用过程中逐步积累 L1/L2/L3 记忆，系统服务的是个人学习陪伴。
- New workflow: 用户导入文件后，系统用 L2 的 ingestion、摘要和 hybrid retrieval 抽取主题，生成课程 wiki 页面，再让 agent 按页面回答并持续补充。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 产品边界是“教学资料整理与答疑”，不是个人学习陪练，也不是纯文档搜索。
- Substantive difference: 原项目围绕个人学习记忆；这个方向把同一套 L2 wiki 能力改成教学资料整理产品，输入从个人对话变成成批讲义文件，结果从陪伴式支持变成可检索的课程知识库。

### D3 — 学习回放站

- Reused capability: 复用 session replay showcase、agent trace timeline 和实时流式展示。
- Evidence: F7, F9
- New audience and recurring problem: 面向家长、导师或班主任；他们经常只看到学习结果，看不到过程里卡住了什么，难以复盘和沟通。
- Input and visible outcome: 原项目在学习过程中持续接收消息、文件和工具动作，输出的是即时支持；新方向接收会话导出和 trace 数据，输出可分享、可审阅的学习过程回放。
- Original workflow: 单人学习者在交互中直接获得陪伴、提醒和练习。
- New workflow: 用户导出某次会话后，系统按时间线回放聊天、工具动作和工作区产物，并同步展示画像变化和生成物，方便旁观者检查过程。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 产品边界是“学习过程回放与审阅”，不是实时教学代理。
- Substantive difference: 原项目直接服务学习者本人；这个方向把输入改成已完成的会话或导出记录，把结果改成可审阅的时间线回放，产品从实时陪伴变成事后复盘。

## Pairwise direction comparison

- 错题复盘教练 vs 讲义整理助手
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 错题复盘教练面向备考自学者，讲义整理助手面向课程助教；前者吃错题证据并产出复习计划，后者吃文件资料并产出课程知识页。
- 错题复盘教练 vs 学习回放站
  - Different axes: audience, workflow, outcome
  - Concrete comparison: 错题复盘教练给学习者自己用，学习回放站给家长或导师看；前者面向当下改错，后者面向事后审阅。
- 讲义整理助手 vs 学习回放站
  - Different axes: input, audience, outcome
  - Concrete comparison: 讲义整理助手服务教学内容管理，学习回放站服务过程审阅；一个输入是未整理资料，一个输入是已完成会话。

## Uncertainty

- None.

## Localization decisions

- 保留 Practice Lab、Feishu、WeChat、SSE、WebSocket、SQLite、Pi SDK 和 React 19 等基础/产品名词，因为它们直接影响读者对产品形态和复用方式的判断。
- 将 wiki 译为“wiki / 知识页”并在摘要中保持英文技术名词，与 README 中的产品语义一致。
- 将 session replay 译为“会话回放”，将 trace timeline 译为“trace 时间线/轨迹时间线”，以保持中文语序自然。

## Refresh notes

- Initial research; no prior published snapshot.
