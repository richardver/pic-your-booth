import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { TOKENS, SAFE } from '../../lib/tokens';

/**
 * LumaRevealText — Big text with gradient for Milø hook.
 * Cyan-to-violet gradient, 140px Bebas Neue, genre pills below.
 */
export const LumaRevealText: React.FC<{
  text: string;
  genreTags: string[];
}> = ({ text, genreTags }) => {
  const frame = useCurrentFrame();

  const opacity = interpolate(frame, [0, 15, 70, 90], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  const scale = interpolate(frame, [0, 20], [1.02, 1.0], {
    extrapolateRight: 'clamp',
  });

  const pillsOpacity = interpolate(frame, [25, 40], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      opacity,
    }}>
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 140,
        letterSpacing: '0.04em',
        lineHeight: 1,
        textAlign: 'center',
        background: 'linear-gradient(135deg, #34d399 0%, #8b5cf6 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        transform: `scale(${scale})`,
      }}>
        {text.toUpperCase()}
      </div>

      <div style={{
        display: 'flex',
        gap: 12,
        marginTop: 32,
        opacity: pillsOpacity,
      }}>
        {genreTags.map((tag, i) => (
          <div key={i} style={{
            fontFamily: TOKENS.fontBody,
            fontSize: 22,
            fontWeight: 600,
            letterSpacing: '0.08em',
            textTransform: 'uppercase' as const,
            padding: '8px 20px',
            borderRadius: 999,
            background: 'rgba(52,211,153,0.10)',
            color: '#5ae0f0',
            border: '1px solid rgba(52,211,153,0.15)',
          }}>
            {tag}
          </div>
        ))}
      </div>
    </AbsoluteFill>
  );
};
