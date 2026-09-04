# TriliumNext/Trilium research notes

Research date: 2026-09-04
Repository: https://github.com/TriliumNext/Trilium
Research mode: new

## Snapshot

- Repository ID: 92111509
- Repository full name: TriliumNext/Trilium
- Repository name: Trilium
- Stars at fetch time: 37699
- Forks at fetch time: 2535
- Primary language: TypeScript
- Latest push at fetch time: 2026-09-04T02:08:37Z
- License: GNU Affero General Public License v3.0
- Default branch: main
- README SHA: 616799e42622ac1911f65001a6f7b1b2c1d78278
- Latest release: v0.105.0 / 2026-08-19T18:19:34Z
- Repository state: active
- Fetched at: 2026-09-04T05:12:18Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/TriliumNext/Trilium — accessed 2026-09-04
- [S2] Official README — https://github.com/TriliumNext/Trilium/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/TriliumNext/Trilium/releases/tag/v0.105.0 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/TriliumNext/Trilium/blob/main/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 快照确认仓库身份、计数、TypeScript 主语言、活动状态与 AGPL-3.0 许可证。 Sources: S1, S4
- [F2] Trilium Notes 是跨平台的层级笔记应用，重点是建立大型个人知识库。 Sources: S2
- [F3] README 列出任意深度笔记树、克隆、富文本和代码笔记、搜索、版本、属性、脚本、同步、分享、加密、画布与关系图。 Sources: S2
- [F4] 项目主要使用 TypeScript，可用桌面端、浏览器和自托管同步服务器。 Sources: S1, S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 92111509 | F1 | verified |
| `repository.fullName` | TriliumNext/Trilium | F1 | verified |
| `repository.name` | Trilium | F1 | verified |
| `repository.stars` | 37699 | F1 | verified |
| `repository.forks` | 2535 | F1 | verified |
| `repository.language` | TypeScript | F1 | verified |
| `repository.pushedAt` | 2026-09-04T02:08:37Z | F1 | verified |
| `repository.license` | GNU Affero General Public License v3.0 | F1 | verified |
| `repository.state` | active | F1 | verified |
| `editorial.hook` | 让笔记按关系生长成个人知识树 | F2, F3 | verified |
| `editorial.summary` | Trilium Notes 用任意深度的笔记树管理大型个人知识库，同一条笔记还能克隆到多个位置。富文本、代码、属性、全文搜索、版本记录和脚本负责组织内容；自托管同步、逐条加密、公开分享、画布与关系图则让知识既能私密积累，也能按关系展示。 | F2, F3 | verified |
| `editorial.meaning` | 它不只保存页面，还允许一条信息同时属于多个脉络并带有关系、属性和历史，因此适合复用为长期生长的家庭、创作或学习记录系统。 | I1 | inferred |
| `editorial.audience` | 需要长期维护大量相互关联笔记，并希望自己控制同步与分享方式的个人知识工作者。 | F2 | verified |
| `editorial.features` | ["任意深度笔记树与笔记克隆", "富文本、代码和多种笔记类型", "属性、搜索、版本记录与脚本", "自托管同步、分享和逐条加密", "画布、关系图和链接图"] | F2, F3 | verified |
| `editorial.stack` | ["TypeScript", "Electron", "Node.js", "SQLite", "Web UI"] | F4 | verified |
| `editorial.opportunity` | ["把层级、属性和版本改造成家庭照护日志。", "把关系图和克隆改造成世界观设定图谱。", "把关系与搜索改造成学习前置知识地图。"] | I1, I2, I3, I4 | inferred |

## Product inferences

- [I1] 它不只保存页面，还允许一条信息同时属于多个脉络并带有关系、属性和历史，因此适合复用为长期生长的家庭、创作或学习记录系统。 Basis: F2, F3. Confidence: high
- [I2] 可将原项目能力改造成“家庭照护日志”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I3] 可将原项目能力改造成“世界观设定图谱”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I4] 可将原项目能力改造成“学习前置地图”这类独立产品。 Basis: F2, F3. Confidence: medium

