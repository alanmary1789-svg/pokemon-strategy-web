// Ce qui relève de l'affichage seulement : libellés des types et explications des difficultés.

export const TYPE_LABELS = {
  normal: 'Normal',
  fire: 'Feu',
  water: 'Eau',
  grass: 'Plante',
  electric: 'Électrik',
}

export const DIFFICULTY_HINTS = {
  easy: "L'ordinateur choisit ses attaques au hasard.",
  medium: 'Il joue toujours son attaque la plus puissante.',
  hard: "Il calcule l'attaque qui fait le plus de dégâts : type, météo et terrain compris.",
}

const number = (value) => String(value).replace('.', ',')

// { fire: 0.5, water: 1.5 } -> "Eau ×1,5, Feu ×0,5"
export function describeModifiers(modifiers) {
  const entries = Object.entries(modifiers).sort(([, a], [, b]) => b - a)
  if (entries.length === 0) return 'aucun effet'
  return entries.map(([type, value]) => `${TYPE_LABELS[type]} ×${number(value)}`).join(', ')
}