# snapotter-hq/SnapOtter research notes

Research date: 2026-09-03
Repository: https://github.com/snapotter-hq/SnapOtter
Research mode: new

## Snapshot

- Repository ID: 1195367387
- Repository full name: snapotter-hq/SnapOtter
- Repository name: SnapOtter
- Stars at fetch time: 2410
- Forks at fetch time: 118
- Primary language: TypeScript
- Latest push at fetch time: 2026-09-03T07:59:18Z
- License: GNU Affero General Public License v3.0
- Default branch: main
- README SHA: 0656e1f9a090dcfbd65d7437ae43b9dc2920b204
- Latest release: v2.2.0 / 2026-07-29T14:05:40Z
- Repository state: active
- Fetched at: 2026-09-03T08:44:24Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/snapotter-hq/SnapOtter — accessed 2026-09-03
- [S2] Official README — https://github.com/snapotter-hq/SnapOtter/blob/main/README.md — accessed 2026-09-03
- [S3] Latest official release — https://github.com/snapotter-hq/SnapOtter/releases/tag/v2.2.0 — accessed 2026-09-03
- [S4] Official repository license file — https://github.com/snapotter-hq/SnapOtter/blob/main/LICENSE — accessed 2026-09-03

## Verified repository facts

- [F1] 该仓库的 GitHub 仓库 ID 为 1195367387，当前仓库名为 snapotter-hq/SnapOtter，项目名为 SnapOtter。 Sources: S1
- [F2] README 将 SnapOtter 描述为开源、自托管的文件处理工具/基础设施，可通过 UI、REST API 和 pipelines 处理图片、视频、音频、PDF 与文档。 Sources: S2
- [F3] README 明确列出 200+ 工具，覆盖五类模态，并举出转换、压缩、裁剪、合并、OCR、转录、PDF 处理和表格/结构化文件转换等能力。 Sources: S2
- [F4] README 说明其本地 AI 能力包括去背景、图像放大、老照片修复与上色、擦除物体、人脸模糊、OCR、音频转录、自动生成视频字幕、扩展画布等，而且在自有硬件上运行。 Sources: S2
- [F5] README 说明提供基于图层的浏览器图像编辑器，并支持画笔、形状、调整、滤镜、曲线和快捷键。 Sources: S2
- [F6] README 说明支持 pipelines，可把工具串成可复用工作流，默认 20 步，并可导入导出为 JSON。 Sources: S2
- [F7] README 说明每个工具都可通过 REST API 调用，使用 API key 鉴权，并在 /api/docs 提供交互文档。 Sources: S2
- [F8] README 强调文件不会离开用户网络，并提供去元数据能力；同时说明可自托管，不依赖外部 SaaS。 Sources: S2
- [F9] README 说明快速启动可用单容器部署，生产环境可用 app + Postgres 17 + Redis 8 的 Compose 栈；S2 还说明支持 AMD64 和 ARM64。 Sources: S2
- [F10] README 说明支持 OIDC / SSO，可接入 Google、GitHub、Okta 或任意 OpenID Connect 提供方，并支持 21 种语言。 Sources: S2
- [F11] S1 显示主语言为 TypeScript，stars 为 2410，forks 为 118，默认分支为 main，仓库未归档、未禁用、不是 fork。 Sources: S1
- [F12] S1 的 pushed_at 为 2026-09-03T07:59:18Z。 Sources: S1
- [F13] S1 的仓库许可证识别为 GNU Affero General Public License v3.0（AGPL-3.0）；S4 的 LICENSE 文件也是 AGPL v3 正文。 Sources: S1, S4
- [F14] 最新发布 v2.2.0 的发布时间为 2026-07-29T14:05:40Z；发布说明提到新增 Rounded Crop、Remove GIF Background、两层 OCR、21 种语言文档/网站等。 Sources: S3

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 1195367387 | F1 | verified |
| `repository.fullName` | snapotter-hq/SnapOtter | F1 | verified |
| `repository.name` | SnapOtter | F1 | verified |
| `repository.stars` | 2410 | F11 | verified |
| `repository.forks` | 118 | F11 | verified |
| `repository.language` | TypeScript | F11 | verified |
| `repository.pushedAt` | 2026-09-03T07:59:18Z | F12 | verified |
| `repository.license` | AGPL-3.0 | F13 | verified |
| `repository.state` | active | F11 | verified |
| `editorial.hook` | 把图片、视频和PDF都留在本地处理 | F2, F8 | inferred |
| `editorial.summary` | 它是一个自托管多模态文件处理平台，支持 UI、REST API 与 pipelines，覆盖转换、压缩、OCR、转录、去元数据、图像编辑和本地 AI。 | F2, F3, F4, F5, F6, F7, F8 | verified |
| `editorial.meaning` | 其可复用价值在于把多模态文件处理、本地 AI、批处理和 API 接入统一进一套私有部署能力。 | F2, F3, F4, F6, F7, F8 | inferred |
| `editorial.audience` | 主要面向希望在自有网络内处理文件的自托管用户、团队管理员和需要通过 UI、API 或 pipeline 使用这些能力的人。 | F2, F7, F8, F10 | verified |
| `editorial.features` | 多模态文件处理、200+ 工具、浏览器图像编辑器、本地 AI、JSON pipelines、REST API、SSO 与多语言。 | F2, F3, F4, F5, F6, F7, F10 | verified |
| `editorial.stack` | TypeScript、Web UI、REST API、JSON pipelines、Postgres 17、Redis 8、Docker、本地 AI / OCR / 转录。 | F11, F7, F6, F9, F4 | verified |
| `editorial.opportunity` | 机会来自多模态处理、本地识别与转录、可复用 pipelines、API 接入与隐私内网部署边界。 | F2, F4, F6, F7, F8 | inferred |

