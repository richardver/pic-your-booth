import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

export const GlitchText: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
  intensity?: number;
}> = ({ children, style = {}, intensity = 3 }) => {
  const frame = useCurrentFrame();

  // Glitch offset oscillates rapidly
  const offset = Math.sin(frame * 2.5) * intensity;
  const offset2 = Math.cos(frame * 3.1) * intensity;

  // Glitch fades out after 20 frames
  const glitchOpacity = interpolate(frame, [0, 15, 20], [0.7, 0.7, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <div style={{ position: 'relative', ...style }}>
      {/* Red layer (left offset) */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: offset,
        color: '#f0654a',
        opacity: glitchOpacity,
        mixBlendMode: 'screen' as const,
        clipPath: 'polygon(0 0, 100% 0, 100% 33%, 0 33%)',
      }}>
        {children}
      </div>
      {/* Cyan layer (right offset) */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: offset2,
        color: '#25f4ee',
        opacity: glitchOpacity,
        mixBlendMode: 'screen' as const,
        clipPath: 'polygon(0 67%, 100% 67%, 100% 100%, 0 100%)',
      }}>
        {children}
      </div>
      {/* Main text */}
      <div style={{ position: 'relative' }}>
        {children}
      </div>
    </div>
  );
};
