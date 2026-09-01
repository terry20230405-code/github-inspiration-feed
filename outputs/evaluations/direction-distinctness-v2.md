# 改造方向差异标准 v2 评测

- 评测日期：2026-09-01
- 固定测试集版本：1
- 修改范围：方向生成、D3 单方向差异审核、E1 两两差异审核、定向修复
- 证据方法：每个案例固定使用仓库现有的 `.project.json` 与 `.research.md`，不刷新 Star、README 或其他来源，不把页面旧文案当作新的仓库事实
- 副作用：没有修改 `src/data/`，没有发布任何测试项目

## 修改前后的判断差异

修改前，生成器只需要为方向写一段自由文本 `difference`，评审也只返回 D3/E1 的一段自由文本证据。像“只处理媒体”“改为 API 调用”这样的描述，即使原项目已经提供相同处理流程或 API，也可能被误判为新产品。

修改后增加两张强制表：

1. 每个方向都必须写出原项目流程、新流程、相对原项目发生实质变化的轴和产品边界。
2. 所有方向必须两两比较用户、输入、核心工作流和可见结果。

程序要求每个方向和每一对方向至少声明两个不同轴，并限制整组最多一个开发者基础设施方向。独立审核 AI 必须重新判断这些差异；它不能直接照抄生成器的声明。任一逐方向审计失败时 D3 必须失败，任一两两审计失败时 E1 必须失败。

## 五个固定案例

| 仓库 | 固定证据 | 旧方向的 v2 复核重点 | 预期结果 |
| --- | --- | --- | --- |
| remotion-dev/remotion | `outputs/generated/published-baseline/remotion-dev-remotion.project.json` 与对应 research | 三个方向都以内容输入生成视频，虽然用户和素材不同，但核心工作流与结果高度接近 | E1 应比旧标准更严格；至少替换一个方向，避免全部成为视频营销/内容模板 |
| excalidraw/excalidraw | `outputs/generated/published-baseline/excalidraw-excalidraw.project.json` 与对应 research | 故事关系图、课堂演示、手机快速草图具有不同用户、输入、流程和结果 | 保持可通过，不因标准收紧而误杀真正不同的方向 |
| immich-app/immich | `outputs/generated/published-baseline/immich-app-immich.project.json` 与对应 research | 家庭周报、旅行地图、隐私清理分别改变消费频率、组织流程和可见结果 | 保持可通过 |
| n8n-io/n8n | `outputs/generated/published-baseline/n8n-io-n8n.project.json` 与对应 research | 都复用自动化执行器，但输入来源、用户工作流和结果分别是合作收件箱、经营行动与个人晨报 | 保持可通过；复用同一底层能力不等于产品换皮 |
| usememos/memos | `outputs/generated/usememos-memos.project.json` 与 `outputs/generated/usememos-memos.research.md` | 语音收件、旧素材回访、多人家庭周记分别改变入口、回顾机制、协作关系和输出 | 保持可通过 |

固定案例说明新规则不是要求每个方向使用不同技术，而是要求它们围绕同一真实能力形成不同的完整产品体验。

## SnapOtter 负面回归案例

固定输入：

- `outputs/generated/discovery-batches/20260901T030804Z-80106c39/snapotter.project.json`
- `outputs/generated/discovery-batches/20260901T030804Z-80106c39/snapotter.research.md`

旧结果错误地把 SnapOtter 判为全部通过。按照 v2：

- “档案整理台”需要证明归档流程和归档包结果相对通用文件处理至少改变两个轴，不能只说“只处理文档”。
- “媒体批处理管线”与原项目已经提供的媒体工具、pipeline 和批处理流程基本相同；只收窄文件类型和用户群不足以通过 D3。
- “内网文件 API”直接复述原项目已有 REST API、API key、工具路由和 pipeline 调用；没有新接口契约、新集成流程或新结果，必须在 D3 失败。
- 因此该版本不能成为发布候选，即使三个标题看起来不同。

## 自动化检查

- 生成结构缺少任意方向对照或任意两两组合时失败。
- 单方向少于两个唯一变化轴时失败。
- 超过一个开发者基础设施方向时失败。
- 审核表中存在失败方向但 D3 标为通过时，判为结构错误并进入修复。
- 审核表中存在失败方向对但 E1 标为通过时，判为结构错误并进入修复。
- 新字段只存在于生成与审核过程，不改变网页项目 JSON 的三层产品结构。
