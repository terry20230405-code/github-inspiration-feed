import rawSnapshots from './repositories.json'
import { projectIds, type ProjectLayerMap, type RepositorySnapshot, type RepositoryState } from './types'

const repositoryStates = new Set<RepositoryState>(['active', 'archived', 'disabled', 'unavailable'])
const repositoryFields = ['githubId', 'fullName', 'name', 'stars', 'forks', 'language', 'pushedAt', 'license', 'state', 'fetchedAt'] as const

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function assertSnapshot(value: unknown, projectId: string): asserts value is RepositorySnapshot {
  if (!isRecord(value)) throw new Error(`Repository snapshot ${projectId} must be an object`)
  const keys = Object.keys(value).sort()
  const expectedKeys = [...repositoryFields].sort()
  if (keys.join('|') !== expectedKeys.join('|')) throw new Error(`Repository snapshot ${projectId} has unexpected fields`)
  if (!Number.isInteger(value.githubId) || Number(value.githubId) <= 0) throw new Error(`Repository snapshot ${projectId} has an invalid GitHub ID`)
  if (typeof value.fullName !== 'string' || !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(value.fullName)) throw new Error(`Repository snapshot ${projectId} has an invalid full name`)
  for (const field of ['name', 'language', 'license', 'pushedAt', 'fetchedAt'] as const) {
    if (typeof value[field] !== 'string' || !value[field]) throw new Error(`Repository snapshot ${projectId} has an invalid ${field}`)
  }
  for (const field of ['stars', 'forks'] as const) {
    if (!Number.isInteger(value[field]) || Number(value[field]) < 0) throw new Error(`Repository snapshot ${projectId} has an invalid ${field}`)
  }
  if (typeof value.state !== 'string' || !repositoryStates.has(value.state as RepositoryState)) throw new Error(`Repository snapshot ${projectId} has an invalid state`)
  const pushedAtValue = value.pushedAt
  const fetchedAtValue = value.fetchedAt
  if (typeof pushedAtValue !== 'string' || typeof fetchedAtValue !== 'string') throw new Error(`Repository snapshot ${projectId} has invalid timestamps`)
  const pushedAt = Date.parse(pushedAtValue)
  const fetchedAt = Date.parse(fetchedAtValue)
  if (!Number.isFinite(pushedAt) || !pushedAtValue.endsWith('Z')) throw new Error(`Repository snapshot ${projectId} has an invalid pushedAt`)
  if (!Number.isFinite(fetchedAt) || !fetchedAtValue.endsWith('Z')) throw new Error(`Repository snapshot ${projectId} has an invalid fetchedAt`)
  if (pushedAt > fetchedAt) throw new Error(`Repository snapshot ${projectId} was fetched before its latest push`)
}

function loadRepositorySnapshots(value: unknown): ProjectLayerMap<RepositorySnapshot> {
  if (!isRecord(value)) throw new Error('Repository snapshots must be an object')
  const keys = Object.keys(value).sort()
  const expectedKeys = [...projectIds].sort()
  if (keys.join('|') !== expectedKeys.join('|')) throw new Error('Repository snapshot IDs must match the published project IDs')
  for (const projectId of projectIds) assertSnapshot(value[projectId], projectId)
  return value as ProjectLayerMap<RepositorySnapshot>
}

export const repositorySnapshots = loadRepositorySnapshots(rawSnapshots)
