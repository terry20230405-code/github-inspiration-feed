import type { RuntimeProject } from './data/runtime'

export type Language = 'zh' | 'en'
export const languageStorageKey = 'inspiration-feed.language'

export function readLanguage(): Language {
  try {
    return localStorage.getItem(languageStorageKey) === 'en' ? 'en' : 'zh'
  } catch {
    return 'zh'
  }
}

export function saveLanguage(language: Language) {
  try {
    localStorage.setItem(languageStorageKey, language)
  } catch {
    // Language switching still works when browser storage is unavailable.
  }
}

export const messages = {
  zh: {
    brand: '灵感流', title: '灵感流 · GitHub 项目再创作', language: '界面语言',
    note: '为你的下一个项目，找一个起点', github: '在 GitHub 查看',
    continueFrom: '从这里继续', explore: '查看 3 个改造方向',
    loading: '正在准备灵感流', loadingNext: '正在准备下一个项目',
    loadError: '项目加载失败，请刷新页面重试。', noProject: '暂无项目',
    goTo: (index: number) => `前往第 ${index} 个项目`, previous: '上一个项目', next: '下一个项目',
    back: '灵感流', originalLink: 'GitHub 原项目', viewOriginal: '查看 GitHub 原项目',
    heroFrom: (name: string) => `从 ${name}`, heroGrow: '长出你的项目',
    original: '01 / 原项目', core: '先看懂它的核心', updated: '更新', license: '许可',
    features: '核心功能', audience: '适合谁', stack: '技术基础',
    opportunity: '02 / 机会', why: '为什么值得继续做？',
    directions: '03 / 选择方向', what: '你想把它变成什么？',
    intro: '先选一个清晰的小切口。选择后，下方会展示这条路线的具体做法。',
    selected: '当前选择', problem: '解决的问题', target: '目标用户',
    approach: '可以怎么做', difference: '与原项目的不同', scope: '最小功能范围',
    unknown: '未知',
  },
  en: {
    brand: 'Inspire', title: 'Inspire · Build on GitHub projects', language: 'Interface language',
    note: 'A starting point for your next project', github: 'View on GitHub',
    continueFrom: 'Make it your own', explore: 'Explore 3 directions',
    loading: 'Preparing your inspiration feed', loadingNext: 'Preparing the next project',
    loadError: 'Could not load the projects. Please refresh to try again.', noProject: 'No project available',
    goTo: (index: number) => `Go to project ${index}`, previous: 'Previous project', next: 'Next project',
    back: 'Feed', originalLink: 'GitHub', viewOriginal: 'View on GitHub',
    heroFrom: (name: string) => `Start with ${name}`, heroGrow: 'Make it your own',
    original: '01 / The original', core: 'Understand the core', updated: 'Updated', license: 'License',
    features: 'Core features', audience: 'Who it is for', stack: 'Built with',
    opportunity: '02 / Opportunity', why: 'Why build on it?',
    directions: '03 / Choose a direction', what: 'What will you turn it into?',
    intro: 'Start with one focused idea. Pick a direction to explore how it could work.',
    selected: 'Your selection', problem: 'The problem', target: 'Who it helps',
    approach: 'How it could work', difference: 'What makes it different', scope: 'Minimum feature set',
    unknown: 'Unknown',
  },
} as const

export function localizeEditorial(project: RuntimeProject, language: Language) {
  return language === 'en' ? project.translations.en : project.editorial
}
