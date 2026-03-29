import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

/**
 * DeckHits — Bold repeating visual hits.
 *
 * Wraps ALL content (video + overlays) and applies:
 * - Zoom kick (1.08x snap-back) on each hit
 * - White flash (visible on any footage color)
 * - Brief invert/contrast spike
 *
 * Must wrap the content it affects — not overlay-only.
 */
export const DeckHits: React.FC<{
  children: React.ReactNode;
  genre: Genre;
  hitInterval?: number;
  hitCount?: number;
}> = ({ children, genre, hitInterval = 28, hitCount = 5 }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  const hitIndex = Math.floor(frame / hitInterval);
  const frameInHit = frame % hitInterval;
  const isActive = hitIndex < hitCount;

  // Zoom kick on each hit
  let scale = 1.0;
  if (isActive && frameInHit < 8) {
    scale = interpolate(frameInHit, [0, 2, 8], [1.08, 1.04, 1.0], {
      extrapolateRight: 'clamp',
    });
  }

  // Brightness spike — white flash visible on any color footage
  const flashOpacity = (isActive && frameInHit < 5)
    ? interpolate(frameInHit, [0, 1, 5], [0.45, 0.25, 0], { extrapolateRight: 'clamp' })
    : 0;

  // Contrast spike on hit
  const contrast = (isActive && frameInHit < 6)
    ? interpolate(frameInHit, [0, 2, 6], [1.3, 1.15, 1.0], { extrapolateRight: 'clamp' })
    : 1.0;

  return (
    <AbsoluteFill style={{
      transform: `scale(${scale})`,
      filter: `contrast(${contrast})`,
    }}>
      {children}
      {flashOpacity > 0 && (
        <AbsoluteFill style={{
          backgroundColor: 'white',
          opacity: flashOpacity,
          mixBlendMode: 'overlay' as const,
          pointerEvents: 'none' as const,
          zIndex: 30,
        }} />
      )}
    </AbsoluteFill>
  );
};
