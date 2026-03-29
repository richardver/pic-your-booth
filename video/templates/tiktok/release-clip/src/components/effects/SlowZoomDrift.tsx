import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

/**
 * SlowZoomDrift — Subtle zoom over time to kill static feeling.
 * Used during build-up to create movement from a single camera angle.
 */
export const SlowZoomDrift: React.FC<{
  children: React.ReactNode;
  fromScale?: number;
  toScale?: number;
}> = ({ children, fromScale = 1.0, toScale = 1.06 }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, 150], [fromScale, toScale], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ transform: `scale(${scale})` }}>
      {children}
    </AbsoluteFill>
  );
};
