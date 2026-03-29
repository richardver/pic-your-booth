import React from 'react';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';
import { GlitchText } from './effects/GlitchText';
import { SlamIn } from './effects/SlamIn';

/**
 * TextHook — The scroll-stopping hook text.
 *
 * Supports accent color on specific words using *word* syntax:
 *   "STUUR JE PLAYLIST\nIK MAAK ER *DIT* VAN"
 *   → "DIT" renders in genre accent color
 *
 * Strategist hook rules:
 *   - First line must stop the scroll
 *   - Accent color on the curiosity/key word only
 *   - Bebas Neue, centered, maximum size
 */
export const TextHook: React.FC<{ text: string; genre: Genre }> = ({ text, genre }) => {
  const { accent } = GENRE_TOKENS[genre];
  const lines = text.split('\n');

  const renderLine = (line: string) => {
    // Split on *word* to find accent words
    const parts = line.split(/(\*[^*]+\*)/);
    return parts.map((part, j) => {
      if (part.startsWith('*') && part.endsWith('*')) {
        // Accent word
        return (
          <span key={j} style={{ color: accent }}>
            {part.slice(1, -1)}
          </span>
        );
      }
      return <span key={j}>{part}</span>;
    });
  };

  return (
    <GlitchText>
      {lines.map((line, i) => (
        <SlamIn key={i} delay={i * 6}>
          <div style={{
            fontFamily: TOKENS.fontDisplay,
            fontSize: 96,
            letterSpacing: '0.04em',
            color: TOKENS.white,
            textShadow: '0 4px 24px rgba(0,0,0,0.9)',
            lineHeight: 1.0,
            textAlign: 'center',
          }}>
            {renderLine(line)}
          </div>
        </SlamIn>
      ))}
    </GlitchText>
  );
};
