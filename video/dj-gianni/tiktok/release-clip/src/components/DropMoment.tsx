import React from 'react';
import { AbsoluteFill } from 'remotion';
import { TOKENS, GENRE_TOKENS, SAFE } from '../lib/tokens';
import { Genre } from '../lib/types';
import { GlitchText } from './effects/GlitchText';
import { SlamIn } from './effects/SlamIn';

export const DropMoment: React.FC<{ serieName: string; genre: Genre }> = ({ serieName, genre }) => {
  const { accent } = GENRE_TOKENS[genre];

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
    }}>
      <GlitchText intensity={5}>
        <SlamIn>
          <div style={{
            fontFamily: TOKENS.fontDisplay,
            fontSize: 140,
            letterSpacing: '0.06em',
            color: TOKENS.white,
            textShadow: `0 4px 30px rgba(0,0,0,0.9), 0 0 80px ${accent}66`,
            textAlign: 'center',
            lineHeight: 1,
          }}>
            DJ GIANNI
          </div>
        </SlamIn>
      </GlitchText>
      <SlamIn delay={3}>
        <div style={{
          fontFamily: TOKENS.fontDisplay,
          fontSize: 52,
          letterSpacing: '0.1em',
          color: accent,
          textShadow: '0 2px 12px rgba(0,0,0,0.9)',
          marginTop: -8,
          textAlign: 'center',
        }}>
          {serieName}
        </div>
      </SlamIn>
    </AbsoluteFill>
  );
};
