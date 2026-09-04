# plausible/analytics research notes

Research date: 2026-09-04
Repository: https://github.com/plausible/analytics
Research mode: new

## Snapshot

- Repository ID: 160427405
- Repository full name: plausible/analytics
- Repository name: analytics
- Stars at fetch time: 28861
- Forks at fetch time: 1833
- Primary language: Elixir
- Latest push at fetch time: 2026-09-03T14:21:35Z
- License: GNU Affero General Public License v3.0
- Default branch: master
- README SHA: d592aef247c5a0192ac0b8d07e5676ad2afbc0ef
- Latest release: v3.2.1 / 2026-05-15T09:15:56Z
- Repository state: active
- Fetched at: 2026-09-04T05:12:18Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/plausible/analytics — accessed 2026-09-04
- [S2] Official README — https://github.com/plausible/analytics/blob/master/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/plausible/analytics/releases/tag/v3.2.1 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/plausible/analytics/blob/master/LICENSE.md — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 快照确认仓库身份、计数、Elixir 主语言、活动状态与 AGPL-3.0 许可证。 Sources: S1, S4
- [F2] Plausible 是隐私优先的网站分析工具，可使用托管服务或自行托管 Community Edition。 Sources: S2
- [F3] README 说明它不使用 Cookie，并提供页面、来源、目标、事件、漏斗、实时数据、报告、共享和统计 API。 Sources: S2
- [F4] README 列出的主要技术包括 Elixir、Phoenix、PostgreSQL、ClickHouse、React 和 Tailwind。 Sources: S1, S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 160427405 | F1 | verified |
| `repository.fullName` | plausible/analytics | F1 | verified |
| `repository.name` | analytics | F1 | verified |
| `repository.stars` | 28861 | F1 | verified |
| `repository.forks` | 1833 | F1 | verified |
| `repository.language` | Elixir | F1 | verified |
| `repository.pushedAt` | 2026-09-03T14:21:35Z | F1 | verified |
| `repository.license` | GNU Affero General Public License v3.0 | F1 | verified |
| `repository.state` | active | F1 | verified |
| `editorial.hook` | 只看网站发生什么，不追踪访问者是谁 | F2, F3 | verified |
| `editorial.summary` | Plausible 用一段轻量统计脚本收集网站访问、来源、页面和自定义事件，再把结果放进一页式仪表盘。它不依赖 Cookie，也不保存可直接识别个人的信息；目标、漏斗、实时数据、定期报告和统计 API 帮助站点负责人持续观察内容是否有效。 | F2, F3 | verified |
| `editorial.meaning` | 它证明网站分析不必先建立个人画像；匿名聚合、事件目标和简洁报告可以被复用到重视隐私的小型公共互动场景。 | I1 | inferred |
| `editorial.audience` | 需要了解网站内容和转化表现，同时希望减少个人追踪的站点负责人、创作者与小团队。 | F2 | verified |
| `editorial.features` | ["无 Cookie 的隐私优先统计", "页面与访问来源的一页式仪表盘", "自定义事件、目标和漏斗", "实时数据与定期报告", "共享链接、导入、CSV 和统计 API"] | F2, F3 | verified |
| `editorial.stack` | ["Elixir", "Phoenix", "PostgreSQL", "ClickHouse", "React", "Tailwind CSS"] | F4 | verified |
| `editorial.opportunity` | ["把匿名事件统计改造成社区活动公开进度板。", "把目标和来源分析改造成独立创作者的阅读回声报告。", "把实时事件和简洁仪表盘改造成展览互动热区图。"] | I1, I2, I3, I4 | inferred |

## Product inferences

- [I1] 它证明网站分析不必先建立个人画像；匿名聚合、事件目标和简洁报告可以被复用到重视隐私的小型公共互动场景。 Basis: F2, F3. Confidence: high
- [I2] 可将原项目能力改造成“社区活动计数板”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I3] 可将原项目能力改造成“创作者阅读回声”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I4] 可将原项目能力改造成“展览互动热区图”这类独立产品。 Basis: F2, F3. Confidence: medium

