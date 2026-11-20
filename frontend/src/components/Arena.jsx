import { useState } from 'react'
import { TYPE_LABELS } from '../labels.js'
import HpBar from './HpBar.jsx'
import TypeIcon from './TypeIcon.jsx'
// Numéros du Pokédex national : PokeAPI range ses sprites par numéro.
const DEX = { bulbizarre: 1, salameche: 4, carapuce: 7, pikachu: 25 }
const SPRITES =
  'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/versions/generation-v/black-white/animated'

// Un combattant : son image (ou l'emblème de son type) + son panneau (dresseur, nom, type, PV).
function Fighter({ side, pokemon, trainer, hp, hit }) {
  const type = pokemon?.type ?? 'unknown'
  const ko = pokemon && hp === 0
  // Comme en jeu : ton Pokémon vu de dos, l'adversaire vu de face.
  const dex = DEX[pokemon?.key]
  const src = dex ? `${SPRITES}${side === 'player' ? '/back' : ''}/${dex}.gif` : null  
  const [failedSrc, setFailedSrc] = useState(null)
  const showImage = src !== null && failedSrc !== src                // image absente -> emblème du type

  return (
    <div className={`fighter fighter-${side}`} data-type={type}>
      <div className={`token${showImage ? ' has-image' : ''}${hit ? ' is-hit' : ''}${ko ? ' is-ko' : ''}`}>
        {showImage ? (
          <img className="token-image" src={src} alt={pokemon.name} onError={() => setFailedSrc(src)} />
        ) : (
          <TypeIcon type={type} className="token-icon" />
        )}
      </div>
      <div className="panel">
        {trainer && <span className="panel-trainer">{trainer}</span>}
        <div className="panel-head">
          <span className="panel-name">{pokemon?.name ?? 'Au hasard'}</span>
          <span className="type-chip" data-type={type}>
            {TYPE_LABELS[type] ?? '?'}
          </span>
        </div>
        {pokemon && hp !== undefined && <HpBar hp={hp} maxHp={pokemon.max_hp} />}
      </div>
    </div>
  )
}

export default function Arena({ weather, terrain, player, opponent, trainers = {}, hp = {}, hit = null }) {
  return (
    <div className="arena" data-weather={weather} data-terrain={terrain}>
      <div className="sky" aria-hidden="true" />
      <div className="ground" aria-hidden="true" />
      <Fighter side="opponent" pokemon={opponent} trainer={trainers.opponent} hp={hp.opponent} hit={hit === 'opponent'} />
      <Fighter side="player" pokemon={player} trainer={trainers.player} hp={hp.player} hit={hit === 'player'} />
    </div>
  )
}