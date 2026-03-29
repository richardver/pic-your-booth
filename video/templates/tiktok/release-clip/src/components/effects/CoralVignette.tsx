import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

export const CoralVignette: React.FC<{ genre: Genre }> = ({ genre }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];
  const intensity = interpolate(frame, [0, 150], [0.02, 0.12], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      background: `radial-gradient(ellipse at 50% 50%, transparent 40%, ${accent} 150%)`,
      opacity: intensity,
      pointerEvents: 'none' as const,
      zIndex: 5,
    }} />
  );
};
