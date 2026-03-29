import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../../lib/tokens';
import { Genre } from '../../lib/types';

const PARTICLES = [
  { x: -120, y: -180, size: 6 },
  { x: 150, y: -140, size: 4 },
  { x: -180, y: 60, size: 5 },
  { x: 140, y: 120, size: 7 },
  { x: -60, y: -200, size: 3 },
  { x: 200, y: -40, size: 5 },
  { x: -140, y: 160, size: 4 },
  { x: 80, y: 180, size: 6 },
  { x: -200, y: -80, size: 3 },
  { x: 160, y: -160, size: 4 },
];

export const ParticleBurst: React.FC<{ genre: Genre }> = ({ genre }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  return (
    <AbsoluteFill style={{ pointerEvents: 'none' as const, zIndex: 40 }}>
      {PARTICLES.map((p, i) => {
        const progress = interpolate(frame, [0, 18], [0, 1], { extrapolateRight: 'clamp' });
        const opacity = interpolate(frame, [0, 5, 18], [0, 1, 0], { extrapolateRight: 'clamp' });
        const x = 540 + p.x * progress;
        const y = 960 + p.y * progress;
        const scale = 1 + progress * 2;

        return (
          <div key={i} style={{
            position: 'absolute',
            left: x,
            top: y,
            width: p.size,
            height: p.size,
            borderRadius: '50%',
            backgroundColor: accent,
            opacity,
            transform: `scale(${scale})`,
          }} />
        );
      })}
    </AbsoluteFill>
  );
};
