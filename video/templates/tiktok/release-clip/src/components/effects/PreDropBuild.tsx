import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

/**
 * PreDropBuild — Tension builder before the drop.
 *
 * 60 frames (2s) of escalating effects:
 * - Increasing vignette
 * - Subtle growing shake
 * - Brightness dip (gets darker before the explosion)
 */
export const PreDropBuild: React.FC<{ genre: Genre; children: React.ReactNode }> = ({ genre, children }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  // Shake builds from 0 to 4px
  const shakeIntensity = interpolate(frame, [0, 60], [0, 4], { extrapolateRight: 'clamp' });
  const x = Math.sin(frame * 4.3) * shakeIntensity;
  const y = Math.cos(frame * 5.7) * shakeIntensity;

  // Brightness dips — gets darker before the drop explodes
  const brightness = interpolate(frame, [0, 50, 60], [1.0, 0.8, 0.7], { extrapolateRight: 'clamp' });

  // Vignette builds
  const vignetteOpacity = interpolate(frame, [0, 60], [0.02, 0.15], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill>
      <AbsoluteFill style={{
        transform: `translate(${x}px, ${y}px)`,
        filter: `brightness(${brightness})`,
      }}>
        {children}
      </AbsoluteFill>
      <AbsoluteFill style={{
        background: `radial-gradient(ellipse at 50% 50%, transparent 30%, ${accent} 150%)`,
        opacity: vignetteOpacity,
        pointerEvents: 'none' as const,
      }} />
    </AbsoluteFill>
  );
};
