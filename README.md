# GitHub 项目灵感流

一个面向 Vibe Coding 用户的中文 GitHub 项目发现与再创作平台。

它不只是展示仓库信息，而是持续从 GitHub 搜索值得关注的开源项目，读取 README 和仓库证据，用 AI 生成容易理解的中文介绍与可继续开发的产品方向，再经过质量检查和人工审核加入灵感流。用户可以像浏览内容流一样发现项目，也可以进入详情页了解原项目、适合人群和三个具体改造方向。

## 核心功能

### 项目灵感流

- 整屏浏览 GitHub 项目，支持触摸、滚轮、键盘和桌面翻页操作。
- 展示项目简介、核心价值、Star、技术语言和 GitHub 原仓库链接。
- 每个项目提供三个重新设计或继续开发的产品方向。
- 详情页解释原项目能力、适合人群、技术基础、机会判断和最小功能范围。
- 前端使用轻量索引和按项目拆分的数据文件，项目数量增长后不需要一次加载全部正文。

### 自动发现新项目

- GitHub Actions 默认在每周二、周五自动搜索 GitHub。
- 搜索范围覆盖 AI、自动化、设计、影音、照片、知识管理、效率、数据、学习、自托管和创作者工具等方向。
- 程序先根据活跃时间、Star、README 完整度、许可证和排除规则筛选仓库。
- AI 深读仓库证据，生成中文介绍、目标读者、核心能力和三个改造方向。
- 候选内容必须通过事实、表达、方向差异和可执行性等 19 项质量检查。
- 自动化为合格候选创建审核 PR；合并 PR 后，正式项目数据会自动写入 `main`。

### 已发布项目持续巡检

- 每次自动发现开始前，先检查已经发布的项目。
- Star、Fork、推送时间等安全字段可以自动刷新。
- README、Topics、Release 或仓库状态发生变化时，系统会生成复审证据。
- 中文介绍、改造方向和视觉身份不会因为一次仓库更新而被程序直接覆盖。
- 仓库转移、归档、变私有、许可证变化等高风险情况会停止自动写入，等待人工判断。

### 内容质量与自动修复

- GitHub ID、仓库名、许可证、Star、Fork 和抓取时间由程序直接核对，不交给 AI 猜测。
- AI 负责需要理解语义的内容，例如项目意义、目标用户和产品改造方向。
- 候选失败后，只针对失败字段进行修复并重新检查。
- 两轮不同修复方案仍不能通过时，停止发布并保留完整失败证据。

### 确定性视觉身份

- 使用仓库完整名称作为稳定种子，自动生成主题色、前景色和 SVG 图形参数。
- 相邻项目会检查色相与感知距离，避免连续出现肉眼相近的颜色。
- 生成结果保存在项目数据中，算法升级不会让已经发布的项目突然改变外观。
- 前端通过通用组件渲染视觉图形，不需要为每个仓库单独编写 CSS。

### 版本保护与回滚

- Git 保存整个项目的正式版本。
- 自动刷新和发布前会创建数据快照与事务记录。
- 写入过程失败时可以恢复整批数据，避免出现只更新一部分的页面。
- 支持查看版本差异、恢复全部项目或只恢复指定项目。

## 完整工作流

```text
定时搜索 GitHub
        ↓
程序筛选仓库并保存一手证据
        ↓
AI 深读并生成中文候选内容
        ↓
19 项质量检查与定向自动修复
        ↓
创建候选审核 PR
        ↓
人工合并表示批准
        ↓
自动写入正式数据并运行完整测试
        ↓
进入项目灵感流
```

同一条定时任务还会巡检旧项目，因此新项目发现和已发布内容维护可以长期并行运行。前端不直接调用 GitHub API 或 AI API，所有密钥只在 GitHub Actions 中使用。

## 技术组成

- 前端：React、TypeScript、Vite
- 自动化：Python 3.12、GitHub Actions
- 数据：本地 JSON
- 仓库信息：GitHub REST API
- 内容分析：OpenAI 兼容的 Chat Completions API
- 视觉系统：确定性颜色算法与内联 SVG
- 版本保护：Git、数据快照和刷新事务

项目不依赖数据库，也不要求单独购买服务器。网页可以作为静态站点构建；定时搜索、AI 分析和旧项目巡检由 GitHub Actions 运行。

## 安装与本地运行

### 环境要求

- Node.js 22
- npm
- Python 3.12（只浏览和开发前端时可以暂时不安装；运行自动化脚本时需要）
- Git

### 1. 获取项目

```bash
git clone https://github.com/terry20230405-code/github-inspiration-feed.git
cd github-inspiration-feed
```

### 2. 安装依赖

```bash
npm install
```

### 3. 启动开发网页

```bash
npm run dev
```

默认访问地址：`http://127.0.0.1:5173`

启动前会自动根据正式项目数据生成浏览器需要的轻量索引和独立项目 JSON，不需要手动执行数据拆分命令。

## 生产构建

```bash
npm run build
npm run preview
```

