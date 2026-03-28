import React from 'react';
import { useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

const BAR_HEIGHTS = [0.35, 0.65, 1.0, 0.5, 0.8, 0.4, 0.7];

export const EQBar: React.FC<{ genre: Genre; height?: number }> = ({ genre, height = 80 }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', height }}>
      {BAR_HEIGHTS.map((h, i) => {
        const pulse = Math.sin((frame + i * 4) * 0.15) * 0.3 + 0.7;
        return (
          <div key={i} style={{
            width: 8,
            height: `${h * pulse * 100}%`,
            borderRadius: 4,
            background: accent,
            opacity: 0.8,
          }} />
        );
      })}
    </div>
  );
};
