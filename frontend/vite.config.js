import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      // En développement, Vite (port 5173) relaie /api vers FastAPI (port 8000) :
      // pour le navigateur, tout vient de la même origine, donc pas de CORS.
      '/api': 'http://127.0.0.1:8000',
    },
  },
})