# tejaswigowda/ffmpeg-webCLI research notes

Research date: 2026-09-03
Repository: https://github.com/tejaswigowda/ffmpeg-webCLI
Research mode: new

## Snapshot

- Repository ID: 1254696756
- Repository full name: tejaswigowda/ffmpeg-webCLI
- Repository name: ffmpeg-webCLI
- Stars at fetch time: 1406
- Forks at fetch time: 128
- Primary language: JavaScript
- Latest push at fetch time: 2026-09-03T01:41:12Z
- License: GNU General Public License v3.0
- Default branch: main
- README SHA: 766cd05f7a52c59035b6d682a8e7d983b07bee56
- Latest release: v2.0.0 / 2026-06-23T04:51:03Z
- Repository state: active
- Fetched at: 2026-09-03T08:44:24Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/tejaswigowda/ffmpeg-webCLI — accessed 2026-09-03
- [S2] Official README — https://github.com/tejaswigowda/ffmpeg-webCLI/blob/main/README.md — accessed 2026-09-03
- [S3] Latest official release — https://github.com/tejaswigowda/ffmpeg-webCLI/releases/tag/v2.0.0 — accessed 2026-09-03
- [S4] Official repository license file — https://github.com/tejaswigowda/ffmpeg-webCLI/blob/main/LICENSE — accessed 2026-09-03

## Verified repository facts

- [F1] 该仓库的 GitHub ID 为 1254696756，完整名称为 tejaswigowda/ffmpeg-webCLI，仓库名为 ffmpeg-webCLI。 Sources: S1
- [F2] 仓库主语言为 JavaScript；Star 1406，Fork 128；最新 push 时间为 2026-09-03T01:41:12Z；仓库未归档、未禁用、不是 fork。 Sources: S1
- [F3] README 将项目描述为基于 ffmpeg.wasm 的浏览器视频编辑器，强调无上传、无服务器，所有处理都在浏览器本地完成。 Sources: S2
- [F4] README 说明项目支持 30+ 种视频操作，包括 GIF 生成、格式转换、压缩、裁切、效果、滤镜、自动字幕等。 Sources: S2, S3
- [F5] README 说明项目支持批量处理：可对多个视频应用同一操作或整条操作链，提供实时进度、逐文件预览、单独下载和 ZIP-All。 Sources: S2, S3
- [F6] README 说明项目支持链式操作（Stack mode），可把多个兼容操作合成为一次编码，并显示实时组合命令预览。 Sources: S2, S3
- [F7] README 说明自动字幕功能使用 Whisper 与 Transformers.js 在浏览器内完成转写，用户可编辑字幕，再选择软字幕或硬字幕嵌入。 Sources: S2, S3
- [F8] README 说明项目是离线优先的 PWA，首次加载后可离线使用，并使用 service worker 缓存资源、用 Web Workers 保持处理时界面响应。 Sources: S2, S3
- [F9] README 说明项目提供浏览器内原始 ffmpeg 命令输入、实时完整命令预览、示例命令库，并可选第二输入文件。 Sources: S2
- [F10] README 说明项目支持多输入操作与多格式处理，包括拼接、并排、画中画、音频混合，以及多种视频、音频、图片格式。 Sources: S2
- [F11] README 明确建议在文件私密、无法安装软件或单纯不想上传到云端时使用该项目。 Sources: S2
- [F12] GitHub 元数据与官方 LICENSE 文件都标识该仓库许可证为 GNU General Public License v3.0（GPL-3.0）。 Sources: S1, S4

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 仓库 GitHub ID 为 1254696756。 | F1 | verified |
| `repository.fullName` | 仓库完整名称为 tejaswigowda/ffmpeg-webCLI。 | F1 | verified |
| `repository.name` | 项目名为 ffmpeg-webCLI。 | F1 | verified |
| `repository.stars` | Star 数为 1406。 | F2 | verified |
| `repository.forks` | Fork 数为 128。 | F2 | verified |
| `repository.language` | 主语言为 JavaScript。 | F2 | verified |
| `repository.pushedAt` | 最新 push 时间为 2026-09-03T01:41:12Z。 | F2 | verified |
| `repository.license` | 许可证为 GPL-3.0。 | F12 | verified |
| `repository.state` | 仓库处于可用状态，未归档、未禁用。 | F2 | verified |
| `editorial.hook` | 项目最突出的产品变换是把私密视频处理放在浏览器本地完成。 | F3, F7, F8 | inferred |
| `editorial.summary` | 摘要将说明本地媒体输入、浏览器内处理、预览下载，以及自动字幕、批量、链式与原始命令等能力。 | F3, F4, F5, F6, F7, F8, F9, F10 | verified |
| `editorial.meaning` | 改造价值在于它已经把本地媒体处理、批量执行、字幕与离线能力连成一条可复用管线。 | F3, F5, F6, F7, F8 | inferred |
| `editorial.audience` | 原项目主要面向不想上传私密文件、无法安装软件或偏好本地处理的人。 | F11 | verified |
| `editorial.features` | 功能列表将覆盖本地处理、30+ 操作、批量、链式、本地字幕与原始 ffmpeg/多输入能力。 | F3, F4, F5, F6, F7, F9, F10 | verified |
| `editorial.stack` | 技术栈将列出 JavaScript、ffmpeg.wasm、WebAssembly、Web Workers、PWA/Service Worker、Transformers.js/Whisper。 | F2, F3, F7, F8 | verified |
| `editorial.opportunity` | 机会点将围绕隐私本地处理、批量标准化、字幕闭环和多素材成片能力展开。 | F3, F5, F6, F7, F10, F11 | inferred |

