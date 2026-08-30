import rawVisuals from './visuals.json'
import { projectIds } from './order'
import { visualMotifs, type ProjectLayerMap, type ProjectVisual } from './types'

const hexPattern = /^#[0-9a-fA-F]{6}$/
const fullNamePattern = /^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function loadVisuals(value: unknown): ProjectLayerMap<ProjectVisual> {
  if (!isRecord(value)) throw new Error('Project visuals must be an object')
  const expected = [...projectIds].sort().join('|')
  if (Object.keys(value).sort().join('|') !== expected) throw new Error('Project visual IDs must match the published project IDs')
  for (const id of projectIds) {
    const visual = value[id]
    if (!isRecord(visual)) throw new Error(`Project visual ${id} must be an object`)
    const fields = ['accent', 'foreground', 'generatorVersion', 'motif', 'seed', 'variant']
    if (Object.keys(visual).sort().join('|') !== fields.join('|')) throw new Error(`Project visual ${id} has unexpected fields`)
    if (visual.generatorVersion !== 1 && visual.generatorVersion !== 2) throw new Error(`Project visual ${id} has an invalid generator version`)
    if (typeof visual.seed !== 'string' || !fullNamePattern.test(visual.seed)) throw new Error(`Project visual ${id} has an invalid seed`)
    if (typeof visual.accent !== 'string' || !hexPattern.test(visual.accent)) throw new Error(`Project visual ${id} has an invalid accent`)
    if (visual.foreground !== '#000000' && visual.foreground !== '#ffffff') throw new Error(`Project visual ${id} has an invalid foreground`)
    if (typeof visual.motif !== 'string' || !visualMotifs.includes(visual.motif as ProjectVisual['motif'])) throw new Error(`Project visual ${id} has an invalid motif`)
    if (!Number.isInteger(visual.variant) || Number(visual.variant) < 0 || Number(visual.variant) > 0xFFFFFFFF) throw new Error(`Project visual ${id} has an invalid variant`)
  }
  return value as ProjectLayerMap<ProjectVisual>
}

export const projectVisuals = loadVisuals(rawVisuals)
