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

  const p = Math.max(0, progress);
  const scale = 1.3 - 0.3 * p;
  const opacity = p;

  return (
    <div style={{
      transform: `scale(${scale})`,
      opacity,
      transformOrigin: 'center center',
    }}>
      {children}
    </div>
  );
};
