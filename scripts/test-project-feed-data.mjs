import { readFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import { generateProjectData } from './generate-project-data.mjs'

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const order = JSON.parse(await readFile(path.join(projectRoot, 'src/data/order.json'), 'utf8'))
const result = await generateProjectData()
const index = JSON.parse(await readFile(path.join(result.outputDirectory, 'index.json'), 'utf8'))

if (index.schemaVersion !== 1) throw new Error('split project index has an unsupported schema version')
if (index.projects.length !== order.length) throw new Error('split project index count does not match order.json')
if (index.projects.map(project => project.id).join('|') !== order.join('|')) throw new Error('split project index order does not match order.json')

for (const id of order) {
  const project = JSON.parse(await readFile(path.join(result.outputDirectory, `${id}.json`), 'utf8'))
  if (project.schemaVersion !== 2 || project.id !== id) throw new Error(`${id}.json has an invalid project identity`)
  if (!project.repository || !project.editorial || !project.visual) throw new Error(`${id}.json is missing a product data layer`)
}

console.log(`OK: generated one lightweight index and ${order.length} individual project JSON files`)