## Product inferences

- [I1] 这个项目的核心不是某一个单点转换器，而是一套可在私有网络中复用的多模态文件处理底座。 Basis: F2, F3, F4, F6, F7, F8. Confidence: high
- [I2] 凡是需要“先识别、再整理、再导出”的资料型产品，都可能从其 OCR、转录、本地 AI 和 pipelines 能力中受益。 Basis: F4, F6, F8. Confidence: high
- [I3] 它既能被收束成面向终端用户的专用工作台，也能被包装成组织内部的受控处理层。 Basis: F6, F7, F8, F9. Confidence: medium
- [I4] 在公开页面中应把仓库许可证写为 AGPL-3.0；README 提到商业许可，但因未提供额外官方许可文件，不能把商业授权范围写成已验证事实。 Basis: F13. Confidence: medium

## Direction rationale

### D1 — 家庭记忆整理柜

- Reused capability: 复用原项目的多模态文件处理、OCR、音频转录、本地 AI 图像修复/上色、去元数据与 pipelines 能力。
- Evidence: F2, F3, F4, F5, F6, F8
- New audience and recurring problem: 家庭成员经常把老照片、扫描证件、家庭录音分散存在手机、网盘和聊天记录里，后续很难整理、检索和长期保存。
- Input and visible outcome: 输入是家庭老照片、扫描 PDF、图片里的文字、语音讲述或采访录音；输出是按人物、时间或主题整理好的可检索家庭记忆档案。
- Original workflow: 原项目用户上传或连接各种文件，按所需工具进行转换、压缩、OCR、转录、编辑或批处理，得到处理后的单个文件或流水线结果。
- New workflow: 家庭成员上传照片、扫描件和录音，产品用 OCR、音频转录、图片修复或上色、元数据清理与批处理流程做统一整理，再生成可搜索的家庭资料库与导出包。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 这是一个面向家庭资料保存的终端产品，边界是导入、整理、检索与导出家庭记忆资料，而不是开放式的全能文件处理台。
- Substantive difference: 原项目是通用型文件处理平台，用户主动挑选工具处理各种文件；这个方向把能力收束成“家庭资料导入—识别整理—生成家庭档案”的单一产品，不再强调通用工具库。

### D2 — 课程资料打包器

