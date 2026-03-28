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
        hookText: 'STUUR JE PLAYLIST\nIK MAAK ER DIT VAN',
        genreTags: ['Afro Beats', 'Amapiano', 'Afro House'],
        videoSrc: 'footage/dj-gianni-set-recording.mov',
        videoStartSec: 10.0,
        dropTimestamp: 540,
        coverArtSrc: 'covers/afro-mixtape-cover.png',
        durationSec: 25,
      }}
    />
  );
};
