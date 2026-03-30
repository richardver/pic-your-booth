import React from 'react';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';
import { SlamIn } from './effects/SlamIn';
import { loadFont } from '@remotion/google-fonts/Anton';

const anton = loadFont();

/**
 * TextHookUrban — Urban NL hook text with gradient accent + Anton font.
 *
 * Differences from TextHook:
 * - Anton font (bolder, more impact than Bebas Neue)
 * - Gradient on accent words (purple → pink for urban)
 * - Subtle text stroke for readability over video
 * - Tighter letter spacing (urban style)
 * - Faster slam (delay 4 instead of 6)
 *
 * Supports *word* syntax — accent words get the gradient treatment.
 */
export const TextHookUrban: React.FC<{ text: string; genre: Genre }> = ({ text, genre }) => {
  const { accent } = GENRE_TOKENS[genre];
  const lines = text.split('\n');

  // Accent word: bigger, solid bright color, strong shadow for readability
  // No gradient-on-text (hard to read over video) — instead solid accent + scale up
  const accentStyle: React.CSSProperties = {
    color: '#e0b0ff',
    fontSize: '1.35em',
    textShadow: `0 0 40px ${accent}aa, 0 4px 30px rgba(0,0,0,0.95), 0 0 80px ${accent}44`,
  };

  const renderLine = (line: string) => {
    const parts = line.split(/(\*[^*]+\*)/);
    return parts.map((part, j) => {
      if (part.startsWith('*') && part.endsWith('*')) {
        return (
          <span key={j} style={accentStyle}>
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
        <SlamIn key={i} delay={i * 4}>
          <div style={{
            fontFamily: anton.fontFamily,
            fontSize: 134,
            letterSpacing: '0.02em',
            color: TOKENS.white,
            textShadow: `0 4px 30px rgba(0,0,0,0.95), 0 0 60px rgba(0,0,0,0.5)`,
            WebkitTextStroke: '1px rgba(255,255,255,0.08)',
            lineHeight: 1.0,
            textAlign: 'center',
            textTransform: 'uppercase' as const,
          }}>
            {renderLine(line)}
          </div>
        </SlamIn>
      ))}
    </div>
  );
};
