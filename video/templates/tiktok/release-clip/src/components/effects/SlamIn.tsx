import React from 'react';
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';

export const SlamIn: React.FC<{
  children: React.ReactNode;
  delay?: number;
}> = ({ children, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const progress = spring({
    fps,
    frame: frame - delay,
    config: { damping: 14, stiffness: 180 },
  });

  const scale = 2.5 - 1.5 * Math.max(0, progress);
  const opacity = Math.max(0, progress);
  const rotation = (1 - Math.max(0, progress)) * -3;

  return (
    <div style={{
      transform: `scale(${scale}) rotate(${rotation}deg)`,
      opacity,
      transformOrigin: 'left center',
    }}>
      {children}
    </div>
  );
};
