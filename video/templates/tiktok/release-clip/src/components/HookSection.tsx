import React from 'react';
import { AbsoluteFill, interpolate, useCurrentFrame } from 'remotion';
import { SAFE } from '../lib/tokens';
import { Genre } from '../lib/types';
import { TextHook } from './TextHook';
import { GenrePills } from './GenrePills';

/**
 * HookSection — Hook text + genre pills. Nothing else.
 *
 * The SoundCloud info goes in the TikTok caption, not on screen.
 * Less is more. Hook stops the scroll, pills give context.
 */
export const HookSection: React.FC<{
  hookText: string;
  genreTags: string[];
  genre: Genre;
}> = ({ hookText, genreTags, genre }) => {
  const frame = useCurrentFrame();

  const pillsOpacity = interpolate(frame, [35, 45], [0, 1], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });

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

      <div style={{ opacity: pillsOpacity, marginTop: 32 }}>
        <GenrePills tags={genreTags} genre={genre} />
      </div>
    </AbsoluteFill>
  );
};
