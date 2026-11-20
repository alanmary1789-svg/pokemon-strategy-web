export default function HpBar({ hp, maxHp }) {
  const ratio = maxHp > 0 ? hp / maxHp : 0
  const level = ratio > 0.5 ? 'high' : ratio > 0.2 ? 'mid' : 'low'
  return (
    <div className="hp">
      <div
        className="hp-track"
        role="meter"
        aria-label="Points de vie"
        aria-valuemin={0}
        aria-valuemax={maxHp}
        aria-valuenow={hp}
      >
        <div className="hp-fill" data-level={level} style={{ width: `${ratio * 100}%` }} />
      </div>
      <span className="hp-numbers">
        {hp}/{maxHp} PV
      </span>
    </div>
  )
}