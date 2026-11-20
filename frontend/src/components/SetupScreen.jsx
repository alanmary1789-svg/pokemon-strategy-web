import { DIFFICULTY_HINTS, TYPE_LABELS, describeModifiers } from '../labels.js'
import Arena from './Arena.jsx'
import TypeIcon from './TypeIcon.jsx'

// Un bouton radio habillé : accessible au clavier, stylé comme une carte ou une pastille.
function Choice({ name, value, current, onSelect, className = '', children }) {
  const selected = current === value
  return (
    <label className={`choice ${className}${selected ? ' is-selected' : ''}`}>
      <input
        type="radio"
        name={name}
        value={value ?? 'random'}
        checked={selected}
        onChange={() => onSelect(value)}
      />
      {children}
    </label>
  )
}

export default function SetupScreen({ options, settings, onChange, onStart, starting, error }) {
  const update = (key) => (value) => onChange({ ...settings, [key]: value })
  const choosePokemon = (key) =>
    onChange({ ...settings, pokemon: key, opponent: settings.opponent === key ? null : settings.opponent })

  const player = options.pokemon.find((p) => p.key === settings.pokemon)
  const opponent = options.pokemon.find((p) => p.key === settings.opponent) ?? null
  const weather = options.weathers.find((w) => w.key === settings.weather)
  const terrain = options.terrains.find((t) => t.key === settings.terrain)

  function submit(event) {
    event.preventDefault()
    onStart()
  }

  return (
    <main className="setup" data-accent={player.type}>
      <header className="setup-head">
        <h1>Arène des types</h1>
        <p>Choisis ton Pokémon et les conditions du combat, puis affronte l'ordinateur.</p>
      </header>

      <form className="setup-grid" onSubmit={submit}>
        <div className="setup-form">
          <fieldset>
            <legend>Ton Pokémon</legend>
            <div className="roster">
              {options.pokemon.map((p) => (
                <Choice key={p.key} name="pokemon" value={p.key} current={settings.pokemon} onSelect={choosePokemon}>
                  <span className="roster-card" data-type={p.type}>
                    <span className="roster-emblem">
                      <TypeIcon type={p.type} />
                    </span>
                    <span className="roster-name">{p.name}</span>
                    <span className="roster-meta">
                      {TYPE_LABELS[p.type]}, {p.max_hp} PV
                    </span>
                    <span className="roster-moves">{p.attacks.map((a) => a.name).join(', ')}</span>
                  </span>
                </Choice>
              ))}
            </div>
          </fieldset>

          <fieldset>
            <legend>Adversaire</legend>
            <div className="segmented">
              <Choice name="opponent" value={null} current={settings.opponent} onSelect={update('opponent')} className="pill">
                Au hasard
              </Choice>
              {options.pokemon
                .filter((p) => p.key !== settings.pokemon)
                .map((p) => (
                  <Choice key={p.key} name="opponent" value={p.key} current={settings.opponent} onSelect={update('opponent')} className="pill">
                    {p.name}
                  </Choice>
                ))}
            </div>
          </fieldset>

          <fieldset>
            <legend>Difficulté</legend>
            <div className="segmented">
              {options.difficulties.map((d) => (
                <Choice key={d.key} name="difficulty" value={d.key} current={settings.difficulty} onSelect={update('difficulty')} className="pill">
                  {d.label}
                </Choice>
              ))}
            </div>
            <p className="hint">{DIFFICULTY_HINTS[settings.difficulty]}</p>
          </fieldset>

          <div className="conditions-grid">
            <fieldset>
              <legend>Météo</legend>
              <div className="segmented">
                {options.weathers.map((w) => (
                  <Choice key={w.key} name="weather" value={w.key} current={settings.weather} onSelect={update('weather')} className="pill">
                    {w.label}
                  </Choice>
                ))}
              </div>
            </fieldset>
            <fieldset>
              <legend>Terrain</legend>
              <div className="segmented">
                {options.terrains.map((t) => (
                  <Choice key={t.key} name="terrain" value={t.key} current={settings.terrain} onSelect={update('terrain')} className="pill">
                    {t.label}
                  </Choice>
                ))}
              </div>
            </fieldset>
          </div>

          <label className="field">
            <span className="field-label">Ton nom de dresseur</span>
            <input
              className="text-input"
              value={settings.trainer}
              onChange={(event) => update('trainer')(event.target.value)}
              maxLength={20}
              required
            />
          </label>

          {error && (
            <p className="error" role="alert">
              {error}
            </p>
          )}

          <button className="primary" type="submit" disabled={starting}>
            {starting ? 'Préparation du combat…' : 'Lancer le combat'}
          </button>
        </div>

        <aside className="preview" aria-label="Aperçu de l'arène">
          <Arena
            weather={settings.weather}
            terrain={settings.terrain}
            player={player}
            opponent={opponent}
            trainers={{ player: settings.trainer, opponent: 'Rival' }}
          />          <dl className="effects">
            <div>
              <dt>{weather.label}</dt>
              <dd>{describeModifiers(weather.modifiers)}</dd>
            </div>
            <div>
              <dt>Terrain {terrain.label.toLowerCase()}</dt>
              <dd>{describeModifiers(terrain.modifiers)}</dd>
            </div>
          </dl>
        </aside>
      </form>
    </main>
  )
}