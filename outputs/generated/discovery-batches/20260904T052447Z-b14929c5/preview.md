# 自动候选审核：20260904T052447Z-b14929c5

- 生成时间：2026-09-04T05:24:47Z
- 合格候选：8
- 未通过深读：3
- 当前状态：等待人工审核
- 合并此 PR 表示批准本批候选进入灵感流；关闭 PR 表示拒绝整批。

## 1. qwen-audio-agent

- 仓库：https://github.com/QwenAudio/qwen-audio-agent
- Star：2335
- 许可证：Apache License 2.0
- 主题色：#8631bf
- Hook：让语音对话边聊边办事
- 介绍：它接入实时语音前端和可兼容 ACP 的后端 Agent，把语音聊天、工具调用、后台异步任务和结果回传放在同一条对话里。用户可以在 WebUI、TUI 或桌面浮窗中继续追问进度、取消任务，并收到持续状态更新。
- 改造方向：
  - 桌面语音任务台：用一句语音发起任务，进度和结果回到对话里
  - 客服接力台：把咨询、查单和人工转接接在同一段对话里
  - 直播口播助理：一边直播一边回答观众、提产品和提醒风险

## 2. inno-agent

- 仓库：https://github.com/hhyqhh/inno-agent
- Star：1082
- 许可证：MIT License
- 主题色：#198655
- Hook：把日常学习交给会记忆的陪练
- 介绍：Inno Agent 接入大模型提供商、个人 IM 和本地工作区，把学习任务、提醒、笔记与练习串成连续的对话工作流。它用 L1 画像、L2 wiki、L3 会话记录和 SQLite 检索保存长期上下文，并在 Web、Desktop 和 CLI 里输出可回放的聊天、终端和练习记录。
- 改造方向：
  - 错题复盘教练：把错题和薄弱点变成复习提醒和再练习
  - 讲义整理助手：把讲义和课件整理成可检索的课程知识页
  - 学习回放站：导出并回看完整学习对话和练习过程

## 3. tldraw

- 仓库：https://github.com/tldraw/tldraw
- Star：50117
- 许可证：tldraw license
- 主题色：#942eb8
- Hook：给 React 应用装上可协作的无限画布
- 介绍：tldraw 是给 React 应用接入无限画布的 SDK。开发者可以组合自定义 shapes、tools、bindings 和 UI 组件，直接得到多人协作、绘图/图形/文本/箭头、图片视频、运行时 Editor API，以及 AI 和网页嵌入能力。
- 改造方向：
  - 评审批注板：把截图和草图放进一块可协作的评审画布
  - 互动课堂黑板：把讲解、板书和学生标注放到同一块黑板上
  - 家庭记忆墙：把照片、视频和留言拼成一面回忆墙

## 4. deeplearning4j

- 仓库：https://github.com/deeplearning4j/deeplearning4j
- Star：14247
- 许可证：Apache License 2.0
- 主题色：#278721
- Hook：让 JVM 项目直接做深度学习训练和推理
- 介绍：它面向 JVM 项目，把原始数据接入、预处理、网络搭建、Keras h5 导入和 TensorFlow frozen .pb 导入放在同一套工具里。最后可在 Java、Scala、Kotlin、Clojure 等 JVM 语言中，得到可训练、可运行的深度学习模型和结果。
- 改造方向：
  - 训练数据整理器：把 HDFS、CSV、图片和音视频整理成训练集
  - Keras 模型迁移器：把 h5 / frozen .pb 模型转成 JVM 可用包
  - SameDiff 练习实验台：改一份 SameDiff 例子，看到前向和反向结果

## 5. it-tools

- 仓库：https://github.com/CorentinTh/it-tools
- Star：40463
- 许可证：GNU General Public License v3.0
- 主题色：#a928c3
- Hook：把开发杂活拆成一个个小工具
- 介绍：它把面向开发者和 IT 从业者的在线小工具放在同一个网页里，能做正则测试、Markdown 转 HTML、JSON/XML 互转、Base64 处理和邮箱规范化。用户直接输入文本或数据，就能得到可复制的结果，也可以用 Docker 自托管到自己的环境里。
- 改造方向：
  - 正则练习台：输入文本和正则，立刻看匹配结果
  - 数据格式转换台：把 JSON、XML、Markdown 和 Base64 互相转换
  - 内网工具柜：把常用开发工具装进团队自托管首页

