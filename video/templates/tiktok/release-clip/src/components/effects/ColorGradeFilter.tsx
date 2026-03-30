import React from 'react';
import { AbsoluteFill } from 'remotion';
import { Genre } from '../../lib/types';

/**
 * Genre color-grade presets — each genre gets its own cinematic signature.
 *
 * Properties:
 *   hueRotate  — CSS hue-rotate shift (degrees)
 *   tintRgba   — multiply-blended tint pushed into midtones/shadows
 *   glowRgba   — screen-blended highlight bleed in lower third
 */
const GRADE_PRESETS: Record<Genre, {
  hueRotate: number;
  tintRgba: string;
  glowRgba: string;
}> = {
  // Milø genres
  house:     { hueRotate: -8,  tintRgba: 'rgba(20,80,70,0.18)',  glowRgba: 'rgba(52,211,153,0.14)' },   // teal
  techno:    { hueRotate: -15, tintRgba: 'rgba(20,50,90,0.20)',  glowRgba: 'rgba(56,189,248,0.14)' },   // cold blue
  deep:      { hueRotate: 8,   tintRgba: 'rgba(50,25,80,0.18)',  glowRgba: 'rgba(139,92,246,0.14)' },   // violet
  // Gianni genres
  afro:      { hueRotate: 5,   tintRgba: 'rgba(90,40,20,0.18)',  glowRgba: 'rgba(240,101,74,0.12)' },   // warm coral
  caribbean: { hueRotate: 10,  tintRgba: 'rgba(80,60,15,0.18)',  glowRgba: 'rgba(245,183,49,0.12)' },   // golden
  urban:     { hueRotate: -5,  tintRgba: 'rgba(60,30,80,0.16)',  glowRgba: 'rgba(192,132,252,0.12)' },  // purple haze
};

/**
 * ColorGradeFilter — Genre-specific cinematic color grade.
 * Wraps video content with a unified look per genre.
 */
export const ColorGradeFilter: React.FC<{
  genre?: Genre;
  angle?: 1 | 2;
  children: React.ReactNode;
}> = ({ genre = 'house', angle = 1, children }) => {
  const preset = GRADE_PRESETS[genre];

  // Angle 1: deeper tunnel vignette. Angle 2: lighter so detail reads.
  const brightness = angle === 1 ? 0.72 : 0.78;
  const vignetteOpacity = angle === 1 ? 0.65 : 0.40;

  return (
    <AbsoluteFill>
      {/* Base grade: lift contrast, desaturate, genre-specific hue shift */}
      <AbsoluteFill style={{
        filter: `brightness(${brightness}) contrast(1.45) saturate(0.45) hue-rotate(${preset.hueRotate}deg)`,
      }}>
        {children}
      </AbsoluteFill>
      {/* Genre tint — multiply blend pushes color into midtones/shadows */}
      <AbsoluteFill style={{
        background: preset.tintRgba,
        mixBlendMode: 'multiply',
        pointerEvents: 'none',
      }} />
      {/* Genre highlight bleed in lower third */}
      <AbsoluteFill style={{
        background: `linear-gradient(0deg, ${preset.glowRgba} 0%, ${preset.glowRgba.replace(/[\d.]+\)$/, '0.04)')} 25%, transparent 50%)`,
        mixBlendMode: 'screen',
        pointerEvents: 'none',
      }} />
      {/* Vignette — tunnel effect, stronger on angle 1 */}
      <AbsoluteFill style={{
        background: `radial-gradient(ellipse at 50% 45%, transparent 20%, rgba(5,5,8,${vignetteOpacity}) 100%)`,
        pointerEvents: 'none',
      }} />
    </AbsoluteFill>
  );
};
