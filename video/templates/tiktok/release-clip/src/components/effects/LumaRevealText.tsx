import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';
import { TOKENS, SAFE } from '../../lib/tokens';

/**
 * LumaRevealText — Premium hook text for Milø.
 *
 * Animation sequence:
 * 0-12f:  Thin cyan line sweeps across (editorial reveal)
 * 8-20f:  "DEEP" slams in (scale 1.5→1.0, spring)
 * 16-28f: "IN THE" slams in
 * 24-36f: "GROOVE" slams in
 * 40-55f: Genre pills fade in below the line
 * 70-90f: Everything fades out
 */
export const LumaRevealText: React.FC<{
  text: string;
  genreTags: string[];
}> = ({ text, genreTags }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Split text into words for staggered slam
  const words = text.toUpperCase().replace('.', '').trim().split(/\s+/);

  // Overall fade out at end
  const fadeOut = interpolate(frame, [70, 90], [1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // --- EDITORIAL LINE ---
  // Thin cyan line sweeps from left to right
  const lineWidth = interpolate(frame, [0, 12], [0, 100], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const lineOpacity = interpolate(frame, [0, 4, 60, 75], [0, 0.8, 0.8, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // --- WORD SLAMS ---
  // Each word slams in with 8-frame stagger
  const wordAnimations = words.map((_, i) => {
    const wordStart = 8 + i * 8;
    const slamScale = spring({
      fps,
      frame: Math.max(0, frame - wordStart),
      config: { damping: 12, stiffness: 180, mass: 0.8 },
    });
    const wordOpacity = interpolate(frame, [wordStart, wordStart + 4], [0, 1], {
      extrapolateLeft: 'clamp',
      extrapolateRight: 'clamp',
    });
    return {
      scale: interpolate(slamScale, [0, 1], [1.5, 1.0]),
      opacity: wordOpacity,
    };
  });

  // --- GENRE PILLS ---
  const pillsOpacity = interpolate(frame, [40, 55], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // --- GLOW PULSE (subtle breathing) ---
  const glowIntensity = interpolate(
    Math.sin(frame * 0.15),
    [-1, 1],
    [0.15, 0.35],
  );

  return (
    <AbsoluteFill style={{
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
      opacity: fadeOut,
    }}>

      {/* Editorial line */}
      <div style={{
        width: `${lineWidth}%`,
        height: 1,
        background: 'linear-gradient(90deg, transparent 0%, #34d399 30%, #8b5cf6 70%, transparent 100%)',
        opacity: lineOpacity,
        marginBottom: 32,
        transition: 'none',
      }} />

      {/* Word-by-word slam */}
      <div style={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        gap: 0,
      }}>
        {words.map((word, i) => (
          <div key={i} style={{
            fontFamily: TOKENS.fontDisplay,
            fontSize: i === 0 || i === words.length - 1 ? 160 : 80,
            letterSpacing: '0.06em',
            lineHeight: 1.0,
            textAlign: 'center',
            background: 'linear-gradient(135deg, #34d399 0%, #8b5cf6 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            transform: `scale(${wordAnimations[i].scale})`,
            opacity: wordAnimations[i].opacity,
            filter: `drop-shadow(0 0 ${40 * glowIntensity}px rgba(52,211,153,${glowIntensity}))`,
          }}>
            {word}
          </div>
        ))}
      </div>

      {/* Editorial line (below text) */}
      <div style={{
        width: `${lineWidth}%`,
        height: 1,
        background: 'linear-gradient(90deg, transparent 0%, #34d399 30%, #8b5cf6 70%, transparent 100%)',
        opacity: lineOpacity * 0.5,
        marginTop: 32,
      }} />

      {/* Genre pills (below bottom line) */}
      <div style={{
        display: 'flex',
        gap: 12,
        marginTop: 24,
        opacity: pillsOpacity,
      }}>
        {genreTags.map((tag, i) => (
          <div key={i} style={{
            fontFamily: TOKENS.fontBody,
            fontSize: 20,
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
