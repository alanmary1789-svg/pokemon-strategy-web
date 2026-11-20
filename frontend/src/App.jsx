import { useEffect, useState } from 'react'
import { createBattle, getOptions } from './api.js'
import BattleScreen from './components/BattleScreen.jsx'
import SetupScreen from './components/SetupScreen.jsx'

const DEFAULT_SETTINGS = {
  trainer: 'Sacha',
  pokemon: 'pikachu',
  opponent: null,          // null : adversaire tiré au sort par le serveur
  difficulty: 'medium',
  weather: 'clear',
  terrain: 'normal',
}

export default function App() {
  const [options, setOptions] = useState(null)
  const [loadError, setLoadError] = useState(null)
  const [settings, setSettings] = useState(DEFAULT_SETTINGS)
  const [battle, setBattle] = useState(null)
  const [starting, setStarting] = useState(false)
  const [startError, setStartError] = useState(null)

  async function loadOptions() {
    setLoadError(null)
    try {
      setOptions(await getOptions())
    } catch (err) {
      setLoadError(err.message)
    }
  }

  useEffect(() => {
    loadOptions()
  }, [])

  async function startBattle() {
    setStarting(true)
    setStartError(null)
    try {
      setBattle(await createBattle(settings))
    } catch (err) {
      setStartError(err.message)
      setBattle(null)            // retour aux réglages, avec le message d'erreur
    } finally {
      setStarting(false)
    }
  }

  if (loadError) {
    return (
      <main className="splash">
        <h1>Arène des types</h1>
        <p className="error" role="alert">
          {loadError}
        </p>
        <button type="button" className="primary" onClick={loadOptions}>
          Réessayer
        </button>
      </main>
    )
  }

  if (!options) {
    return (
      <main className="splash">
        <p>Chargement de l'arène…</p>
      </main>
    )
  }

  if (battle) {
    return (
      <BattleScreen
        key={battle.id}          // nouvelle partie = composant neuf, état remis à zéro
        initialBattle={battle}
        options={options}
        onReplay={startBattle}
        replaying={starting}
        onExit={() => setBattle(null)}
      />
    )
  }

  return (
    <SetupScreen
      options={options}
      settings={settings}
      onChange={setSettings}
      onStart={startBattle}
      starting={starting}
      error={startError}
    />
  )
}