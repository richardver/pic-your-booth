import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { TOKENS, GENRE_TOKENS, SAFE } from '../lib/tokens';
import { Genre } from '../lib/types';
import { SlamIn } from './effects/SlamIn';
import { loadFont } from '@remotion/google-fonts/Anton';

const anton = loadFont();

/**
 * DropMomentUrban — DJ name slam with gradient glow.
 *
 * Anton font, gradient text on the DJ name, accent glow burst.
 */
export const DropMomentUrban: React.FC<{ djName: string; serieName: string; genre: Genre }> = ({ djName, serieName, genre }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  const glowSize = interpolate(frame, [0, 5, 15], [140, 70, 45], {
    extrapolateRight: 'clamp',
  });

  const fadeOut = interpolate(frame, [80, 100], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
      opacity: fadeOut,
    }}>
      <SlamIn>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            fontFamily: anton.fontFamily,
            fontSize: 196,
            letterSpacing: '0.03em',
            lineHeight: 1,
            background: `linear-gradient(180deg, #ffffff 0%, ${accent} 100%)`,
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            filter: `drop-shadow(0 4px 30px rgba(0,0,0,0.9)) drop-shadow(0 0 ${glowSize}px ${accent}88)`,
          }}>
            {djName}
          </div>
          <div style={{
            fontFamily: anton.fontFamily,
            fontSize: 68,
            letterSpacing: '0.08em',
            color: accent,
            textShadow: '0 2px 16px rgba(0,0,0,0.9)',
            marginTop: 16,
          }}>
            {serieName}
          </div>
        </div>
      </SlamIn>
    </AbsoluteFill>
  );
};
