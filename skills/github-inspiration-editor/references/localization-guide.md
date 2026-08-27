# Contextual localization guide

Use this guide whenever repository material contains English or other non-Chinese terminology. The goal is not to translate every word; it is to express the same product meaning in accurate, natural Simplified Chinese.

## Target reader and technical depth

The target reader understands basic Vibe Coding concepts such as frontend, backend, and APIs but does not read code or know low-level implementation principles.

- Keep established basic terms when they help explain how the product works or what can be reused. Do not replace `API` with a vague phrase such as “a magical connection method”.
- Keep a more specialized term only when removing it would make the reader misunderstand a core capability, constraint, or reuse path. Explain its role or visible consequence in the same sentence.
- Omit protocol internals, implementation patterns, dependency details, and other low-level terms when they do not change the product mental model or reuse decision.
- A term is not valuable merely because it appears in the README or manifest. It must earn its place in the page copy.

## Translation method

1. Determine what the term refers to in this repository: a product role, technical component, interface label, protocol, or general verb.
2. Prefer the established Chinese term used in the relevant AI, software, design, or product context.
3. Rewrite the complete sentence in natural Chinese order. Do not preserve English grammar or translate line by line.
4. Keep product names, library names, API names, file formats, and necessary abbreviations in their original form.
5. When a term is important but potentially unfamiliar, introduce it once as `中文术语（English term）`, then use the Chinese term afterward.
6. Record consequential or uncertain translation choices in the research notes under `Localization decisions`.

## Context-sensitive examples

The same English word can require different Chinese translations:

- `AI agent` → `AI 智能体`, not `AI 代理` or `编程代理`.
- `coding agent` → `编程智能体` or `AI 编程智能体`, depending on whether AI is explicit in context.
- `user agent` → `用户代理` because this is the established web protocol term.
- `agent process` in infrastructure may mean `代理进程` or `执行进程`; determine its actual role first.

Common product and software terms:

- `workflow` → `工作流`.
- `prompt` → `提示词` when referring to model input instructions.
- `self-hosted` → `自托管`.
- `repository` → `代码仓库` in technical context; use `开源项目` when explaining the product to beginners.
- `issue` → keep `GitHub Issues` when naming the GitHub feature; otherwise use `问题`, `需求讨论`, or `议题` according to context.
- `fork` → keep `Fork` for the GitHub action or metric; use `派生版本` when describing the resulting project to general users.
- `fine-tuning` → `微调`; `inference` → `推理`; `embedding` → `嵌入向量` when these established AI meanings apply.

These examples are guidance, not a blind replacement dictionary. Check the surrounding sentence and the repository's actual behavior before choosing a term.

## Quality checks

- Would a Chinese practitioner in the relevant field recognize the chosen term?
- Would the target Vibe Coding reader understand the sentence without losing useful technical meaning?
- Has a useful basic technical term been removed and replaced by less accurate everyday language?
- Does every specialized term change the reader's understanding of a capability, constraint, or reuse path?
- Has an established term been replaced by an awkward literal translation?
- Is English retained only where it improves accuracy or recognition?
- Does the final Chinese copy read as original Chinese writing rather than a translated README?
