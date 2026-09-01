# HKUDS/nanobot research notes

Research date: 2026-09-01
Repository: https://github.com/HKUDS/nanobot
Research mode: new

## Snapshot

- Repository ID: 1147094660
- Repository full name: HKUDS/nanobot
- Repository name: nanobot
- Stars at fetch time: 47606
- Forks at fetch time: 8404
- Primary language: Python
- Latest push at fetch time: 2026-09-01T12:19:34Z
- License: MIT License
- Default branch: main
- README SHA: 244ee0fcf54e5fd46c42852289aea2c617d2beb5
- Latest release: v0.3.0 / 2026-07-25T08:08:47Z
- Repository state: active
- Fetched at: 2026-09-01T13:15:32Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/HKUDS/nanobot — accessed 2026-09-01
- [S2] Official README — https://github.com/HKUDS/nanobot/blob/main/README.md — accessed 2026-09-01
- [S3] Latest official release — https://github.com/HKUDS/nanobot/releases/tag/v0.3.0 — accessed 2026-09-01

## Verified repository facts

- [F1] GitHub 仓库 ID 为 1147094660，规范名为 HKUDS/nanobot，项目名 nanobot，默认分支是 main，主页是 https://nanobot.wiki Sources: S1
- [F2] 仓库的 Star 数为 47606，Fork 数为 8404，主语言是 Python Sources: S1
- [F3] 仓库当前状态为未归档、未禁用、非 fork，许可证是 MIT；最新推送时间为 2026-09-01T12:19:34Z Sources: S1
- [F4] nanobot 是一个 ultra-lightweight、open-source、self-hosted 的个人 AI agent framework，使用 Python 编写 Sources: S2
- [F5] nanobot 可在 WebUI、终端或聊天应用中运行，并结合 tools、long-term memory、MCP integrations、model routing、multi-agent delegation、scheduled automation 和 OpenAI-compatible API Sources: S2
- [F6] nanobot 能连接 Telegram、Discord、Slack、WeChat、Email、Mattermost 等聊天应用，并使用 files、shell、web search、web fetch、MCP、cron、image generation、subagents；还通过 Dream 提供长期记忆、长航程目标和 Python SDK Sources: S2
- [F7] WebUI 随发布 wheel 一起提供，没有单独的 frontend build；它承载 persistent topics、temporary chats、visible agent activity、workspace controls、Apps、Skills、Automations 和 settings Sources: S2
- [F8] 最新 release v0.3.0 强调 guided WebUI setup、inline subagents、按 session 切换 model presets、live configuration reloads，以及更稳的 deployment/runtime Sources: S3
- [F9] v0.3.0 的发布说明把 nanobot 描述为一个能够协调 helpers、按 session 切换模型、并把授权工作持续完成的 agent runtime Sources: S3

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 1147094660 | F1 | verified |
| `repository.fullName` | HKUDS/nanobot | F1 | verified |
| `repository.name` | nanobot | F1 | verified |
| `repository.stars` | 47606 | F2 | verified |
| `repository.forks` | 8404 | F2 | verified |
| `repository.language` | Python | F2, F4 | verified |
| `repository.pushedAt` | 2026-09-01T12:19:34Z | F3 | verified |
| `repository.license` | MIT | F3 | verified |
| `repository.state` | active | F3 | verified |
| `editorial.hook` | 把聊天、文件和工具结果收成一条工作线 | F4, F5, F7, F9 | inferred |
| `editorial.summary` | nanobot 是用 Python 写的自托管个人 AI agent 框架，可在 WebUI、终端和聊天应用里接入模型、工具、长期记忆和 MCP。它会把对话、文件操作、工具调用和自动化结果留在同一条可回看的会话里，并可通过 OpenAI-compatible API 和 Python SDK 接到外部系统。 | F4, F5, F6, F7, F9 | verified |
| `editorial.meaning` | 这套能力的价值在于把聊天、工具、记忆和自动化放进同一个可持久运行的核心里，适合拆成更专注的前台入口或专用流程。 | F5, F6, F7, F9 | inferred |
| `editorial.audience` | 想把个人 AI agent 自托管到 WebUI、终端或聊天应用里的人 | F4, F5, F6, F7 | inferred |
| `editorial.features` | 可在 WebUI、终端和聊天应用里运行；接入 tools、MCP、web search、web fetch、cron、image generation 和 subagents；长期记忆与长航程目标；OpenAI-compatible API；Python SDK 和模型路由 | F5, F6, F7, F8, F9 | verified |
| `editorial.stack` | Python、WebUI、MCP、OpenAI-compatible API | F4, F5, F6, F7 | verified |
| `editorial.opportunity` | 可拆出任务交接包、模型试配台和长期跟进管家三类更窄产品 | F5, F6, F7, F8, F9 | inferred |

## Product inferences

- [I1] nanobot 的核心不是单一聊天机器人，而是一个可自托管的个人 AI agent 运行时，能把渠道、工具、记忆和自动化放在一起。 Basis: F4, F5, F6, F7, F9. Confidence: high
- [I2] 它的主要使用者是希望在 WebUI、终端或聊天应用里直接使用并掌控这套 agent 的人，而不是只想拿到一个单点 API 的开发者。 Basis: F5, F6, F7. Confidence: high
- [I3] 可复用的能力单位很清楚：WebUI、chat apps 接入、工具调用、长期记忆、自动化和模型路由，因此适合拆成更窄的前台产品。 Basis: F5, F6, F7, F9. Confidence: high
- [I4] 三条方向都成立，因为它们分别改变了输入来源、目标用户、工作流和可见结果，而不是只换一个界面或文件类型。 Basis: F5, F6, F7, F8, F9. Confidence: high

