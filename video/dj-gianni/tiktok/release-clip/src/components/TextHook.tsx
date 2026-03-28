import React from 'react';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';
import { GlitchText } from './effects/GlitchText';
import { SlamIn } from './effects/SlamIn';

export const TextHook: React.FC<{ text: string; genre: Genre }> = ({ text, genre }) => {
  const { accent } = GENRE_TOKENS[genre];
  const lines = text.split('\n');

  return (
    <GlitchText>
      {lines.map((line, i) => (
        <SlamIn key={i} delay={i * 4}>
          <div style={{
            fontFamily: TOKENS.fontDisplay,
            fontSize: 90,
            letterSpacing: '0.04em',
            color: TOKENS.white,
            textShadow: '0 4px 20px rgba(0,0,0,0.9)',
            lineHeight: 1.0,
            textAlign: 'center',
          }}>
            {line}
          </div>
        </SlamIn>
      ))}
    </GlitchText>
  );
};
