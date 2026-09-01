# GitHub 项目灵感流

一个手机优先的 GitHub 项目灵感浏览器。用户可以像刷短视频一样上下翻页，从开源项目中发现适合自己的 Vibe Coding 小项目方向。

## 当前功能

- Remotion、Excalidraw、Immich、n8n、Archify 五个已发布项目
- CSS Scroll Snap 整屏翻页
- 支持触摸、鼠标滚轮、键盘方向键和桌面翻页按钮
- 项目摘要、意义、Star、语言、GitHub 链接和拓展方向预告
- 项目再创作详情页
- 拓展依据、方向分析和最小功能范围
- 拓展方向选择
- 当前方向的问题、目标用户、实现方式、差异和最小功能范围
- 手机和桌面响应式布局

## 本地运行

```bash
npm install
npm run dev
```

默认地址：`http://127.0.0.1:5173`

## 生产构建

```bash
npm run build
```

页面仍使用本地 JSON，不包含登录、数据库、浏览器运行时 GitHub API 或 AI API。自动发现只在 GitHub Actions 服务端使用 GitHub API 与 OpenAI API，密钥不会进入前端构建。项目顺序保存在 `src/data/order.json`，三层数据分别位于 `src/data/repositories.json`、`src/data/editorial.json` 和 `src/data/visuals.json`。同目录下的 TypeScript 加载器会先校验 JSON，`src/data.ts` 再把三层组合给页面；页面拿到的 TypeScript 类型均为只读，避免意外改写源数据。

## GitHub 元数据刷新

阶段六加入了服务端/本地刷新命令。默认只读取 GitHub 并展示变化，不写入文件：

```powershell
npm run refresh:repositories
```

确认报告中的 `reviewRequired` 和 `failed` 都为 `0` 后，才执行：

```powershell
npm run refresh:repositories:write
npm run test:repository-refresh
```

刷新器会自动更新 Star、Fork、推送时间等安全字段；新 push 只触发“建议重新研究”，不会直接重写中文内容。仓库转移、许可证变化、归档、禁用、404、变私有或变成 Fork 都会阻止该项目写入并要求人工确认。结果保存在 `outputs/refresh/latest.json`，条件请求缓存保存在 `outputs/refresh/github-cache.json`。

