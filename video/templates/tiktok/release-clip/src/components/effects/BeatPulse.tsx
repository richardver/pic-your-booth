import React from 'react';
import { AbsoluteFill, useCurrentFrame } from 'remotion';
import { DJProfile } from '../../lib/types';

const DEFAULT_ENERGY = new Array(50).fill(0.5);

interface BeatPulseProps {
  children: React.ReactNode;
  energyData?: number[];
  djProfile?: DJProfile;
}

export const BeatPulse: React.FC<BeatPulseProps> = ({
  children,
  energyData = DEFAULT_ENERGY,
  djProfile = 'gianni',
}) => {
  const frame = useCurrentFrame();

  const scaleMult = djProfile === 'milo' ? 0.06 : 0.08;
  const brightnessMult = djProfile === 'milo' ? 0.15 : 0.20;

  const windowIndex = Math.floor(frame / 15);
  const e = energyData[Math.min(windowIndex, energyData.length - 1)] || 0.5;
  const next = energyData[Math.min(windowIndex + 1, energyData.length - 1)] || 0.5;
  const pos = (frame % 15) / 15;
  const smooth = e + (next - e) * pos;

  const beatBounce = Math.sin(frame * 0.38) * 0.5 + 0.5;
  const scale = 1.0 + smooth * scaleMult * beatBounce;
  const brightness = (1.0 - brightnessMult / 2) + smooth * brightnessMult;
  const contrast = 1.0 + smooth * 0.08;

  return (
    <AbsoluteFill style={{
      transform: `scale(${scale})`,
      filter: `brightness(${brightness}) contrast(${contrast})`,
    }}>
      {children}
    </AbsoluteFill>
  );
};
