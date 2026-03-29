import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';

/**
 * PostDropDecay — Aftershock effects after the drop.
 *
 * 45 frames (1.5s) of decaying effects:
 * - Aftershock shake (starts at 6px, decays to 0)
 * - Brightness returns to normal
 * - Slight zoom settles
 */
export const PostDropDecay: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();

  // Aftershock shake decays
  const shakeIntensity = interpolate(frame, [0, 45], [6, 0], { extrapolateRight: 'clamp' });
  const x = Math.sin(frame * 3.7) * shakeIntensity;
  const y = Math.cos(frame * 4.9) * shakeIntensity;

  // Scale settles from 1.03 to 1.0
  const scale = interpolate(frame, [0, 45], [1.03, 1.0], { extrapolateRight: 'clamp' });

  // Brightness recovers
  const brightness = interpolate(frame, [0, 30], [1.1, 1.0], { extrapolateRight: 'clamp' });

  return (
    <AbsoluteFill style={{
      transform: `translate(${x}px, ${y}px) scale(${scale})`,
      filter: `brightness(${brightness})`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
