# 阶段七来源复审前向测试

- 日期：2026-08-27
- 测试对象：`github-inspiration-editor` 固定案例 B1–B5
- 变更范围：来源变化侦测和语义审核门禁；不改变中文写作标准

## 相同证据条件

五个固定仓库分别使用同一组受控来源状态：仓库元数据、README SHA/正文、最新正式 Release。旧行为只有阶段六的 `pushedAt` 活动信号，无法证明 README 或产品说明是否改变；新行为先建立来源指纹，再将同一份 README 变化应用于每个案例。

## 比较结果

| 固定案例 | 旧行为 | 新行为 | 发布副作用 |
| --- | --- | --- | --- |
| B1 Remotion | 只建议重新研究 | README 变化生成待审核证据包 | 无 |
| B2 Excalidraw | 只建议重新研究 | README 变化生成待审核证据包 | 无 |
| B3 Immich | 只建议重新研究 | README 变化生成待审核证据包 | 无 |
| B4 n8n | 只建议重新研究 | README 变化生成待审核证据包 | 无 |
| B5 Memos | 只建议重新研究 | README 变化生成待审核证据包 | 无 |

`test_fixed_benchmark_repositories_use_the_same_source_change_gate` 对五个案例执行同一基线和变化流程。全部案例都必须停在 `semanticReviewStatus: pending`，并生成 `*.source.json` 数据；测试禁止写入产品数据。

## 结论

新行为补上了“活动信号 → 可审查的一手来源变化”之间的缺口，但没有把来源变化直接解释为内容变化。中文内容仍需指纹匹配的 AI 审核；`meaningful` 只能生成 `outputs/generated/` 草稿，`critical` 必须询问用户，任何结果都不自动发布。
