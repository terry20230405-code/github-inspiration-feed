# Project instructions

When a task turns a GitHub repository into inspiration-feed content, refreshes an existing project card, or adds a repository to the feed, use the local skill at `skills/github-inspiration-editor/SKILL.md`. Read that file completely, then read the references it routes to before generating or editing content.

Keep generated repository drafts and evidence notes under `outputs/generated/` until the user asks to add them to the product feed.

Whenever a project is added to `src/data/order.json` or its Chinese editorial copy changes, add or update the structurally matching English entry in `src/locales/projects.en.json` in the same change. English coverage is mandatory; do not publish a project that would fall back to Chinese in English mode.
