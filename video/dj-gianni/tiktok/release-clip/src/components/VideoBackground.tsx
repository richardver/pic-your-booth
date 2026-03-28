import React from 'react';
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';
import { TOKENS } from '../lib/tokens';

export const VideoBackground: React.FC<{ src: string; startFromSec?: number }> = ({ src, startFromSec = 0 }) => {
  return (
    <AbsoluteFill>
      {src ? (
        <OffthreadVideo
          src={staticFile(src)}
          startFrom={Math.round(startFromSec * 24)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      ) : (
        <AbsoluteFill style={{ backgroundColor: TOKENS.void }} />
      )}
      <AbsoluteFill
        style={{
          background: 'linear-gradient(180deg, rgba(5,5,8,0.15) 0%, rgba(5,5,8,0.5) 50%, rgba(5,5,8,0.85) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
