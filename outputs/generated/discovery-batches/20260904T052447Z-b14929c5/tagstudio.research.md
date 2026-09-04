# TagStudioDev/TagStudio research notes

Research date: 2026-09-04
Repository: https://github.com/TagStudioDev/TagStudio
Research mode: new

## Snapshot

- Repository ID: 787908531
- Repository full name: TagStudioDev/TagStudio
- Repository name: TagStudio
- Stars at fetch time: 7166
- Forks at fetch time: 465
- Primary language: Python
- Latest push at fetch time: 2026-09-03T23:48:11Z
- License: GNU General Public License v3.0
- Default branch: main
- README SHA: 57b2d3b94e7ad6d049681825386e30bc3ee8a7f8
- Latest release: v9.6.3 / 2026-08-15T21:11:51Z
- Repository state: active
- Fetched at: 2026-09-04T06:17:55Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/TagStudioDev/TagStudio — accessed 2026-09-04
- [S2] Official README — https://github.com/TagStudioDev/TagStudio/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/TagStudioDev/TagStudio/releases/tag/v9.6.3 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/TagStudioDev/TagStudio/blob/main/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] repository.githubId / repository.fullName / repository.name 分别是 787908531、TagStudioDev/TagStudio、TagStudio Sources: S1
- [F2] repository.stars = 7166，repository.forks = 465，repository.pushedAt = 2026-09-03T23:48:11Z Sources: S1
- [F3] repository.language 是 Python Sources: S1
- [F4] repository.state 为 active：未归档、未禁用、非 fork Sources: S1
- [F5] repository.license 是 GPL-3.0 Sources: S4, S1
- [F6] TagStudio 是一个面向用户的照片与文件管理应用，采用基于标签的系统，不要求把文件搬走、复制或依赖 sidecar 文件 Sources: S2
- [F7] library 叠加在现有系统目录之上，条目和标签数据存放在 .TagStudio 里的 SQLite 数据库中 Sources: S2
- [F8] library 支持所有文件类型；已说明的预览和播放包括图片、视频、音频、文本、文档、电子书、PSD、Blender、Krita 等 Sources: S2
- [F9] 标签支持 name、shorthand name、aliases、color、parent tags 和 is category Sources: S2
- [F10] 字段支持 text lines、text boxes 和 datetimes Sources: S2
- [F11] 搜索支持 tag、path、filetype、mediatype、AND/OR/NOT、括号、special:untagged 和 special:empty；还能处理 moved/unlinked entries Sources: S2
- [F12] v9.6.3 改进了 tag/field search bars 的默认展开、横向滚动、Tab 导航和提示图标，并修复了部分刷新与颜色问题 Sources: S3
- [F13] 视频缩略图和播放需要 FFmpeg，快速扫描与刷新建议安装 ripgrep Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 787908531 | F1 | verified |
| `repository.fullName` | TagStudioDev/TagStudio | F1 | verified |
| `repository.name` | TagStudio | F1 | verified |
| `repository.stars` | 7166 | F2 | verified |
| `repository.forks` | 465 | F2 | verified |
| `repository.language` | Python | F3 | verified |
| `repository.pushedAt` | 2026-09-03T23:48:11Z | F2 | verified |
| `repository.license` | GPL-3.0 | F5 | verified |
| `repository.state` | active | F4 | verified |
| `editorial.hook` | 让照片和文件夹变成可回头找的标签库 | F6, F7, F8, F9, F10, F11 | inferred |
| `editorial.summary` | 说明输入、核心操作、主要能力与可见结果 | F6, F7, F8, F9, F10, F11 | verified |
| `editorial.meaning` | 解释可复用的文件组织模型为何有价值 | F7, F8, F9, F10, F11 | inferred |
| `editorial.audience` | 需要在不搬动原文件前提下管理照片和各类文件的人 | F6, F7, F8, F9, F10, F11 | inferred |
| `editorial.features` | 列出已验证的核心能力 | F7, F8, F9, F10, F11 | verified |
| `editorial.stack` | Python、SQLite、FFmpeg、ripgrep | F3, F7, F13 | verified |
| `editorial.opportunity` | 把现有能力与具体整理摩擦连接到新产品可能性 | F7, F9, F10, F11, F13 | inferred |

## Product inferences

- [I1] TagStudio 的核心复用单元是“现有目录上的标签层 + SQLite 元数据 + 搜索/预览/重连流程”。 Basis: F6, F7, F11. Confidence: high
- [I2] 它更像一个离线资料库底座，而不是只做单一文件类型的查看器。 Basis: F8, F9, F10, F11, F13. Confidence: high
- [I3] GPL-3.0 允许继续研究和改造，但页面不应因此暗示任何额外的部署或再分发便利。 Basis: F5, F6, F7. Confidence: high

