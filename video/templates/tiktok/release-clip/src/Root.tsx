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
 *   - videoSrc1 + videoSrc2 + videoStartSec (from audio analyzer)
 *   - coverArtSrc (from images/<dj>/mixtape/)
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
        djProfile: 'gianni',
        djName: 'DJ GIANNI',
        serieName: 'AFRO BEATS VOL. 2',
        hookText: 'POV: *DIT* IS HOE\nJOUW FEEST KLINKT',
        genreTags: ['Afro Beats', 'Amapiano', 'Afro House'],
        videoSrc1: 'footage/dj-gianni-set-recording.mov',
        videoSrc2: 'footage/dj-gianni-set-recording.mov',
        videoStartSec: 10.0,
        dropTimestamp: 540,
        energyData: [
          0.80, 0.79, 0.89, 0.68, 0.87, 0.82, 0.79, 0.78, 0.27, 0.33,
          0.36, 0.42, 0.46, 0.35, 0.44, 0.38, 0.45, 0.49, 0.43, 0.44,
          0.94, 0.74, 0.84, 0.82, 0.83, 0.90, 0.72, 0.84, 0.80, 0.90,
          0.83, 0.77, 0.89, 0.78, 0.98, 0.86, 0.70, 0.92, 0.98, 0.96,
          0.81, 0.44, 0.97, 0.81, 0.98, 0.81, 0.48, 1.00, 0.77, 0.94,
        ],
        coverArtSrc: 'covers/afro-mixtape-cover.png',
        durationSec: 25,
      }}
    />
  );
};
