import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { ReleaseClipProps } from '../lib/types';
import { TOKENS } from '../lib/tokens';
import { VideoBackgroundMilo } from '../components/VideoBackgroundMilo';
import { EndCard } from '../components/EndCard';
import { FilmGrain } from '../components/effects/FilmGrain';
import { LumaRevealText } from '../components/effects/LumaRevealText';
import { SpeedRamp } from '../components/effects/SpeedRamp';

/**
 * Variant 1: CLEAN & BRIGHT
 *
 * Let the footage breathe. Near-original colors with only a light
 * teal tint and gentle contrast boost. No tunnel gradients, no vignette.
 * Soft bottom fade for text readability only.
 */
export const MiloCleanBright: React.FC<ReleaseClipProps> = (props) => {
  const {
    genre, djName, serieName, hookText,
    videoSrc1, videoSrc2, videoStartSec, cutPoints = [],
    coverArtSrc, durationSec,
  } = props;

  const fps = 30;
  const totalFrames = durationSec * fps;
  const hookEnd = 150;
  const setEnd = 570;
  const rampEnd = 630;

  const cuts = cutPoints.length > 0 ? cutPoints : [180, 300, 420];

  const segments: Array<{ from: number; duration: number; src: string }> = [];
  let segStart = hookEnd;
  for (let i = 0; i < cuts.length; i++) {
    const cutFrame = Math.min(cuts[i], setEnd);
    if (cutFrame <= segStart) continue;
    segments.push({
      from: segStart,
      duration: cutFrame - segStart,
      src: i % 2 === 0 ? videoSrc1 : videoSrc2,
    });
    segStart = cutFrame;
  }
  if (segStart < setEnd) {
    segments.push({
      from: segStart,
      duration: setEnd - segStart,
      src: segments.length % 2 === 0 ? videoSrc1 : videoSrc2,
    });
  }
  const lastSrc = segments.length > 0 ? segments[segments.length - 1].src : videoSrc1;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>
      {videoSrc1 && (
        <Audio src={staticFile(videoSrc1)} startFrom={Math.round(videoStartSec * fps)} />
      )}

      {/* HOOK: Bright footage with light teal wash */}
      <Sequence from={0} durationInFrames={hookEnd}>
        <CleanGrade>
          <VideoBackgroundMilo src={videoSrc1} startFromSec={videoStartSec} angle={1} />
        </CleanGrade>
        {/* Soft bottom fade for text only */}
        <AbsoluteFill style={{
          background: 'linear-gradient(180deg, transparent 50%, rgba(5,5,8,0.4) 100%)',
          pointerEvents: 'none',
        }} />
      </Sequence>
      <Sequence from={0} durationInFrames={hookEnd}>
        <LumaRevealText text={hookText} djName={djName} />
      </Sequence>

      {/* SET: Clean footage, hard cuts */}
      {segments.map((seg, i) => (
        <Sequence key={i} from={seg.from} durationInFrames={seg.duration}>
          <CleanGrade>
            <VideoBackgroundMilo
              src={seg.src}
              startFromSec={videoStartSec + seg.from / fps}
              angle={i % 2 === 0 ? 1 : 2}
            />
          </CleanGrade>
        </Sequence>
      ))}

      {/* SPEED RAMP */}
      <Sequence from={setEnd} durationInFrames={rampEnd - setEnd}>
        <SpeedRamp durationFrames={rampEnd - setEnd}>
          <CleanGrade>
            <VideoBackgroundMilo src={lastSrc} startFromSec={videoStartSec + setEnd / fps} />
          </CleanGrade>
        </SpeedRamp>
      </Sequence>

      {/* END CARD */}
      <Sequence from={rampEnd} durationInFrames={totalFrames - rampEnd}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      <FilmGrain opacity={0.04} />
    </AbsoluteFill>
  );
};

/** Minimal grade: slight teal tint, gentle contrast, full brightness */
const CleanGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill>
    <AbsoluteFill style={{
      filter: 'brightness(0.95) contrast(1.12) saturate(0.85)',
    }}>
      {children}
    </AbsoluteFill>
    {/* Very light teal wash */}
    <AbsoluteFill style={{
      background: 'rgba(52,211,153,0.06)',
      mixBlendMode: 'overlay',
      pointerEvents: 'none',
    }} />
  </AbsoluteFill>
);
