import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { TOKENS } from '../../lib/tokens';

/**
 * BlackoutLumaTransition — Flash-whip cut transition.
 *
 * Timeline (9 frames):
 *   0-1f:  Quick white/teal flash (energy burst)
 *   2-3f:  Hard black hold (the cut)
 *   4-8f:  Luma fade back in with teal accent glow
 *
 * The brief flash before black sells the "whip" feel —
 * eyes register the flash, then the black resets perception,
 * making the new angle feel fresh.
 */
export const BlackoutLumaTransition: React.FC<{
  startFrame: number;
}> = ({ startFrame }) => {
  const frame = useCurrentFrame();
  const relFrame = frame - startFrame;

  if (relFrame < 0 || relFrame > 8) return null;

  // Phase 1: White/teal flash (frames 0-1)
  if (relFrame < 2) {
    const flashOpacity = interpolate(relFrame, [0, 1], [0.7, 0.4], {
      extrapolateRight: 'clamp',
    });
    return (
      <AbsoluteFill style={{ zIndex: 50 }}>
        <AbsoluteFill style={{
          backgroundColor: TOKENS.void,
          opacity: 0.5,
        }} />
        <AbsoluteFill style={{
          background: 'radial-gradient(ellipse at 50% 50%, rgba(90,224,240,0.6) 0%, rgba(255,255,255,0.3) 40%, transparent 70%)',
          opacity: flashOpacity,
        }} />
      </AbsoluteFill>
    );
  }

  // Phase 2: Hard black (frames 2-3)
  if (relFrame < 4) {
    return (
      <AbsoluteFill style={{
        backgroundColor: TOKENS.void,
        zIndex: 50,
      }} />
    );
  }

  // Phase 3: Luma fade-in with teal accent (frames 4-8)
  const lumaOpacity = interpolate(relFrame, [4, 8], [0.85, 0], {
    extrapolateRight: 'clamp',
  });
  const glowOpacity = interpolate(relFrame, [4, 6, 8], [0.3, 0.15, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ zIndex: 50 }}>
      <AbsoluteFill style={{
        backgroundColor: TOKENS.void,
        opacity: lumaOpacity,
      }} />
      {/* Teal accent glow on fade-in */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 50% 50%, rgba(52,211,153,0.4) 0%, transparent 60%)',
        opacity: glowOpacity,
        mixBlendMode: 'screen',
      }} />
    </AbsoluteFill>
  );
};
