import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

export const LightLeak: React.FC<{ genre: Genre }> = ({ genre }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  const position = interpolate(frame, [0, 30], [-50, 150], {
    extrapolateRight: 'clamp',
  });

  const opacity = interpolate(frame, [0, 8, 22, 30], [0, 0.3, 0.3, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      background: `linear-gradient(90deg, transparent ${position - 30}%, ${accent} ${position}%, transparent ${position + 30}%)`,
      opacity,
      mixBlendMode: 'screen' as const,
      pointerEvents: 'none' as const,
      zIndex: 30,
    }} />
  );
};
