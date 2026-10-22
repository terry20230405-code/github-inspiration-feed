# CorentinTh/it-tools research notes

Research date: 2026-09-04
Repository: https://github.com/CorentinTh/it-tools
Research mode: new

## Snapshot

- Repository ID: 253222599
- Repository full name: CorentinTh/it-tools
- Repository name: it-tools
- Stars at fetch time: 40463
- Forks at fetch time: 5386
- Primary language: Vue
- Latest push at fetch time: 2026-09-03T22:29:01Z
- License: GNU General Public License v3.0
- Default branch: main
- README SHA: 72cbbd8d93469b91a93d39486dbd1a1b33c8884c
- Latest release: v2024.10.22-7ca5933 / 2024-10-22T09:58:03Z
- Repository state: active
- Fetched at: 2026-09-04T05:57:44Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/CorentinTh/it-tools — accessed 2026-09-04
- [S2] Official README — https://github.com/CorentinTh/it-tools/blob/main/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/CorentinTh/it-tools/releases/tag/v2024.10.22-7ca5933 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/CorentinTh/it-tools/blob/main/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] 仓库的 GitHub 数字 ID 是 253222599，规范全名是 CorentinTh/it-tools。 Sources: S1
- [F2] 仓库显示名是 it-tools。 Sources: S1
- [F3] 仓库当前星标数为 40463，Fork 数为 5386。 Sources: S1
- [F4] 主语言是 Vue。 Sources: S1
- [F5] 最新推送时间是 2026-09-03T22:29:01Z，仓库未归档、未禁用，也不是 fork。 Sources: S1
- [F6] GitHub 识别的许可证是 GNU GPLv3。 Sources: S1, S4
- [F7] README 将项目定位为面向开发者和 IT 从业者的实用工具集合。 Sources: S2
- [F8] README 明确提供自托管方案，并给出 Docker 运行命令。 Sources: S2
- [F9] 最新 release 新增了 Regex Tester（和 Cheatsheet）、Markdown to HTML、email normalizer、JSON to XML/XML to JSON。 Sources: S3
- [F10] 最新 release 提到 Base64 enhancements。 Sources: S3
- [F11] 最新 release 提到 lorem-ipsum 刷新按钮。 Sources: S3
- [F12] README 说明可以用脚本生成新工具目录，并把它导入 src/tools/index.ts。 Sources: S2
- [F13] 官方 LICENSE 文件与 GitHub 检测结果一致，均指向 GPL-3.0。 Sources: S1, S4

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 253222599 | F1 | verified |
| `repository.fullName` | CorentinTh/it-tools | F1 | verified |
| `repository.name` | it-tools | F2 | verified |
| `repository.stars` | 40463 | F3 | verified |
| `repository.forks` | 5386 | F3 | verified |
| `repository.language` | Vue | F4 | verified |
| `repository.pushedAt` | 2026-09-03T22:29:01Z | F5 | verified |
| `repository.license` | GNU GPLv3 / GPL-3.0 | F13 | verified |
| `repository.state` | active（未归档、未禁用、不是 fork） | F5 | verified |
| `editorial.hook` | 把开发杂活拆成一个个小工具 | F7, F8, F9, F10, F11 | inferred |
| `editorial.summary` | 说明这个仓库是一个面向开发者和 IT 从业者的多工具网页，覆盖正则、Markdown、JSON/XML、Base64、邮箱规范化，并支持自托管。 | F7, F8, F9, F10, F11 | verified |
| `editorial.meaning` | 说明这些通用小工具适合拆成更窄的单用途产品。 | F7, F9, F10, F11, F12 | inferred |
| `editorial.audience` | 开发者和 IT 从业者 | F7 | verified |
| `editorial.features` | 列出已明确验证的核心能力。 | F9, F10, F11 | verified |
| `editorial.stack` | Vue、TypeScript、Docker | F4, F8, F12 | verified |
| `editorial.opportunity` | 给出从现有能力到更窄产品的具体桥接理由。 | F9, F10, F11, F12 | inferred |

## Product inferences

- [I1] 这是一个由多个单用途网页工具组成的开发者工具箱。 Basis: F7, F9, F10, F11, F12. Confidence: high
- [I2] 这些能力共享同类输入-处理-结果交互骨架，因此可以拆成更窄的专用产品。 Basis: F9, F10, F11, F12. Confidence: high
- [I3] 自托管使它更适合内网、实验室或本地部署场景。 Basis: F8, F13. Confidence: medium

## Direction rationale

### D1 — 正则练习台

