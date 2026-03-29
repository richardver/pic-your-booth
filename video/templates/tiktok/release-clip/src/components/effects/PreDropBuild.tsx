import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

/**
 * PreDropBuild — Pure overlay. Darkening vignette + brightness dip.
 * Applied on top of the continuous video layer.
 */
export const PreDropBuild: React.FC<{ genre: Genre; children?: React.ReactNode }> = ({ genre }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  const brightness = interpolate(frame, [0, 50, 60], [1.0, 0.8, 0.7], { extrapolateRight: 'clamp' });
  const vignetteOpacity = interpolate(frame, [0, 60], [0.02, 0.15], { extrapolateRight: 'clamp' });

  return (
    <>
      {/* Brightness dip overlay */}
      <AbsoluteFill style={{
        backgroundColor: 'black',
        opacity: 1 - brightness,
        pointerEvents: 'none' as const,
        zIndex: 3,
      }} />
      {/* Vignette */}
      <AbsoluteFill style={{
        background: `radial-gradient(ellipse at 50% 50%, transparent 30%, ${accent} 150%)`,
        opacity: vignetteOpacity,
        pointerEvents: 'none' as const,
        zIndex: 3,
      }} />
    </>
  );
};
