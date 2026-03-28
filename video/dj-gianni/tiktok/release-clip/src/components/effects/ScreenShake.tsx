import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

export const ScreenShake: React.FC<{
  children: React.ReactNode;
  intensity?: number;
  durationFrames?: number;
}> = ({ children, intensity = 8, durationFrames = 10 }) => {
  const frame = useCurrentFrame();

  const decay = interpolate(frame, [0, durationFrames], [1, 0], {
    extrapolateRight: 'clamp',
  });

  const x = Math.sin(frame * 5.3) * intensity * decay;
  const y = Math.cos(frame * 7.1) * intensity * decay;

  return (
    <AbsoluteFill style={{
      transform: `translate(${x}px, ${y}px)`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