## Direction rationale

### D1 — 任务交接包

- Reused capability: 复用 WebUI 的 persistent topics、visible agent activity、文件 diff 和 workspace controls。
- Evidence: F5, F7, F9
- New audience and recurring problem: 面向经常把一个任务交给别人、或者隔一段时间还要自己接着做的人；他们需要的不是继续聊天，而是把已发生的对话、文件改动和工具结果整理成一份能交接的记录。
- Input and visible outcome: 原流程：用户在 WebUI、终端或聊天应用里发起对话 → 运行时调工具、记忆和模型 → 得到回复或自动化结果。新流程：用户把一个 topic 里的聊天、文件和工具痕迹交给系统 → 系统借用可见 agent activity、文件 diff 和 workspace 控制整理成交接包 → 用户拿到可分享的项目摘要。
- Original workflow: 多入口 agent runtime：WebUI/终端/聊天应用 → 工具/记忆/MCP/模型路由/自动化 → 回复或执行结果。
- New workflow: 把 persistent topics、visible agent activity、文件 diff 和 workspace controls 组合成一条可导出的交接记录。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做可分享的交接材料，不承担全渠道接入、长跑 gateway 或通用 agent 编排。
- Substantive difference: 原项目是通用个人 AI agent 运行时，这里收窄成任务交接包，只解决整理、摘要和导出。

### D2 — 模型试配台

- Reused capability: 复用 model routing、session 级 model preset 切换和 fallback 机制。
- Evidence: F5, F8, F9
- New audience and recurring problem: 面向要在真正开始工作前先挑对模型的人，比如独立开发者或小团队里负责配置 AI 的人；他们常常需要比较不同 provider、fallback 和 session preset 的差异，而不是只跑一次普通对话。
- Input and visible outcome: 原流程：用户在 WebUI 或终端里选择模型并继续任务 → 运行时按 session 路由到合适模型 → 得到一段正常的 agent 结果。新流程：用户输入同一提示词并选几组 model preset → 系统复用 session 切换和 routing 跑出对照结果 → 用户得到可比较的模型表现和首选配置。
- Original workflow: 通用 agent runtime：单次任务执行 + 模型路由 + 工具调用 → 输出结果。
- New workflow: 把 model routing、按 session 切换 preset 和 fallback 变成一个专门的对照体验，用来比较模型输出并保存偏好。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做模型试配和对照，不把整套 WebUI、gateway 或后端 runtime 重新包装成另一个 API 服务。
- Substantive difference: 原项目把 model routing 用在一个 agent 运行时里，这里收窄成模型试配台，专门做同题对照和选型。

### D3 — 长期跟进管家

- Reused capability: 复用 long-term memory、scheduled automations 和 long-horizon goals。
- Evidence: F5, F6, F8, F9
- New audience and recurring problem: 面向要替家人、课程或个人项目持续跟进的人；他们面对的不是一次性问答，而是隔几天还得继续检查、提醒和记录进度。
- Input and visible outcome: 原流程：用户发起对话或任务 → agent 调工具、记忆和自动化 → 返回一次性回复或执行结果。新流程：用户输入目标、期限和上下文 → 系统用 goals、cron 和 Dream 反复检查并提醒 → 用户收到进度更新、待办或完成通知。
- Original workflow: 通用 agent runtime：即时对话/工具调用/自动化执行 → 一次性结果。
- New workflow: 把 long-horizon goals、scheduled automations、Dream 和记忆历史串起来，持续追踪同一个目标并在合适时间提醒。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做持续跟进与提醒，不承担多渠道通用聊天入口或复杂项目工作台。
- Substantive difference: 原项目处理的是通用对话和即时任务，这里收窄成单目标的持续跟进。

## Pairwise direction comparison

- 任务交接包 vs 模型试配台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 任务交接包面向要把一段 agent 工作交出去的人，模型试配台面向先选对模型的人；前者吃进去的是一个 topic 的聊天、文件和工具痕迹，后者吃进去的是同一提示词和多个 model preset。
- 任务交接包 vs 长期跟进管家
  - Different axes: input, workflow, outcome
  - Concrete comparison: 任务交接包强调整理与导出可分享的工作记录，长期跟进管家强调反复检查、提醒和回报进度；一个产出交接材料，一个产出持续通知。
- 模型试配台 vs 长期跟进管家
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 模型试配台处理的是同一请求在多个模型间的对照，长期跟进管家处理的是跨天的目标推进；一个围绕选型和比较，一个围绕定时追踪和完成。

## Uncertainty

- None.

## Localization decisions

- 保留 WebUI、MCP、OpenAI-compatible API、Python SDK 等基础术语；Dream 作为项目内记忆模块名不翻译。
- 将 self-hosted 译为“自托管”，agent 译为“AI agent”，multi-agent 译为“多 agent”以保持产品语义。

## Refresh notes

- Initial research; no prior published snapshot.
