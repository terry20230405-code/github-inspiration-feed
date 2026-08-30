import rawEditorial from './editorial.json'
import { projectIds } from './order'
import type { Direction, ProjectEditorial, ProjectLayerMap } from './types'

const editorialFields = ['audience', 'directions', 'features', 'hook', 'meaning', 'opportunity', 'stack', 'summary']
const directionFields = ['approach', 'audience', 'difference', 'id', 'name', 'problem', 'scope', 'tagline']
const slugPattern = /^[a-z0-9]+(?:-[a-z0-9]+)*$/

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function hasExactFields(value: Record<string, unknown>, fields: readonly string[]) {
  return Object.keys(value).sort().join('|') === [...fields].sort().join('|')
}

function isStringList(value: unknown, minimum: number, maximum: number): value is string[] {
  return Array.isArray(value) && value.length >= minimum && value.length <= maximum && value.every((item) => typeof item === 'string' && item.trim())
}

function assertDirection(value: unknown, projectId: string, index: number): asserts value is Direction {
  if (!isRecord(value) || !hasExactFields(value, directionFields)) throw new Error(`Direction ${projectId}[${index}] has unexpected fields`)
  for (const field of directionFields.filter((field) => field !== 'scope')) {
    if (typeof value[field] !== 'string' || !value[field]) throw new Error(`Direction ${projectId}[${index}] has an invalid ${field}`)
  }
  if (typeof value.id !== 'string' || !slugPattern.test(value.id)) throw new Error(`Direction ${projectId}[${index}] has an invalid ID`)
  if (!isStringList(value.scope, 3, 6)) throw new Error(`Direction ${projectId}[${index}] must have 3-6 scope items`)
}

function loadEditorial(value: unknown): ProjectLayerMap<ProjectEditorial> {
  if (!isRecord(value)) throw new Error('Project editorial data must be an object')
  if (Object.keys(value).sort().join('|') !== [...projectIds].sort().join('|')) throw new Error('Project editorial IDs must match the published project IDs')
  for (const id of projectIds) {
    const editorial = value[id]
    if (!isRecord(editorial) || !hasExactFields(editorial, editorialFields)) throw new Error(`Project editorial ${id} has unexpected fields`)
    for (const field of ['hook', 'summary', 'meaning', 'audience']) {
      if (typeof editorial[field] !== 'string' || !editorial[field]) throw new Error(`Project editorial ${id} has an invalid ${field}`)
    }
    if (!isStringList(editorial.features, 3, 6)) throw new Error(`Project editorial ${id} must have 3-6 features`)
    if (!isStringList(editorial.stack, 1, 8)) throw new Error(`Project editorial ${id} must have 1-8 stack entries`)
    if (!isStringList(editorial.opportunity, 2, 5)) throw new Error(`Project editorial ${id} must have 2-5 opportunities`)
    if (!Array.isArray(editorial.directions) || editorial.directions.length < 3 || editorial.directions.length > 5) throw new Error(`Project editorial ${id} must have 3-5 directions`)
    editorial.directions.forEach((direction, index) => assertDirection(direction, id, index))
    const directionIds = editorial.directions.map((direction) => (direction as Direction).id)
    if (new Set(directionIds).size !== directionIds.length) throw new Error(`Project editorial ${id} has duplicate direction IDs`)
  }
  return value as ProjectLayerMap<ProjectEditorial>
}

export const projectEditorial = loadEditorial(rawEditorial)
