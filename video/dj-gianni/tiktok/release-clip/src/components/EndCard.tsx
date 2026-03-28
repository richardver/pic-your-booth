import React from 'react';
import { AbsoluteFill, Img, spring, useCurrentFrame, useVideoConfig, staticFile } from 'remotion';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

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
      background: `radial-gradient(ellipse at 50% 45%, ${accent}33 0%, transparent 55%), ${TOKENS.void}`,
      padding: '160px 110px 280px 40px',
    }}>
      {coverArtSrc ? (
        <Img
          src={staticFile(coverArtSrc)}
          style={{
            width: 480,
            height: 480,
            borderRadius: 48,
            border: `3px solid ${accent}55`,
            boxShadow: `0 20px 60px rgba(0,0,0,0.6), 0 0 40px ${accent}33`,
            transform: `scale(${enter})`,
          }}
        />
      ) : (
        <div style={{
          width: 480, height: 480, borderRadius: 48,
          background: `linear-gradient(180deg, ${TOKENS.void} 0%, ${accent}22 100%)`,
          border: `3px solid ${accent}55`,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: TOKENS.fontDisplay, fontSize: 72, color: TOKENS.white,
          transform: `scale(${enter})`,
        }}>
          DJ GIANNI
        </div>
      )}
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 72,
        letterSpacing: '0.06em',
        color: TOKENS.white,
        textAlign: 'center',
        marginTop: 40,
        opacity: enter,
      }}>
        {serieName}
      </div>
      <div style={{ fontSize: 36, color: TOKENS.muted, marginTop: 8, opacity: enter }}>
        Volledige set op SoundCloud
      </div>
      <div style={{
        fontSize: 36, fontWeight: 700, color: accent,
        letterSpacing: '0.1em', textTransform: 'uppercase' as const,
        marginTop: 28, opacity: enter,
      }}>
        LINK IN BIO &#10148;
      </div>
    </AbsoluteFill>
  );
};
