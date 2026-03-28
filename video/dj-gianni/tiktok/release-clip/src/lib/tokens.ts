import { Genre } from './types';

export const GENRE_TOKENS: Record<Genre, { accent: string; dim: string; name: string }> = {
  afro:      { accent: '#f0654a', dim: 'rgba(240,101,74,0.10)', name: 'Afro Beats' },
  caribbean: { accent: '#f5b731', dim: 'rgba(245,183,49,0.10)', name: 'Caribbean' },
  urban:     { accent: '#c084fc', dim: 'rgba(192,132,252,0.10)', name: 'NL Urban' },
};

export const TOKENS = {
  void: '#050508',
  white: '#ededf0',
  muted: 'rgba(237,237,240,0.45)',
  fontDisplay: "'Bebas Neue', Impact, sans-serif",
  fontBody: "'Space Grotesk', system-ui, sans-serif",
};
