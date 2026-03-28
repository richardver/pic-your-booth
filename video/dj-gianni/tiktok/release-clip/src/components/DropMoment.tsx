import React from 'react';
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const DropMoment: React.FC<{ serieName: string; genre: Genre }> = ({ serieName, genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent } = GENRE_TOKENS[genre];

  const scale = spring({ fps, frame, config: { damping: 12, stiffness: 200 } });
  const glow = spring({ fps, frame, config: { damping: 200 } });

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      background: `radial-gradient(ellipse at 50% 50%, ${accent}33 0%, transparent 60%)`,
      opacity: glow,
    }}>
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 140,
        letterSpacing: '0.06em',
        color: TOKENS.white,
        textShadow: `0 4px 30px rgba(0,0,0,0.9), 0 0 80px ${accent}66`,
        textAlign: 'center',
        transform: `scale(${scale})`,
      }}>
        DJ GIANNI
      </div>
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 52,
        letterSpacing: '0.1em',
        color: accent,
        textShadow: '0 2px 12px rgba(0,0,0,0.9)',
        marginTop: -8,
        opacity: scale,
      }}>
        {serieName}
      </div>
    </AbsoluteFill>
  );
};
