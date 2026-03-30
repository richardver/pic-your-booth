import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate, spring, useVideoConfig } from 'remotion';
import { TOKENS, SAFE } from '../../lib/tokens';

/**
 * LumaRevealText — Premium hook for Milø.
 *
 * Sequence (150 frames / 5 seconds at 30fps):
 *   0-15f:    "MILØ" scales in large with neon glow
 *   25-40f:   "deep in the" fades in small above main word
 *   35-48f:   "GROOVE" slams in huge with spring + neon glow
 *   120-150f: Everything fades out
 */
export const LumaRevealText: React.FC<{
  text: string;
  djName: string;
}> = ({ text, djName }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Split tagline into prefix + last word
  const words = text.replace('.', '').trim().split(/\s+/);
  const lastWord = words[words.length - 1].toUpperCase();
  const prefix = words.slice(0, -1).join(' ').toLowerCase();

  // --- DJ NAME ("MILØ") ---
  const nameOpacity = interpolate(frame, [0, 12, 70, 90], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const nameScale = interpolate(
    spring({ fps, frame, config: { damping: 14, stiffness: 160, mass: 0.8 } }),
    [0, 1],
    [1.1, 1.0],
  );

  // --- PREFIX ("deep in the") ---
  const prefixOpacity = interpolate(frame, [25, 38, 120, 145], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // --- MAIN WORD ("GROOVE") slam ---
  const slamProgress = spring({
    fps,
    frame: Math.max(0, frame - 35),
    config: { damping: 10, stiffness: 200, mass: 0.7 },
  });
  const mainScale = interpolate(slamProgress, [0, 1], [1.6, 1.0]);
  const mainOpacity = interpolate(frame, [35, 42, 120, 145], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

  // --- NEON GLOW (pulsing) ---
  const glowPulse = interpolate(
    Math.sin(frame * 0.2),
    [-1, 1],
    [0.6, 1.0],
  );
  const glowSize = 20 + glowPulse * 15;
  const glowCyan = `rgba(52,211,153,${0.5 * glowPulse})`;
  const glowViolet = `rgba(139,92,246,${0.3 * glowPulse})`;

  return (
    <AbsoluteFill style={{
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
    }}>

      {/* DJ Name: "MILØ" */}
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 200,
        letterSpacing: '0.06em',
        lineHeight: 0.9,
        textAlign: 'center',
        background: 'linear-gradient(135deg, #34d399 0%, #5ae0f0 40%, #8b5cf6 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        transform: `scale(${nameScale})`,
        opacity: nameOpacity,
        filter: `drop-shadow(0 0 ${glowSize}px ${glowCyan}) drop-shadow(0 0 ${glowSize * 2}px ${glowViolet})`,
        marginBottom: 48,
      }}>
        {djName}
      </div>

      {/* Prefix: "deep in the" */}
      <div style={{
        fontFamily: TOKENS.fontBody,
        fontSize: 48,
        fontWeight: 300,
        fontStyle: 'italic',
        letterSpacing: '0.12em',
        color: 'rgba(237,237,240,0.6)',
        opacity: prefixOpacity,
        marginBottom: 8,
      }}>
        {prefix}
      </div>

      {/* Main word: "GROOVE" with neon glow */}
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 180,
        letterSpacing: '0.06em',
        lineHeight: 0.9,
        textAlign: 'center',
        background: 'linear-gradient(135deg, #34d399 0%, #5ae0f0 40%, #8b5cf6 100%)',
        WebkitBackgroundClip: 'text',
        WebkitTextFillColor: 'transparent',
        backgroundClip: 'text',
        transform: `scale(${mainScale})`,
        opacity: mainOpacity,
        filter: `drop-shadow(0 0 ${glowSize}px ${glowCyan}) drop-shadow(0 0 ${glowSize * 2}px ${glowViolet})`,
      }}>
        {lastWord}
      </div>

    </AbsoluteFill>
  );
};
