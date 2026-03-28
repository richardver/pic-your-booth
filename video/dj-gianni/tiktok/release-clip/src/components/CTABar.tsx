import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { GENRE_TOKENS, TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const CTABar: React.FC<{ genre: Genre }> = ({ genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent } = GENRE_TOKENS[genre];
  const enter = spring({ fps, frame, config: { damping: 200 } });
  const y = interpolate(enter, [0, 1], [100, 0]);

  return (
    <div style={{
      position: 'absolute',
      bottom: 160,
      left: 40,
      right: 180,
      background: `${accent}26`,
      backdropFilter: 'blur(12px)',
      border: `2px solid ${accent}44`,
      borderRadius: 28,
      padding: '28px 40px',
      display: 'flex',
      alignItems: 'center',
      gap: 20,
      transform: `translateY(${y}px)`,
      opacity: enter,
    }}>
      <div>
        <div style={{ fontSize: 32, fontWeight: 700, color: TOKENS.white }}>
          Volledige set op SoundCloud
        </div>
        <div style={{ fontSize: 24, color: TOKENS.muted, marginTop: 4 }}>
          Link in bio
        </div>
      </div>
      <div style={{ marginLeft: 'auto', fontSize: 48, color: accent }}>&#10148;</div>
    </div>
  );
};