- Reused capability: 复用原项目的 PDF/文档转换、OCR、音频转录、视频字幕生成、批处理与 JSON pipelines。
- Evidence: F2, F3, F4, F6
- New audience and recurring problem: 老师、培训讲师和社群组织者常常要把讲义、录音、录屏和作业模板整理成可分发资料，但不同格式混杂，字幕、PDF 和压缩包常要分开处理。
- Input and visible outcome: 输入是讲义 PDF、课件文档、录音或录屏视频；输出是带文字提取、字幕、格式统一和压缩包导出的课程学习包。
- Original workflow: 原项目用户逐个或批量处理文件，自己决定选哪些工具、怎样串联 pipeline，再拿到各类处理结果。
- New workflow: 组织者上传课程资料，产品自动抽取 PDF/图片文字、转录音频、给视频生成字幕、把表格和文档转为统一格式，再按课程导出一套可下载资料包。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 这是一个教学资料打包产品，边界是课程资料整理、统一格式与发布，不覆盖原项目的大量通用编辑与 AI 工具选择界面。
- Substantive difference: 原项目提供通用工具与 API；这个方向围绕一次课程交付，把多种资料自动收束成统一学习包，结果是面向学员分发的成品。

### D3 — 文件脱敏工作台

- Reused capability: 复用原项目的 PDF 工具、OCR、图片与文档处理、元数据清理和批处理能力。
- Evidence: F2, F3, F4, F5, F8
- New audience and recurring problem: 社区服务站、学校行政或小型机构经常需要共享表单、证件扫描件和证明材料，但手工脱敏容易漏掉姓名、证件号或图片里的文字。
- Input and visible outcome: 输入是 PDF、扫描图片和常见文档；输出是去元数据、完成文字识别并做遮盖处理后的可共享文件。
- Original workflow: 原项目用户按单个工具需求处理文件，比如转换、压缩、OCR、编辑或批处理，结果是一般性的处理输出。
- New workflow: 办事人员上传待共享文件，产品先 OCR 识别扫描件文字，再清除元数据、执行 PDF 遮盖或导出安全副本，最后生成可下载和留档的脱敏版本。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 这是一个事务文件脱敏工作台，边界是检查、遮盖、清理和导出安全版本，不提供原项目那种开放式多模态创作和转换中心。
- Substantive difference: 原项目支持 PDF 编辑、OCR、去元数据与文件处理；这个方向把这些能力组合成专门的“安全共享前检查与脱敏”流程，目标结果是可发送的安全副本。

## Pairwise direction comparison

- 家庭记忆整理柜 vs 课程资料打包器
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: D1 面向需要整理与保护家庭资料的人，输入是扫描件、老照片与音频，结果是可检索的家庭记忆档案；D2 面向学校或培训组织者，输入是课件与录音录像，结果是可分发的学习包。两者在 audience、input、outcome 上都不同，核心 workflow 也分别偏向归档整理与教学打包。
- 家庭记忆整理柜 vs 文件脱敏工作台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: D1 的重点是家庭记忆资料归档；D4 面向社区志愿者或服务窗口，输入是表单与证件文件，结果是脱敏后的可共享版本。两者至少在 audience、workflow、outcome 上不同，输入也从记忆资料变为需脱敏的事务文件。
- 课程资料打包器 vs 文件脱敏工作台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: D2 把课程资料整理成学习包；D4 把表单与证件文件脱敏后再共享。两者在 audience、workflow、outcome 上均不同，输入对象也不同。

## Uncertainty

- README 声称项目为 AGPLv3 与商业许可证双授权，但提供的 S4 只有 AGPL-3.0 正文；未提供 LICENSING.md 或商业许可文本，因此不能验证商业授权边界。
- 未提供 repository.fetchedAt，无法在 fieldEvidence 中为该字段建立主张；因此本草稿只覆盖 schema 中可由现有证据验证的字段。

## Localization decisions

- 保留 pipelines、REST API、JSON、OCR、OIDC / SSO、Docker、Postgres、Redis 等词，因为它们直接影响产品理解与复用判断。
- 将 self-hosted 译为“自托管”，将 local AI 译为“本地 AI”，并在上下文中说明是在自有硬件或自有网络内运行。
- hook 避免直译成“文件处理基础设施”，改写成用户更容易理解的“把图片、视频和PDF都留在本地处理”。

## Refresh notes

- Initial research; no prior published snapshot.
