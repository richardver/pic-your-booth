import React from 'react';
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { GENRE_TOKENS, TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

/**
 * CTABar — Booking CTA, not SoundCloud link.
 *
 * Strategist marketing psychology:
 * - Scarcity: "Populaire data gaan snel"
 * - Direct CTA: "Check beschikbaarheid"
 * - Personal: "Boek DJ Gianni" not generic "link in bio"
 */
export const CTABar: React.FC<{ genre: Genre; djName?: string }> = ({ genre, djName = 'DJ GIANNI' }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent } = GENRE_TOKENS[genre];
  const enter = spring({ fps, frame, config: { damping: 200 } });
  const y = interpolate(enter, [0, 1], [80, 0]);

  return (
    <div style={{
      background: `${accent}30`,
      backdropFilter: 'blur(16px)',
      border: `2px solid ${accent}55`,
      borderRadius: 28,
      padding: '24px 36px',
      display: 'flex',
      alignItems: 'center',
      gap: 20,
      transform: `translateY(${y}px)`,
      opacity: enter,
    }}>
      <div>
        <div style={{ fontFamily: TOKENS.fontDisplay, fontSize: 36, letterSpacing: '0.04em', color: TOKENS.white }}>
          BOEK {djName}
        </div>
        <div style={{ fontFamily: TOKENS.fontBody, fontSize: 22, color: accent, marginTop: 2 }}>
          Populaire data gaan snel
        </div>
      </div>
      <div style={{
        marginLeft: 'auto',
        fontFamily: TOKENS.fontBody,
        fontSize: 20,
        fontWeight: 700,
        color: TOKENS.void,
        background: accent,
        padding: '10px 20px',
        borderRadius: 14,
      }}>
        Check &#10148;
      </div>
    </div>
  );
};
