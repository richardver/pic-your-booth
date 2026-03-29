import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';
import { TOKENS } from '../../lib/tokens';

/**
 * BlackoutLumaTransition — 2 frames black, then 3 frames luma fade.
 * Darks hold, lights transition first. Underground club visual feel.
 */
export const BlackoutLumaTransition: React.FC<{
  startFrame: number;
}> = ({ startFrame }) => {
  const frame = useCurrentFrame();
  const relFrame = frame - startFrame;

  if (relFrame < 0 || relFrame > 5) return null;

  if (relFrame < 2) {
    return (
      <AbsoluteFill style={{
        backgroundColor: TOKENS.void,
        zIndex: 50,
      }} />
    );
  }

  const lumaOpacity = interpolate(relFrame, [2, 5], [0.9, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      backgroundColor: TOKENS.void,
      opacity: lumaOpacity,
      mixBlendMode: 'multiply',
      zIndex: 50,
    }} />
  );
};
