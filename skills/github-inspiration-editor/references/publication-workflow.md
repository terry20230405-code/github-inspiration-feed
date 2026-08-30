# 候选项目与安全发布工作流

本流程负责把已经完成研究、写作和质量检查的项目安全加入产品数据，或只替换已有项目的中文内容。它不负责研究仓库，也不把“质量通过”当成“允许发布”。

## 四道门

一个项目进入页面前必须依次通过：

1. **候选准备：** 项目 JSON、研究笔记和 19 项质量记录全部通过；仓库身份不重复；新增卡片与相邻卡片的主题色有足够差异。
2. **冻结预览：** 将三个文件复制到独立候选目录并记录 SHA-256 指纹，生成中文预览。之后哪怕原草稿被修改，批准也不会错误地套到新内容上。
3. **人工批准：** 只有用户明确表示同意发布后，才能写入与候选指纹绑定的 `approval.json`。AI 的研究结论、质量检查或语义审查都不能代替这一步。
4. **发布事务：** 一次性更新顺序、仓库数据、中文内容和视觉身份四个 JSON；随后运行视觉检查、SVG 检查、Lint 和生产构建。任一检查失败，四个文件全部恢复到发布前版本。

## 数据位置

- 待批准候选：`outputs/generated/publication-candidates/<candidate-id>/`
- 页面顺序：`src/data/order.json`
- 仓库快照：`src/data/repositories.json`
- 中文内容：`src/data/editorial.json`
- 视觉身份：`src/data/visuals.json`
- 发布事务备份：`outputs/versions/publications/<transaction-id>/`

候选目录包含冻结后的 `project.json`、`research.md`、`quality.json`、`manifest.json` 和 `preview.md`。批准后才会出现 `approval.json`。

## 新增项目

先预演，不写文件：

```bash
npm run publication:prepare -- path/to/project.json path/to/research.md path/to/quality.json --after existing-project
```

确认输出后写入候选队列：

```bash
npm run publication:prepare -- path/to/project.json path/to/research.md path/to/quality.json --after existing-project --write
```

省略 `--after` 表示加到末尾。新增模式会同时检查 `id`、GitHub 数字 ID 和 `owner/repo`，任何一种重复都停止。

## 更新已有中文内容

```bash
npm run publication:prepare -- path/to/project.json path/to/research.md path/to/quality.json --mode replace --write
```

替换模式只允许 `editorial` 改变。仓库快照继续由刷新工作流管理，视觉身份和页面顺序保持不变。需要改变视觉身份或顺序时必须作为单独的产品决策处理，不能借内容修订顺便修改。

## 人工批准

用户查看候选目录中的 `preview.md` 后明确同意，才可以执行：

```bash
npm run publication:approve -- <candidate-id> --approved-by Terry --write
```

不加 `--write` 只显示将要批准什么，不产生授权。批准绑定候选指纹；候选内容变化后旧批准立即失效。

自动发现使用等价但独立的批次批准方式：定时任务把冻结候选和批次指纹放入审核 PR；用户合并该 PR，表示批准该批次全部候选。合并触发器记录合并者、PR 编号和批次指纹，再由 `publish_discovery_batch.py` 在一个事务中写入四层数据。关闭 PR 不授权发布。具体边界见 [discovery-workflow.md](discovery-workflow.md)。

## 发布与自动恢复

先查看发布计划：

```bash
npm run publication:publish -- <candidate-id>
```

用户已批准且计划无误后执行：

```bash
npm run publication:publish -- <candidate-id> --write
```

发布前如果四份页面数据存在未提交修改，或从准备候选以后发生过变化，程序会停止并要求重新准备候选。发布成功后仍需用 Git 提交这一批改动；程序不会自行上传远程 GitHub。

## 失败与恢复

写入前会在 `outputs/versions/publications/` 保存四份页面数据及其哈希。视觉测试、渲染测试、Lint 或构建任意失败时，程序自动恢复全部四份文件并校验哈希，同时把事务标记为 `rolled-back`。

如果电脑断电或进程被强制结束，来不及执行自动恢复，事务会停在 `backup-created`。下一次发布会因此被阻止。先预览恢复范围，再恢复：

```bash
npm run publication:recover -- <transaction-id>
npm run publication:recover -- <transaction-id> --write
```

恢复会重新校验备份与恢复后的四个文件，并把事务标记为 `manually-restored`。

不要用阶段八的仓库刷新快照替代这里的发布备份：刷新只管理动态仓库事实；发布事务必须同时保护顺序、仓库、中文内容和视觉身份。