公开仓库无需 Token；项目增多后可在终端中提供 `GITHUB_TOKEN` 提高限额。刷新规则和退出码见 [`refresh-workflow.md`](skills/github-inspiration-editor/references/refresh-workflow.md)。GitHub 的调用方式遵循[官方 REST API 最佳实践](https://docs.github.com/en/rest/using-the-rest-api/best-practices-for-using-the-rest-api)。

## 仓库内容变化复审

阶段七接收阶段六标记的项目，比较仓库描述、Topics、默认分支、README SHA/内容哈希和最新正式 Release。脚本只生成来源证据包；AI必须针对当前来源指纹写出 `none`、`minor`、`meaningful` 或 `critical` 审核结论。只有 `meaningful + draft` 才会生成新的内容候选，而且候选仍保存在 `outputs/generated/`，不会覆盖已发布页面。

```powershell
npm run refresh:research
npm run refresh:research:write
npm run test:research-refresh
```

来源状态、缓存和报告位于 `outputs/refresh/`，待审核证据和 AI 复审位于 `outputs/generated/research-refresh/`。完整边界见 [`research-refresh-workflow.md`](skills/github-inspiration-editor/references/research-refresh-workflow.md)。

## 版本控制与回滚

阶段八使用两层保护：本地 Git 保存整个代码项目的里程碑；刷新事务快照保存阶段六和阶段七写入前的数据状态。正式刷新遇到技术失败或关键人工决策时，会自动恢复整组刷新文件并校验哈希。

```powershell
npm run versions:list
npm run versions:diff -- <snapshot-id>
npm run versions:restore -- <snapshot-id>
npm run versions:restore -- <snapshot-id> --write
```

恢复默认只预演，真正恢复前还会创建一张安全快照。也可以使用 `--project immich` 只恢复某个项目。快照与事务记录位于 `outputs/versions/`，不会混进 Git 提交。完整边界见 [`version-control-workflow.md`](skills/github-inspiration-editor/references/version-control-workflow.md)。

## 后续自动化总控

自动化总控把工程预检、阶段六和阶段七组合成一条有暂停点的流水线，并使用阶段八的快照保护正式写入：

```powershell
npm run refresh:cycle
npm run refresh:cycle:write
npm run refresh:cycle:resume
```

第一个命令只预演；第二个命令写入安全的仓库快照和来源证据；第三个命令在 AI 完成语义审核后继续。统一状态保存在 `outputs/automation/latest.json`，历史运行保存在 `outputs/automation/runs/`。流水线会区分“已完成、等待 AI、需要草稿、需要用户决定、技术失败”，所有结果都固定为 `publicationAuthorized: false`。

自动化总控与已发布项目刷新仍遵循暂停边界。新项目发现已经由独立工作流定时运行；公网部署平台仍未接入。完整职责、恢复方式和 AI 续跑规则见 [`automation-workflow.md`](skills/github-inspiration-editor/references/automation-workflow.md)。

## 自动发现新项目

`.github/workflows/discover-projects.yml` 默认在每周二、周五北京时间 09:00 自动运行，也支持在 GitHub Actions 页面手动启动。默认每次让 AI 深读最多 12 个仓库，生成最多 8 个候选，也就是理论上每周最多 16 个；实际数量取决于证据和 19 项质量检查。

搜索主题、Star 下限、活跃窗口和每次数量集中保存在 `config/discovery.json`。手动运行时可以临时覆盖 AI 深读数量和候选数量。候选上限不能高于 AI 深读数量，单次候选安全上限为 20。

本地只搜索、不写文件：

```powershell
npm run discover:repositories
```

写入搜索报告：

```powershell
npm run discover:repositories:write
```

自动化在服务端继续读取 README，通过 OpenAI 兼容的 Chat Completions 接口调用 AI、生成项目/研究/质量三件套并创建一张候选审核 PR。当前默认服务地址是 `https://4router.net/v1`，模型是 `gpt-5.4`；这两个公开配置保存在 `config/discovery.json`，API Key 仍只放在 GitHub Secret 中。它不会直接改页面：

- 合并候选 PR：明确批准整批，随后一次性写入四层产品数据并运行完整检查。
- 关闭候选 PR：拒绝整批，正式页面不改变。
- 发布中任一检查失败：四层页面数据全部恢复，不产生半成品。

其中 GitHub ID、仓库名、许可证、状态、抓取时间、Star、Fork 和推送时间由程序直接对照本轮 GitHub 快照，不再让 AI 判断。需要理解上下文的来源矛盾和不确定性仍由 AI 严格审核。即使一轮最终是 0 个候选，Actions 页面也会保留 30 天的 `discovery-audit-<run-id>` 审计文件，里面能看到每个仓库的具体失败证据和两轮修复轨迹。

首次启用需要在 GitHub 仓库的 Actions Secrets 中添加 `OPENAI_API_KEY`（这个名字为兼容现有设置而保留，里面可以保存当前 4Router Key），并允许 GitHub Actions 写入仓库和创建 Pull Request。`GITHUB_TOKEN` 由 Actions 自动提供，不要把任何 Token 写入代码或前端。以后若更换兼容服务，可以在 Actions Variables 中设置 `AI_API_BASE_URL` 和 `AI_MODEL` 临时覆盖仓库默认值，不需要修改密钥读取代码。完整搜索、授权和恢复边界见 [`discovery-workflow.md`](skills/github-inspiration-editor/references/discovery-workflow.md)。

## 校验项目草稿

```bash
npm run validate:research -- outputs/generated/<owner>-<repo>.research.md
npm run validate:project -- outputs/generated/<owner>-<repo>.project.json
```

项目草稿采用 schema version 2 的 `repository`、`editorial`、`visual` 三层结构，不再生成展示分类、方向难度或开发天数。Star 和 Fork 保存原始数字，推送与抓取时间保存 UTC ISO 时间，缩写和相对时间只在页面显示时计算。

## 确定性视觉身份

新仓库以 `owner/repository` 为稳定种子生成受约束主题色、前景色、SVG 图形家族和变体参数。视觉生成器 v2 同时检查色相间隔和 OKLab 感知距离；新增卡片必须用 `--avoid` 传入相邻卡片颜色，避免数字不同但肉眼仍像同一种绿色。结果完整保存在 `visual` 中，页面刷新和 GitHub 元数据更新不会重新抽取。前端的 `ProjectIdentity` 通用组件根据配置渲染 5–12 个 SVG 元素，不再包含 Remotion、Immich 等项目名 CSS。

```bash
python skills/github-inspiration-editor/scripts/generate_visual_identity.py owner/repository --family-hint photo --avoid '#588019'
npm run test:visual-identity
npm run test:identity-renderer
```

追加项目时传前一张卡片的颜色；插入项目时传前后两张卡片的颜色。`test:visual-identity` 会按真实页面顺序检查所有相邻项目。图形家族选择、相邻颜色避让和版本稳定规则见 [`visual-identity.md`](skills/github-inspiration-editor/references/visual-identity.md)。

页面字段的唯一内容契约见 [`content-contract.md`](skills/github-inspiration-editor/references/content-contract.md)。新增、删除或改变字段职责时，需要同步更新前端、类型、schema、校验器和现有数据。

## 内容质量评估

格式校验通过只代表“资料没有漏填”，不代表文字已经写好。内容质量使用 19 个必要检查项，覆盖事实、原项目解释、技术表达层次、字段分工、单个改造方向和整组方向差异。每项只有“通过”或“失败”；全部通过才成为发布候选。

自动候选还必须提供方向差异证明：逐个比较原项目与新方向的用户、输入、核心工作流和可见结果，并列出所有方向的两两对照。每个方向相对原项目、每一对方向之间都至少要有两项实质变化；已有 API、同一处理管线换文件类型或行业名称不能单独算新产品，整组最多保留一个真正成立的开发者基础设施方向。

- [内容质量评分标准](skills/github-inspiration-editor/references/quality-rubric.md)
- [内容质量自动修复闭环](skills/github-inspiration-editor/references/quality-repair-loop.md)
- [固定质量测试仓库集](skills/github-inspiration-editor/references/benchmark-set.md)

出现失败项时，AI 只修复对应字段并重新检查；同一问题使用两种方案仍无法解决时，停止并询问用户。Skill 的生成规则发生变化时，使用相同研究证据对修改前后进行比较。测试结果保存在 `outputs/evaluations/`，不会自动加入产品页面。
