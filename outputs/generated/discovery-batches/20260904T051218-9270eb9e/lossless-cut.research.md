# mifi/lossless-cut research notes

Research date: 2026-09-04
Repository: https://github.com/mifi/lossless-cut
Research mode: new

## Snapshot

- Repository ID: 72343657
- Repository full name: mifi/lossless-cut
- Repository name: lossless-cut
- Stars at fetch time: 43431
- Forks at fetch time: 2148
- Primary language: TypeScript
- Latest push at fetch time: 2026-09-03T10:26:44Z
- License: GNU General Public License v2.0
- Default branch: master
- README SHA: f6e053c59dc6280954a0f758d5a9c703971a7dc8
- Latest release: v3.69.0 / 2026-06-04T08:14:49Z
- Repository state: active
- Fetched at: 2026-09-04T05:12:18Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/mifi/lossless-cut — accessed 2026-09-04
- [S2] Official README — https://github.com/mifi/lossless-cut/blob/master/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/mifi/lossless-cut/releases/tag/v3.69.0 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/mifi/lossless-cut/blob/master/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 快照确认仓库身份、计数、TypeScript 主语言、活动状态与 GPL-2.0 许可证。 Sources: S1, S4
- [F2] LosslessCut 是跨平台 FFmpeg 图形界面，可快速无损裁切和处理视频、音频、字幕等媒体。 Sources: S2
- [F3] README 列出时间线裁切、轨道重排、合并、重封装、元数据、快照、章节及黑场、静音和场景检测。 Sources: S2
- [F4] 项目主要使用 TypeScript，并以 Chromium 播放界面配合 FFmpeg 处理媒体。 Sources: S1, S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 72343657 | F1 | verified |
| `repository.fullName` | mifi/lossless-cut | F1 | verified |
| `repository.name` | lossless-cut | F1 | verified |
| `repository.stars` | 43431 | F1 | verified |
| `repository.forks` | 2148 | F1 | verified |
| `repository.language` | TypeScript | F1 | verified |
| `repository.pushedAt` | 2026-09-03T10:26:44Z | F1 | verified |
| `repository.license` | GNU General Public License v2.0 | F1 | verified |
| `repository.state` | active | F1 | verified |
| `editorial.hook` | 剪掉视频废片，不再整段重新编码 | F2, F3 | verified |
| `editorial.summary` | LosslessCut 给 FFmpeg 套上跨平台时间线界面，让用户标记片段后快速裁切、合并或重封装视频、音频和字幕，而不必为普通剪切重新编码整段素材。它还支持轨道与元数据处理、快照、章节，以及黑场、静音和场景检测。 | F2, F3 | verified |
| `editorial.meaning` | 它把耗时的媒体重编码换成对容器和片段的精确操作，适合改造成围绕家庭记忆、课程材料或现场录音的轻量整理产品。 | I1 | inferred |
| `editorial.audience` | 需要快速清理相机、录屏、无人机或录音素材，又不想因重复编码损失质量的个人与内容工作者。 | F2 | verified |
| `editorial.features` | ["快速无损裁切与合并", "视频、音频和字幕轨道处理", "媒体重封装与元数据编辑", "帧快照、章节和片段项目", "黑场、静音与场景检测"] | F2, F3 | verified |
| `editorial.stack` | ["TypeScript", "Electron", "Chromium", "FFmpeg"] | F4 | verified |
| `editorial.opportunity` | ["把场景检测和无损裁切做成家庭影像整理器。", "把章节、片段和快照输出做成课程拆解工具。", "把静音检测和音频裁切做成田野录音整理台。"] | I1, I2, I3, I4 | inferred |

## Product inferences

