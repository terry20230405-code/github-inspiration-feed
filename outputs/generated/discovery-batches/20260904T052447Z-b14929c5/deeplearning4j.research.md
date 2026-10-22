# deeplearning4j/deeplearning4j research notes

Research date: 2026-09-04
Repository: https://github.com/deeplearning4j/deeplearning4j
Research mode: new

## Snapshot

- Repository ID: 14734876
- Repository full name: deeplearning4j/deeplearning4j
- Repository name: deeplearning4j
- Stars at fetch time: 14247
- Forks at fetch time: 3825
- Primary language: Java
- Latest push at fetch time: 2026-09-04T05:35:30Z
- License: Apache License 2.0
- Default branch: master
- README SHA: 354786f638a90f11507b4b05d02f1410b6689f06
- Latest release: 未知
- Repository state: active
- Fetched at: 2026-09-04T05:56:09Z
- Snapshot note: Star, Fork, and push values are captured facts from this fetch, not live values.

## Sources

- [S1] Canonical repository metadata — https://github.com/deeplearning4j/deeplearning4j — accessed 2026-09-04
- [S2] Official README — https://github.com/deeplearning4j/deeplearning4j/blob/master/README.md — accessed 2026-09-04
- [S4] Official repository license file — https://github.com/deeplearning4j/deeplearning4j/blob/master/LICENSE — accessed 2026-09-04

## Verified repository facts

- [F1] GitHub 仓库 ID 为 14734876，canonical full name 是 deeplearning4j/deeplearning4j，项目名是 deeplearning4j。 Sources: S1
- [F2] 仓库有 14247 个 stars、3825 个 forks，主语言是 Java。 Sources: S1
- [F3] 仓库未归档、未禁用、不是 fork，默认分支是 master，最近推送时间为 2026-09-04T05:35:30Z。 Sources: S1
- [F4] 官方 LICENSE 文件确认项目许可证是 Apache License 2.0。 Sources: S4
- [F5] DL4J 生态面向 JVM 深度学习应用，覆盖从原始数据读取和预处理到构建和调优各种网络。 Sources: S2
- [F6] DL4J 可用于 Java 之外的 JVM 语言，包括 Scala、Kotlin 和 Clojure。 Sources: S2
- [F7] DL4J 提供 MultiLayerNetwork、ComputationGraph、自定义层，并支持基于 Apache Spark 的分布式训练。 Sources: S2
- [F8] ND4J 提供 500 多个数学、线性代数和深度学习运算，基于 LibND4J，并支持 CPU 和 GPU 加速。 Sources: S2
- [F9] SameDiff 是自动微分 / 深度学习框架，采用图式 define-then-run，并支持自定义层和损失函数。 Sources: S2
- [F10] DataVec 负责机器学习数据的 ETL，覆盖 HDFS、Spark、图片、视频、音频、CSV 和 Excel 等格式。 Sources: S2
- [F11] DL4J 支持导入 Keras 的 h5 模型，SameDiff 支持导入 TensorFlow frozen .pb 模型。 Sources: S2
- [F12] Python4J 提供 bundled cpython execution for the JVM。 Sources: S2

## Page field evidence

| Field | Planned claim | Evidence | Status |
| --- | --- | --- | --- |
| `repository.githubId` | repository.githubId 是 14734876 | F1 | verified |
| `repository.fullName` | repository.fullName 是 deeplearning4j/deeplearning4j | F1 | verified |
| `repository.name` | repository.name 是 deeplearning4j | F1 | verified |
| `repository.stars` | repository.stars 是 14247 | F2 | verified |
| `repository.forks` | repository.forks 是 3825 | F2 | verified |
| `repository.language` | repository.language 是 Java | F2 | verified |
| `repository.pushedAt` | repository.pushedAt 是 2026-09-04T05:35:30Z | F3 | verified |
| `repository.license` | repository.license 是 Apache License 2.0 | F4 | verified |
| `repository.state` | repository.state 是 active | F3 | verified |
| `editorial.hook` | hook 概括为 JVM 项目的深度学习训练与推理能力 | F5, F6, F7, F8, F9, F10, F11, F12 | inferred |
| `editorial.summary` | summary 说明该生态接收数据、搭建网络、导入模型并在 JVM 中训练和运行深度学习，且交代可见结果 | F5, F6, F7, F8, F9, F10, F11, F12 | verified |
| `editorial.meaning` | meaning 说明这些能力可被拆成训练、迁移、推理和实验等可复用模块 | F5, F7, F8, F9, F10, F11 | inferred |
| `editorial.audience` | audience 指向 JVM 语言栈里的机器学习开发者和相关工程师 | F5, F6 | inferred |
| `editorial.features` | features 列出数据处理、网络构建、模型导入、数值运算和自动微分等核心能力 | F7, F8, F9, F10, F11 | verified |
| `editorial.stack` | stack 包括 Java、JVM、ND4J、DataVec、SameDiff、Apache Spark、C++、CUDA | F2, F5, F6, F7, F8, F9, F10, F11 | verified |
| `editorial.opportunity` | opportunity 说明可从数据整理、模型迁移、在线推理和学习实验中拆出窄产品 | F10, F11, F7, F8, F9 | inferred |

## Product inferences

