# vkohaupt/vokoscreenNG research notes

Research date: 2026-09-04
Repository: https://github.com/vkohaupt/vokoscreenNG
Research mode: new

## Snapshot

- Repository ID: 103692141
- Repository full name: vkohaupt/vokoscreenNG
- Repository name: vokoscreenNG
- Stars at fetch time: 1499
- Forks at fetch time: 110
- Primary language: C++
- Latest push at fetch time: 2026-09-02T20:24:06Z
- License: GNU General Public License v2.0
- Default branch: 3.0
- README SHA: 419dccfda420ae4f82b15e6cdb4ac7c863ac2c70
- Latest release: 4.10.0 / 2026-06-27T16:36:17Z
- Repository state: active
- Fetched at: 2026-09-04T06:33:15Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/vkohaupt/vokoscreenNG — accessed 2026-09-04
- [S2] Official README — https://github.com/vkohaupt/vokoscreenNG/blob/3.0/.github/README.md — accessed 2026-09-04
- [S3] Latest official release — https://github.com/vkohaupt/vokoscreenNG/releases/tag/4.10.0 — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/vkohaupt/vokoscreenNG/blob/3.0/COPYING — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 元数据显示仓库为 vkohaupt/vokoscreenNG，仓库 ID 是 103692141，项目名为 vokoscreenNG，官方主页指向 linuxecke.volkoh.de 的 vokoscreen 页面。 Sources: S1
- [F2] GitHub 统计显示该仓库有 1499 个 stars 和 110 个 forks。 Sources: S1
- [F3] 仓库的主要语言是 C++。 Sources: S1
- [F4] 仓库最近一次推送时间是 2026-09-02T20:24:06Z。 Sources: S1
- [F5] 仓库未归档、未禁用，默认分支是 3.0。 Sources: S1
- [F6] GitHub 检测到的许可证与 COPYING 文件都指向 GPL-2.0 / GNU General Public License v2.0。 Sources: S1, S4
- [F7] README 明确说明它是面向 Windows 和 Linux 的录屏工具。 Sources: S2
- [F8] README 说明它可以录制屏幕、某个区域或窗口，并注明窗口录制是 Linux only。 Sources: S2
- [F9] README 说明它支持来自多个来源的音频录制。 Sources: S2
- [F10] README 说明它内建摄像头支持。 Sources: S2
- [F11] README 说明它提供 systray、放大镜、倒计时、定时器、Showclick 和 Halo 等辅助工具。 Sources: S2
- [F12] 最新发布版本是 4.10.0，发布时间为 2026-06-27T16:36:17Z。 Sources: S3
- [F13] README 的 Linux 环境与构建要求列出 Qt6、PulseAudio、Wayland、GStreamer 和相关插件。 Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | 103692141 | F1 | verified |
| `repository.fullName` | vkohaupt/vokoscreenNG | F1 | verified |
| `repository.name` | vokoscreenNG | F1 | verified |
| `repository.stars` | 1499 | F2 | verified |
| `repository.forks` | 110 | F2 | verified |
| `repository.language` | C++ | F3 | verified |
| `repository.pushedAt` | 2026-09-02T20:24:06Z | F4 | verified |
| `repository.license` | GPL-2.0 | F6 | verified |
| `repository.state` | active | F5 | verified |
| `editorial.hook` | 把屏幕、摄像头和多路声音录成讲解视频 | F7, F8, F9, F10, F11 | inferred |
| `editorial.summary` | Windows 和 Linux 录屏、区域/窗口录制、多路音频、摄像头叠加和辅助录制工具。 | F7, F8, F9, F10, F11 | verified |
| `editorial.meaning` | 这些能力可以重组为课堂、演示、排障和讲解类新产品。 | F8, F9, F10, F11 | inferred |
| `editorial.audience` | 需要在 Windows 或 Linux 上录课、做演示或讲解的人 | F7, F8, F9, F10, F11 | inferred |
| `editorial.features` | 录制屏幕、区域或窗口；混录多路音频；内建摄像头叠加；倒计时与定时器；放大镜、Showclick、Halo 辅助 | F8, F9, F10, F11 | verified |
| `editorial.stack` | C++、Qt6、GStreamer、PulseAudio、Wayland、pipewire、xdg-desktop-portal | F3, F13 | verified |
| `editorial.opportunity` | 课堂录课、软件演示、故障复现和直播素材四类方向都能从现有录制链路中拆出来。 | F8, F9, F10, F11 | inferred |

## Product inferences

