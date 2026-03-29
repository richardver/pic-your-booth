import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

/**
 * PostDropDecay — Pure overlay. Brightness recovery after the drop.
 */
export const PostDropDecay: React.FC<{ children?: React.ReactNode }> = () => {
  const frame = useCurrentFrame();

  // Brightness settles from bright back to normal
  const brightOverlay = interpolate(frame, [0, 30], [0.08, 0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      backgroundColor: 'white',
      opacity: brightOverlay,
      mixBlendMode: 'overlay' as const,
      pointerEvents: 'none' as const,
      zIndex: 3,
    }} />
  );
};
