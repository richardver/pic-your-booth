import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

/**
 * SpeedRamp — Progressive dim to black with subtle zoom.
 * "Moment suspended" before end card.
 */
export const SpeedRamp: React.FC<{
  children: React.ReactNode;
  durationFrames: number;
}> = ({ children, durationFrames }) => {
  const frame = useCurrentFrame();

  const brightness = interpolate(frame, [0, durationFrames], [1.0, 0.0], {
    extrapolateRight: 'clamp',
  });

  const scale = interpolate(frame, [0, durationFrames], [1.0, 1.03], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      filter: `brightness(${brightness})`,
      transform: `scale(${scale})`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