构建结果位于 `dist/`。`npm run build` 同样会先生成运行时项目数据，再执行 TypeScript 检查和 Vite 构建。

## 项目数据

正式数据源位于 `src/data/`：

- `order.json`：项目展示顺序。
- `repositories.json`：GitHub 仓库事实和动态数字。
- `editorial.json`：中文介绍、内容分析和改造方向。
- `visuals.json`：稳定主题色和 SVG 视觉参数。

开发或构建时，`scripts/generate-project-data.mjs` 会生成：

- `public/data/projects/index.json`：只包含首屏和导航所需的轻量信息。
- `public/data/projects/<project-id>.json`：单个项目的完整数据。

`public/data/projects/` 是自动生成目录，不应手动维护。自动发现和发布工作流仍然只修改 `src/data/` 中的正式数据源。

### 中英文切换

首页和详情页右上角提供「中文 / EN」切换，默认中文，并在浏览器中保存语言偏好。切换不会重置当前项目或已选方向。

界面文案位于 `src/i18n.ts`，项目英文译文位于 `src/locales/projects.en.json`，不修改中文正式数据。生成脚本将译文随单个项目 JSON 一起输出，保留窗口懒加载。英文层和项目顺序必须拥有完全相同的项目 ID；新增项目缺少英文或英文中残留中文时，开发启动和生产构建会直接失败，避免页面静默混用两种语言。

修改译文后运行 `node scripts/generate-project-data.mjs` 并刷新页面。使用 `npm run test:i18n` 检查全项目覆盖、字段、方向 ID、技术名称、时间文案和语言偏好保存。更多约定见 [翻译维护说明](src/locales/README.md)。

## 配置 GitHub 自动化

### 1. 添加 AI API Key

进入仓库：

```text
Settings → Secrets and variables → Actions → New repository secret
```

添加：

```text
OPENAI_API_KEY=你的 API Key
```

变量名为了兼容现有工作流而保留。只要服务支持 OpenAI Chat Completions 格式，也可以使用第三方兼容 API。

### 2. 配置可选变量

可以在 Actions Variables 中添加：

- `AI_API_BASE_URL`：覆盖默认 API 地址。
- `AI_MODEL`：覆盖默认模型名称。

### 3. 设置 Actions 权限

在仓库 Actions 设置中允许工作流：

- 写入仓库内容。
- 创建 Pull Request。

GitHub 会自动提供 `GITHUB_TOKEN`，不需要自行创建，也不要把任何 Token 写进代码或前端文件。

### 4. 运行自动发现

进入 GitHub 仓库的 `Actions` 页面，选择“自动发现 GitHub 灵感项目”，可以手动运行，也可以等待每周二、周五的定时任务。

自动化会创建候选审核 PR：

- 合并 PR：批准整批候选，随后自动写入正式数据。
- 关闭 PR：拒绝整批候选，正式页面不改变。
- 检查失败：停止发布并保留审计文件。

搜索主题、Star 下限、活跃窗口和单次候选数量位于 `config/discovery.json`。

## 常用命令

| 命令 | 用途 |
| --- | --- |
| `npm run dev` | 启动本地开发网页 |
| `npm run build` | 生成项目数据并构建生产版本 |
| `npm run preview` | 预览生产构建结果 |
| `npm run lint` | 检查前端代码 |
| `npm run discover:repositories` | 本地预演 GitHub 仓库搜索 |
| `npm run refresh:cycle` | 预演已发布项目巡检 |
| `npm run refresh:cycle:write` | 正式写入安全的旧项目更新 |
| `npm run versions:list` | 查看可恢复的数据快照 |
| `npm run versions:diff -- <snapshot-id>` | 查看快照与当前数据的差异 |
| `npm run versions:restore -- <snapshot-id> --write` | 恢复指定快照 |
| `npm run test:feed-data` | 检查运行时项目数据拆分 |
| `npm run test:feed-window` | 检查大规模灵感流加载窗口 |
| `npm run test:visual-identity` | 检查颜色生成与相邻颜色避让 |
| `npm run test:identity-renderer` | 检查通用 SVG 图形渲染 |

## 主要目录

```text
.github/workflows/                  GitHub 自动发现与发布工作流
config/discovery.json               自动搜索范围和数量配置
scripts/                            前端数据生成与测试脚本
skills/github-inspiration-editor/   内容研究、生成、校验和刷新规则
src/                                React 前端
src/data/                           正式项目数据源
outputs/                            审计、候选、刷新和版本记录
```

## 进一步文档

- [内容字段契约](skills/github-inspiration-editor/references/content-contract.md)
- [自动发现工作流](skills/github-inspiration-editor/references/discovery-workflow.md)
- [旧项目自动化巡检](skills/github-inspiration-editor/references/automation-workflow.md)
- [内容质量标准](skills/github-inspiration-editor/references/quality-rubric.md)
- [自动修复闭环](skills/github-inspiration-editor/references/quality-repair-loop.md)
- [确定性视觉身份](skills/github-inspiration-editor/references/visual-identity.md)
- [版本控制与回滚](skills/github-inspiration-editor/references/version-control-workflow.md)
