import assert from 'node:assert/strict'
import { readFile } from 'node:fs/promises'
import { createServer } from 'vite'
import { validateTranslation } from './project-translations.mjs'
import { generateProjectData } from './generate-project-data.mjs'

const readJson = async file => JSON.parse(await readFile(new URL(file, import.meta.url), 'utf8'))
const [source, english, order] = await Promise.all([
  readJson('../src/data/editorial.json'), readJson('../src/locales/projects.en.json'), readJson('../src/data/order.json'),
])
const server = await createServer({ configFile: false, appType: 'custom', server: { middlewareMode: true } })
const storageDescriptor = Object.getOwnPropertyDescriptor(globalThis, 'localStorage')
try {
  const { messages, localizeEditorial, readLanguage, saveLanguage, languageStorageKey } = await server.ssrLoadModule('/src/i18n.ts')
  const { formatRelativeDate } = await server.ssrLoadModule('/src/data.ts')
  assert.deepEqual(Object.keys(messages.zh).sort(), Object.keys(messages.en).sort())
  assert.equal(messages.en.goTo(3), 'Go to project 3')
  const now = Date.parse('2026-09-04T12:00:00Z')
  assert.equal(formatRelativeDate('invalid', now, 'en'), 'Unknown')
  assert.equal(formatRelativeDate('2026-09-04T11:59:40Z', now, 'en'), 'Just now')
  assert.equal(formatRelativeDate('2026-09-04T11:00:00Z', now, 'en'), '1 hour ago')
  assert.equal(formatRelativeDate('2026-09-02T12:00:00Z', now, 'en'), '2 days ago')
  assert.equal(formatRelativeDate('2026-09-02T12:00:00Z', now), '2 天前')
  const values = new Map()
  Object.defineProperty(globalThis, 'localStorage', { configurable: true, value: {
    getItem: key => values.get(key) ?? null, setItem: (key, value) => values.set(key, value),
  } })
  assert.equal(readLanguage(), 'zh')
  saveLanguage('en')
  assert.equal(readLanguage(), 'en')
  assert.equal(values.get(languageStorageKey), 'en')
  values.set(languageStorageKey, 'unsupported')
  assert.equal(readLanguage(), 'zh')
  Object.defineProperty(globalThis, 'localStorage', { configurable: true, get() { throw new Error('Storage blocked') } })
  assert.equal(readLanguage(), 'zh')
  assert.doesNotThrow(() => saveLanguage('en'))

  await generateProjectData()
  for (const id of order) {
    validateTranslation(source[id], english[id], id)
    const project = await readJson(`../public/data/projects/${id}.json`)
    assert.deepEqual(localizeEditorial(project, 'zh'), source[id])
    assert.deepEqual(localizeEditorial(project, 'en'), english[id])
    const invalid = structuredClone(english[id])
    invalid.directions[0].id = 'wrong-id'
    assert.throws(() => validateTranslation(source[id], invalid, id))
    const missing = structuredClone(english[id])
    delete missing.summary
    assert.throws(() => validateTranslation(source[id], missing, id))
  }
  assert.deepEqual(Object.keys(english).sort(), [...order].sort())
  console.log(`OK: all ${order.length} projects have complete English content; UI keys, IDs, dates and language persistence verified`)
} finally {
  if (storageDescriptor) Object.defineProperty(globalThis, 'localStorage', storageDescriptor)
  else delete globalThis.localStorage
  await server.close()
}
