# tldraw/tldraw research notes

Research date: 2026-09-04
Repository: https://github.com/tldraw/tldraw
Research mode: new

## Snapshot

- Repository ID: 365739812
- Repository full name: tldraw/tldraw
- Repository name: tldraw
- Stars at fetch time: 50117
- Forks at fetch time: 3495
- Primary language: TypeScript
- Latest push at fetch time: 2026-09-03T17:19:50Z
- License: tldraw license
- Default branch: main
- README SHA: c046510d2708142d9538bb62649383c1f3abb728
- Latest release: v5.4.0 / 2026-09-02T11:04:14Z
- Repository state: active
- Fetched at: 2026-09-04T05:47:05Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/tldraw/tldraw — accessed 2026-09-04
- [S2] Official README — https://github.com/tldraw/tldraw/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/tldraw/tldraw/releases/tag/v5.4.0 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/tldraw/tldraw/blob/main/LICENSE.md — accessed 2026-09-04

## Verified repository facts

- [F1] 仓库是 tldraw/tldraw，GitHub 数字 ID 为 365739812。 Sources: S1
- [F2] 仓库当前有 50117 个 star、3495 个 fork。 Sources: S1
- [F3] 仓库的主要语言是 TypeScript。 Sources: S1
- [F4] 仓库默认分支是 main，最近一次 push 时间为 2026-09-03T17:19:50Z，且未归档、未禁用、不是 fork。 Sources: S1
- [F5] 官方 LICENSE.md 写明这是 tldraw license，允许开发环境使用，但生产环境需要 license key；GitHub 检测到的许可证身份为 Other/NOASSERTION。 Sources: S1, S4
- [F6] README 将项目定位为给 React 应用构建无限画布的 tldraw SDK，并称其为可作为任意画布应用基础的完整引擎。 Sources: S2
- [F7] SDK 支持自定义 shapes、tools、bindings 和 UI 组件，也保留默认白板工具集。 Sources: S2
- [F8] SDK 提供可自托管的实时多人协作，基于 @tldraw/sync。 Sources: S2
- [F9] SDK 提供绘图和图表能力，包括压感绘制、几何图形、富文本、箭头、吸附、边缘滚动、图片和视频支持，以及图片导出。 Sources: S2
- [F10] SDK 公开运行时 Editor API。 Sources: S2
- [F11] SDK 支持 side effects 和 event hooks 等扩展点。 Sources: S2
- [F12] SDK 提供 AI integrations。 Sources: S2
- [F13] SDK 的 DOM canvas 能嵌入网页内容，包括 YouTube、Figma、GitHub 等。 Sources: S2
- [F14] SDK 能在桌面、触屏、平板和移动设备上的浏览器里工作。 Sources: S2
- [F15] README 还列出 starter kits：multiplayer、Agent、Workflow、Chat、Image pipeline、Branching chat 和 Shader。 Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 365739812 | F1 | verified |
| `repository.fullName` | tldraw/tldraw | F1 | verified |
| `repository.name` | tldraw | F1 | verified |
| `repository.stars` | 50117 | F2 | verified |
| `repository.forks` | 3495 | F2 | verified |
| `repository.language` | TypeScript | F3 | verified |
| `repository.pushedAt` | 2026-09-03T17:19:50Z | F4 | verified |
| `repository.license` | tldraw license | F5 | verified |
| `repository.state` | active | F4 | inferred |
| `editorial.hook` | 给 React 应用装上可协作的无限画布 | F6, F7, F8 | inferred |
| `editorial.summary` | tldraw 是给 React 应用接入无限画布的 SDK，支持自定义 shapes、tools、bindings、UI 组件、多人协作、绘图、Editor API、AI 和网页嵌入。 | F6, F7, F8, F9, F10, F12, F13 | verified |
| `editorial.meaning` | 这些能力构成可复用的画布底座，适合衍生出评审板、课堂黑板、研究整理板和分支叙事图等新产品。 | F6, F7, F8, F9, F10, F11, F12, F13 | inferred |
| `editorial.audience` | 用 React 做画布应用、白板工具和交互编辑器的开发者 | F6, F8, F9, F14, F15 | inferred |
| `editorial.features` | 无限画布引擎；自定义 shapes/tools/bindings/UI 组件；多人实时协作；绘图、几何图形、文本、箭头、图片/视频和导出；运行时 Editor API；AI integrations 和网页嵌入 | F7, F8, F9, F10, F12, F13 | verified |
| `editorial.stack` | TypeScript、React、@tldraw/sync、Cloudflare Durable Objects | F3, F6, F8, F15 | verified |
| `editorial.opportunity` | 自定义画布组件、协作同步、媒体嵌入和 AI/运行时控制，说明它适合做多种窄产品。 | F7, F8, F9, F10, F11, F12, F13, F15 | inferred |

## Product inferences

