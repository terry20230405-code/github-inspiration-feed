# snownico0722/PaperTodo research notes

Research date: 2026-09-01
Repository: https://github.com/snownico0722/PaperTodo
Research mode: new

## Snapshot

- Repository ID: 1250907197
- Repository full name: snownico0722/PaperTodo
- Repository name: PaperTodo
- Stars at fetch time: 2192
- Forks at fetch time: 110
- Primary language: C#
- Latest push at fetch time: 2026-09-01T04:57:48Z
- License: Other
- Default branch: main
- README SHA: ebf70992a77c673359227ef9b4191926e57bea49
- Latest release: v3.31 / 2026-08-30T17:28:21Z
- Repository state: active
- Fetched at: 2026-09-01T09:47:12Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/snownico0722/PaperTodo — accessed 2026-09-01
- [S2] Official README — https://github.com/snownico0722/PaperTodo/blob/main/README.md — accessed 2026-09-01
- [S3] Latest official release — https://github.com/snownico0722/PaperTodo/releases/tag/v3.31 — accessed 2026-09-01

## Verified repository facts

- [F1] GitHub repository numeric ID is 1250907197. Sources: S1
- [F2] Canonical repository full name is snownico0722/PaperTodo. Sources: S1
- [F3] Official project name is PaperTodo. Sources: S1
- [F4] Repository has 2192 stars, 110 forks, uses C# as primary language, pushed at 2026-09-01T04:57:48Z, and defaults to main. Sources: S1
- [F5] License label is Other / NOASSERTION and repository state is active. Sources: S1
- [F6] PaperTodo is a minimalist Windows desktop sticky note tool, with native WPF support for to-dos and Markdown. Sources: S2
- [F7] The app uses independent desktop paper windows, supports todo papers and note papers, and auto-saves content locally. Sources: S2
- [F8] Todo papers support checking, editing, deleting, clearing completed items, drag reordering, and multi-line paste; note papers support Markdown, local images, and opening in an external editor. Sources: S2
- [F9] Capsule mode, auto edge docking, multi-monitor edge queues, linked papers, and script capsules with `!p` / `!power` are documented capabilities. Sources: S2
- [F10] Data is stored locally in data.json with backups, note images use note-assets.lmdb, and the product stack includes WPF, .NET 10, LMDB, AvalonEdit, Hardcodet.NotifyIcon.Wpf, and Vortice.DirectComposition. Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 1250907197 | F1 | verified |
| `repository.fullName` | snownico0722/PaperTodo | F2 | verified |
| `repository.name` | PaperTodo | F3 | verified |
| `repository.stars` | 2192 | F4 | verified |
| `repository.forks` | 110 | F4 | verified |
| `repository.language` | C# | F4 | verified |
| `repository.pushedAt` | 2026-09-01T04:57:48Z | F4 | verified |
| `repository.license` | Other / NOASSERTION | F5 | verified |
| `repository.state` | active | F5 | verified |
| `editorial.hook` | 把便签变成安静的桌面纸片 | F6, F7, F8, F9 | inferred |
| `editorial.summary` | PaperTodo 是一款 Windows 桌面便签工具，把待办纸和笔记纸做成独立窗口，直接放在桌面上。它支持勾选、拖排、Markdown、本地图片和自动保存，还能折成胶囊贴到屏幕边缘，减少打扰。 | F6, F7, F8, F9, F10 | verified |
| `editorial.meaning` | 它的价值不只在于记事，而是把独立窗口、自动保存、贴边胶囊和待办关联纸片拆开后，可以继续拼成更窄的桌面工具：收工清单、贴边资料架，或者任务说明跳转纸。 | F7, F8, F9, F10 | inferred |
| `editorial.audience` | Windows 桌面用户，尤其是习惯把待办和短笔记放在桌面的个人用户 | F6, F7 | inferred |
| `editorial.features` | 独立桌面纸片，待办纸和笔记纸分开；待办可勾选、拖排、清理已完成；笔记支持 Markdown、本地图片和外部编辑器打开；胶囊模式与自动贴边，支持多屏；内容自动保存到本地 data.json 和 note-assets.lmdb | F7, F8, F9, F10 | verified |
| `editorial.stack` | C#、WPF、.NET 10、LMDB、AvalonEdit、Hardcodet.NotifyIcon.Wpf、Vortice.DirectComposition | F6, F8, F9, F10 | verified |
| `editorial.opportunity` | 独立窗口 + 自动保存适合做只收当天收尾事项的桌面清单；胶囊模式 + 自动贴边 + 多屏队列适合做桌面边缘的临时资料架；待办关联纸片适合做任务与背景说明之间的桌面跳转 | F7, F8, F9, F10 | inferred |

## Product inferences

