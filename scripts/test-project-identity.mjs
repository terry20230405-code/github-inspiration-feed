import { renderToStaticMarkup } from 'react-dom/server'
import { createServer } from 'vite'

const motifs = ['orbit', 'network', 'wave', 'radial', 'stack', 'grid', 'path', 'polyline']
const server = await createServer({ appType: 'custom', server: { middlewareMode: true } })

try {
  const { ProjectIdentity } = await server.ssrLoadModule('/src/components/ProjectIdentity.tsx')

  for (const [index, motif] of motifs.entries()) {
    const visual = {
      generatorVersion: 1,
      seed: `example/repository-${index}`,
      accent: '#315e88',
      foreground: '#ffffff',
      motif,
      variant: 1000 + index,
    }
    const first = renderToStaticMarkup(ProjectIdentity({ visual }))
    const second = renderToStaticMarkup(ProjectIdentity({ visual }))
    const elementCount = (first.match(/<(?:circle|ellipse|rect|path|line|polyline)\b/g) ?? []).length

    if (first !== second) throw new Error(`${motif} renderer is not deterministic`)
    if (elementCount < 5 || elementCount > 12) throw new Error(`${motif} renders ${elementCount} elements; expected 5-12`)
    if (!first.includes('aria-hidden="true"')) throw new Error(`${motif} is missing decorative accessibility state`)
    if (/remotion|excalidraw|immich|n8n/i.test(first)) throw new Error(`${motif} contains a project-specific name`)
    console.log(`OK: ${motif} renders ${elementCount} deterministic SVG elements`)
  }
} finally {
  await server.close()
}
