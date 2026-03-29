import React from 'react';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';
import { SlamIn } from './effects/SlamIn';

/**
 * TextHook — Clean, readable hook text. No glitch effects.
 *
 * The GlitchText RGB split created ghost copies of words floating
 * around the screen. Removed. The SlamIn + accent color is enough.
 * Bass flash + zoom punch provide the visual energy.
 *
 * Supports *word* syntax for accent color.
 */
export const TextHook: React.FC<{ text: string; genre: Genre }> = ({ text, genre }) => {
  const { accent } = GENRE_TOKENS[genre];
  const lines = text.split('\n');

  const renderLine = (line: string) => {
    const parts = line.split(/(\*[^*]+\*)/);
    return parts.map((part, j) => {
      if (part.startsWith('*') && part.endsWith('*')) {
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
    <div>
      {lines.map((line, i) => (
        <SlamIn key={i} delay={i * 6}>
          <div style={{
            fontFamily: TOKENS.fontDisplay,
            fontSize: 96,
            letterSpacing: '0.04em',
            color: TOKENS.white,
            textShadow: '0 4px 24px rgba(0,0,0,0.9)',
            lineHeight: 1.05,
            textAlign: 'center',
          }}>
            {renderLine(line)}
          </div>
        </SlamIn>
      ))}
    </div>
  );
};
