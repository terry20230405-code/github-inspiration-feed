# QwenAudio/qwen-audio-agent research notes

Research date: 2026-09-04
Repository: https://github.com/QwenAudio/qwen-audio-agent
Research mode: new

## Snapshot

- Repository ID: 1313435339
- Repository full name: QwenAudio/qwen-audio-agent
- Repository name: qwen-audio-agent
- Stars at fetch time: 2335
- Forks at fetch time: 201
- Primary language: JavaScript
- Latest push at fetch time: 2026-09-04T05:24:27Z
- License: Apache License 2.0
- Default branch: main
- README SHA: 8876160e2bf1225a6bc554a38df2fd0eae0ad1f0
- Latest release: v1.11.0 / 2026-08-20T14:38:07Z
- Repository state: active
- Fetched at: 2026-09-04T05:24:48Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/QwenAudio/qwen-audio-agent — accessed 2026-09-04
- [S2] Official README — https://github.com/QwenAudio/qwen-audio-agent/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/QwenAudio/qwen-audio-agent/releases/tag/v1.11.0 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/QwenAudio/qwen-audio-agent/blob/main/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] 仓库的 GitHub 数字 ID 为 1313435339，完整名称是 QwenAudio/qwen-audio-agent，显示名为 qwen-audio-agent，主要语言是 JavaScript，当前分支是 main，仓库未归档、未禁用，且在 2026-09-04T05:24:27Z 有最新推送。 Sources: S1
- [F2] 仓库的官方定位是一个实时语音运行时，用来让 Agent 保持说话、继续工作并保持在场。 Sources: S2
- [F3] 项目支持全双工实时语音交互、自然打断和持续多轮对话。 Sources: S2
- [F4] 项目可以一键接入你偏好的 Agent，并复用它的 model config、tools、MCP、Skills 和 authentication。 Sources: S2
- [F5] 前台对话与后台任务可以并行运行，用户能随时询问进度或取消任务。 Sources: S2
- [F6] 项目支持创建多个独立任务，后端 Agent 异步执行并持续跟踪状态，任务结果会自动回到当前对话并支持继续追问和修改。 Sources: S2
- [F7] 项目提供 WebUI、terminal TUI 和桌面浮窗入口，覆盖 macOS、Windows 和 Linux。 Sources: S2
- [F8] 项目提供按用户划分的长期个性化和跨会话记忆。 Sources: S2
- [F9] 项目的架构说明强调：能直接回答的问题立即回答，需要工具或持续处理时则委派给后端 Agent，而且用户始终面对同一个助手。 Sources: S2
- [F10] README 的场景扩展示例包括 desktop、smart cockpit、customer support、embodied intelligence 和 livestream assistant。 Sources: S2
- [F11] v1.11.0 最新发布加入了跨 TUI、WebUI 和 Gateway 的 multimodal input parts、技能管理、可注入 realtime providers、插件化契约以及桌面与 CLI 资产共享和运行态隔离。 Sources: S3
- [F12] 官方 LICENSE 文件确认项目采用 Apache License 2.0。 Sources: S4
- [F13] README 说明项目需要 Node.js 22.22.2+ 或 24.15.0+ 和 npm 10+，并默认使用 DashScope realtime voice frontend，也支持本地 speech-to-speech frontend。 Sources: S2
- [F14] README 的场景说明把 smart cockpit 写成 vehicle control、navigation、music、weather、services；customer support 写成 issue clarification、order lookup、tickets、human handoff；embodied intelligence 写成 voice commands、action execution、inspection、exception feedback；livestream assistant 写成 audience interaction、product explanation、coupons、risk reminders。 Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 1313435339 | F1 | verified |
| `repository.fullName` | QwenAudio/qwen-audio-agent | F1 | verified |
| `repository.name` | qwen-audio-agent | F1 | verified |
| `repository.stars` | 2335 | F1 | verified |
| `repository.forks` | 201 | F1 | verified |
| `repository.language` | JavaScript | F1 | verified |
| `repository.pushedAt` | 2026-09-04T05:24:27Z | F1 | verified |
| `repository.license` | Apache License 2.0 | F12 | verified |
| `repository.state` | active | F1 | inferred |
| `editorial.hook` | 让语音对话边聊边办事 | F3, F5, F6 | inferred |
| `editorial.summary` | 接入实时语音前端和可兼容 ACP 的后端 Agent，把语音聊天、工具调用、后台异步任务和结果回传放在同一条对话里 | F2, F3, F5, F6, F7, F13 | verified |
| `editorial.meaning` | 把前台不断线对话、后台持续执行、结果回到同一会话的能力做成可复用底座 | F2, F5, F6, F7, F8, F10, F11, F14 | inferred |
| `editorial.audience` | 需要用语音接入并协调后台 Agent 的桌面用户，以及做多端语音交互产品的开发者 | F7, F10, F13, F11 | inferred |
| `editorial.features` | 全双工实时语音互动和自然打断；可接入兼容 ACP 的后端 Agent，复用 model config、tools、MCP、Skills 和 authentication；前台对话与后台异步任务并行，支持进度查询和取消；多个独立任务可持续跟踪，结果自动回到当前对话；WebUI、TUI 和桌面浮窗入口；跨会话记忆和个人长期个性化 | F3, F4, F5, F6, F7, F8, F11, F13 | verified |
| `editorial.stack` | JavaScript、Node.js 22.22.2+ / 24.15.0+、ACP、MCP、DashScope realtime voice frontend、speech-to-speech frontend | F1, F4, F13 | verified |
| `editorial.opportunity` | 把实时语音、后台任务、跨会话记忆、多端入口和多模态输入，分别收窄到桌面办事、车内控制、客服接力、巡检执行和直播口播这些更窄场景 | F5, F6, F10, F11, F14 | inferred |

