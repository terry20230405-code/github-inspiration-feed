export const indicatorCount = 5

export function clampProjectIndex(index: number, total: number) {
  return Math.max(0, Math.min(Math.max(0, total - 1), index))
}

export function renderedProjectIndices(active: number, total: number) {
  if (total <= 0) return []
  const current = clampProjectIndex(active, total)
  const start = Math.max(0, current - 1)
  const end = Math.min(total - 1, current + 1)
  return Array.from({ length: end - start + 1 }, (_, offset) => start + offset)
}

export function retainedProjectIndices(active: number, total: number) {
  const rendered = renderedProjectIndices(active, total)
  if (!rendered.length) return rendered
  const preload = clampProjectIndex(active, total) + 2
  return preload < total ? [...rendered, preload] : rendered
}

export function progressIndicatorTargets(active: number, total: number) {
  if (total <= 0) return Array.from({ length: indicatorCount }, () => null)
  const current = clampProjectIndex(active, total)
  const windowSize = Math.min(indicatorCount, total)
  const start = Math.max(0, Math.min(current - Math.floor(windowSize / 2), total - windowSize))
  const targets: Array<number | null> = Array.from({ length: windowSize }, (_, offset) => start + offset)
  while (targets.length < indicatorCount) targets.push(null)
  return targets
}
