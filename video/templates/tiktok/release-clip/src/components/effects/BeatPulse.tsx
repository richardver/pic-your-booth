import React from 'react';
import { AbsoluteFill, useCurrentFrame, interpolate } from 'remotion';

/**
 * BeatPulse — Video breathes with the music.
 *
 * Cranked up: 8% scale pulse + 20% brightness swing.
 * Visible on every beat, not just a subtle hint.
 */

// Energy data (0.5s windows, from audio analyzer, clip starts at 10s)
const ENERGY = [
  0.80, 0.79, 0.89, 0.68, 0.87, 0.82, 0.79, 0.78, 0.27, 0.33,
  0.36, 0.42, 0.46, 0.35, 0.44, 0.38, 0.45, 0.49, 0.43, 0.44,
  0.94, 0.74, 0.84, 0.82, 0.83, 0.90, 0.72, 0.84, 0.80, 0.90,
  0.83, 0.77, 0.89, 0.78, 0.98, 0.86, 0.70, 0.92, 0.98, 0.96,
  0.81, 0.44, 0.97, 0.81, 0.98, 0.81, 0.48, 1.00, 0.77, 0.94,
];

export const BeatPulse: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();

  // 15 frames per energy window (0.5s at 30fps)
  const windowIndex = Math.floor(frame / 15);
  const energy = ENERGY[Math.min(windowIndex, ENERGY.length - 1)] || 0.5;
  const nextEnergy = ENERGY[Math.min(windowIndex + 1, ENERGY.length - 1)] || 0.5;

  // Position within current window (0-1)
  const pos = (frame % 15) / 15;

  // Smooth energy transition
  const smoothEnergy = energy + (nextEnergy - energy) * pos;

  // Fast sine pulse for "bounce on beat" feel (~110 BPM = ~3.6Hz)
  const beatBounce = Math.sin(frame * 0.38) * 0.5 + 0.5; // 0-1 oscillation

  // Scale: 1.0 on silence, up to 1.08 on loudest beats
  const scale = 1.0 + smoothEnergy * 0.08 * beatBounce;

  // Brightness: darker on quiet, brighter on loud
  const brightness = 0.85 + smoothEnergy * 0.20;

  // Contrast boost on high energy
  const contrast = 1.0 + smoothEnergy * 0.08;

  return (
    <AbsoluteFill style={{
      transform: `scale(${scale})`,
      filter: `brightness(${brightness}) contrast(${contrast})`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
