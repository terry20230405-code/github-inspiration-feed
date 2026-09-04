# Frontend translations

- `../i18n.ts` owns interface labels. Chinese is the default; the top-right 中文 / EN switch saves `inspiration-feed.language` locally. If browser storage is unavailable, switching still works for the session.
- `projects.en.json` translates the published Chinese editorial copy, without changing repository facts, IDs, direction scope, technology names, order or visual identity. This is a presentation-only layer; the four canonical JSON layers in `src/data/` are unchanged.
- The data generator validates translated fields and direction IDs, then includes the English copy in each lazy-loaded project's `translations.en`. English is not bundled into the initial JavaScript or the lightweight index.
- After editing translations, run `node scripts/generate-project-data.mjs` and reload the page (Vite does not automatically rerun predev for JSON changes).
- English coverage is mandatory. Every ID in `order.json` must have a structurally identical entry in `projects.en.json`; generation, development startup and production builds fail if an entry is missing or contains Chinese text. This prevents newly added projects from silently falling back to Chinese.
- `npm run test:i18n` checks translation structure, IDs, unchanged technologies, generated data, UI key parity, dates, fallback and storage errors. Review wording against the Chinese source as well; structural tests cannot detect semantic drift.

The English copy uses the existing Chinese project records as its source, not a new repository research pass. Product and technology names remain unchanged. Proposed directions stay proposals, not claims that the upstream project already implements them. The Remotion short-video direction retains its Chinese-language audience even in the English interface.
