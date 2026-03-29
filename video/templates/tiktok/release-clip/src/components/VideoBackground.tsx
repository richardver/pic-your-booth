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
          volume={0}
          style={{
            width: '100%',
            height: '100%',
            objectFit: 'cover',
            filter: 'contrast(1.15) saturate(1.1) brightness(0.95)',
          }}
        />
      ) : (
        <AbsoluteFill style={{ backgroundColor: TOKENS.void }} />
      )}
      <AbsoluteFill
        style={{
          background: 'linear-gradient(180deg, rgba(5,5,8,0.15) 0%, rgba(5,5,8,0.5) 50%, rgba(5,5,8,0.85) 100%)',
        }}
      />
      <AbsoluteFill
        style={{
          background: 'linear-gradient(180deg, rgba(0,20,30,0.15) 0%, transparent 40%, rgba(0,20,30,0.2) 100%)',
          mixBlendMode: 'multiply' as const,
          pointerEvents: 'none' as const,
        }}
      />
    </AbsoluteFill>
  );
};
