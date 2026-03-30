import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';
import { TOKENS } from '../lib/tokens';

/**
 * VideoBackgroundMilo — Dark, desaturated video layer for Milø clips.
 *
 * angle 1: Heavy tunnel gradient (dark edges, visible center)
 * angle 2: Lighter overlay so it reads brighter on the cut
 */
export const VideoBackgroundMilo: React.FC<{
  src: string;
  startFromSec?: number;
  angle?: 1 | 2;
}> = ({ src, startFromSec = 0, angle = 1 }) => {
  // Angle 1: heavy tunnel — dark top + bottom, clear center
  // Angle 2: lighter — just enough mood without crushing detail
  const gradient = angle === 1
    ? 'linear-gradient(180deg, rgba(5,5,8,0.50) 0%, rgba(5,5,8,0.08) 25%, rgba(5,5,8,0.08) 55%, rgba(5,5,8,0.80) 100%)'
    : 'linear-gradient(180deg, rgba(5,5,8,0.22) 0%, rgba(5,5,8,0.06) 30%, rgba(5,5,8,0.10) 60%, rgba(5,5,8,0.50) 100%)';

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
      <AbsoluteFill style={{ background: gradient }} />
    </AbsoluteFill>
  );
};