- [I1] 这是一个面向 JVM 开发者、数据工程师和 ML 工程师的深度学习工具生态，而不是单点模型库。 Basis: F5, F6, F7, F8, F9, F10, F11, F12. Confidence: high
- [I2] 其可复用能力天然分成数据处理、数值计算、模型导入和自动微分几层，适合拆成更窄的产品。 Basis: F7, F8, F9, F10, F11. Confidence: high
- [I3] Spark 分布式训练和 CPU / GPU 支持说明它既能做本地开发，也能覆盖更重的训练场景。 Basis: F7, F8. Confidence: medium

## Direction rationale

### D1 — 训练数据整理器

- Reused capability: DataVec 对多种格式的 ETL 与读取能力。
- Evidence: F5, F10
- New audience and recurring problem: 面向数据工程师和标注运营，他们要把 HDFS、CSV、图片、视频、音频或 Excel 里的原始素材整理成训练集，重复做清洗、切分和导出。
- Input and visible outcome: 原流程是先把数据接进整个深度学习栈，再继续训练模型；新流程是直接接收原始文件或目录，得到整理、验证、切分后的数据集。
- Original workflow: JVM 开发者 + 各类数据 → 用 DataVec 作为深度学习生态的一部分，再继续建模和训练。
- New workflow: 数据工程师 + 原始数据目录 → 读取、清洗、校验、切分、导出 → 训练就绪的数据集和错误报告。
- Materially changed axes: audience, workflow, outcome
- Product form: end-user-product
- Product boundary: 不做模型训练、不做推理，只保留数据接入、转换和导出。
- Substantive difference: 原项目把数据处理放在训练生态里；这个方向把它单独做成数据整理产品，只输出可训练的数据包和质量报告。

### D2 — Keras 模型迁移器

- Reused capability: Keras h5 模型导入能力，以及 SameDiff 对 TensorFlow frozen .pb 模型的导入支持。
- Evidence: F7, F11
- New audience and recurring problem: 面向已经有 Keras 或 TensorFlow 模型的团队，他们需要把旧模型迁到 JVM 项目里验证能否直接复用。
- Input and visible outcome: 原流程是把模型导入后继续参与训练或在代码里使用；新流程是上传 h5 或 TensorFlow 冻结模型，得到 JVM 可用包和兼容报告。
- Original workflow: JVM 开发者 + 模型和数据 → 继续用 DL4J / SameDiff 构建、训练或部署模型。
- New workflow: 迁移工程师 + h5 / .pb 模型文件 → 导入、兼容检查、样本验证、打包 → JVM 可用的迁移产物。
- Materially changed axes: input, workflow, outcome
- Product form: end-user-product
- Product boundary: 只做模型迁移与验证，不做数据整理和训练编排。
- Substantive difference: 原项目只是支持导入模型作为训练或运行能力的一部分；这个方向把导入、兼容检查和打包独立成迁移产品。

### D3 — SameDiff 练习实验台

- Reused capability: SameDiff 的自动微分、图式执行和自定义层 / 损失函数能力。
- Evidence: F8, F9
- New audience and recurring problem: 面向学生、老师和初级工程师，他们想在 JVM 里练习深度学习，但需要可反复修改、立即看到结果的实验环境。
- Input and visible outcome: 原流程是开发者把 SameDiff 放进自己的应用里；新流程是学习者在示例图或练习模型上改一小步，马上看到前向、反向和损失变化。
- Original workflow: JVM 开发者 + 数据和模型定义 → 用 SameDiff 构建自动微分图并嵌入自己的项目。
- New workflow: 学习者打开示例图和样本数据 → 修改层、损失或参数 → 运行前向 / 反向 → 查看对比结果并导出练习版本。
- Materially changed axes: audience, input, workflow, outcome
- Product form: end-user-product
- Product boundary: 不做生产部署或大规模数据处理，只做练习、对比和导出。
- Substantive difference: 原项目是开发者库；这个方向把 SameDiff 的图式计算和自定义层能力做成练习台，强调试验反馈而不是生产集成。

## Pairwise direction comparison

- 训练数据整理器 vs Keras 模型迁移器
  - Different axes: input, workflow, outcome
  - Concrete comparison: 一个整理原始数据，一个迁移现成模型；输入从素材文件换成模型文件，产出从训练集换成迁移产物。
- 训练数据整理器 vs SameDiff 练习实验台
  - Different axes: audience, input, outcome
  - Concrete comparison: 一个服务数据整理岗位，一个服务学习实验人群；输入和结果都不同。
- Keras 模型迁移器 vs SameDiff 练习实验台
  - Different axes: audience, input, outcome
  - Concrete comparison: 一个帮团队迁移旧模型，一个帮学习者改 SameDiff 示例；前者关注兼容和打包，后者关注前向、反向和对比结果。

## Uncertainty

- README 提到 ONNX、TensorFlow SavedModel 和 Keras import planned，但这些不是当前已验证能力，未写入事实或页面主张。
- 官方 README 给出 examples 和文档链接，但未进一步核验外部站点内容，因此未把这些链接相关能力写入页面主张。

## Localization decisions

- 保留 JVM、ND4J、DataVec、SameDiff、Apache Spark、Keras、TensorFlow frozen .pb、Python4J、C++、CUDA 等术语，因为它们直接说明复用边界和技术基础。
- 不把 tf.keras 写进摘要或特征，因为一手证据只明确到 Keras h5 与 TensorFlow frozen .pb 导入；避免把未单独证实的能力写成确定能力。
- 摘要中移除 Python4J，避免把未直接影响产品画面的技术细节塞进主叙述。

## Refresh notes

- Initial research; no prior published snapshot.
