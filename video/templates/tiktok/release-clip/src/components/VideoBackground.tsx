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
            filter: 'contrast(1.12) saturate(1.08) brightness(1.0)',
          }}
        />
      ) : (
        <AbsoluteFill style={{ backgroundColor: TOKENS.void }} />
      )}
      {/* Lighter gradient — just enough for text readability, not a dark wash */}
      <AbsoluteFill
        style={{
          background: 'linear-gradient(180deg, rgba(5,5,8,0.08) 0%, rgba(5,5,8,0.25) 50%, rgba(5,5,8,0.55) 100%)',
        }}
      />
    </AbsoluteFill>
  );
};
