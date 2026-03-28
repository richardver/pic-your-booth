import React from 'react';
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const GenrePills: React.FC<{ tags: string[]; genre: Genre }> = ({ tags, genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent, dim } = GENRE_TOKENS[genre];

  return (
    <div style={{ display: 'flex', gap: 16, marginTop: 24 }}>
      {tags.map((tag, i) => {
        const enter = spring({ fps, frame: frame - i * 4, config: { damping: 200 } });
        return (
          <div key={tag} style={{
            fontSize: 28,
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase' as const,
            padding: '8px 24px',
            borderRadius: 999,
            background: dim,
            color: accent,
            opacity: Math.max(0, enter),
            transform: `translateY(${(1 - Math.max(0, enter)) * 10}px)`,
          }}>
            {tag}
          </div>
        );
      })}
    </div>
  );
};