## Product inferences

- [I1] 该项目的可复用核心不是单个编辑功能，而是一条已完成的浏览器端媒体处理管线：本地读写、ffmpeg 执行、预览、批量与导出都已经打通。 Basis: F3, F4, F5, F6, F8. Confidence: high
- [I2] 批量处理与链式操作让它不仅适合一次性编辑，也适合需要反复应用同一规则的标准化处理产品。 Basis: F5, F6. Confidence: high
- [I3] 本地自动字幕与不上传定位，使它特别适合被收窄为面向敏感录音录像的字幕审校类产品。 Basis: F3, F7, F11. Confidence: high
- [I4] 原始命令预览与多输入操作说明它可以承载模板化的专用工作台，而不只是一组预设按钮。 Basis: F9, F10. Confidence: medium
- [I5] GPL-3.0 允许继续修改和分发，但基于它分发修改版本时需要遵守相应 copyleft 条款。 Basis: F12. Confidence: high

## Direction rationale

### D1 — 访谈字幕审校台

- Reused capability: 复用本地处理、Whisper 自动字幕、字幕编辑与软/硬字幕嵌入能力。
- Evidence: F3, F7, F8, F11
- New audience and recurring problem: README 已验证本地自动字幕、字幕编辑与软/硬字幕嵌入能力；这使它适合需要整理访谈、会议或口语录音的人，他们常常想先在本地转写，再人工校对后发布。
- Input and visible outcome: 输入从泛用本地媒体文件收窄为单段访谈或会议录像；输出从各种媒体处理结果收窄为 SRT、软字幕视频和硬字幕视频。
- Original workflow: 不想上传私密视频的用户 + 本地媒体文件 → 在浏览器里选择一种或多种 ffmpeg 操作、可批量处理并预览 → 得到处理后的视频、音频、GIF 或图片文件
- New workflow: 需要整理口语视频的人 + 单个录像 → 本地提取音频、用 Whisper 转写、人工校对字幕、选择软字幕或硬字幕导出 → 得到可交付的字幕文件和带字幕视频
- Materially changed axes: audience, workflow, outcome
- Product form: end-user-product
- Product boundary: 用户面对的是完整的字幕交付体验，而不是一组分散的编辑按钮；核心能力被组织成一个围绕字幕成品的流程。
- Substantive difference: 原项目是通用浏览器视频工具箱；这个方向把边界收窄成“转写—审校—导出字幕”的专用工作台。

### D2 — 课程视频批量定型器

