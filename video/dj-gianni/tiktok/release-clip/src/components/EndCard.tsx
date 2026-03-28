import React from 'react';
import { AbsoluteFill, Img, spring, useCurrentFrame, useVideoConfig, staticFile } from 'remotion';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';
import { EQBar } from './EQBar';
import { HexBadge } from './HexBadge';

export const EndCard: React.FC<{
  serieName: string;
  genre: Genre;
  coverArtSrc: string;
}> = ({ serieName, genre, coverArtSrc }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent } = GENRE_TOKENS[genre];
  const enter = spring({ fps, frame, config: { damping: 15, stiffness: 120 } });

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      background: `radial-gradient(ellipse at 50% 55%, ${accent}33 0%, transparent 55%), ${TOKENS.void}`,
    }}>
      <div style={{ position: 'absolute', top: 120, right: 48 }}>
        <HexBadge genre={genre} />
      </div>
      {coverArtSrc ? (
        <Img
          src={staticFile(coverArtSrc)}
          style={{
            width: 540,
            height: 540,
            borderRadius: 48,
            border: `3px solid ${accent}55`,
            boxShadow: `0 20px 60px rgba(0,0,0,0.6), 0 0 40px ${accent}33`,
            transform: `scale(${enter})`,
          }}
        />
      ) : (
        <div style={{
          width: 540, height: 540, borderRadius: 48,
          background: `linear-gradient(180deg, ${TOKENS.void} 0%, ${accent}22 100%)`,
          border: `3px solid ${accent}55`,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: TOKENS.fontDisplay, fontSize: 80, color: TOKENS.white,
          transform: `scale(${enter})`,
        }}>
          DJ GIANNI
        </div>
      )}
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 80,
        letterSpacing: '0.06em',
        color: TOKENS.white,
        textAlign: 'center',
        marginTop: 48,
        opacity: enter,
      }}>
        {serieName}
      </div>
      <div style={{ fontSize: 40, color: TOKENS.muted, marginTop: 12, opacity: enter }}>
        Volledige set op SoundCloud
      </div>
      <div style={{
        fontSize: 40, fontWeight: 700, color: accent,
        letterSpacing: '0.1em', textTransform: 'uppercase' as const,
        marginTop: 32, display: 'flex', alignItems: 'center', gap: 16, opacity: enter,
      }}>
        LINK IN BIO &#10148;
      </div>
      <div style={{ marginTop: 48 }}>
        <EQBar genre={genre} height={60} />
      </div>
    </AbsoluteFill>
  );
};
