import { Genre } from './types';
import { loadFont as loadBebasNeue } from '@remotion/google-fonts/BebasNeue';
import { loadFont as loadSpaceGrotesk } from '@remotion/google-fonts/SpaceGrotesk';

// Load fonts — Remotion needs this to render correctly
const bebasNeue = loadBebasNeue();
const spaceGrotesk = loadSpaceGrotesk();

export const GENRE_TOKENS: Record<Genre, { accent: string; dim: string; name: string }> = {
  afro:      { accent: '#f0654a', dim: 'rgba(240,101,74,0.10)', name: 'Afro Beats' },
  caribbean: { accent: '#f5b731', dim: 'rgba(245,183,49,0.10)', name: 'Caribbean' },
  urban:     { accent: '#c084fc', dim: 'rgba(192,132,252,0.10)', name: 'NL Urban' },
};

export const TOKENS = {
  void: '#050508',
  white: '#ededf0',
  muted: 'rgba(237,237,240,0.45)',
  fontDisplay: bebasNeue.fontFamily,
  fontBody: spaceGrotesk.fontFamily,
};

// TikTok safe zone padding (pixels at 1080x1920)
export const SAFE = {
  top: 160,
  right: 110,
  bottom: 280,
  left: 40,
};
