// Emblèmes de type dessinés à la main (pas d'illustrations officielles des Pokémon).
const PATHS = {
  electric: <path d="M13.5 2 4.5 14h6l-1.5 8 9.5-12.5h-6.2L13.5 2z" />,
  fire: (
    <path d="M12 2.5c.6 3.6 5.8 5.6 5.8 11.3a5.8 5.8 0 0 1-11.6 0c0-2.8 1.5-4.6 2.8-6 .1 1.8.9 3 2 3.3-.4-3.1.2-5.9 1-8.6z" />
  ),
  water: <path d="M12 2.5S5.5 9.8 5.5 14.6a6.5 6.5 0 0 0 13 0C18.5 9.8 12 2.5 12 2.5z" />,
  grass: (
    <>
      <path d="M20 3.5C10.6 3.8 4.5 9.4 4.5 17.6V20h2.2C14.9 19.6 20.2 13 20 3.5z" />
      <path d="M5.5 19 15 9" fill="none" stroke="var(--icon-vein)" strokeWidth="1.6" strokeLinecap="round" />
    </>
  ),
  normal: (
    <path
      fillRule="evenodd"
      d="M12 3a9 9 0 1 1 0 18 9 9 0 0 1 0-18zm0 5a4 4 0 1 0 0 8 4 4 0 0 0 0-8z"
    />
  ),
}

export default function TypeIcon({ type, className }) {
  if (!PATHS[type]) {
    return (
      <svg className={className} viewBox="0 0 24 24" aria-hidden="true">
        <text x="12" y="17.5" textAnchor="middle" fontSize="16" fontWeight="700" fill="currentColor">?</text>
      </svg>
    )
  }
  return (
    <svg className={className} viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
      {PATHS[type]}
    </svg>
  )
}