# Editorial guide

Use this guide after reading [content-contract.md](content-contract.md). Write for people who understand basic Vibe Coding concepts such as frontend, backend, and APIs, but do not read code or know the repository's low-level technical domain. The copy should feel like careful product editing, not a repository README or generic AI summary.

## Homepage hierarchy

### Hook (`hook`)

- Express the project's most distinctive product idea, not its category.
- Make it understandable without repository-specific or low-level technical background.
- Prefer a concrete transformation, contrast, or outcome.
- Use roughly 10–24 Chinese characters.
- Do not end with punctuation.
- Avoid empty excitement such as “重新定义未来”, “释放无限可能”, or “一站式解决方案”.

A useful shape is `让/把 + familiar thing + unexpected capability or result`.

### Dense introduction (`summary`)

- Use 2 sentences and roughly 70–150 Chinese characters.
- Explain what the product accepts or connects, what it lets the user do, and what result it produces.
- Include several verified core functions when they help form a complete mental model.
- Explain what technical mechanisms do in the product. Apply the contextual terminology rules in `localization-guide.md`; retain basic Vibe Coding concepts and technology names that materially help the reader understand the product or judge reuse.
- Do not repeat the hook, praise popularity, or discuss extension potential here.

### Meaning (`meaning`)

Explain why the underlying capability is valuable for making new products. Keep this separate from the factual introduction and connect it to a real product opportunity.

## Tone

- Use direct, natural Simplified Chinese and concrete nouns and verbs.
- Rewrite the meaning in natural Chinese sentence order instead of mirroring the English source sentence by sentence.
- Avoid “赋能”, “生态”, “智能化”, “无缝”, “创新性”, and stacked claims.
- Do not remove useful technical meaning merely to sound simple. Omit low-level implementation details only when they do not help the target reader understand the product or judge reuse.
- Do not claim a project is easy to reuse merely because it is open source; consider its license, architecture, and setup burden.

## Extension preview

`name` should look like a small product someone could choose to build. `tagline` should state the input and outcome in one compact sentence.

Good: `旅行轨迹相册 — 用照片位置自动还原一段旅程`

Weak: `AI 旅行助手 — 用 AI 提升旅行体验`

## Human value before commercial value

- Start with a real inconvenience, unmet need, or meaningful experience in everyday life.
- Consider personal efficiency, learning, accessibility, privacy, family care, community coordination, creative expression, memory preservation, and enjoyment before commercial potential.
- Do not treat monetization, profitability, market size, or business buyers as mandatory signs of a good direction.
- If a direction serves a business or seller, describe the person's actual workflow and benefit rather than promising growth, conversion, or revenue.
- Keep the set varied. Unless the user explicitly requests a purely commercial theme, at least one of the 3–5 directions must primarily serve personal, family, learning, creative, or community value rather than a marketing, sales, or revenue workflow.

## Final pass

Remove repeated ideas across the hook, summary, meaning, and directions. If the hook could describe many unrelated repositories, rewrite it. If the summary leaves the reader asking “具体能做哪些事”, add verified functions. If a direction cannot be described as a single user journey, narrow it. Replace literal translation artifacts and check that the directions describe concrete improvements to people's lives rather than defaulting to commercial outcomes.
