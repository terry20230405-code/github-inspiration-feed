# 自动候选审核：20260901T150054Z-44a78a5d

- 生成时间：2026-09-01T15:00:54Z
- 合格候选：1
- 未通过深读：4
- 当前状态：等待人工审核
- 合并此 PR 表示批准本批候选进入灵感流；关闭 PR 表示拒绝整批。

## 1. maka

- 仓库：https://github.com/apache/maka
- Star：4391
- 许可证：Apache License 2.0
- 主题色：#bf5831
- Hook：把 AI 代理做成可回放工作区
- 介绍：它把本地项目、模型连接和权限设置接到同一个 AI agent 工作区里，让你在 Desktop、TUI/CLI 或 Eval 中发起任务、查看工具轨迹并接续中断的回合。模型消息、tool calls、tool results、权限决策和终止事件都会写成可回放的记录。
- 改造方向：
  - 会话复盘台：从历史会话里找出失败点并接着跑
  - 权限审计台：先连模型和工具，再把越界动作关进审批
  - 实验对照台：把评测结果和失败点放在一起看

## 未进入候选的仓库

### Pinvou/pinvou-agent

- 停止阶段：首轮修复无实质进展
- 结果：首轮修复后方向差异没有可测量改善，停止无效第二轮：D3（单个方向与原项目的实质差异通过数 2→2）；仍未通过：D3
- 最终失败证据：
  - D3：方向复用 F12/F15/F16 的资料闭环能力，但把原项目的通用 workspace 改成资料检索、摘证与文档交付；与原项目相比，用户、输入、工作流、可见结果都发生实质变化。
- 修复轨迹：
  - 初次检查：失败 D3；改动 无；策略 生成后首次完整检查；A3 由程序核对，A4 及其他语义项由 AI 审核。
    - D3 当轮证据：\`受控代码协作桌面\` 只是在原项目已存在的 code mode 上改写命名：F14 已给出真实项目/临时工作区、plan、permission requests、file changes 与代码读写/命令执行，因此不足两项实质变化。
    - 方向 受控代码协作桌面：变化轴 audience；F14 已经覆盖真实项目或临时工作区、ACP、plan、tool steps、permission requests、file changes 和代码读写/命令执行；方向没有在输入、核心工作流或可见结果上形成新的重复集成流程，只是把原有 code mode 改写成面向开发者的叙述。
  - 第 1 轮修复后复检：失败 D3；改动 editorial.directions, editorial.opportunity, decisionReason, fieldEvidence, directionRationales, directionComparisons；策略 针对失败证据，只删除、降级或重新绑定没有一手来源支持的主张；保持已通过字段不变。
    - D3 当轮证据：方向复用 F12/F15/F16 的资料闭环能力，但把原项目的通用 workspace 改成资料检索、摘证与文档交付；与原项目相比，用户、输入、工作流、可见结果都发生实质变化。
    - 方向 hai-bao-gai-gao-tai：变化轴 audience, input；F13 已明确“design mode 可以用自然语言创建海报和数据可视化，并在设计界面里直接改元素”，F15 也包含可编辑 artifacts；该方向只是把同一能力改写成海报/图表、文案/数据/尺寸的子集，没有新的核心工作流或可见结果，改动不足两项实质轴。

### apache/superset

- 停止阶段：A3 程序校验
- 结果：GitHub 客观数据未能与本轮快照完全对应
- 最终失败证据：
  - A3：repository.pushedAt 不能晚于 repository.fetchedAt
- 当前结构错误：
  - repository.pushedAt must not be later than repository.fetchedAt

### tldraw/tldraw

- 停止阶段：两轮自动修复后质量复检
- 结果：两轮修复后仍未通过：A4
- 最终失败证据：
  - A4：The project JSON asserts repository.license='Other' while the research note explicitly treats repository.license as unknown because GitHub metadata and README licensing language do not align cleanly.
- 当前阻断项：
  - License state remains unresolved: GitHub metadata is recorded as Other/NOASSERTION, the README says tldraw license with a production license key requirement, and the research note marks repository.license as unknown while the project JSON sets it to Other.
- 修复轨迹：
  - 初次检查：失败 A4, E3；改动 无；策略 生成后首次完整检查；A3 由程序核对，A4 及其他语义项由 AI 审核。
    - A4 当轮证据：research note 的 Uncertainty 明确写出“GitHub 元数据把许可证记为 Other/NOASSERTION，README 则写的是 tldraw license 并说明生产使用需要 license key”，license 语义未被页面消解。
    - E3 当轮证据：所有方向都面向商业团队/内部工具场景，没有一条主要服务于个人、家庭、学习、创作或社区，因此缺少必须保留的非商业主题方向。
  - 第 1 轮修复后复检：失败 无；改动 editorial.directions, editorial.opportunity, editorial.summary, decisionReason, fieldEvidence, inferences, directionRationales, directionComparisons, uncertainty, localizationDecisions；策略 针对失败证据，只删除、降级或重新绑定没有一手来源支持的主张；保持已通过字段不变。
  - 第 2 轮修复后复检：失败 A4；改动 decisionReason, directionComparisons；策略 采用不同方案：从已验证事实重新构造受影响字段，不沿用上一轮仍然失败的句式或推断。
    - A4 当轮证据：The project JSON asserts repository.license='Other' while the research note explicitly treats repository.license as unknown because GitHub metadata and README licensing language do not align cleanly.

### labring/FastGPT

- 停止阶段：A3 程序校验
- 结果：GitHub 客观数据未能与本轮快照完全对应
- 最终失败证据：
  - A3：repository.pushedAt 不能晚于 repository.fetchedAt
- 当前结构错误：
  - fieldEvidence must contain every required field exactly once and in order
  - repository.pushedAt must not be later than repository.fetchedAt
  - page field evidence is missing \`editorial.meaning\`



## AI 执行统计

- 候选并发上限：2
- AI 逻辑调用：18
- 深读阶段墙钟时间：1807.9 秒
- 各请求耗时合计：2623.0 秒（并发请求会重叠）
- 返回 usage 的调用：18
- 输入 Token：217310
- 输出 Token：139749
- 其中缓存输入 Token：75520
- 其中推理 Token：85589
