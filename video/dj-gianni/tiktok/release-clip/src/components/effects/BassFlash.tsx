import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

export const BassFlash: React.FC<{ genre: Genre }> = ({ genre }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  const opacity = interpolate(frame, [0, 2, 8], [0.7, 0.4, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: accent,
      opacity,
      mixBlendMode: 'overlay' as const,
      zIndex: 50,
      pointerEvents: 'none' as const,
    }} />
  );
};