- [I1] tldraw 的核心可复用能力不是单一白板页面，而是一套可组合的无限画布底座。 Basis: F6, F7, F8, F9, F10, F11, F12, F13. Confidence: high
- [I2] 它的主要受众是需要在 React 里构建画布型体验的开发者。 Basis: F6, F15. Confidence: high
- [I3] 这些能力足以支撑多个彼此不同的成品画布产品，而不只是一个通用 SDK 外壳。 Basis: F7, F8, F9, F10, F12, F13. Confidence: high

## Direction rationale

### D1 — 评审批注板

- Reused capability: 无限画布、多人协作、自定义形状与 UI、图像导出
- Evidence: F6, F7, F8, F9, F10, F11, F14
- New audience and recurring problem: 设计师、产品经理和客户评审团队常把反馈散在聊天、文档和图片里，修改点难以统一回看。
- Input and visible outcome: 原流程是开发者用 React 组合 SDK 能力，做出可嵌入的画布应用；新流程是评审者把截图和草图放进画布，现场批注后得到一张可导出的评审板。
- Original workflow: 开发者在 React 应用里接入 tldraw SDK，组合 shapes、tools、bindings 和 UI 组件，得到可嵌入的无限画布应用。
- New workflow: 评审者导入截图、草图和说明，在无限画布上画箭头、写文字、多人同步修改，再导出。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做评审批注、协作留痕和导出，不做通用画布 SDK。
- Substantive difference: 原项目面向 React 开发者把画布能力集成进应用；这个方向面向方案确认场景，把成品画布变成可留痕的评审板。

### D2 — 互动课堂黑板

- Reused capability: 手写绘制、图形与媒体插入、实时协作、跨设备支持
- Evidence: F6, F7, F8, F9, F13, F14
- New audience and recurring problem: 老师、培训讲师和助教需要把讲解、板书和学生标注放在同一处，否则课堂互动容易被切碎。
- Input and visible outcome: 原流程是开发者把画布能力嵌进 React 应用；新流程是老师输入题目、板书和视频，在课堂里边讲边画，最后得到可回看的讲义黑板。
- Original workflow: 开发者在 React 里接入 SDK，定义 shapes、tools、bindings 和 UI 组件，生成通用画布应用。
- New workflow: 老师在大屏或平板上写字、画几何图形、插入图片和视频，学生可同步标注，课后导出讲义。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做课堂讲解、互动标注和讲义导出，不做通用开发框架。
- Substantive difference: 原项目服务开发者组装画布；这个方向服务课堂现场使用，把画布变成互动黑板。

### D3 — 家庭记忆墙

- Reused capability: 照片/视频处理、多人协作、导出与跨设备显示
- Evidence: F6, F8, F9, F13, F14
- New audience and recurring problem: 家庭成员、朋友小组和活动组织者常把旅行、聚会和成长素材散在相册与聊天里，难以一起回看。
- Input and visible outcome: 原流程是开发者把 tldraw 作为组件接进 React 应用；新流程是家人把照片和视频拖进画布，共同补记说明，最后得到一面可分享的回忆墙。
- Original workflow: 开发者组合 shapes、tools、UI 组件和协作能力，做出通用画布应用。
- New workflow: 多人把照片和视频拖到无限画布，补上文字、箭头和位置关系，一起整理并导出。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做家庭记忆拼贴、共同整理和分享，不做通用白板 SDK。
- Substantive difference: 原项目面向开发者集成画布；这个方向面向日常记忆整理，把协作画布变成家庭记忆墙。

## Pairwise direction comparison

- 评审批注板 vs 互动课堂黑板
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 评审批注板更像设计/方案确认工具，互动课堂黑板更像教学讲解工具；前者输入是截图和草图，后者输入是题目、板书和视频，工作流与输出也不同。
- 评审批注板 vs 家庭记忆墙
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 评审批注板围绕设计确认，家庭记忆墙围绕日常回忆；输入从截图/草图换成照片/视频，流程从修改意见协作换成拼贴整理，输出也从评审留痕换成记忆墙。
- 互动课堂黑板 vs 家庭记忆墙
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 互动课堂黑板服务课堂互动，家庭记忆墙服务家庭保存；输入从教学内容换成照片视频，流程从边讲边画换成共同整理，输出也从讲义板换成回忆墙。

## Uncertainty

- GitHub metadata 的 license 识别为 Other/NOASSERTION，而 LICENSE.md 明确写的是 tldraw license；本稿采用官方 LICENSE.md 的表述，并保留这一识别差异。

## Localization decisions

- 保留 React、SDK、API、AI、DOM、Cloudflare Durable Objects、TypeScript 等术语，因为它们直接影响复用判断。
- 将 canvas 统一表达为“画布”，将 whiteboarding tool set 处理为“白板工具集”。

## Refresh notes

- Initial research; no prior published snapshot.