## Direction rationale

### D1 — 家庭照护日志

- Reused capability: 层级笔记、属性、关系和版本记录
- Evidence: F2, F3
- New audience and recurring problem: 共同照护家人的家庭成员；长期照护记录散在聊天、纸张和文件夹里，家人难以知道某次变化之后发生了什么。
- Input and visible outcome: 输入是每日观察、文件、联系人和复查事项；最终得到可追溯的家庭照护时间线。
- Original workflow: 把不同类型笔记放进可任意加深的树中，通过克隆、属性、关系、搜索和关系图建立大型个人知识库，并可自托管同步。
- New workflow: 按日记录→关联资料→标记待办→交接复查
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只保存家庭观察和资料，不提供医疗结论。
- Substantive difference: 从自由知识库改成按时间交接、关系追踪和复查的家庭日志。

### D2 — 世界观设定图谱

- Reused capability: 笔记克隆、属性、关系图和搜索
- Evidence: F2, F3
- New audience and recurring problem: 小说和游戏剧情创作者；长篇故事的角色与地点跨章节重复出现，作者容易忘记时间关系和设定冲突。
- Input and visible outcome: 输入是人物、地点、事件和章节设定；最终得到可视世界观图谱和连续性清单。
- Original workflow: 把不同类型笔记放进可任意加深的树中，通过克隆、属性、关系、搜索和关系图建立大型个人知识库，并可自托管同步。
- New workflow: 建立设定→连接关系→生成章节视图→核对冲突
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动代写剧情，只帮助维护已输入设定。
- Substantive difference: 从通用笔记改成围绕叙事连续性的关系检查产品。

### D3 — 学习前置地图

- Reused capability: 关系、属性、搜索和关系图
- Evidence: F2, F3
- New audience and recurring problem: 进行长期自学的学生和成年人；自学者积累很多笔记，却不知道某个概念卡住是因为缺少哪项前置知识。
- Input and visible outcome: 输入是概念笔记、前置关系和理解状态；最终得到从目标倒推的学习路径图。
- Original workflow: 把不同类型笔记放进可任意加深的树中，通过克隆、属性、关系、搜索和关系图建立大型个人知识库，并可自托管同步。
- New workflow: 连接前置→标记理解→查找断点→安排复习
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动判定知识正确性，也不代替课程教学。
- Substantive difference: 从按主题存笔记变成按知识依赖决定学习顺序。

## Pairwise direction comparison

- 家庭照护日志 vs 世界观设定图谱
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭照护成员”与“小说和游戏剧情作者”；输入分别是“每日观察、文件、联系人和复查事项”与“人物、地点、事件和章节设定”；流程分别是“按日记录→关联资料→标记待办→交接复查”与“建立设定→连接关系→生成章节视图→核对冲突”
- 家庭照护日志 vs 学习前置地图
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭照护成员”与“长期自学者”；输入分别是“每日观察、文件、联系人和复查事项”与“概念笔记、前置关系和理解状态”；流程分别是“按日记录→关联资料→标记待办→交接复查”与“连接前置→标记理解→查找断点→安排复习”
- 世界观设定图谱 vs 学习前置地图
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“小说和游戏剧情作者”与“长期自学者”；输入分别是“人物、地点、事件和章节设定”与“概念笔记、前置关系和理解状态”；流程分别是“建立设定→连接关系→生成章节视图→核对冲突”与“连接前置→标记理解→查找断点→安排复习”

## Uncertainty

- 本批只验证仓库公开资料，不推断未在 README 或发布页出现的商业能力。

## Localization decisions

- 保留必要的产品名和基础技术名词，并在相邻句中说明它们的作用。

## Refresh notes

- Initial research; no prior published snapshot.
