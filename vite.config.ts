import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig(async ({ command }) => {
  const plugins = [react()]

  if (command === 'serve') {
    const selectorPackage = '@terry/selector-dev'
    const { default: selectorDev } = await import(/* @vite-ignore */ selectorPackage)
    plugins.push(selectorDev())
  }

  return {
    plugins,
    server: { host: '127.0.0.1', port: 5173 },
  }
})
