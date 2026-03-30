import React from 'react';
import { Composition } from 'remotion';
import { ReleaseClip } from './ReleaseClip';
import { ReleaseClipGianniAfro } from './ReleaseClipGianniAfro';
import { ReleaseClipGianniUrban } from './ReleaseClipGianniUrban';
import { ReleaseClipMilo } from './ReleaseClipMilo';
import { MiloCleanBright } from './variants/MiloCleanBright';
import { MiloSplitScreen } from './variants/MiloSplitScreen';
import { MiloLumaSilhouette } from './variants/MiloLumaSilhouette';
import { MiloDuotoneFlash } from './variants/MiloDuotoneFlash';
import { MiloRGBGlitch } from './variants/MiloRGBGlitch';
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
const miloDefaults: ReleaseClipProps = {
  genre: 'house',
  djProfile: 'milo',
  djName: 'MILØ',
  serieName: 'TECH HOUSE SESSIONS VOL 1',
  hookText: 'deep in the groove.',
  genreTags: ['Tech House', 'House', 'Deep'],
  videoSrc1: 'footage/angle1.mp4',
  videoSrc2: 'footage/angle2.mp4',
  videoStartSec: 5.8,
  dropTimestamp: 261,
  energyData: [
    0.80, 0.79, 0.89, 0.68, 0.87, 0.82, 0.79, 0.78, 0.27, 0.33,
    0.36, 0.42, 0.46, 0.35, 0.44, 0.38, 0.45, 0.49, 0.43, 0.44,
    0.94, 0.74, 0.84, 0.82, 0.83, 0.90, 0.72, 0.84, 0.80, 0.90,
    0.83, 0.77, 0.89, 0.78, 0.98, 0.86, 0.70, 0.92, 0.98, 0.96,
    0.81, 0.44, 0.97, 0.81, 0.98, 0.81, 0.48, 1.00, 0.77, 0.94,
  ],
  cutPoints: [180, 300, 420],
  coverArtSrc: 'covers/cover.png',
  durationSec: 25,
};

export const RemotionRoot: React.FC = () => {
  return (
    <>
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
    <Composition<ReleaseClipProps>
      id="ReleaseClipGianniAfro"
      component={ReleaseClipGianniAfro}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        genre: 'afro',
        djProfile: 'gianni',
        djName: 'DJ GIANNI',
        serieName: 'AFRO BEATS VOL. 2',
        hookText: 'JE VOELT *DE BASS*\nOF JE VOELT NIKS',
        genreTags: ['Afro Beats', 'Amapiano', 'Afro House'],
        videoSrc1: 'footage/angle1.mp4',
        videoSrc2: 'footage/angle2.mp4',
        videoStartSec: 5.0,
        dropTimestamp: 261,
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
    <Composition<ReleaseClipProps>
      id="ReleaseClipGianniUrban"
      component={ReleaseClipGianniUrban}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        genre: 'urban',
        djProfile: 'gianni',
        djName: 'DJ GIANNI',
        serieName: 'NEDERLANDS URBAN VOL 1',
        hookText: 'NIEMAND STAAT\n*STIL* HIEROP',
        genreTags: ['Nederlands', 'Urban', 'Hits'],
        videoSrc1: 'footage/angle1.mp4',
        videoSrc2: 'footage/angle2.mp4',
        brollSources: [
          'footage/broll/hands-faders.mp4',
          'footage/broll/knob-closeup.mp4',
          'footage/broll/hands-knobs.mp4',
        ],
        videoStartSec: 5.0,
        dropTimestamp: 262,
        energyData: [
          0.80, 0.79, 0.89, 0.68, 0.87, 0.82, 0.79, 0.78, 0.27, 0.33,
          0.36, 0.42, 0.46, 0.35, 0.44, 0.38, 0.45, 0.49, 0.43, 0.44,
          0.94, 0.74, 0.84, 0.82, 0.83, 0.90, 0.72, 0.84, 0.80, 0.90,
          0.83, 0.77, 0.89, 0.78, 0.98, 0.86, 0.70, 0.92, 0.98, 0.96,
          0.81, 0.44, 0.97, 0.81, 0.98, 0.81, 0.48, 1.00, 0.77, 0.94,
        ],
        coverArtSrc: 'covers/cover.png',
        durationSec: 25,
      }}
    />
    <Composition<ReleaseClipProps>
      id="ReleaseClipMilo"
      component={ReleaseClipMilo}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={miloDefaults}
    />
    {/* === MILØ VARIANTS === */}
    <Composition<ReleaseClipProps>
      id="MiloCleanBright"
      component={MiloCleanBright}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={miloDefaults}
    />
    <Composition<ReleaseClipProps>
      id="MiloSplitScreen"
      component={MiloSplitScreen}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={miloDefaults}
    />
    <Composition<ReleaseClipProps>
      id="MiloLumaSilhouette"
      component={MiloLumaSilhouette}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={miloDefaults}
    />
    <Composition<ReleaseClipProps>
      id="MiloDuotoneFlash"
      component={MiloDuotoneFlash}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={miloDefaults}
    />
    <Composition<ReleaseClipProps>
      id="MiloRGBGlitch"
      component={MiloRGBGlitch}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={miloDefaults}
    />
    </>
  );
};