- [I1] 它把耗时的媒体重编码换成对容器和片段的精确操作，适合改造成围绕家庭记忆、课程材料或现场录音的轻量整理产品。 Basis: F2, F3. Confidence: high
- [I2] 可将原项目能力改造成“家庭影像整理器”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I3] 可将原项目能力改造成“课程拆解工具”这类独立产品。 Basis: F2, F3. Confidence: medium
- [I4] 可将原项目能力改造成“田野录音整理台”这类独立产品。 Basis: F2, F3. Confidence: medium

## Direction rationale

### D1 — 家庭影像整理器

- Reused capability: 场景检测、时间线标记、无损裁切和快照
- Evidence: F2, F3
- New audience and recurring problem: 整理家庭照片和视频的个人；家庭视频越积越多，重复片段和长时间空镜让人很难回看。
- Input and visible outcome: 输入是相机和手机中的长视频；最终得到按日期整理的家庭短片和联系表。
- Original workflow: 在时间线上标记媒体片段，用 FFmpeg 快速无损裁切、合并、重封装或导出轨道，并保存片段项目。
- New workflow: 扫描素材→提示场景→确认片段→按事件归档
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动识别人脸，也不替用户决定哪些家庭片段重要。
- Substantive difference: 从自由媒体工具改成家庭事件归档与回看流程。

### D2 — 课程拆解工具

- Reused capability: 时间线片段、章节、批量导出和帧快照
- Evidence: F2, F3
- New audience and recurring problem: 制作线上课程的教师；教师要从长录课中制作章节与复习片段，常要重复定位时间点和截图。
- Input and visible outcome: 输入是长录课、章节表和关键时间点；最终得到章节化课程包和复习图卡。
- Original workflow: 在时间线上标记媒体片段，用 FFmpeg 快速无损裁切、合并、重封装或导出轨道，并保存片段项目。
- New workflow: 匹配章节→核对时间点→批切片段→导出索引
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不生成教学内容，也不评价课程质量。
- Substantive difference: 从单次剪切改成按教学结构批量产出课程材料。

### D3 — 田野录音整理台

- Reused capability: 音频波形、静音检测、片段标记和无损导出
- Evidence: F2, F3
- New audience and recurring problem: 做访谈或自然声音记录的研究者；研究者面对数小时现场录音，难以快速排除静音并保持片段与笔记对应。
- Input and visible outcome: 输入是长录音与现场笔记；最终得到带来源笔记的音频片段目录。
- Original workflow: 在时间线上标记媒体片段，用 FFmpeg 快速无损裁切、合并、重封装或导出轨道，并保存片段项目。
- New workflow: 检测静音→划分区段→绑定笔记→导出证据
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不自动转写或判断说话内容。
- Substantive difference: 输入变成录音与现场笔记，结果是可引用的证据片段目录。

## Pairwise direction comparison

- 家庭影像整理器 vs 课程拆解工具
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭影像整理者”与“教师和课程制作者”；输入分别是“相机和手机中的长视频”与“长录课、章节表和关键时间点”；流程分别是“扫描素材→提示场景→确认片段→按事件归档”与“匹配章节→核对时间点→批切片段→导出索引”
- 家庭影像整理器 vs 田野录音整理台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“家庭影像整理者”与“田野和访谈研究者”；输入分别是“相机和手机中的长视频”与“长录音与现场笔记”；流程分别是“扫描素材→提示场景→确认片段→按事件归档”与“检测静音→划分区段→绑定笔记→导出证据”
- 课程拆解工具 vs 田野录音整理台
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 用户分别是“教师和课程制作者”与“田野和访谈研究者”；输入分别是“长录课、章节表和关键时间点”与“长录音与现场笔记”；流程分别是“匹配章节→核对时间点→批切片段→导出索引”与“检测静音→划分区段→绑定笔记→导出证据”

## Uncertainty

- 本批只验证仓库公开资料，不推断未在 README 或发布页出现的商业能力。

## Localization decisions

- 保留必要的产品名和基础技术名词，并在相邻句中说明它们的作用。

## Refresh notes

- Initial research; no prior published snapshot.
