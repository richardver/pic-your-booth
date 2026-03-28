import React from 'react';
import { GENRE_TOKENS, TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const HexBadge: React.FC<{ genre: Genre; size?: number }> = ({ genre, size = 72 }) => {
  const { accent } = GENRE_TOKENS[genre];
  return (
    <div style={{
      width: size,
      height: size,
      clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
      background: accent,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: TOKENS.fontDisplay,
      fontSize: size * 0.45,
      color: TOKENS.void,
    }}>
      G
    </div>
  );
};
