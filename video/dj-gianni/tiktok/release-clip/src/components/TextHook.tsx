import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const TextHook: React.FC<{ text: string; genre: Genre }> = ({ text, genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ fps, frame, config: { damping: 200 } });
  const exit = spring({ fps, frame: frame - 60, config: { damping: 200 } });
  const opacity = enter - exit;

  return (
    <div style={{
      fontSize: 62,
      fontWeight: 700,
      fontFamily: TOKENS.fontBody,
      color: TOKENS.white,
      textShadow: '0 4px 20px rgba(0,0,0,0.9)',
      lineHeight: 1.2,
      maxWidth: 800,
      opacity: Math.max(0, opacity),
      transform: `translateY(${interpolate(enter, [0, 1], [20, 0])}px)`,
    }}>
      {text}
    </div>
  );
};
