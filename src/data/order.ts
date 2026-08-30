import rawOrder from './order.json'
import type { ProjectId } from './types'

const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/

function loadProjectIds(value: unknown): readonly ProjectId[] {
  if (!Array.isArray(value) || value.length === 0) throw new Error('Published project order must be a non-empty array')
  if (!value.every((id) => typeof id === 'string' && slugPattern.test(id))) throw new Error('Published project IDs must be lowercase kebab-case slugs')
  if (new Set(value).size !== value.length) throw new Error('Published project order must not contain duplicate IDs')
  return value
}

export const projectIds = loadProjectIds(rawOrder)