## Direction rationale

### D1 — 旅行相册标签册

- Reused capability: 现有目录上的标签层、SQLite 元数据、组合搜索和媒体预览。
- Evidence: F6, F7, F9, F10, F11
- New audience and recurring problem: 给经常拍照、整理旅行素材的人：照片散在原文件夹里，但希望按地点、人物、日期快速回头找。
- Input and visible outcome: 输入是相机或手机导出的照片文件夹；输出是带标签、字段和搜索条件的旅行相册。
- Original workflow: 用户打开现有目录 → 建 library → 给各种文件加标签和字段 → 组合搜索、预览、重连条目 → 维护通用资料库。
- New workflow: 用户把旅行照片所在目录作为 library 打开，给照片补地点、人物和日期字段，再用标签与路径搜索回看整段旅程。
- Materially changed axes: audience, input, outcome
- Product form: end-user-product
- Product boundary: 只服务照片和相册整理，不做云同步、自动成片或社交分享。
- Substantive difference: 原项目是通用照片/文件资料库；这个方向只围绕旅行照片和相册回看，结果是可翻找、可检索的旅行影集。

### D2 — 设计素材档案库

- Reused capability: 标签继承、别名、字段和多格式预览。
- Evidence: F6, F7, F8, F9, F10, F11
- New audience and recurring problem: 给设计师、插画师和 3D 创作者：PSD、Blender、Krita 和参考图混在一起时，常常只记得内容，不记得文件名。
- Input and visible outcome: 输入是设计工程文件、参考图和草稿；输出是按主题、版本、人物或项目分层的素材档案库。
- Original workflow: 用户打开现有目录 → 建 library → 给各种文件加标签和字段 → 组合搜索、预览、重连条目 → 维护通用资料库。
- New workflow: 用户先用父标签、别名和分类位建立素材词表，再给文件挂字段和标签，按 filetype、mediatype 和路径筛选具体资产。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做离线素材整理和检索，不变成在线协作评审或版本管理工具。
- Substantive difference: 原项目面向泛用文件管理；这个方向收窄到创作素材库，把复杂格式文件当作可复用资产来组织。

### D3 — 音视频素材柜

- Reused capability: 媒体预览、播放和组合搜索。
- Evidence: F6, F8, F11, F13
- New audience and recurring problem: 给做视频、播客和剪辑素材管理的人：媒体文件体积大、格式杂，单靠文件名很难直接找出要用的片段。
- Input and visible outcome: 输入是视频、音频和动图素材；输出是带标签、可播放、可按类型搜的离线媒体柜。
- Original workflow: 用户打开现有目录 → 建 library → 给各种文件加标签和字段 → 组合搜索、预览、重连条目 → 维护通用资料库。
- New workflow: 用户把素材目录打开成 library，先靠缩略图和播放确认内容，再用标签、mediatype 和路径把可用片段归类。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做本地媒体整理和回看，不做剪辑器、转码器或云媒体库。
- Substantive difference: 原项目是通用文件管理；这个方向把预览和播放放到核心位置，结果是一个可直接浏览内容的音视频素材柜。

## Pairwise direction comparison

- 旅行相册标签册 vs 设计素材档案库
  - Different axes: input, workflow, outcome
  - Concrete comparison: 旅行相册标签册更偏照片回看，设计素材档案库更偏多格式创作资产管理；前者主要变的是输入、后者主要变的是输入和工作流。
- 旅行相册标签册 vs 音视频素材柜
  - Different axes: input, workflow, outcome
  - Concrete comparison: 旅行相册标签册以照片为主，音视频素材柜以视频、音频和动图为主；后者还把播放和缩略图当成核心结果。
- 设计素材档案库 vs 音视频素材柜
  - Different axes: workflow, outcome
  - Concrete comparison: 设计素材档案库强调标签继承、别名和分类位，音视频素材柜强调预览与播放；一个侧重组织模型，一个侧重浏览体验。

## Uncertainty

- None.

## Localization decisions

- 保留 library、SQLite、sidecar 文件、filetype、mediatype、FFmpeg、ripgrep 这些基本技术词，因为它们直接影响产品理解和复用判断。
- 把 README 中的 'photo & file management system' 译为 '照片和文件管理应用/资料库'，避免直译成生硬的堆叠名词。
- 将 tag/field search bars 译为 '标签/字段搜索栏'，保持界面含义而不引入额外术语。
- 将 moved/unlinked entries 译为 '移动后的条目/未链接条目'，突出可见结果。

## Refresh notes

- Initial research; no prior published snapshot.
