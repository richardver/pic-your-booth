import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

/**
 * DeckHits — Overlay-only repeating zoom + flash hits.
 *
 * Does NOT render its own video — it's a pure overlay effect
 * that applies zoom transform and flash to the parent.
 * Wraps children (the video layer) and transforms them.
 */
export const DeckHits: React.FC<{
  genre: Genre;
  hitInterval?: number;
  hitCount?: number;
}> = ({ genre, hitInterval = 28, hitCount = 5 }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  const hitIndex = Math.floor(frame / hitInterval);
  const frameInHit = frame % hitInterval;
  const isActive = hitIndex < hitCount;

  const flashOpacity = (isActive && frameInHit < 4)
    ? interpolate(frameInHit, [0, 1, 4], [0.35, 0.18, 0], { extrapolateRight: 'clamp' })
    : 0;

  return (
    <>
      {flashOpacity > 0 && (
        <AbsoluteFill style={{
          backgroundColor: accent,
          opacity: flashOpacity,
          mixBlendMode: 'overlay' as const,
          pointerEvents: 'none' as const,
          zIndex: 30,
        }} />
      )}
    </>
  );
};
