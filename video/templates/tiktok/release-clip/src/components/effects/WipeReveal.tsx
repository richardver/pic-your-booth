import React from 'react';
import { interpolate, useCurrentFrame } from 'remotion';

export const WipeReveal: React.FC<{
  children: React.ReactNode;
  delay?: number;
}> = ({ children, delay = 0 }) => {
  const frame = useCurrentFrame();
  const reveal = interpolate(frame - delay, [0, 12], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ clipPath: `inset(0 ${100 - reveal}% 0 0)` }}>
      {children}
    </div>
  );
};
