import type { Project, ProjectVisual } from './types'

export type ProjectIndexEntry = {
  readonly id: string
  readonly name: string
  readonly hook: string
  readonly accent: string
  readonly foreground: ProjectVisual['foreground']
}

type ProjectIndexPayload = {
  readonly schemaVersion: 1
  readonly projects: readonly ProjectIndexEntry[]
}

const projectCache = new Map<string, Project>()
const projectRequests = new Map<string, { controller: AbortController; promise: Promise<Project> }>()
let indexRequest: Promise<readonly ProjectIndexEntry[]> | null = null

function dataUrl(file: string) {
  return `${import.meta.env.BASE_URL}data/projects/${file}`
}

function assertIndex(value: unknown): asserts value is ProjectIndexPayload {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error('项目索引格式无效')
  const payload = value as Record<string, unknown>
  if (payload.schemaVersion !== 1 || !Array.isArray(payload.projects) || payload.projects.length === 0) throw new Error('项目索引为空或版本不兼容')
  const ids = new Set<string>()
  for (const item of payload.projects) {
    if (!item || typeof item !== 'object' || Array.isArray(item)) throw new Error('项目索引包含无效条目')
    const entry = item as Record<string, unknown>
    if (typeof entry.id !== 'string' || !/^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(entry.id)) throw new Error('项目索引包含无效 ID')
    if (ids.has(entry.id)) throw new Error(`项目索引包含重复 ID：${entry.id}`)
    ids.add(entry.id)
    if (typeof entry.name !== 'string' || typeof entry.hook !== 'string' || typeof entry.accent !== 'string') throw new Error(`项目索引 ${entry.id} 缺少展示数据`)
    if (entry.foreground !== '#000000' && entry.foreground !== '#ffffff') throw new Error(`项目索引 ${entry.id} 的前景色无效`)
  }
}

function assertProject(value: unknown, id: string): asserts value is Project {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`项目 ${id} 的数据格式无效`)
  const project = value as Record<string, unknown>
  if (project.schemaVersion !== 2 || project.id !== id || !project.repository || !project.editorial || !project.visual) {
    throw new Error(`项目 ${id} 的数据不完整`)
  }
}

async function fetchJson(url: string, signal?: AbortSignal) {
  const response = await fetch(url, { signal })
  if (!response.ok) throw new Error(`读取项目数据失败（${response.status}）`)
  return response.json() as Promise<unknown>
}

export function loadProjectIndex() {
  if (!indexRequest) {
    indexRequest = fetchJson(dataUrl('index.json')).then(value => {
      assertIndex(value)
      return value.projects
    }).catch(error => {
      indexRequest = null
      throw error
    })
  }
  return indexRequest
}

export function loadProject(id: string) {
  const cached = projectCache.get(id)
  if (cached) return Promise.resolve(cached)
  const pending = projectRequests.get(id)
  if (pending) return pending.promise

  const controller = new AbortController()
  const request = fetchJson(dataUrl(`${encodeURIComponent(id)}.json`), controller.signal)
    .then(value => {
      assertProject(value, id)
      projectCache.set(id, value)
      if (projectRequests.get(id)?.promise === request) projectRequests.delete(id)
      return value
    })
    .catch(error => {
      if (projectRequests.get(id)?.promise === request) projectRequests.delete(id)
      throw error
    })
  projectRequests.set(id, { controller, promise: request })
  return request
}

export function retainProjectCache(ids: ReadonlySet<string>) {
  for (const id of projectCache.keys()) {
    if (!ids.has(id)) projectCache.delete(id)
  }
  for (const [id, request] of projectRequests) {
    if (!ids.has(id)) {
      request.controller.abort()
      projectRequests.delete(id)
    }
  }
}

export function getCachedProject(id: string) {
  return projectCache.get(id)
}