## Direction rationale

### D1 — 社区活动计数板

- Reused capability: 无 Cookie 事件统计、目标与共享仪表盘
- Evidence: F2, F3
- New audience and recurring problem: 社区组织者和参与居民；社区活动需要公开传播效果，但不应为统计点击而建立居民画像。
- Input and visible outcome: 输入是活动链接、二维码与匿名事件；最终得到不含个人记录的活动进度板。
- Original workflow: 网站接入轻量统计脚本后，系统聚合页面、来源、事件和转化数据，并在一页仪表盘里查看趋势。
- New workflow: 分配事件→聚合来源→核对趋势→公开进度
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只显示聚合数量，不建立个人档案，也不替代正式报名系统。
- Substantive difference: 从站点经营分析改成面向社区透明度的公开汇总产品。

### D2 — 创作者阅读回声

- Reused capability: 页面统计、自定义目标和定期报告
- Evidence: F2, F3
- New audience and recurring problem: 经营个人网站和通讯的独立创作者；独立创作者知道总访问量，却难以快速判断哪些文章和来源带来持续阅读。
- Input and visible outcome: 输入是文章页面、来源和阅读完成事件；最终得到内容阅读回声周报。
- Original workflow: 网站接入轻量统计脚本后，系统聚合页面、来源、事件和转化数据，并在一页仪表盘里查看趋势。
- New workflow: 接入页面→聚合阅读→比较来源→生成周报
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只呈现匿名内容数据，不判断读者身份或兴趣标签。
- Substantive difference: 把通用网站指标改成围绕内容复盘的固定周报。

### D3 — 展览互动热区图

- Reused capability: 实时事件、聚合筛选和简洁仪表盘
- Evidence: F2, F3
- New audience and recurring problem: 博物馆和社区展览策展人；小型展览想改善动线，却没有预算部署复杂摄像或身份识别系统。
- Input and visible outcome: 输入是展签二维码与互动按钮事件；最终得到展览互动热区图和调整清单。
- Original workflow: 网站接入轻量统计脚本后，系统聚合页面、来源、事件和转化数据，并在一页仪表盘里查看趋势。
- New workflow: 编号点位→收集匿名触碰→按时段聚合→标记冷热点
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不使用人脸、设备指纹或个体轨迹。
- Substantive difference: 输入从网页访问变成线下展区互动，结果变成空间布置建议。

## Pairwise direction comparison

- 社区活动计数板 vs 创作者阅读回声
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“社区组织者和居民”与“独立创作者”；输入分别是“活动链接、二维码与匿名事件”与“文章页面、来源和阅读完成事件”；流程分别是“分配事件→聚合来源→核对趋势→公开进度”与“接入页面→聚合阅读→比较来源→生成周报”
- 社区活动计数板 vs 展览互动热区图
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“社区组织者和居民”与“展览策展人”；输入分别是“活动链接、二维码与匿名事件”与“展签二维码与互动按钮事件”；流程分别是“分配事件→聚合来源→核对趋势→公开进度”与“编号点位→收集匿名触碰→按时段聚合→标记冷热点”
- 创作者阅读回声 vs 展览互动热区图
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“独立创作者”与“展览策展人”；输入分别是“文章页面、来源和阅读完成事件”与“展签二维码与互动按钮事件”；流程分别是“接入页面→聚合阅读→比较来源→生成周报”与“编号点位→收集匿名触碰→按时段聚合→标记冷热点”

## Uncertainty

- 本批只验证仓库公开资料，不推断未在 README 或发布页出现的商业能力。

## Localization decisions

- 保留必要的产品名和基础技术名词，并在相邻句中说明它们的作用。

## Refresh notes

- Initial research; no prior published snapshot.
