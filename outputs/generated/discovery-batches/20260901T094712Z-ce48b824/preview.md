# 自动候选审核：20260901T094712Z-ce48b824

- 生成时间：2026-09-01T09:47:12Z
- 合格候选：1
- 未通过深读：1
- 当前状态：等待人工审核
- 合并此 PR 表示批准本批候选进入灵感流；关闭 PR 表示拒绝整批。

## 1. PaperTodo

- 仓库：https://github.com/snownico0722/PaperTodo
- Star：2192
- 许可证：Other
- 主题色：#777718
- Hook：把便签变成安静的桌面纸片
- 介绍：PaperTodo 是一款 Windows 桌面便签工具，把待办纸和笔记纸做成独立窗口，直接放在桌面上。它支持勾选、拖排、Markdown、本地图片和自动保存，还能折成胶囊贴到屏幕边缘，减少打扰。
- 改造方向：
  - 收工清单纸：粘贴收尾事项，生成只留未完成项的桌面清单
  - 贴边资料架：把截图和短摘录收进屏幕边缘，随用随开
  - 任务说明纸：把待办和说明页绑在一起，点任务就能打开背景说明

## 未进入候选的仓库

### Pinvou/pinvou-agent

- 停止阶段：两轮自动修复后质量复检
- 结果：两轮修复后仍未通过：D3
- 最终失败证据：
  - D3：D3 failed because the directions only narrow existing capabilities from F3/F5/F6 instead of creating a new recurring workflow/outcome.
- 当前结构错误：
  - quality items must contain A1-E3 exactly once and in order
- 当前阻断项：
  - D3 failed: all three directions mostly restate existing F3/F5/F6 capabilities; compared with the original repo, each direction only materially changes audience and does not add a new recurring workflow/outcome beyond the current workspace, design mode, or ACP code mode.
- 修复轨迹：
  - 初次检查：失败 D3；改动 无；策略 生成后首次完整检查；A3 由程序核对，A4 及其他语义项由 AI 审核。
    - D3 当轮证据：\`acp-coding-session\` is not a new product boundary: F6 already says the repo supports ACP, real projects/temp workspaces, commands, plan/permission requests, file tracking, and restartable sessions; the direction only narrows the audience and repeats the same workflow/outcome.
    - 方向 acp-coding-session：变化轴 audience；Direction \`acp-coding-session\` repeats F6 almost verbatim: the original repo already supports ACP-based read/write on real projects or temp workspaces, command execution, plan/permission display, file-change tracking, and resume-after-restart. The direction only shifts the audience toward developers, so it does not reach two material changedAxes.
  - 第 1 轮修复后复检：失败 D3；改动 editorial.directions, editorial.features, editorial.meaning, editorial.opportunity, decisionReason, fieldEvidence, directionRationales, directionComparisons；策略 针对失败证据，只删除、降级或重新绑定没有一手来源支持的主张；保持已通过字段不变。
    - D3 当轮证据：editable-design-studio 与 local-ai-ops-console 仅复用原项目已存在的 Design mode、运行监控、GitHub Releases 更新与模型切换能力；至少两项实质变化没有成立，因此这一项失败。
    - 方向 editable-design-studio：变化轴 audience；F5 已经写明 Design mode 可以用自然语言创建海报和数据可视化，并在画布里直接选中元素修改文案、字体、颜色、尺寸和布局；该方向的 input、workflow、outcome 与原功能基本相同，只是把使用者改成内容运营/活动设计者等。
    - 方向 local-ai-ops-console：变化轴 audience, outcome；F7/F8 已经包含运行监控、GitHub Releases 更新、本地 vLLM、OpenAI-compatible API 和按会话切换模型；该方向只是把这些现成能力收缩成巡检台，没有新增原项目没有提供的重复集成流程或结果。
  - 第 2 轮修复后复检：失败 D3；改动 editorial.directions, editorial.meaning, editorial.opportunity, decisionReason, fieldEvidence, directionRationales, directionComparisons；策略 采用不同方案：从已验证事实重新构造受影响字段，不沿用上一轮仍然失败的句式或推断。
    - D3 当轮证据：D3 failed because the directions only narrow existing capabilities from F3/F5/F6 instead of creating a new recurring workflow/outcome.
    - 方向 deliverable-workspace：变化轴 audience；Compared with F3/F4/F7, this direction still uses the same attachments/knowledge base/Skills/MCP/workflows → artifact panel/Markdown path and the same file-delivery outcome; only the audience narrows to researchers, ops, project coordinators, and knowledge workers.
    - 方向 editable-design-studio：变化轴 audience；Compared with F2 and F5, this direction repeats the same natural-language/data → design mode → element editing → iterative visual result workflow; the only clear change is the audience (content ops, event designers, teachers, creators).
    - 方向 code-handoff-workbench：变化轴 audience；Compared with F6/F7/F8, this direction repeats the same ACP repo/workspace access, command execution, plan/permission requests, change tracking, and resume-after-restart workflow; the only clear change is the audience (developers and small teams).

