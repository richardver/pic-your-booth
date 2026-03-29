import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { TOKENS, GENRE_TOKENS, SAFE } from '../lib/tokens';
import { Genre } from '../lib/types';
import { SlamIn } from './effects/SlamIn';

/**
 * DropMoment — DJ name on the drop. BIG. LONG.
 *
 * Font size 180 (was 140). Stays 90 frames (was 60) = 3 seconds.
 * Fades out gradually in the last 20 frames.
 */
export const DropMoment: React.FC<{ djName: string; serieName: string; genre: Genre }> = ({ djName, serieName, genre }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  const glowSize = interpolate(frame, [0, 5, 15], [120, 60, 40], {
    extrapolateRight: 'clamp',
  });

  // Fade out in last 20 frames
  const fadeOut = interpolate(frame, [70, 90], [1, 0], {
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
        <div style={{
          fontFamily: TOKENS.fontDisplay,
          fontSize: 180,
          letterSpacing: '0.06em',
          color: TOKENS.white,
          textShadow: `0 4px 30px rgba(0,0,0,0.9), 0 0 ${glowSize}px ${accent}88`,
          textAlign: 'center',
          lineHeight: 1,
        }}>
          {djName}
        </div>
      </SlamIn>
      <SlamIn delay={4}>
        <div style={{
          fontFamily: TOKENS.fontDisplay,
          fontSize: 60,
          letterSpacing: '0.1em',
          color: accent,
          textShadow: '0 2px 12px rgba(0,0,0,0.9)',
          marginTop: 12,
          textAlign: 'center',
        }}>
          {serieName}
        </div>
      </SlamIn>
    </AbsoluteFill>
  );
};
