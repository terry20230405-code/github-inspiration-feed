# 阶段八：版本控制与回滚

阶段八为项目提供两层保护：Git 保存整个项目代码的长期版本；刷新事务快照保护阶段六和阶段七会自动改动的数据。两层不能互相替代。

## 为什么需要两层

| 保护层 | 主要保护什么 | 适合解决的问题 |
| --- | --- | --- |
| Git | 前端、Skill、脚本、文档和已确认的数据版本 | 几天后发现代码改坏了；比较两个里程碑；恢复某个文件 |
| 刷新快照 | GitHub 数字、刷新缓存、来源状态、刷新报告和 `*.source.json` | 一次自动刷新写到一半失败；需要恢复某个项目的刷新数据 |

自动刷新不能执行 `git reset --hard`，因为工作区里可能存在尚未提交的用户修改。它只回滚自己有权修改的刷新数据。Git 提交则由用户或获得明确授权的 AI 在一个完整里程碑通过验证后创建。

## 受刷新快照保护的文件

- `src/data/repositories.json`
- `outputs/refresh/github-cache.json`
- `outputs/refresh/latest.json`
- `outputs/refresh/source-state.json`
- `outputs/refresh/source-cache.json`
- `outputs/refresh/research-latest.json`
- `outputs/generated/research-refresh/*.source.json`

`src/data/editorial.ts` 和 `src/data/visuals.ts` 不属于自动刷新写入范围，因此不会被刷新事务回滚。它们由 Git 保护。AI生成的 `*.review.json` 和候选草稿也不会被一次元数据回滚误删。

## 快照包含什么

每个快照保存在 `outputs/versions/snapshots/<snapshot-id>/`：

- `manifest.json`：创建时间、原因、受保护文件清单、原来是否存在、文件大小和 SHA-256 哈希。
- `files/`：当时文件的实际副本。

恢复前必须重新计算所有哈希。文件被篡改、缺失、路径越界或格式错误时立即拒绝恢复。快照没有自动删除策略，避免在没有用户决定的情况下破坏历史版本。

## 人工查看与恢复

列出历史快照：

```powershell
npm run versions:list
```

查看一个快照：

```powershell
npm run versions:show -- <snapshot-id>
```

比较快照和当前状态。JSON 会列出类似 `$.immich.stars` 的字段路径，而不只是告诉你“文件变了”：

```powershell
npm run versions:diff -- <snapshot-id>
```

恢复命令默认只是预演：

```powershell
npm run versions:restore -- <snapshot-id>
```

确认预演内容后才真正恢复：

```powershell
npm run versions:restore -- <snapshot-id> --write
```

只恢复某一个项目的仓库快照、缓存、来源状态和来源证据：

```powershell
npm run versions:restore -- <snapshot-id> --project immich
npm run versions:restore -- <snapshot-id> --project immich --write
```

单项目恢复不会改其他项目，也不会伪造新的阶段六/阶段七运行报告。恢复完成后应先执行 `npm run refresh:cycle` 重新预演，不要直接执行 `refresh:cycle:resume`。

每次真正恢复前，系统会先创建 `before-restore:<snapshot-id>` 安全快照。因此即使选错历史版本，也能用新生成的安全快照恢复回来。

## 自动刷新事务

`npm run refresh:cycle:write` 和 `npm run refresh:cycle:resume` 使用以下顺序：

1. dry-run 和工程预检通过。
2. 创建写入前快照；快照失败就不开始写。
3. 执行阶段六、阶段七允许的写入。
4. 运行写入后 Lint 和生产构建。
5. 全部成功：事务记录为 `committed`。
6. 技术失败，或写入后出现 `human-decision-required`：自动恢复写入前快照，并验证哈希完全一致。
7. 自动恢复失败：停止所有后续写入，把下一位处理者设为用户。

事务记录保存在 `outputs/versions/transactions/`。统一自动化报告的 `versioning` 字段会显示：

- `committed`：安全写入和验证都成功。
- `rolled-back`：发生问题，已经恢复到写入前。
- `rollback-failed`：自动恢复没有通过验证，必须人工处理。
- `not-required`：本次只是 dry-run，没有写入。

任何一种结果都不代表已经发布网页。

## Git 的使用边界

阶段八初始化本地 Git，并在全部验证通过后建立一个基线提交。以后每完成一个明确阶段，可以创建一个新的里程碑提交。

小白日常最需要的三个只读命令是：

```powershell
git status
git diff
git log --oneline
```

- `git status`：哪些文件还没有保存进版本历史。
- `git diff`：这些文件具体改了什么。
- `git log --oneline`：已经保存了哪些里程碑。

不要让自动刷新运行 `git reset --hard`、`git clean` 或自动提交整个工作区。需要恢复代码时，先查看差异，再精确恢复指定提交或文件，避免覆盖用户尚未提交的工作。
