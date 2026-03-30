import React from 'react';
import { AbsoluteFill } from 'remotion';
import { SAFE } from '../lib/tokens';
import { Genre } from '../lib/types';
import { TextHook } from './TextHook';

/**
 * HookSection — Hook text only. No genre pills.
 *
 * Genre pills removed — they add clutter without stopping power.
 * The hook text communicates vibe through word choice + accent color.
 *
 * Genre accent color is applied to *starred* words via TextHook:
 * - Afro: coral (#f0654a)
 * - Caribbean: gold (#f5b731)
 * - Urban NL: purple (#c084fc)
 */
export const HookSection: React.FC<{
  hookText: string;
  genreTags: string[];
  genre: Genre;
}> = ({ hookText, genre }) => {
  return (
    <AbsoluteFill style={{
      padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
      zIndex: 10,
      display: 'flex',
      flexDirection: 'column',
      justifyContent: 'center',
      alignItems: 'center',
    }}>
      <TextHook text={hookText} genre={genre} />
    </AbsoluteFill>
  );
};
