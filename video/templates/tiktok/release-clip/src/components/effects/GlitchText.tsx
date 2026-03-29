import React from 'react';
import { useCurrentFrame, interpolate } from 'remotion';

export const GlitchText: React.FC<{
  children: React.ReactNode;
  style?: React.CSSProperties;
  intensity?: number;
}> = ({ children, style = {}, intensity = 5 }) => {
  const frame = useCurrentFrame();

  // Rapid oscillation for glitch feel
  const offset1 = Math.sin(frame * 3.7) * intensity;
  const offset2 = Math.cos(frame * 4.3) * intensity;
  const offsetY = Math.sin(frame * 5.1) * (intensity * 0.4);

  // Glitch stays visible longer, fades after 25 frames
  const glitchOpacity = interpolate(frame, [0, 20, 28], [0.85, 0.85, 0], {
    extrapolateRight: 'clamp',
  });

  // Random horizontal slice shift for that "broken screen" feel
  const sliceShift = Math.sin(frame * 8.7) * intensity * 1.5;
  const sliceVisible = frame % 3 === 0 ? 0.5 : 0; // flickers every 3rd frame

  return (
    <div style={{ position: 'relative', ...style }}>
      {/* Red layer — top third */}
      <div style={{
        position: 'absolute',
        top: offsetY,
        left: offset1,
        color: '#f0654a',
        opacity: glitchOpacity,
        mixBlendMode: 'screen' as const,
        clipPath: 'polygon(0 0, 100% 0, 100% 35%, 0 35%)',
      }}>
        {children}
      </div>
      {/* Cyan layer — bottom third */}
      <div style={{
        position: 'absolute',
        top: -offsetY,
        left: offset2,
        color: '#25f4ee',
        opacity: glitchOpacity,
        mixBlendMode: 'screen' as const,
        clipPath: 'polygon(0 65%, 100% 65%, 100% 100%, 0 100%)',
      }}>
        {children}
      </div>
      {/* Horizontal slice glitch — random slice shifts */}
      <div style={{
        position: 'absolute',
        top: 0,
        left: sliceShift,
        opacity: sliceVisible,
        clipPath: 'polygon(0 42%, 100% 42%, 100% 58%, 0 58%)',
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