- Reused capability: 复用已验证的 regex tester 和 cheatsheet 能力。
- Evidence: F3, F5, F12
- New audience and recurring problem: 面向经常写校验、搜索和过滤规则的前端/后端开发者，以及正在学正则的人；他们每次都要反复试一段规则是否真的命中样本文本。
- Input and visible outcome: 原项目的输入是各种不同任务的文本或数据，结果分散在多个工具里；新方向只吃正则和样本文本，输出匹配高亮、命中列表和速查提示。
- Original workflow: 开发者和 IT 从业者打开工具站，在多个工具之间切换，完成各类一次性小任务。
- New workflow: 用户粘贴一段文本、写下正则、切换必要选项后，立刻查看匹配位置和说明，把试错过程压缩成一个循环。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 这是一个面向正则学习与校验的单用途产品，不再保留整个工具站的广泛入口。
- Substantive difference: 原项目是一个通用开发工具集合；这个方向把其中的 regex tester 和 cheatsheet 收拢成单一练习台，只服务“输入正则和文本→立刻验证并理解结果”。

### D2 — 数据格式转换台

- Reused capability: 复用 JSON/XML 互转、Markdown to HTML 和 Base64 处理能力。
- Evidence: F3, F6, F7, F8
- New audience and recurring problem: 面向经常在接口、文档和代码片段之间搬运内容的前后端开发者；他们需要把同一份数据快速转成不同结构，避免手工改格式。
- Input and visible outcome: 原项目允许用户在不同工具里分别处理不同类型内容；新方向统一接收待转换文本，输出可直接复制的目标格式。
- Original workflow: 用户先进入通用工具站，再按任务切换到对应的小工具。
- New workflow: 用户贴入数据、选择源/目标格式，系统完成转换并给出可复制结果和错误提示。
- Materially changed axes: input, workflow, outcome
- Product form: end-user-product
- Product boundary: 这是一个以格式互转为核心的专用产品，不是原站点的完整复刻。
- Substantive difference: 原项目提供多种分散的小工具；这个方向把 JSON、XML、Markdown 和 Base64 这些已验证能力合并成一个转换台，只做“贴入内容→选目标格式→得到结果”。

### D3 — 内网工具柜

- Reused capability: 复用自托管部署、收藏保存和多工具导航能力。
- Evidence: F3, F4, F9, F12
- New audience and recurring problem: 面向小团队、实验室管理员和内网协作成员；他们需要一个统一入口放常用开发工具，而不是每个人各自收藏一堆外部网页。
- Input and visible outcome: 原项目的输入是单次处理的文本或数据；新方向的输入是团队日常会反复选择和收藏的工具需求，输出是一个可控的内部工具页。
- Original workflow: 开发者和 IT 从业者打开公开网站，临时找工具解决手头任务。
- New workflow: 团队部署到自己的环境后，把常用工具加入收藏，成员直接从内网页面进入需要的转换器或解析器。
- Materially changed axes: audience, workflow, outcome
- Product form: end-user-product
- Product boundary: 这是一个面向团队自托管的内部工具柜，不是原站点的公共首页原样复制。
- Substantive difference: 原项目是公开的多工具站；这个方向把自托管、收藏和多工具导航结合成团队内部工具页，重点是共享入口和固定复用。

## Pairwise direction comparison

- 正则练习台 vs 数据格式转换台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 前者服务想把正则写准的人，后者服务在 JSON、XML、Markdown 和 Base64 之间搬运数据的人；前者输入模式和样本文本，后者输入待转换内容；前者看匹配结果，后者看转换后的文本。
- 正则练习台 vs 内网工具柜
  - Different axes: audience, workflow, outcome
  - Concrete comparison: 前者面向个人试正则，后者面向团队共用工具入口；前者是单次验证，后者是收藏和复用常用工具；前者结果是规则是否命中，后者结果是一个可自托管的内部工具页。
- 数据格式转换台 vs 内网工具柜
  - Different axes: audience, workflow, outcome
  - Concrete comparison: 前者是单人转换台，后者是团队收藏工具页；前者围绕一次性格式处理，后者围绕常用工具复用；前者输出转换后的内容，后者输出内部统一入口。

## Uncertainty

- README 没有完整列出全部工具目录，因此 `features` 只写已被 README 或最新 release 明确点名的能力。

## Localization decisions

- 将 self-host 译为“自托管”，因为它在 README 中直接指向部署方式。
- 将 cheatsheet 译为“速查表”，保留 Regex Tester、Base64、JWT 等必要英文/缩写。

## Refresh notes

- Initial research; no prior published snapshot.