- [I1] 原项目的可复用能力不是单一便签，而是独立窗口、自动保存、折叠贴边、本地图片和脚本入口这几块可拆开的桌面组件。 Basis: F6, F7, F8, F9, F10. Confidence: medium
- [I2] 它的工作方式可以被读成：在桌面上直接创建、编辑并保存多张纸片，必要时把纸片收成胶囊，再按内容类型继续处理。 Basis: F7, F8, F9. Confidence: medium
- [I3] 这些能力足以拆出三类更窄的新产品：收工清单、贴边资料架、任务说明跳转纸。 Basis: F7, F8, F9, F10. Confidence: medium
- [I4] 目标用户更像是 Windows 桌面上的个人用户，而不是需要复杂协作或云端工作流的团队。 Basis: F6, F7. Confidence: low

## Direction rationale

### D1 — 收工清单纸

- Reused capability: 复用待办纸的勾选、拖排、多行粘贴、完成后清理和自动保存。
- Evidence: F7, F8, F10
- New audience and recurring problem: 每天收工前要核对一串收尾事项的个人用户，需要一张能快速勾掉、第二天还能接着看的桌面清单。
- Input and visible outcome: 输入是一串收尾事项或多行粘贴内容，输出是一张只剩未完成项、可反复打开的桌面清单纸。
- Original workflow: 原项目里，用户会在独立纸片中处理待办、普通笔记、Markdown、图片或脚本，并可按需折叠成胶囊。
- New workflow: 把收尾事项粘进待办纸 → 勾选、拖排、清理已完成 → 保留未完成项，供下一次收工继续用。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不做长笔记、图片册或脚本入口，只做日终收尾清单。
- Substantive difference: 原项目是通用桌面便签，能同时装待办、笔记、图片和脚本；这个方向只保留日终收尾清单，重点是把当天剩余事项清掉。

### D2 — 贴边资料架

- Reused capability: 复用纸片独立窗口、胶囊模式、自动贴边、多屏队列和本地保存。
- Evidence: F7, F8, F9, F10
- New audience and recurring problem: 做方案、写文档或整理页面时，需要临时保留截图、摘录和短备注的人，常常想把这些参考放在手边但别占满屏幕。
- Input and visible outcome: 输入是短文本、截图和零散参考，输出是一排折成胶囊、停在屏幕边缘的可展开资料纸。
- Original workflow: 原项目先让用户在纸片里编辑内容，再可选折叠成胶囊；收纳只是附加能力。
- New workflow: 新建或拖入参考内容 → 折成胶囊 → 自动贴边并按多屏归位 → 需要时悬停或点击展开。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不强调长文写作或知识库管理，只做桌面边缘的临时资料架。
- Substantive difference: 原项目把纸片当成可直接编辑的内容容器；这个方向把重点放在把碎资料收进边缘、随用随开。

### D3 — 任务说明纸

- Reused capability: 复用待办纸、笔记纸、拖拽关联和本地自动保存。
- Evidence: F7, F8, F9
- New audience and recurring problem: 经常要先看说明再做事的人，需要把任务本身和背景说明绑在一起，否则来回找资料很费神。
- Input and visible outcome: 输入是一张待办纸和一张说明笔记纸，输出是带有直接打开入口的任务清单。
- Original workflow: 原项目里，待办纸和笔记纸可以各自独立编辑，关联只是可选能力之一。
- New workflow: 先建待办项 → 把相关笔记纸拖到任务上建立关联 → 之后从待办项直接打开背景说明。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不做通用笔记本或协作任务系统，只做任务与说明之间的桌面跳转。
- Substantive difference: 原项目主要是独立处理待办或笔记；这个方向把待办项和说明页之间的跳转变成核心体验。

## Pairwise direction comparison

- 收工清单纸 vs 贴边资料架
  - Different axes: audience, input, workflow, outcome
  - Concrete comparison: 一个围绕下班前清空收尾事项，一个围绕把截图和短摘录留在屏幕边缘；前者看重勾选与清理，后者看重折叠、贴边和随手展开。
- 收工清单纸 vs 任务说明纸
  - Different axes: input, workflow, outcome, audience
  - Concrete comparison: 一个只处理日终收尾清单，一个把待办和说明页绑定起来；前者输入是事项列表，后者输入是任务加关联笔记，结果一个留下未完成项，一个留下可跳转的任务上下文。
- 贴边资料架 vs 任务说明纸
  - Different axes: input, workflow, outcome, audience
  - Concrete comparison: 一个是桌面边缘的临时资料架，一个是任务与说明之间的跳转层；前者收纳碎资料，后者连接待办和背景说明，工作流和产出都不同。

## Uncertainty

- README 没有单独写出目标人群画像，audience 只能从产品定位推断。
- 许可证标签是 Other / NOASSERTION，能确认标签本身，但不能从这里进一步推出宽松或可商用的重用结论。

## Localization decisions

- 保留 WPF、Markdown、PowerShell、LMDB、Alt+Tab、Task View 等基础术语，因为它们直接影响产品理解和复用判断。
- 将核心产品隐喻保留为“纸片 / 胶囊”，避免把它改写成抽象的便签、卡片或组件。

## Refresh notes

- Initial research; no prior published snapshot.
