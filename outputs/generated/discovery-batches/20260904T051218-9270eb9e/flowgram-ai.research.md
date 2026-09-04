# bytedance/flowgram.ai research notes

Research date: 2026-09-04
Repository: https://github.com/bytedance/flowgram.ai
Research mode: new

## Snapshot

- Repository ID: 933963452
- Repository full name: bytedance/flowgram.ai
- Repository name: flowgram.ai
- Stars at fetch time: 8420
- Forks at fetch time: 768
- Primary language: TypeScript
- Latest push at fetch time: 2026-09-01T04:02:40Z
- License: MIT License
- Default branch: main
- README SHA: fff923c97febbc2f9684f6f4d84ee37f03077da2
- Latest release: v1.0.14 / 2026-08-20T06:11:25Z
- Repository state: active
- Fetched at: 2026-09-04T05:12:18Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/bytedance/flowgram.ai — accessed 2026-09-04
- [S2] Official README — https://github.com/bytedance/flowgram.ai/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/bytedance/flowgram.ai/releases/tag/v1.0.14 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/bytedance/flowgram.ai/blob/main/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 快照确认仓库身份、计数、TypeScript 主语言、活动状态与 MIT 许可证。 Sources: S1, S4
- [F2] FlowGram 是可组合、可扩展的可视化工作流开发框架，目标是帮助开发者搭建 AI 工作流平台。 Sources: S2
- [F3] README 明确它不是现成平台，并列出自由画布、固定布局、节点表单、变量作用域、材料和运行时。 Sources: S2
- [F4] 项目主要使用 TypeScript，文档示例覆盖 LLM、条件、代码、循环和 HTTP 等节点。 Sources: S1, S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 933963452 | F1 | verified |
| `repository.fullName` | bytedance/flowgram.ai | F1 | verified |
| `repository.name` | flowgram.ai | F1 | verified |
| `repository.stars` | 8420 | F1 | verified |
| `repository.forks` | 768 | F1 | verified |
| `repository.language` | TypeScript | F1 | verified |
| `repository.pushedAt` | 2026-09-01T04:02:40Z | F1 | verified |
| `repository.license` | MIT License | F1 | verified |
| `repository.state` | active | F1 | verified |
| `editorial.hook` | 把节点画布变成可运行的工作流产品 | F2, F3 | verified |
| `editorial.summary` | FlowGram 不是现成的自动化平台，而是一套用来搭建这类平台的 TypeScript 框架。开发者可以组合自由或固定布局画布、节点配置表单、变量作用域、现成节点材料与运行时，让用户在自己的产品里连接条件、循环、HTTP、代码和大模型步骤。 | F2, F3 | verified |
| `editorial.meaning` | 它把工作流产品最难重复建设的画布、数据流和节点配置拆成可嵌入模块，因此适合快速验证面向具体人群的可视化流程工具。 | I1 | inferred |
| `editorial.audience` | 正在开发 AI 工作流、自动化编排或节点式编辑器产品的前端和平台团队。 | F2 | verified |
| `editorial.features` | ["自由布局与固定布局画布", "节点配置表单和校验", "变量作用域与类型推断", "LLM、条件、代码等节点材料", "可嵌入运行时"] | F2, F3 | verified |
| `editorial.stack` | ["TypeScript", "React", "Node.js", "Workflow Runtime"] | F4 | verified |
| `editorial.opportunity` | ["把节点画布改造成家庭照护日程设计器。", "把变量和分支改造成课堂实验流程卡。", "把条件与连线改造成互动故事分支工坊。"] | I1, I2, I3, I4 | inferred |

## Product inferences

- [I1] 它把工作流产品最难重复建设的画布、数据流和节点配置拆成可嵌入模块，因此适合快速验证面向具体人群的可视化流程工具。 Basis: F2, F3. Confidence: high
- [I2] 可将原项目能力改造成“家庭照护流程板”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I3] 可将原项目能力改造成“课堂实验流程卡”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I4] 可将原项目能力改造成“故事分支工坊”这类独立产品。 Basis: F2, F3. Confidence: medium

## Direction rationale

### D1 — 家庭照护流程板

- Reused capability: 固定布局画布、表单、变量和条件节点
- Evidence: F2, F3
- New audience and recurring problem: 共同照护老人或病后家人的家庭成员；家庭多人轮流照护时，条件、提醒和交接信息容易散落在聊天记录。
- Input and visible outcome: 输入是照护事项、时间和异常条件；最终得到每日照护清单和交接摘要。
- Original workflow: 开发者把画布、节点表单、变量作用域和运行时材料嵌入自己的产品，搭建可视化 AI 工作流平台。
- New workflow: 画步骤→设置条件→生成日程→记录交接
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只协助整理家庭约定，不给出医疗诊断或剂量建议。
- Substantive difference: 从开发框架变成家庭直接使用的照护流程产品。

### D2 — 课堂实验流程卡

- Reused capability: 节点表单、变量作用域、分支和运行时
- Evidence: F2, F3
- New audience and recurring problem: 组织探究课的教师和学生；学生做探究实验时容易跳过控制变量、记录或复盘步骤。
- Input and visible outcome: 输入是实验步骤、变量和观察问题；最终得到可复盘的实验过程记录。
- Original workflow: 开发者把画布、节点表单、变量作用域和运行时材料嵌入自己的产品，搭建可视化 AI 工作流平台。
- New workflow: 设计流程→学生运行→填写观察→回看分支
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不替教师判断实验安全，也不自动给学生评分。
- Substantive difference: 把任意工作流编辑器改成有教学检查点的学生执行界面。

### D3 — 故事分支工坊

- Reused capability: 自由画布、变量、条件分支和运行时
- Evidence: F2, F3
- New audience and recurring problem: 创作互动小说和游戏剧情的作者；互动故事作者在文档中维护条件和分支时，很难发现断路与无法到达的结局。
- Input and visible outcome: 输入是场景、人物状态和选择条件；最终得到可点击的互动故事原型。
- Original workflow: 开发者把画布、节点表单、变量作用域和运行时材料嵌入自己的产品，搭建可视化 AI 工作流平台。
- New workflow: 连接场景→设置状态→检查路径→试玩分支
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动代写故事正文，也不包含完整游戏引擎。
- Substantive difference: 输出从工作流配置变成读者可试玩的叙事原型。

## Pairwise direction comparison

- 家庭照护流程板 vs 课堂实验流程卡
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭照护成员”与“教师和学生”；输入分别是“照护事项、时间和异常条件”与“实验步骤、变量和观察问题”；流程分别是“画步骤→设置条件→生成日程→记录交接”与“设计流程→学生运行→填写观察→回看分支”
- 家庭照护流程板 vs 故事分支工坊
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭照护成员”与“互动故事创作者”；输入分别是“照护事项、时间和异常条件”与“场景、人物状态和选择条件”；流程分别是“画步骤→设置条件→生成日程→记录交接”与“连接场景→设置状态→检查路径→试玩分支”
- 课堂实验流程卡 vs 故事分支工坊
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“教师和学生”与“互动故事创作者”；输入分别是“实验步骤、变量和观察问题”与“场景、人物状态和选择条件”；流程分别是“设计流程→学生运行→填写观察→回看分支”与“连接场景→设置状态→检查路径→试玩分支”

## Uncertainty

- 本批只验证仓库公开资料，不推断未在 README 或发布页出现的商业能力。

## Localization decisions

- 保留必要的产品名和基础技术名词，并在相邻句中说明它们的作用。

## Refresh notes

- Initial research; no prior published snapshot.
