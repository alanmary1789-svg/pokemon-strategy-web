// Toutes les requêtes passent par ici. Les chemins sont relatifs (« /api/... ») :
// en dev, Vite les relaie vers FastAPI ; en production, FastAPI sert le site lui-même.

const SERVER_DOWN = "Le serveur ne répond pas. Vérifie qu'uvicorn tourne sur le port 8000, puis réessaie."

function messageFrom(payload, status) {
  if (typeof payload?.detail === 'string') return payload.detail      // 400, 404, 409
  if (Array.isArray(payload?.detail)) return 'Réglages invalides.'      // 422 de Pydantic
  if (status >= 500) return SERVER_DOWN                                // proxy Vite sans backend
  return `Erreur HTTP ${status}`
}

export async function request(path, { body, ...options } = {}) {
  let response
  try {
    response = await fetch(path, {
      ...options,
      headers: body ? { 'Content-Type': 'application/json' } : undefined,
      body,
    })
  } catch {
    throw new Error(SERVER_DOWN)                     // réseau coupé, serveur arrêté
  }
  if (!response.ok) {                                // fetch ne rejette pas un 4xx/5xx
    const payload = await response.json().catch(() => null)
    throw new Error(messageFrom(payload, response.status))
  }
  return response.json()
}

export const getOptions = () => request('/api/options')

export const createBattle = (settings) =>
  request('/api/battles', { method: 'POST', body: JSON.stringify(settings) })

export const sendAttack = (battleId, attackIndex) =>
  request(`/api/battles/${battleId}/attack`, {
    method: 'POST',
    body: JSON.stringify({ attack_index: attackIndex }),
  })

export const sendPotion = (battleId) =>
  request(`/api/battles/${battleId}/potion`, { method: 'POST' })