## 6. flowgram.ai

- 仓库：https://github.com/bytedance/flowgram.ai
- Star：8419
- 许可证：MIT License
- 主题色：#8c7221
- Hook：给 AI 工作流平台搭好可拼装底座
- 介绍：FlowGram 是一个面向开发者的 TypeScript workflow 开发框架和工具包，内置自由布局画布、固定布局画布、节点配置表单、变量作用域链和可复用材料。它不是现成平台，而是让团队把这些能力组合起来，更快搭出自己的 AI workflow platform。
- 改造方向：
  - 节点配置面板工厂：用节点 schema 生成可校验的配置面板
  - 自由画布流程原型器：在自由画布上拖节点、连流程
  - 分支循环编排器：把分支和循环排成一张清楚的流程图

## 7. TagStudio

- 仓库：https://github.com/TagStudioDev/TagStudio
- Star：7166
- 许可证：GNU General Public License v3.0
- 主题色：#4e2ebd
- Hook：让照片和文件夹变成可回头找的标签库
- 介绍：TagStudio 把你现有的照片和文件夹开成一个本地资料库，条目和标签存进 .TagStudio 里的 SQLite 数据库，不用搬文件也不用 sidecar 文件。它能给文件加标签、别名、父标签和字段，按标签、路径、filetype、mediatype 搜索，还能预览图片、视频、音频和文本并找回移动后的条目。
- 改造方向：
  - 旅行相册标签册：把相机照片和文件夹整理成可搜的相册
  - 设计素材档案库：把设计文件和参考图收进可查的素材库
  - 音视频素材柜：把音视频素材放进能直接浏览的柜子

## 8. vokoscreenNG

- 仓库：https://github.com/vkohaupt/vokoscreenNG
- Star：1499
- 许可证：GNU General Public License v2.0
- 主题色：#1f8468
- Hook：把屏幕、摄像头和多路声音录成讲解视频
- 介绍：它面向 Windows 和 Linux，把屏幕、某个区域或窗口录成录屏视频，Linux 还支持窗口录制。它还能混录多路声音，叠加内建摄像头，并用倒计时、定时器、放大镜、Showclick 和 Halo 辅助录制，让成片更适合讲解和演示。
- 改造方向：
  - 课堂录屏器：把课件窗口和讲解声录成课后视频
  - 产品演示短片机：录下窗口和点击提示，直接给客户看
  - 故障复现录像包：把屏幕、声音和步骤一起留给同事

## 未进入候选的仓库

### 0xsline/OpenChatCut

