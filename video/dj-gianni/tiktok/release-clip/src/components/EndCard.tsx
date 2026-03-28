import React from 'react';
import { AbsoluteFill, Img, spring, useCurrentFrame, useVideoConfig, staticFile, interpolate } from 'remotion';
import { TOKENS, GENRE_TOKENS, SAFE } from '../lib/tokens';
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
  const kenBurns = interpolate(frame, [0, 150], [0.95, 1.05], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      background: `radial-gradient(ellipse at 50% 40%, ${accent}33 0%, transparent 55%), ${TOKENS.void}`,
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
    }}>
      {coverArtSrc ? (
        <Img
          src={staticFile(coverArtSrc)}
          style={{
            width: 680,
            height: 680,
            borderRadius: 48,
            border: `3px solid ${accent}55`,
            boxShadow: `0 24px 80px rgba(0,0,0,0.6), 0 0 60px ${accent}33`,
            transform: `scale(${enter * kenBurns})`,
          }}
        />
      ) : (
        <div style={{
          width: 680, height: 680, borderRadius: 48,
          background: `linear-gradient(180deg, ${TOKENS.void} 0%, ${accent}22 100%)`,
          border: `3px solid ${accent}55`,
          display: 'flex', alignItems: 'center', justifyContent: 'center',
          fontFamily: TOKENS.fontDisplay, fontSize: 96, color: TOKENS.white,
          transform: `scale(${enter * kenBurns})`,
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
        marginTop: 40,
        opacity: enter,
      }}>
        {serieName}
      </div>
      <div style={{
        fontFamily: TOKENS.fontBody,
        fontSize: 32,
        color: TOKENS.muted,
        marginTop: 8,
        opacity: enter,
      }}>
        Volledige set op SoundCloud
      </div>
      <div style={{
        fontFamily: TOKENS.fontBody,
        fontSize: 36,
        fontWeight: 700,
        color: accent,
        letterSpacing: '0.1em',
        textTransform: 'uppercase' as const,
        marginTop: 28,
        opacity: enter,
      }}>
        LINK IN BIO &#10148;
      </div>
    </AbsoluteFill>
  );
};