- Reused capability: 复用批量队列、链式操作、单次编码、多格式导出与预览下载能力。
- Evidence: F4, F5, F6, F8
- New audience and recurring problem: README 和发布说明已验证批量处理、链式操作、逐文件预览和 ZIP-all 导出；这适合经常要把一批课程或培训视频统一成同一规格的人。
- Input and visible outcome: 输入从任意本地媒体文件变成一批课程或教程视频；输出从单次处理结果变成规格一致、可逐个检查的成片。
- Original workflow: 不想上传私密视频的用户 + 本地媒体文件 → 在浏览器里选择一种或多种 ffmpeg 操作、可批量处理并预览 → 得到处理后的视频、音频、GIF 或图片文件
- New workflow: 录制系列课程的人 + 一批视频和一套链式处理规则 → 批量排队、按同一规则处理每个文件、逐个预览并下载或 ZIP 打包 → 得到整批规格统一的视频成片
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 产品边界是“批量定型工作台”；用户维护的是一套统一处理规则和交付结果，而不是通用编辑器里的所有按钮。
- Substantive difference: 原项目允许用户自由组合单步和多步操作；这个方向把它改造成面向整批课程素材的批处理产品，重点是统一规则而不是自由试验。

### D3 — 成长片段卡片机

- Reused capability: 复用裁切、GIF 生成、缩略图提取、循环处理、批量预览与下载能力。
- Evidence: F4, F5
- New audience and recurring problem: README 已验证 GIF、缩略图、循环和裁切能力；这些能力可重组为从长视频里提炼可分享瞬间的家庭向工具。
- Input and visible outcome: 输入从泛用视频文件变成家庭回忆、旅行或成长记录；输出从任意处理结果收窄为 GIF、缩略图和循环短片。
- Original workflow: 不想上传私密视频的用户 + 本地媒体文件 → 在浏览器里选择一种或多种 ffmpeg 操作、可批量处理并预览 → 得到处理后的视频、音频、GIF 或图片文件
- New workflow: 想整理家庭回忆的人 + 一段或一批家庭视频 → 标记几个时间点、裁切片段、生成 GIF 或缩略图、导出循环短片 → 得到便于发给亲友的小内容
- Materially changed axes: audience, workflow, outcome
- Product form: end-user-product
- Product boundary: 它不是通用剪辑器，而是一个专门帮用户从长视频里提炼“值得分享的瞬间”的家庭整理产品。
- Substantive difference: 原项目是通用媒体处理器；这个方向只保留“挑瞬间、做轻量分享物”的流程，把结果从通用文件转成适合聊天发送的小内容。

## Pairwise direction comparison

- 访谈字幕审校台 vs 课程视频批量定型器
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 访谈字幕审校台面向需要整理口语视频的人，输入是一段访谈或会议录像；课程批量定型器面向要统一整批课程素材的人，输入是一批视频和同一套处理规则。前者的核心工作流是转写、校对、嵌字，后者是批量排队、链式处理、逐个预览与打包导出。
- 访谈字幕审校台 vs 成长片段卡片机
  - Different axes: input, workflow, outcome
  - Concrete comparison: 访谈字幕审校台主要处理单段口语内容；成长片段卡片机主要从家庭素材里挑出几个值得保留的瞬间。前者的结果是字幕文件和带字幕视频，后者的结果是 GIF、缩略图和循环短片。
- 课程视频批量定型器 vs 成长片段卡片机
  - Different axes: audience, workflow, outcome
  - Concrete comparison: 课程批量定型器把同一套规则应用到整批课程视频；成长片段卡片机把长视频提炼成可转发的小片段。前者输出整批统一成片，后者输出面向亲友分享的动图和封面图。

## Uncertainty

- 除 README、发布说明与许可证文件外，未提供其他官方文档来源；因此所有产品理解都以这些一手材料为边界。

## Localization decisions

- 保留 ffmpeg.wasm、WebAssembly、Whisper、PWA、Web Workers、service worker 等术语，因为它们直接影响读者对本地处理、离线能力和可复用方式的理解。
- 将 hard-burn 译为“硬字幕”或“烧录进画面”，避免直译造成理解负担。
- 将 Stack mode 译为“链式操作”，因为 README 描述的是把多个兼容操作合成为一次处理流程。

## Refresh notes

- Initial research; no prior published snapshot.
