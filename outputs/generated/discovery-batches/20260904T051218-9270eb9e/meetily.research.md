# Zackriya-Solutions/meetily research notes

Research date: 2026-09-04
Repository: https://github.com/Zackriya-Solutions/meetily
Research mode: new

## Snapshot

- Repository ID: 908589694
- Repository full name: Zackriya-Solutions/meetily
- Repository name: meetily
- Stars at fetch time: 30299
- Forks at fetch time: 3273
- Primary language: Rust
- Latest push at fetch time: 2026-09-03T09:51:34Z
- License: MIT License
- Default branch: main
- README SHA: a62e67055589d2a1ee764c48126c30ac8dd4f999
- Latest release: v0.4.0 / 2026-06-05T17:12:25Z
- Repository state: active
- Fetched at: 2026-09-04T05:12:18Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/Zackriya-Solutions/meetily — accessed 2026-09-04
- [S2] Official README — https://github.com/Zackriya-Solutions/meetily/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/Zackriya-Solutions/meetily/releases/tag/v0.4.0 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/Zackriya-Solutions/meetily/blob/main/LICENSE.md — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 快照确认仓库身份、计数、Rust 主语言、活动状态与 MIT 许可证。 Sources: S1, S4
- [F2] Meetily 是隐私优先的会议助手，可在本机捕获会议、实时转写并生成摘要。 Sources: S2
- [F3] README 列出离线本地处理、导入录音、AI 摘要、自定义 OpenAI 兼容端点、音频混合和 GPU 加速。 Sources: S2
- [F4] 项目主要使用 Rust，支持 Windows、macOS 和 Linux，并强调用户控制会议数据。 Sources: S1, S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 908589694 | F1 | verified |
| `repository.fullName` | Zackriya-Solutions/meetily | F1 | verified |
| `repository.name` | meetily | F1 | verified |
| `repository.stars` | 30299 | F1 | verified |
| `repository.forks` | 3273 | F1 | verified |
| `repository.language` | Rust | F1 | verified |
| `repository.pushedAt` | 2026-09-03T09:51:34Z | F1 | verified |
| `repository.license` | MIT License | F1 | verified |
| `repository.state` | active | F1 | verified |
| `editorial.hook` | 让会议声音留在本机，也能变成清晰纪要 | F2, F3 | verified |
| `editorial.summary` | Meetily 在本机捕获会议声音、实时转写并生成摘要，核心目标是不把敏感对话交给外部会议服务。它支持导入已有录音、使用本地开源模型，也可接入用户自己选择的 OpenAI 兼容端点；多平台桌面应用和音频混合能力负责把收音、文字与总结接成一条流程。 | F2, F3 | verified |
| `editorial.meaning` | 本地收音、转写和结构化摘要不仅能服务商务会议，也能成为口述历史、学习复盘与社区协作这类重视隐私场景的基础。 | I1 | inferred |
| `editorial.audience` | 需要记录会议又希望自己掌握音频、转写文本和模型连接的个人、专业人士与组织。 | F2 | verified |
| `editorial.features` | ["本机录音与实时转写", "导入已有音频继续处理", "使用本地模型生成摘要", "支持自定义 OpenAI 兼容端点", "跨平台桌面端与音频混合"] | F2, F3 | verified |
| `editorial.stack` | ["Rust", "Tauri", "Local Speech Model", "OpenAI-compatible API"] | F4 | verified |
| `editorial.opportunity` | ["把本地转写改造成家庭口述史笔记。", "把录音与摘要改造成学习复盘教练。", "把行动项提取改造成志愿者交接日志。"] | I1, I2, I3, I4 | inferred |

## Product inferences

- [I1] 本地收音、转写和结构化摘要不仅能服务商务会议，也能成为口述历史、学习复盘与社区协作这类重视隐私场景的基础。 Basis: F2, F3. Confidence: high
- [I2] 可将原项目能力改造成“家庭口述史笔记”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I3] 可将原项目能力改造成“学习复盘教练”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I4] 可将原项目能力改造成“志愿者交接日志”这类独立产品。 Basis: F2, F3. Confidence: medium

## Direction rationale

### D1 — 家庭口述史笔记

- Reused capability: 本地录音、转写和摘要
- Evidence: F2, F3
- New audience and recurring problem: 记录家族故事的个人和家庭；家庭访谈录完后常被搁置，重要人物、时间和原声片段难以对应。
- Input and visible outcome: 输入是长辈访谈音频、人物和年代线索；最终得到可追溯到原声的家庭故事线。
- Original workflow: 在本机捕获会议声音，实时转写，再用本地模型或自定义 OpenAI 兼容端点生成会议摘要。
- New workflow: 本地转写→人工校正→标注年代→链接原声
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动确认历史事实，也不把音频公开上传。
- Substantive difference: 从会议纪要改成需要人工考证和原声回链的家庭档案。

### D2 — 学习复盘教练

- Reused capability: 本地收音、转写和结构化摘要
- Evidence: F2, F3
- New audience and recurring problem: 自学课程和备考的学生；学习者读完材料后自以为理解，却很少通过口头复述发现概念缺口。
- Input and visible outcome: 输入是个人口头讲解与课程提纲；最终得到知识缺口清单和下一轮复习题。
- Original workflow: 在本机捕获会议声音，实时转写，再用本地模型或自定义 OpenAI 兼容端点生成会议摘要。
- New workflow: 录下复述→转写分段→对照提纲→生成复习问题
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动判分，也不替代教师反馈。
- Substantive difference: 输入从多人会议变成个人讲解，输出从纪要变成知识缺口和复习题。

### D3 — 志愿者交接日志

- Reused capability: 会议录音、转写和摘要生成
- Evidence: F2, F3
- New audience and recurring problem: 轮班协作的社区志愿团队；社区志愿者轮班开会后，后续人员常不知道已经决定什么、谁负责、何时跟进。
- Input and visible outcome: 输入是轮班会议音频、成员和待办日期；最终得到带责任人与日期的轮班交接卡。
- Original workflow: 在本机捕获会议声音，实时转写，再用本地模型或自定义 OpenAI 兼容端点生成会议摘要。
- New workflow: 转写会议→提取决定→确认负责人→生成交接
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动指派责任，也不替代团队的最终确认。
- Substantive difference: 从通用摘要变成必须人工确认责任关系的轮班交接产品。

## Pairwise direction comparison

- 家庭口述史笔记 vs 学习复盘教练
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭口述史记录者”与“自学者和备考学生”；输入分别是“长辈访谈音频、人物和年代线索”与“个人口头讲解与课程提纲”；流程分别是“本地转写→人工校正→标注年代→链接原声”与“录下复述→转写分段→对照提纲→生成复习问题”
- 家庭口述史笔记 vs 志愿者交接日志
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭口述史记录者”与“社区志愿团队”；输入分别是“长辈访谈音频、人物和年代线索”与“轮班会议音频、成员和待办日期”；流程分别是“本地转写→人工校正→标注年代→链接原声”与“转写会议→提取决定→确认负责人→生成交接”
- 学习复盘教练 vs 志愿者交接日志
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“自学者和备考学生”与“社区志愿团队”；输入分别是“个人口头讲解与课程提纲”与“轮班会议音频、成员和待办日期”；流程分别是“录下复述→转写分段→对照提纲→生成复习问题”与“转写会议→提取决定→确认负责人→生成交接”

## Uncertainty

- 本批只验证仓库公开资料，不推断未在 README 或发布页出现的商业能力。

## Localization decisions

- 保留必要的产品名和基础技术名词，并在相邻句中说明它们的作用。

## Refresh notes

- Initial research; no prior published snapshot.
