import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';
import { TOKENS } from '../lib/tokens';

/**
 * VideoBackgroundMilo — Clean & bright video layer for Milø clips.
 *
 * No tunnel gradients or heavy overlays. Let the footage breathe.
 * Both angles get the same clean treatment — no darkening.
 */
export const VideoBackgroundMilo: React.FC<{
  src: string;
  startFromSec?: number;
  angle?: 1 | 2;
}> = ({ src, startFromSec = 0, angle = 1 }) => {
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
    </AbsoluteFill>
  );
};
