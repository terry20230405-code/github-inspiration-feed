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
- Fetched at: 2026-09-04T05:12:18Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/TagStudioDev/TagStudio — accessed 2026-09-04
- [S2] Official README — https://github.com/TagStudioDev/TagStudio/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/TagStudioDev/TagStudio/releases/tag/v9.6.3 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/TagStudioDev/TagStudio/blob/main/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 快照确认仓库身份、计数、Python 主语言、活动状态与 GPL-3.0 许可证。 Sources: S1, S4
- [F2] TagStudio 是以标签为基础的照片与文件整理应用，资料库覆盖现有文件夹而不要求搬动或复制文件。 Sources: S2
- [F3] README 说明资料库使用 SQLite 保存条目、标签和字段，并支持多种文件预览、标签关系及布尔组合搜索。 Sources: S2
- [F4] 项目主要使用 Python，目标包括私密、开放、可扩展且能适应文件在外部移动或改名的整理方式。 Sources: S1, S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 787908531 | F1 | verified |
| `repository.fullName` | TagStudioDev/TagStudio | F1 | verified |
| `repository.name` | TagStudio | F1 | verified |
| `repository.stars` | 7166 | F1 | verified |
| `repository.forks` | 465 | F1 | verified |
| `repository.language` | Python | F1 | verified |
| `repository.pushedAt` | 2026-09-03T23:48:11Z | F1 | verified |
| `repository.license` | GNU General Public License v3.0 | F1 | verified |
| `repository.state` | active | F1 | verified |
| `editorial.hook` | 不搬动原文件，也能重新整理整座资料库 | F2, F3 | verified |
| `editorial.summary` | TagStudio 在现有文件夹上建立一层标签资料库，不要求用户搬动、复制或改名文件。照片、视频、音频、文档等条目可以添加人物、地点、概念等标签和自定义字段，再用 AND、OR、NOT 等组合条件搜索；资料库数据集中保存在本地 SQLite 中。 | F2, F3 | verified |
| `editorial.meaning` | 它把文件的位置与文件的含义分开，适合复用为任何需要保留原目录、却又要按多重关系重新发现资料的个人知识产品。 | I1 | inferred |
| `editorial.audience` | 想整理大量照片和混合文件，同时不愿打乱原有文件夹结构的个人、创作者和资料管理者。 | F2 | verified |
| `editorial.features` | ["在现有文件夹上建立资料库而不搬动文件", "为文件条目添加标签和自定义字段", "标签可包含别名、关系等属性", "支持多种媒体预览和播放", "支持布尔条件、路径与媒体类型搜索"] | F2, F3 | verified |
| `editorial.stack` | ["Python", "Qt", "SQLite", "Local File System"] | F4 | verified |
| `editorial.opportunity` | ["把标签关系改造成家庭记忆索引。", "把字段与组合搜索改造成研究证据架。", "把多媒体预览与标签改造成手作材料目录。"] | I1, I2, I3, I4 | inferred |

## Product inferences

- [I1] 它把文件的位置与文件的含义分开，适合复用为任何需要保留原目录、却又要按多重关系重新发现资料的个人知识产品。 Basis: F2, F3. Confidence: high
- [I2] 可将原项目能力改造成“家庭记忆索引”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I3] 可将原项目能力改造成“研究证据架”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I4] 可将原项目能力改造成“手作材料目录”这类独立产品。 Basis: F2, F3. Confidence: medium

## Direction rationale

### D1 — 家庭记忆索引

- Reused capability: 不搬文件的资料库、关系标签和媒体预览
- Evidence: F2, F3
- New audience and recurring problem: 整理家庭照片和录音的个人；家庭照片散在多年文件夹中，按日期能找到文件，却找不到跨年份的人物与事件故事。
- Input and visible outcome: 输入是家庭照片、录音和人物线索；最终得到可按人物和事件浏览的家庭记忆索引。
- Original workflow: 选择现有文件夹建立资料库，在不搬动文件的前提下为条目添加标签和字段，再用组合条件搜索和重新发现内容。
- New workflow: 扫描原目录→标注人物事件→组成故事→共同确认
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动做人脸身份判断，也不把原文件上传到云端。
- Substantive difference: 从通用文件标签改成围绕家庭人物与事件的共同确认流程。

### D2 — 研究证据架

- Reused capability: 自定义字段、关系标签和组合搜索
- Evidence: F2, F3
- New audience and recurring problem: 进行桌面研究的学生和独立研究者；研究资料包含 PDF、图片和录音，文件名与文件夹很难同时表达主题、可信度和引用状态。
- Input and visible outcome: 输入是PDF、图片、录音和研究论点；最终得到可追溯的研究证据包。
- Original workflow: 选择现有文件夹建立资料库，在不搬动文件的前提下为条目添加标签和字段，再用组合条件搜索和重新发现内容。
- New workflow: 登记来源→绑定论点→标记核对→组合检索
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不判断来源真假，不替代正式引用管理器。
- Substantive difference: 把浏览文件改成按论点组装、核对和导出证据的研究流程。

### D3 — 手作材料目录

- Reused capability: 图片预览、标签、字段和组合搜索
- Evidence: F2, F3
- New audience and recurring problem: 管理手作材料的个人创作者；手作爱好者积累布料、颜料和零件后，常忘记颜色、数量、存放位置和曾用于什么作品。
- Input and visible outcome: 输入是材料照片、属性和存放位置；最终得到可查询的手作材料与作品目录。
- Original workflow: 选择现有文件夹建立资料库，在不搬动文件的前提下为条目添加标签和字段，再用组合条件搜索和重新发现内容。
- New workflow: 拍摄登记→补充属性→关联作品→按需求筛选
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只记录个人库存，不处理采购付款或仓储物流。
- Substantive difference: 输入变成材料照片和库存属性，结果是创作前可查询的选材目录。

## Pairwise direction comparison

- 家庭记忆索引 vs 研究证据架
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭成员”与“学生和独立研究者”；输入分别是“家庭照片、录音和人物线索”与“PDF、图片、录音和研究论点”；流程分别是“扫描原目录→标注人物事件→组成故事→共同确认”与“登记来源→绑定论点→标记核对→组合检索”
- 家庭记忆索引 vs 手作材料目录
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭成员”与“个人手作爱好者”；输入分别是“家庭照片、录音和人物线索”与“材料照片、属性和存放位置”；流程分别是“扫描原目录→标注人物事件→组成故事→共同确认”与“拍摄登记→补充属性→关联作品→按需求筛选”
- 研究证据架 vs 手作材料目录
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“学生和独立研究者”与“个人手作爱好者”；输入分别是“PDF、图片、录音和研究论点”与“材料照片、属性和存放位置”；流程分别是“登记来源→绑定论点→标记核对→组合检索”与“拍摄登记→补充属性→关联作品→按需求筛选”

## Uncertainty

- 本批只验证仓库公开资料，不推断未在 README 或发布页出现的商业能力。

## Localization decisions

- 保留必要的产品名和基础技术名词，并在相邻句中说明它们的作用。

## Refresh notes

- Initial research; no prior published snapshot.