- [I1] 它的主要使用者是需要把屏幕操作整理成可观看视频的人，而不是只想拿到底层接口的开发者。 Basis: F7, F8, F9, F10, F11. Confidence: high
- [I2] 可复用的核心能力是把屏幕/区域/窗口、音频和摄像头合成到一条录制流程里。 Basis: F8, F9, F10. Confidence: high
- [I3] 放大镜、倒计时、定时器、Showclick 和 Halo 这类工具把录屏从“录下来”推进到“看得懂”。 Basis: F11. Confidence: medium
- [I4] 这类能力适合延展为教学、演示、排障、创作和讲解型产品。 Basis: F7, F8, F9, F10, F11. Confidence: medium

## Direction rationale

### D1 — 课堂录屏器

- Reused capability: 复用屏幕/窗口录制、多路音频和内建摄像头能力。
- Evidence: F7, F8, F9, F10, F11
- New audience and recurring problem: 线上授课老师、培训讲师在反复录课时，既要保住课件画面，又要把人像和讲解声一起留住。
- Input and visible outcome: 课件窗口、讲解麦克风和摄像头 → 可回放的课后视频。
- Original workflow: 通用录屏用户选择屏幕、区域或窗口并录音，得到一段录屏视频。
- New workflow: 选择屏幕或课件窗口，接入麦克风和摄像头，倒计时后开始录制，最后导出一段适合回放的讲解视频。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 面向授课留档的成片工具，不是单纯录制画面的底层组件。
- Substantive difference: 原项目是通用录屏；这个方向把主要场景收窄到授课，强调课件窗口、人像和讲解声的组合输出。

### D2 — 产品演示短片机

- Reused capability: 复用窗口录制、放大镜、Showclick/Halo 和多路音频。
- Evidence: F8, F9, F11
- New audience and recurring problem: 售前演示人员、产品经理和客户成功在做软件演示时，观众常看不清点击位置和操作顺序。
- Input and visible outcome: 软件窗口、旁白和点击动作 → 带提示的演示短片。
- Original workflow: 通用用户录下屏幕、区域或窗口和声音，得到录屏视频。
- New workflow: 选定应用窗口或屏幕，打开 Showclick/Halo 和放大镜，录入旁白或系统音，输出能直接发给客户的演示短片。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 面向客户演示的可读短片，不是现有录屏面板的换皮。
- Substantive difference: 原项目强调把操作录进去；这里强调让客户看懂操作，核心是窗口演示和点击提示，而不是通用录屏。

### D3 — 故障复现录像包

- Reused capability: 复用区域/窗口录制、多路音频、倒计时和定时器。
- Evidence: F8, F9, F11
- New audience and recurring problem: 客服、技术支持和内部排障人员遇到复现问题时，需要把操作步骤、声音和现场画面一起交给下一位同事。
- Input and visible outcome: 故障现场画面、说明声音和步骤 → 可交接的复现视频。
- Original workflow: 通用录屏用户录下屏幕和声音，得到一段录屏视频。
- New workflow: 录制出问题的屏幕区域或窗口，同时保留系统音和麦克风说明，再用倒计时、定时器控制开始与长度，最后导出复现视频。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 面向排障交接的证据型视频工具，不是录屏功能的简单打包。
- Substantive difference: 原项目偏录下完整讲解；这个方向偏证据留档和交接，输入更像故障现场，结果更像复现包。

## Pairwise direction comparison

- 课堂录屏器 vs 产品演示短片机
  - Different axes: audience, workflow, outcome
  - Concrete comparison: 一个更像课堂回放，另一个更像客户演示；前者围绕课件讲解和人像，后者围绕窗口操作和点击提示。
- 课堂录屏器 vs 故障复现录像包
  - Different axes: audience, input, outcome
  - Concrete comparison: 前者是授课录制，后者是故障留档；输入都包含屏幕和声音，但复现录像包更强调现场交接和证据保存。
- 产品演示短片机 vs 故障复现录像包
  - Different axes: audience, input, outcome
  - Concrete comparison: 两个方向都录软件，但一个给客户看，一个给同事查；演示短片偏展示，故障复现偏排障。

## Uncertainty

- README 只明确写出窗口录制是 Linux only；Windows 是否也支持窗口录制，原始材料未单独说明。

## Localization decisions

- 将 screencast 译为“录屏视频”，更符合中文读者的产品理解。
- 保留 Showclick、Halo、Qt6、GStreamer、PulseAudio、Wayland、pipewire 和 xdg-desktop-portal 等名称，因为它们直接说明了可复用技术基础。

## Refresh notes

- Initial research; no prior published snapshot.
