import { createServer } from 'vite'

const server = await createServer({
  configFile: false,
  appType: 'custom',
  server: { middlewareMode: true },
})

try {
  const { indicatorCount, progressIndicatorTargets, renderedProjectIndices, retainedProjectIndices } = await server.ssrLoadModule('/src/feed-window.ts')
  const equal = (actual, expected, label) => {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) throw new Error(`${label}: ${JSON.stringify(actual)} !== ${JSON.stringify(expected)}`)
  }

  equal(renderedProjectIndices(0, 10), [0, 1], 'first project render window')
  equal(retainedProjectIndices(0, 10), [0, 1, 2], 'first project preload window')
  equal(renderedProjectIndices(4, 10), [3, 4, 5], 'middle project render window')
  equal(retainedProjectIndices(4, 10), [3, 4, 5, 6], 'middle project preload window')
  equal(renderedProjectIndices(9, 10), [8, 9], 'last project render window')
  equal(retainedProjectIndices(9, 10), [8, 9], 'last project preload window')
  equal(progressIndicatorTargets(0, 10), [0, 1, 2, 3, 4], 'first indicator window')
  equal(progressIndicatorTargets(5, 10), [5, 6, 7, 8, 9], 'second indicator cycle')
  equal(progressIndicatorTargets(9, 10), [5, 6, 7, 8, 9], 'end of second indicator cycle')
  equal(progressIndicatorTargets(5, 6), [5, 1, 2, 3, 4], 'partial indicator cycle stays full')
  equal(progressIndicatorTargets(10, 12), [10, 11, 7, 8, 9], 'final partial indicator cycle')
  for (let active = 0; active < 12; active += 1) {
    const targets = progressIndicatorTargets(active, 12)
    if (targets.indexOf(active) !== active % indicatorCount) throw new Error(`indicator did not advance cyclically for project ${active + 1}`)
  }
  if (progressIndicatorTargets(5, 1000).length !== indicatorCount) throw new Error('indicator count is not fixed')
  console.log('OK: feed window is bounded and the five-dot indicator advances cyclically')
} finally {
  await server.close()
}