- 停止阶段：两轮自动修复后质量复检
- 结果：两轮修复后仍未通过：B1
- 最终失败证据：
  - B1：\`editorial.hook\` = "把聊天改片写进真实视频时间线"; \`聊天改片\` is a coined abstraction and the compressed verb-object relation is not natural Chinese.
- 当前结构错误：
  - fact F11 cites an unavailable source
  - fieldEvidence must contain every required field exactly once and in order
  - editorial.summary should contain 60-180 characters
  - page field evidence is missing \`editorial.opportunity\`
  - fact F11 cites an unavailable source
  - fieldEvidence must contain every required field exactly once and in order
  - editorial.summary should contain 60-180 characters
  - page field evidence is missing \`editorial.opportunity\`
- 当前阻断项：
  - B1: \`editorial.hook\` uses the unnatural phrase "把聊天改片写进真实视频时间线"; \`聊天改片\` is a coined noun stack and the verb-object pairing is not natural Chinese.
- 修复轨迹：
  - 初次检查：失败 无；改动 无；策略 生成后首次完整检查；A3 由程序核对，A4 及其他语义项由 AI 审核。
  - 第 1 轮修复后复检：失败 A1, A4；改动 editorial.meaning, editorial.summary, decisionReason, fieldEvidence, directionComparisons；策略 第一轮采用完整语义单元重写：根据每条失败证据重写整句、整个字段或整个失败方向，并同步更新直接依赖的证据绑定、方向依据和两两比较。禁止只换词、补一句或改标题。
    - A1 当轮证据：\`editorial.summary\` 写入了“Codex、Claude Code”，但研究笔记只在 \`F4\`/\`F5\`/\`F6\`/\`F8\` 中验证了 built-in agent、外部 MCP agents、真实时间线、转写驱动编辑和导出，没有任何 fact ID 支持这两个具体工具名。
    - A4 当轮证据：\`repository.license\` 填的是“GNU Affero General Public License v3.0”，但研究 \`F9\` 和官方 LICENSE 文件明确是“GNU Affero General Public License v3.0 or later”；同时 \`editorial.summary\` 额外声称 Codex/Claude Code，超出已验证来源。
  - 第 2 轮修复后复检：失败 B1；改动 editorial.audience, editorial.directions, editorial.features, editorial.hook, editorial.meaning, editorial.opportunity, editorial.summary, decisionReason, facts, fieldEvidence, inferences, directionRationales, directionComparisons, uncertainty, localizationDecisions；策略 第二轮采用替代方案重建：丢弃上一轮仍失败的表达角度、核心工作流或差异理由，从已验证事实重新选择方案；可以修改失败单元的全部直接依赖字段，但不得改动无关内容。
    - B1 当轮证据：\`editorial.hook\` = "把聊天改片写进真实视频时间线"; \`聊天改片\` is a coined abstraction and the compressed verb-object relation is not natural Chinese.

### apache/echarts

- 停止阶段：两轮自动修复后质量复检
- 结果：两轮修复后仍未通过：fieldEvidence must contain every required field exactly once and in order; page field evidence is missing \`editorial.opportunity\`; fieldEvidence must contain every required field exactly once and in order
- 当前结构错误：
  - fieldEvidence must contain every required field exactly once and in order
  - page field evidence is missing \`editorial.opportunity\`
  - fieldEvidence must contain every required field exactly once and in order
  - page field evidence is missing \`editorial.opportunity\`
- 修复轨迹：
  - 初次检查：失败 无；改动 无；策略 生成后首次完整检查；A3 由程序核对，A4 及其他语义项由 AI 审核。
  - 第 1 轮修复后复检：失败 无；改动 editorial.meaning, decisionReason, fieldEvidence, directionRationales, directionComparisons；策略 第一轮采用完整语义单元重写：根据每条失败证据重写整句、整个字段或整个失败方向，并同步更新直接依赖的证据绑定、方向依据和两两比较。禁止只换词、补一句或改标题。
  - 第 2 轮修复后复检：失败 无；改动 decisionReason, facts, fieldEvidence, directionRationales；策略 第二轮采用替代方案重建：丢弃上一轮仍失败的表达角度、核心工作流或差异理由，从已验证事实重新选择方案；可以修改失败单元的全部直接依赖字段，但不得改动无关内容。

### f/prompts.chat

- 停止阶段：两轮自动修复后质量复检
- 结果：两轮修复后仍未通过：A1, A4
- 最终失败证据：
  - A1：失败。研究笔记 \`Page field evidence\` 中 \`repository.license\` 的已验证主张是 \`MIT / CC0 1.0 Universal 双许可\`，但项目 JSON \`repository.license\` 实际写成 \`This project uses a dual-license model:\`，字段值与可追溯主张不一致。且 \`editorial.stack\` 写入 \`Next.js\`、\`TypeScript\`、\`PostgreSQL\`，但研究笔记只给出 \`F3, F9, F10\`，其中 \`F9\`、\`F10\`并未逐项登记这三项技术，栈字段缺少逐项可追溯事实。
  - A4：失败。项目 JSON \`repository.license\` 为 \`This project uses a dual-license model:\`，而研究笔记 \`F11\` 明确许可证内容是“源码和站点作者内容采用 MIT；提示词内容和数据采用 CC0 1.0 Universal”，\`Page field evidence\` 也计划写成 \`MIT / CC0 1.0 Universal 双许可\`。这是项目 JSON、研究笔记与官方 LICENSE 之间的实质不一致，不应以模糊句代替已验证许可证。另，\`I3\` 已注明 GitHub 检测值 \`Other / NOASSERTION\` 与官方 LICENSE 可见冲突，属于必须谨慎处理的许可证不确定性。
- 当前结构错误：
  - fact F13 cites an unavailable source
  - fact F13 cites an unavailable source
- 当前阻断项：
  - A4：许可证存在实质矛盾。\`project.repository.license\` 写成 \`This project uses a dual-license model:\`，但研究笔记 \`Page field evidence\` 中 \`repository.license\` 的已验证主张是 \`MIT / CC0 1.0 Universal 双许可\`，且 \`F11\` 明确写明“源码和站点作者内容采用 MIT；提示词内容和数据采用 CC0 1.0 Universal”。许可证属于必须暂停项。
- 修复轨迹：
  - 初次检查：失败 无；改动 无；策略 生成后首次完整检查；A3 由程序核对，A4 及其他语义项由 AI 审核。
  - 第 1 轮修复后复检：失败 无；改动 editorial.directions, editorial.features, editorial.meaning, editorial.summary, decisionReason, facts, fieldEvidence, inferences, directionRationales, directionComparisons, uncertainty, localizationDecisions；策略 第一轮采用完整语义单元重写：根据每条失败证据重写整句、整个字段或整个失败方向，并同步更新直接依赖的证据绑定、方向依据和两两比较。禁止只换词、补一句或改标题。
  - 第 2 轮修复后复检：失败 A1, A4；改动 editorial.hook, decisionReason, facts, fieldEvidence, directionComparisons, uncertainty；策略 第二轮采用替代方案重建：丢弃上一轮仍失败的表达角度、核心工作流或差异理由，从已验证事实重新选择方案；可以修改失败单元的全部直接依赖字段，但不得改动无关内容。
    - A1 当轮证据：失败。研究笔记 \`Page field evidence\` 中 \`repository.license\` 的已验证主张是 \`MIT / CC0 1.0 Universal 双许可\`，但项目 JSON \`repository.license\` 实际写成 \`This project uses a dual-license model:\`，字段值与可追溯主张不一致。且 \`editorial.stack\` 写入 \`Next.js\`、\`TypeScript\`、\`PostgreSQL\`，但研究笔记只给出 \`F3, F9, F10\`，其中 \`F9\`、\`F10\`并未逐项登记这三项技术，栈字段缺少逐项可追溯事实。
    - A4 当轮证据：失败。项目 JSON \`repository.license\` 为 \`This project uses a dual-license model:\`，而研究笔记 \`F11\` 明确许可证内容是“源码和站点作者内容采用 MIT；提示词内容和数据采用 CC0 1.0 Universal”，\`Page field evidence\` 也计划写成 \`MIT / CC0 1.0 Universal 双许可\`。这是项目 JSON、研究笔记与官方 LICENSE 之间的实质不一致，不应以模糊句代替已验证许可证。另，\`I3\` 已注明 GitHub 检测值 \`Other / NOASSERTION\` 与官方 LICENSE 可见冲突，属于必须谨慎处理的许可证不确定性。



## 技术故障（不是内容质量不合格）

- 技术失败：1
- 已通过全部检查的候选仍保留在审核批次中；失败候选不会发布。
- 本轮仍以失败状态报告，请修复服务问题后再发起新运行。

- Pinvou/pinvou-agent：第 1 轮定向修复；AI provider request failed (RemoteDisconnected): Remote end closed connection without response

## AI 执行统计

- 候选并发上限：3
- AI 逻辑调用：51
- 深读阶段墙钟时间：4894.3 秒
- 各请求耗时合计：12565.1 秒（并发请求会重叠）
- 返回 usage 的调用：50
- 输入 Token：762960
- 输出 Token：443565
- 其中缓存输入 Token：65024
- 其中推理 Token：238667
- Token 统计仅汇总成功响应返回的 usage；断线、失败尝试或缺失 usage 可能仍计费，请以服务商账单为准。
