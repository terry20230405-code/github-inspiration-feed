import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import selectorDev from '@terry/selector-dev'

export default defineConfig({
  plugins: [react(), selectorDev()],
  server: { host: '127.0.0.1', port: 5173 },
})
