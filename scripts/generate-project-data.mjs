import { mkdir, readFile, readdir, unlink, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'

const projectRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..')
const sourceDirectory = path.join(projectRoot, 'src', 'data')
const outputDirectory = path.join(projectRoot, 'public', 'data', 'projects')

async function readJson(name) {
  return JSON.parse(await readFile(path.join(sourceDirectory, name), 'utf8'))
}

function assertLayer(name, value, projectIds) {
  if (!value || typeof value !== 'object' || Array.isArray(value)) throw new Error(`${name} must be an object`)
  const actual = Object.keys(value).sort().join('|')
  const expected = [...projectIds].sort().join('|')
  if (actual !== expected) throw new Error(`${name} project IDs must match order.json`)
}

export async function generateProjectData() {
  const [order, repositories, editorial, visuals] = await Promise.all([
    readJson('order.json'),
    readJson('repositories.json'),
    readJson('editorial.json'),
    readJson('visuals.json'),
  ])

  if (!Array.isArray(order) || order.length === 0 || !order.every(id => typeof id === 'string' && /^[a-z0-9]+(?:-[a-z0-9]+)*$/.test(id))) {
    throw new Error('order.json must contain non-empty lowercase project IDs')
  }
  if (new Set(order).size !== order.length) throw new Error('order.json contains duplicate project IDs')
  assertLayer('repositories.json', repositories, order)
  assertLayer('editorial.json', editorial, order)
  assertLayer('visuals.json', visuals, order)

  const projects = order.map(id => ({
    schemaVersion: 2,
    id,
    repository: repositories[id],
    editorial: editorial[id],
    visual: visuals[id],
  }))
  const index = {
    schemaVersion: 1,
    projects: projects.map(project => ({
      id: project.id,
      name: project.repository.name,
      hook: project.editorial.hook,
      accent: project.visual.accent,
      foreground: project.visual.foreground,
    })),
  }

  await mkdir(outputDirectory, { recursive: true })
  const expectedFiles = new Set(['index.json', ...order.map(id => `${id}.json`)])
  for (const entry of await readdir(outputDirectory, { withFileTypes: true })) {
    if (entry.isFile() && entry.name.endsWith('.json') && !expectedFiles.has(entry.name)) {
      await unlink(path.join(outputDirectory, entry.name))
    }
  }

  await Promise.all([
    writeFile(path.join(outputDirectory, 'index.json'), `${JSON.stringify(index)}\n`, 'utf8'),
    ...projects.map(project => writeFile(path.join(outputDirectory, `${project.id}.json`), `${JSON.stringify(project)}\n`, 'utf8')),
  ])

  return { outputDirectory, projectCount: projects.length, files: expectedFiles.size }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const result = await generateProjectData()
  console.log(`Generated ${result.projectCount} split project records in ${result.outputDirectory}`)
}
