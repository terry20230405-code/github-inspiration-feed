# snapotter-hq/SnapOtter research notes

Research date: 2026-09-01
Repository: https://github.com/snapotter-hq/SnapOtter
Research mode: new

## Snapshot

- Repository ID: 1195367387
- Repository full name: snapotter-hq/SnapOtter
- Repository name: SnapOtter
- Stars at fetch time: 2399
- Forks at fetch time: 118
- Primary language: TypeScript
- Latest push at fetch time: 2026-08-31T16:44:04Z
- License: GNU Affero General Public License v3.0
- Default branch: main
- README SHA: 0656e1f9a090dcfbd65d7437ae43b9dc2920b204
- Latest release: v2.2.0 / 2026-07-29T14:05:40Z
- Repository state: active
- Fetched at: 2026-09-01T03:08:04Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/snapotter-hq/SnapOtter — accessed 2026-09-01
- [S2] Official README — https://github.com/snapotter-hq/SnapOtter/blob/main/README.md — accessed 2026-09-01
- [S3] Latest official release — https://github.com/snapotter-hq/SnapOtter/releases/tag/v2.2.0 — accessed 2026-09-01

## Verified repository facts

- [F1] 仓库是 snapotter-hq/SnapOtter，GitHub ID 为 1195367387，当前非 fork、未归档、未禁用。 Sources: S1
- [F2] 仓库星标 2399、Fork 118，主语言是 TypeScript，最新 push 时间为 2026-08-31T16:44:04Z，许可证为 AGPL-3.0。 Sources: S1
- [F3] README 将 SnapOtter 定位为开源、自托管的文件处理基础设施，强调文件不会离开你的网络，并提供 UI、REST API 和 pipelines。 Sources: S2
- [F4] 它接受 image、video、audio、PDF 和 documents/files，能做 convert、compress、OCR、transcribe、strip metadata，并运行 local AI。 Sources: S2
- [F5] README 还明确列出 image editor、OIDC/SSO、21 种语言、pipelines 的 JSON 导入导出，以及带 API key 的 REST API。 Sources: S2
- [F6] 部署方式包括 Docker 单容器快速启动，以及 app + Postgres 17 + Redis 8 的生产 Compose 栈。 Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 1195367387 | F1 | verified |
| `repository.fullName` | snapotter-hq/SnapOtter | F1 | verified |
| `repository.name` | SnapOtter | F1 | verified |
| `repository.stars` | 2399 | F2 | verified |
| `repository.forks` | 118 | F2 | verified |
| `repository.language` | TypeScript | F2 | verified |
| `repository.pushedAt` | 2026-08-31T16:44:04Z | F2 | verified |
| `repository.license` | AGPL-3.0 | F2 | verified |
| `repository.state` | active | F1 | verified |
| `editorial.hook` | 把文件处理搬进内网工厂 | F3, F4 | inferred |
| `editorial.summary` | 解释输入、核心动作、多个已验证能力和结果。 | F3, F4, F5, F6 | inferred |
| `editorial.meaning` | 说明这些能力为什么适合拆成更小的复用产品。 | F3, F4, F5, F6 | inferred |
| `editorial.audience` | 需要在自己网络里批量处理图片、视频、音频、PDF 和通用文件的人和团队。 | F3, F4, F6 | inferred |
| `editorial.features` | 列出 3-6 个已验证核心能力。 | F4, F5 | verified |
| `editorial.stack` | TypeScript、Docker、Postgres 17、Redis 8、REST API、OpenID Connect。 | F2, F5, F6 | verified |
| `editorial.opportunity` | 把现有能力拆成归档台、媒体管线和内网 API 三条更窄的产品路。 | F3, F4, F5, F6 | inferred |

## Product inferences

- [I1] 这个仓库足以被准确解释成一套自托管文件处理平台，而不是单一工具。 Basis: F3, F4, F6. Confidence: high
- [I2] 主要用户可以合理推断为需要内网处理文件、重视数据不外流的个人、团队和管理员。 Basis: F3, F4, F6. Confidence: medium
- [I3] 它的可复用能力核心在于多模态文件处理、OCR/转写、local AI 和 pipelines/API 编排。 Basis: F4, F5, F6. Confidence: high
- [I4] 这些能力可以稳定拆成文档归档、媒体批处理和内部文件 API 三种不同的新产品。 Basis: F3, F4, F5. Confidence: high

## Direction rationale

### D1 — 档案整理台

- Reused capability: 复用 OCR、PDF 工具、UI、REST API 和自托管部署能力。
- Evidence: F3, F4, F5, F6
- New audience and recurring problem: 面向财务、行政、法务和档案人员；他们反复要把扫描件、合同、票据和 PDF 整理成可检索、可留存的内网文件。
- Input and visible outcome: 输入是扫描件、图片和 PDF；经过 OCR、拆分、合并、脱敏和导出后，得到可归档的文档包。
- Substantive difference: 比原项目更窄，只保留文档归档这条工作流，不覆盖音视频和通用文件处理。

### D2 — 媒体批处理管线

- Reused capability: 复用多模态文件处理、pipelines、批处理和局部媒体工具。
- Evidence: F4, F5, F6
- New audience and recurring problem: 面向内容运营、剪辑、播客后期或个人素材整理者；他们会反复做转码、压缩、提取音频、调尺寸和批量清理素材。
- Input and visible outcome: 输入是一批图片、视频和音频；经过预设 pipeline 处理后，输出统一规格的成品文件。
- Substantive difference: 比原项目更像一套媒体生产工具，只围绕图片、视频和音频批处理。

### D3 — 内网文件 API

- Reused capability: 复用 REST API、API key 认证、单工具能力和 pipelines。
- Evidence: F3, F4, F5, F6
- New audience and recurring problem: 面向后端工程师和内部平台团队；他们常常需要在自己的系统里补上转换、OCR、转写和压缩能力，而不想接外部 SaaS。
- Input and visible outcome: 输入是业务系统发来的文件和 API 调用；处理后返回文件结果或结构化输出，供其他服务继续使用。
- Substantive difference: 比原项目更偏后端集成，主要通过 API 使用，不以人工操作界面为中心。

## Uncertainty

- 官方文档没有直接列出典型行业用户，用户画像只能从自托管、隐私和多模态文件处理定位推断。

## Localization decisions

- 保留 REST API、pipeline、OCR、SSO、Docker、Postgres、Redis、TypeScript 这些基本术语，因为它们直接影响复用判断。
- 把 self-hosted 统一表达为“自托管”，把 no external SaaS 译为“外部 SaaS”，保持产品含义清楚。
- README 没有单独点名典型行业用户，因此 audience 采用基于自托管和隐私定位的推断写法。

## Refresh notes

- Initial research; no prior published snapshot.
