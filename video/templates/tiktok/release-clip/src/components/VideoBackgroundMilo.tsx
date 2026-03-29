import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';
import { TOKENS } from '../lib/tokens';

/**
 * VideoBackgroundMilo — Dark, desaturated video layer for Milø clips.
 *
 * Differences from VideoBackground (Gianni):
 * - Uses 30fps for startFrom (not 24fps)
 * - No brightness/saturation boost filter
 * - Darker gradient overlay for underground feel
 */
export const VideoBackgroundMilo: React.FC<{ src: string; startFromSec?: number }> = ({ src, startFromSec = 0 }) => {
  return (
    <AbsoluteFill>
      {src ? (
        <OffthreadVideo
          src={staticFile(src)}
          startFrom={Math.round(startFromSec * 30)}
          volume={0}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
          }}
        />
      ) : (
        <AbsoluteFill style={{ backgroundColor: TOKENS.void }} />
      )}
      {/* Darker gradient for underground feel */}
      <AbsoluteFill
        style={{
          background: 'linear-gradient(180deg, rgba(5,5,8,0.15) 0%, rgba(5,5,8,0.25) 40%, rgba(5,5,8,0.70) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
