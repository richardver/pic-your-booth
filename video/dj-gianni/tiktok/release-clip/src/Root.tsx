import React from 'react';
import { Composition } from 'remotion';
import { ReleaseClip } from './ReleaseClip';
import { ReleaseClipProps } from './lib/types';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition<ReleaseClipProps>
      id="ReleaseClip"
      component={ReleaseClip}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        genre: 'afro',
        serieName: 'AFRO BEATS VOL. 2',
        hookText: 'Nieuwe Afro Beats mix is LIVE',
        genreTags: ['Afro Beats', 'Amapiano', 'Afro House'],
        videoSrc: '',
        dropTimestamp: 240,
        coverArtSrc: 'covers/afro-mixtape-cover.png',
        durationSec: 25,
      }}
    />
  );
};
