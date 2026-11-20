import { useEffect, useRef, useState } from 'react'
import { sendAttack, sendPotion } from '../api.js'
import { TYPE_LABELS } from '../labels.js'
import Arena from './Arena.jsx'

const wait = (ms) => new Promise((resolve) => setTimeout(resolve, ms))
const pauseBetweenEvents = () =>
  window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 250 : 900

const plural = (count, word) => (count === 0 ? `aucune ${word}` : `${count} ${word}${count > 1 ? 's' : ''}`)

export default function BattleScreen({ initialBattle, options, onReplay, replaying, onExit }) {
  const [battle, setBattle] = useState(initialBattle)          // dernier état reçu du serveur
  const [hp, setHp] = useState({                               // PV affichés, mis à jour événement par événement
    player: initialBattle.player.pokemon.hp,
    opponent: initialBattle.opponent.pokemon.hp,
  })
  const [messages, setMessages] = useState(initialBattle.log)
  const [hit, setHit] = useState(null)                         // 'player' | 'opponent' | null
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState(null)
  const dialogRef = useRef(null)

  useEffect(() => {
    const dialog = dialogRef.current
    if (dialog) dialog.scrollTop = dialog.scrollHeight
  }, [messages, busy])

  // Envoie une action, puis rejoue un par un les nouveaux événements du journal.
  async function play(action) {
    setBusy(true)
    setError(null)
    try {
      const next = await action()
      const fresh = next.log.slice(battle.log.length)
      for (const event of fresh) {
        setMessages((current) => [...current, event])
        if (event.kind === 'attack') {
          const target = event.side === 'player' ? 'opponent' : 'player'
          setHp((current) => ({ ...current, [target]: event.hp }))
          setHit(target)
        } else if (event.kind === 'potion') {
          setHp((current) => ({ ...current, player: event.hp }))
        }
        await wait(pauseBetweenEvents())
        setHit(null)
      }
      setBattle(next)
    } catch (err) {
      setError(err.message)                                    // l'état affiché ne bouge pas
    } finally {
      setBusy(false)
    }
  }

    // L'état du combat donne le nom du Pokémon ; le roster donne sa clé (pour l'image).
  const withKey = (pokemon) => ({ ...pokemon, key: options.pokemon.find((p) => p.name === pokemon.name)?.key })
  const player = withKey(battle.player.pokemon)
  const opponent = withKey(battle.opponent.pokemon)
  const over = battle.status !== 'in_progress'
  const potions = battle.player.potions
  const fullHp = hp.player === player.max_hp
  const label = (list, key) => list.find((item) => item.key === key)?.label ?? key

  return (
    <main className="battle" data-accent={player.type}>
      <header className="battle-bar">
        <h1 className="battle-title">Arène des types</h1>
        <ul className="chips" aria-label="Conditions du combat">
          <li>Tour {battle.turn}</li>
          <li>{label(options.weathers, battle.weather)}</li>
          <li>Terrain {label(options.terrains, battle.terrain).toLowerCase()}</li>
          <li>Rival {label(options.difficulties, battle.difficulty).toLowerCase()}</li>
        </ul>
        <button type="button" className="link-button" onClick={onExit}>
          Quitter le combat
        </button>
      </header>

      <Arena
        weather={battle.weather}
        terrain={battle.terrain}
        player={player}
        opponent={opponent}
        trainers={{ player: battle.player.name, opponent: battle.opponent.name }}
        hp={hp}
        hit={hit}
      />
      <section className="console">
        <div className="dialog" ref={dialogRef} aria-live="polite">
          <p className="line">
            {battle.opponent.name} envoie {opponent.name} !
          </p>
          {messages.map((event, index) => (
            <p key={index} className={`line line-${event.side}`}>
              {event.message}
            </p>
          ))}
          {!over && !busy && <p className="line prompt">Que doit faire {player.name} ?</p>}
        </div>

        {over ? (
          <div className="result" data-outcome={battle.status}>
            <p className="result-title">{battle.status === 'won' ? 'Victoire !' : 'Défaite'}</p>
            <p>
              {battle.status === 'won'
                ? `${opponent.name} est K.O. en ${battle.turn - 1} tours.`
                : `${player.name} est K.O. Essaie une autre météo, un autre terrain ou un autre Pokémon.`}
            </p>
            <div className="result-actions">
              <button type="button" className="primary" onClick={onReplay} disabled={replaying}>
                {replaying ? 'Préparation…' : 'Rejouer'}
              </button>
              <button type="button" className="secondary" onClick={onExit}>
                Changer les réglages
              </button>
            </div>
          </div>
        ) : (
          <div className="actions">
            {player.attacks.map((move, index) => (
              <button
                key={move.name}
                type="button"
                className="move"
                data-type={move.type}
                disabled={busy}
                onClick={() => play(() => sendAttack(battle.id, index))}
              >
                <span className="move-name">{move.name}</span>
                <span className="move-meta">
                  {TYPE_LABELS[move.type]}, puissance {move.damage}
                </span>
              </button>
            ))}
            <button
              type="button"
              className="move move-potion"
              disabled={busy || potions === 0 || fullHp}
              onClick={() => play(() => sendPotion(battle.id))}
            >
              <span className="move-name">Potion</span>
              <span className="move-meta">
                {fullHp && potions > 0 ? 'PV déjà au maximum' : `+30 PV, ${plural(potions, 'restante')}`}
              </span>
            </button>
          </div>
        )}
      </section>

      {error && (
        <p className="error" role="alert">
          {error}
        </p>
      )}
    </main>
  )
}