# GitHub 元数据刷新工作流

阶段六只负责更新已发布项目的 GitHub 快照和生成变化报告。它不会自动重写中文介绍、改造方向或视觉身份，也不会自动发布内容。

## 为什么先分级再处理

GitHub 上的变化并不都意味着页面文章已经过时。刷新器按风险分成四层：

| 级别 | 例子 | 自动处理 | 后续动作 |
| --- | --- | --- | --- |
| `freshness` / `statistics` | 抓取时间、Star、Fork | 更新 `repository` | 无需内容复审 |
| `activity` | `pushedAt` 变化 | 更新 `repository` | 建议重新检查 README、Release 等资料，但不直接改文案 |
| `metadata` | 项目名称或主要语言发生实质变化 | 更新 `repository` | 建议检查受影响的页面事实 |
| `critical` | 仓库 ID、完整名称、许可证、归档/禁用状态变化，或仓库变私有、变成 Fork、返回 404 | 不写入该项目 | 必须由人确认是否继续收录以及如何处理 |

API 返回的仓库 slug 可能全部小写。如果它和现有展示名称仅大小写不同，刷新器保留已经审核过的品牌写法，例如 `Remotion` 和 `Immich`。

## 安全边界

- 默认运行是 dry-run，只输出报告，不写文件。
- `--write` 只写 `src/data/repositories.json`、ETag 缓存和刷新报告。
- `src/data/editorial.ts` 与 `src/data/visuals.ts` 永远不是刷新器输入或输出。
- 任一项目发生关键变化时，该项目保持原快照，不部分覆盖。
- GitHub 限流后立即停止后续请求，不持续重试。
- 不关闭 TLS/SSL 证书校验。
- 不把 `GITHUB_TOKEN` 写进报告、数据或日志。
- 由总控执行正式写入时，必须先按 [version-control-workflow.md](version-control-workflow.md) 创建刷新状态快照；写入后验证失败则恢复整组文件。

## 运行方式

项目根目录执行：

```powershell
npm run refresh:repositories
```

确认报告中 `reviewRequired` 和 `failed` 都是 `0` 后，再执行：

```powershell
npm run refresh:repositories:write
```

只检查某个项目：

```powershell
py -3.12 skills/github-inspiration-editor/scripts/refresh_repositories.py --only immich
```

公开仓库可以不登录调用 GitHub API。项目数量增加后，可在当前终端设置 `GITHUB_TOKEN`；脚本只在请求头中使用它。GitHub 官方文档说明，未认证请求通常为每小时 60 次，个人认证请求通常为每小时 5,000 次。

## 输出

- Published snapshot: `src/data/repositories.json`
- Conditional request cache: `outputs/refresh/github-cache.json`
- Latest report: `outputs/refresh/latest.json`

报告包含每个项目的字段变化、变化等级、是否建议资料复查、是否需要内容复审，以及剩余 API 请求额度。退出码：

- `0`：本次检查没有失败或关键变化。
- `1`：网络、API、限流或数据格式失败。
- `2`：发现需要人工确认的关键变化。

## 与阶段七的交接

阶段六完成“发现变化并安全更新快照”。当结果中的 `researchRefreshRecommended` 为 `true` 时，阶段七按照 [research-refresh-workflow.md](research-refresh-workflow.md) 比较 README、Release、Topics 等内容信号。阶段七先生成来源证据和语义审核；只有审核结论为 `draft` 时才允许在 `outputs/generated/` 新建内容草稿。任何阶段都不能直接覆盖已发布中文内容。
