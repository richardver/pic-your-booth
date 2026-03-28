import React from 'react';
import { GENRE_TOKENS, TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';
import { WipeReveal } from './effects/WipeReveal';

export const GenrePills: React.FC<{ tags: string[]; genre: Genre }> = ({ tags, genre }) => {
  const { accent, dim } = GENRE_TOKENS[genre];

  return (
    <div style={{ display: 'flex', gap: 16, marginTop: 24, justifyContent: 'center' }}>
      {tags.map((tag, i) => (
        <WipeReveal key={tag} delay={10 + i * 5}>
          <div style={{
            fontFamily: TOKENS.fontBody,
            fontSize: 28,
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase' as const,
            padding: '8px 24px',
            borderRadius: 999,
            background: dim,
            color: accent,
          }}>
            {tag}
          </div>
        </WipeReveal>
      ))}
    </div>
  );
};
