import { TYPE_LABELS } from '../labels.js'
import HpBar from './HpBar.jsx'
import TypeIcon from './TypeIcon.jsx'

// Un combattant : son jeton posé sur l'arène + son panneau (nom, type, PV).
function Fighter({ side, pokemon, hp, hit }) {
  const type = pokemon?.type ?? 'unknown'
  const ko = pokemon && hp === 0
  return (
    <div className={`fighter fighter-${side}`} data-type={type}>
      <div className={`token${hit ? ' is-hit' : ''}${ko ? ' is-ko' : ''}`}>
        <TypeIcon type={type} className="token-icon" />
      </div>
      <div className="panel">
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

export default function Arena({ weather, terrain, player, opponent, hp = {}, hit = null }) {
  return (
    <div className="arena" data-weather={weather} data-terrain={terrain}>
      <div className="sky" aria-hidden="true" />
      <div className="ground" aria-hidden="true" />
      <Fighter side="opponent" pokemon={opponent} hp={hp.opponent} hit={hit === 'opponent'} />
      <Fighter side="player" pokemon={player} hp={hp.player} hit={hit === 'player'} />
    </div>
  )
}