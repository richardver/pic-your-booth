import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

/**
 * SlowPan — Subtle horizontal pan to create visual variety.
 * Used during vibe section to differentiate from build-up.
 */
export const SlowPan: React.FC<{
  children: React.ReactNode;
  fromX?: number;
  toX?: number;
}> = ({ children, fromX = 0, toX = -30 }) => {
  const frame = useCurrentFrame();
  const x = interpolate(frame, [0, 240], [fromX, toX], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      transform: `translateX(${x}px) scale(1.04)`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
