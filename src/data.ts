import { projectEditorial } from './data/editorial'
import { repositorySnapshots } from './data/repositories'
import { projectIds, type Project } from './data/types'
import { projectVisuals } from './data/visuals'

export const projects: Project[] = projectIds.map((id) => ({
  schemaVersion: 2,
  id,
  repository: repositorySnapshots[id],
  editorial: projectEditorial[id],
  visual: projectVisuals[id],
}))

export function repositoryUrl(fullName: string) {
  return `https://github.com/${fullName}`
}

export function formatRepositoryCount(value: number) {
  if (value < 1_000) return String(value)
  if (value >= 100_000) return `${Math.round(value / 1_000)}k`
  return `${(value / 1_000).toFixed(1).replace(/\.0$/, '')}k`
}

export function formatRelativeDate(isoDate: string, now = Date.now()) {
  const timestamp = Date.parse(isoDate)
  if (Number.isNaN(timestamp)) return '未知'

  const seconds = Math.max(0, Math.floor((now - timestamp) / 1_000))
  if (seconds < 60) return '刚刚'
  if (seconds < 3_600) return `${Math.floor(seconds / 60)} 分钟前`
  if (seconds < 86_400) return `${Math.floor(seconds / 3_600)} 小时前`
  if (seconds < 2_592_000) return `${Math.floor(seconds / 86_400)} 天前`
  if (seconds < 31_536_000) return `${Math.floor(seconds / 2_592_000)} 个月前`
  return `${Math.floor(seconds / 31_536_000)} 年前`
}

export type { Direction, Project } from './data/types'