## Product inferences

- [I1] 这个仓库最核心的可复用能力，是把实时语音前台、后台 Agent 执行、状态回传和跨会话记忆拼成一条连续的工作流。 Basis: F2, F3, F4, F5, F6, F7, F8, F9. Confidence: high
- [I2] 它更像一个“对话不断线、任务继续跑”的运行时，而不是单纯的语音聊天界面。 Basis: F3, F5, F6, F7, F9. Confidence: high
- [I3] README 的场景扩展示例和最新版本的多模态、插件化能力，说明它可以稳定拆成更窄的场景产品。 Basis: F10, F11, F14. Confidence: medium
- [I4] 跨会话记忆和场景扩展说明，支持把它做成更强调持续陪伴或持续上下文的产品。 Basis: F8, F10. Confidence: medium

## Direction rationale

### D1 — 桌面语音任务台

- Reused capability: 全双工语音互动、异步任务、进度查询和取消、结果回流、跨会话记忆
- Evidence: F3, F5, F6, F7, F8, F9, F13
- New audience and recurring problem: 面向经常在桌面上边说边办事的个人用户和小团队，他们发完语音后还要反复催进度、补要求、等结果。
- Input and visible outcome: 原来是语音对话配后台任务，结果回到同一会话；这里是个人语音办事，最后得到的是可继续追问的任务完成回执。
- Original workflow: 用户在 WebUI、TUI 或桌面浮窗里持续语音对话，复杂操作交给后端 Agent，结果再回到原会话。
- New workflow: 用户用语音发起任务，系统把任务交给后端 Agent 异步处理，持续回报状态，完成后把结果带回当前对话。
- Materially changed axes: audience, workflow, outcome
- Product form: end-user-product
- Product boundary: 面向个人桌面办事，不做车载、客服或直播场景编排，也不把已有入口包装成单独 API。
- Substantive difference: 原项目是通用实时语音运行时，这个方向收窄成个人桌面办事台，只保留任务接力、进度追踪和结果回流。

### D2 — 客服接力台

- Reused capability: 前台对话和后台处理并行、结果回流、持续状态跟踪
- Evidence: F5, F6, F9, F10, F14
- New audience and recurring problem: 面向一线客服和售后坐席，他们常常要边接话边查信息，还要把需要人工处理的部分接稳。
- Input and visible outcome: 原来输入是个人语音任务，输出是任务结果回到对话；这里输入是客户咨询和单据线索，输出是连续答复和人工转接摘要。
- Original workflow: 用户在语音运行时里把任务交给后台 Agent，完成后结果回到当前会话。
- New workflow: 客服在同一段语音对话里接住问题，系统帮助澄清诉求、查单、整理工单，必要时把上下文交给人工坐席。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 面向客服接力，不做通用聊天机器人，也不把它简化成知识库查询界面。
- Substantive difference: 原项目强调个人任务接力，这里改成客服接力台，围绕 issue clarification、order lookup、tickets 和 human handoff 组织工作流。

### D3 — 直播口播助理

- Reused capability: 实时语音对话、后台任务协作、结果回流和持续上下文
- Evidence: F3, F5, F6, F9, F10, F14
- New audience and recurring problem: 面向直播间主播和场控，他们要一边讲产品一边回应观众，还要及时补充优惠和风险提醒。
- Input and visible outcome: 原来输入是个人语音任务，输出是后台结果；这里输入是直播口播和活动信息，输出是不断线的问答、提词和提醒。
- Original workflow: 用户在语音界面里交代任务，系统异步执行，完成后把结果回到原会话。
- New workflow: 主播边直播边提问，系统持续接住观众问题、补充商品说明、提醒优惠和风险，再把内容回填到口播节奏里。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 面向直播协作，不做客服工单或车载控制。
- Substantive difference: 原项目是通用语音运行时，这里变成直播口播助理，工作流围绕 audience interaction、product explanation、coupons 和 risk reminders 展开。

## Pairwise direction comparison

- 桌面语音任务台 vs 客服接力台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 前者处理个人语音办事，后者处理客服咨询接力；输入从个人任务变成问题、查单和工单，工作流从异步任务回流变成澄清、查询和转人工，结果也从任务完成回执变成客服接续摘要。
- 桌面语音任务台 vs 直播口播助理
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 前者围绕个人任务接力，后者围绕直播口播协作；输入从个人语音任务变成观众问题和商品信息，工作流从后台执行变成实时接话和提词，结果也从任务结果回到对话变成直播中的连续口播。
- 客服接力台 vs 直播口播助理
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 一个是客服接力，另一个是直播口播；前者接住咨询和工单，后者接住观众问题和商品说明，输出也分别是人工接续摘要和不断线的口播反馈。

## Uncertainty

- repository.state 由 archived=false、disabled=false 推断为 active。

## Localization decisions

- 保留 ACP、MCP、TUI、WebUI、API、Node.js、DashScope 这些基础术语，因为它们直接说明复用边界。
- 将 speech-to-speech frontend 保留为英文并在语境中解释为本地语音前端，避免硬造生僻中文短语。
- 将 Agent 译为 Agent，保留产品语境中的通用识别度。
- 将 human handoff 译为“人工转接”，将 exception feedback 译为“异常反馈”，以保持中文自然度。

## Refresh notes

- Initial research; no prior published snapshot.
