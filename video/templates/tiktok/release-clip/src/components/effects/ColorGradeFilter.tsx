import React from 'react';
import { AbsoluteFill } from 'remotion';

/**
 * ColorGradeFilter — Uniform dark/cyan color grade for Milø.
 * Applied to video content so both angles look identical.
 */
export const ColorGradeFilter: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{
        filter: 'brightness(0.85) contrast(1.2) saturate(0.7)',
      }}>
        {children}
      </AbsoluteFill>
      {/* Cyan underlight tint in shadows */}
      <AbsoluteFill style={{
        background: 'linear-gradient(0deg, rgba(52,211,153,0.08) 0%, transparent 40%)',
        mixBlendMode: 'screen',
        pointerEvents: 'none',
      }} />
      {/* Crush blacks overlay */}
      <AbsoluteFill style={{
        background: 'radial-gradient(ellipse at 50% 50%, transparent 30%, rgba(5,5,8,0.3) 100%)',
        pointerEvents: 'none',
      }} />
    </AbsoluteFill>
  );
};
