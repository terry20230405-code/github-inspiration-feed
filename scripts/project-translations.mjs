// A translation may change wording, never structure, IDs or technology names.
export function validateTranslation(source, translation, path = 'editorial') {
  if (typeof source === 'string') {
    if (typeof translation !== 'string' || !translation.trim()) throw new Error(`${path}: missing translation`)
    if (/\p{Script=Han}/u.test(translation)) throw new Error(`${path}: English translation contains Chinese text`)
    if ((path.endsWith('.id') || /\.stack\.\d+$/.test(path)) && translation !== source) {
      throw new Error(`${path}: stable identifiers and technology names must not change`)
    }
    return
  }
  if (Array.isArray(source)) {
    if (!Array.isArray(translation) || source.length !== translation.length) throw new Error(`${path}: translation length differs`)
    source.forEach((item, index) => validateTranslation(item, translation[index], `${path}.${index}`))
    return
  }
  if (!translation || typeof translation !== 'object' || Array.isArray(translation)) throw new Error(`${path}: invalid translation`)
  if (Object.keys(source).sort().join('|') !== Object.keys(translation).sort().join('|')) throw new Error(`${path}: translation fields differ`)
  for (const key of Object.keys(source)) validateTranslation(source[key], translation[key], `${path}.${key}`)
}
