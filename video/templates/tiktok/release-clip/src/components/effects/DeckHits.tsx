import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

/**
 * DeckHits — Repeating zoom + flash hits during vibe section.
 *
 * Simulates the video "reacting" to the DJ working the deck.
 * Bold zoom punches (1.12x) repeating every ~30 frames (1s)
 * with a light flash on each hit.
 */
export const DeckHits: React.FC<{
  children: React.ReactNode;
  genre: Genre;
  hitInterval?: number;
  hitCount?: number;
}> = ({ children, genre, hitInterval = 28, hitCount = 5 }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  // Which hit are we on?
  const hitIndex = Math.floor(frame / hitInterval);
  const frameInHit = frame % hitInterval;

  // Only apply effects for the defined number of hits
  const isActive = hitIndex < hitCount;

  // Zoom punch on each hit — snaps to 1.12x then settles back
  let scale = 1.0;
  if (isActive && frameInHit < 10) {
    scale = interpolate(frameInHit, [0, 2, 10], [1.12, 1.08, 1.0], {
      extrapolateRight: 'clamp',
    });
  }

  // Brightness spike on each hit
  let brightness = 1.0;
  if (isActive && frameInHit < 6) {
    brightness = interpolate(frameInHit, [0, 1, 6], [1.25, 1.15, 1.0], {
      extrapolateRight: 'clamp',
    });
  }

  // Flash opacity on each hit
  const flashOpacity = (isActive && frameInHit < 4)
    ? interpolate(frameInHit, [0, 1, 4], [0.3, 0.15, 0], { extrapolateRight: 'clamp' })
    : 0;

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{
        transform: `scale(${scale})`,
        filter: `brightness(${brightness})`,
      }}>
        {children}
      </AbsoluteFill>
      {flashOpacity > 0 && (
        <AbsoluteFill style={{
          backgroundColor: accent,
          opacity: flashOpacity,
          mixBlendMode: 'overlay' as const,
          pointerEvents: 'none' as const,
          zIndex: 30,
        }} />
      )}
    </AbsoluteFill>
  );
};
