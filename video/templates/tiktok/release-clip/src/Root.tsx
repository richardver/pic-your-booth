import React from 'react';
import { Composition } from 'remotion';
import { ReleaseClip } from './ReleaseClip';
import { ReleaseClipProps } from './lib/types';

/**
 * Release Clip Template — shared across all DJs.
 *
 * The defaultProps below are for preview/development.
 * Production renders pass props via CLI: --props='{ ... }'
 *
 * Each DJ provides:
 *   - genre + accent colors (from dj-promoter agent)
 *   - hookText + sub-hook (from strategist agent)
 *   - videoSrc + videoStartSec (from audio analyzer)
 *   - coverArtSrc (from docs/images/<dj>/mixtape/)
 *
 * Output goes to: video/output/<dj>/tiktok/release-clip/<serie-name>/
 */
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
        djName: 'DJ GIANNI',
        serieName: 'AFRO BEATS VOL. 2',
        hookText: 'POV: *DIT* IS HOE\nJOUW FEEST KLINKT',
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
