export type ProjectId = string

export type Direction = {
  readonly id: string
  readonly name: string
  readonly tagline: string
  readonly problem: string
  readonly audience: string
  readonly approach: string
  readonly difference: string
  readonly scope: readonly string[]
}

export type RepositoryState = 'active' | 'archived' | 'disabled' | 'unavailable'

export type RepositorySnapshot = {
  readonly githubId: number
  readonly fullName: string
  readonly name: string
  readonly stars: number
  readonly forks: number
  readonly language: string
  readonly pushedAt: string
  readonly license: string
  readonly state: RepositoryState
  readonly fetchedAt: string
}

export type ProjectEditorial = {
  readonly hook: string
  readonly summary: string
  readonly meaning: string
  readonly audience: string
  readonly features: readonly string[]
  readonly stack: readonly string[]
  readonly opportunity: readonly string[]
  readonly directions: readonly Direction[]
}

export const visualMotifs = ['orbit', 'network', 'wave', 'radial', 'stack', 'grid', 'path', 'polyline'] as const

export type VisualMotif = (typeof visualMotifs)[number]

export type ProjectVisual = {
  readonly generatorVersion: 1 | 2
  readonly seed: string
  readonly accent: string
  readonly foreground: '#000000' | '#ffffff'
  readonly motif: VisualMotif
  readonly variant: number
}

export type Project = {
  readonly schemaVersion: 2
  readonly id: ProjectId
  readonly repository: RepositorySnapshot
  readonly editorial: ProjectEditorial
  readonly visual: ProjectVisual
}

export type ProjectLayerMap<T> = Readonly<Record<string, T>>
