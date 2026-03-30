import React from 'react';
import {
  AbsoluteFill, Audio, Sequence, staticFile,
  useCurrentFrame, interpolate,
} from 'remotion';
import { ReleaseClipProps } from '../lib/types';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { VideoBackgroundMilo } from '../components/VideoBackgroundMilo';
import { EndCard } from '../components/EndCard';
import { FilmGrain } from '../components/effects/FilmGrain';
import { LumaRevealText } from '../components/effects/LumaRevealText';
import { SpeedRamp } from '../components/effects/SpeedRamp';

/**
 * Variant 4: DUOTONE FLASH (recommended)
 *
 * Bright, near-original footage with a light teal grade.
 * At each cut point: 3-frame cyan duotone flash → hard cut to next angle.
 * The flash creates rhythmic visual punctuation without darkening the clip.
 */
export const MiloDuotoneFlash: React.FC<ReleaseClipProps> = (props) => {
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

  const segments: Array<{ from: number; duration: number; src: string; angle: 1 | 2 }> = [];
  let segStart = hookEnd;
  for (let i = 0; i < cuts.length; i++) {
    const cutFrame = Math.min(cuts[i], setEnd);
    if (cutFrame <= segStart) continue;
    const angle: 1 | 2 = i % 2 === 0 ? 1 : 2;
    segments.push({ from: segStart, duration: cutFrame - segStart, src: angle === 1 ? videoSrc1 : videoSrc2, angle });
    segStart = cutFrame;
  }
  if (segStart < setEnd) {
    const angle: 1 | 2 = segments.length % 2 === 0 ? 1 : 2;
    segments.push({ from: segStart, duration: setEnd - segStart, src: angle === 1 ? videoSrc1 : videoSrc2, angle });
  }
  const lastSrc = segments.length > 0 ? segments[segments.length - 1].src : videoSrc1;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>
      {videoSrc1 && (
        <Audio src={staticFile(videoSrc1)} startFrom={Math.round(videoStartSec * fps)} />
      )}

      {/* HOOK */}
      <Sequence from={0} durationInFrames={hookEnd}>
        <BrightGrade>
          <VideoBackgroundMilo src={videoSrc1} startFromSec={videoStartSec} angle={1} />
        </BrightGrade>
        <AbsoluteFill style={{
          background: 'linear-gradient(180deg, transparent 50%, rgba(5,5,8,0.35) 100%)',
          pointerEvents: 'none',
        }} />
      </Sequence>
      <Sequence from={0} durationInFrames={hookEnd}>
        <LumaRevealText text={hookText} djName={djName} />
      </Sequence>

      {/* SET */}
      {segments.map((seg, i) => (
        <Sequence key={i} from={seg.from} durationInFrames={seg.duration}>
          <BrightGrade>
            <VideoBackgroundMilo
              src={seg.src}
              startFromSec={videoStartSec + seg.from / fps}
              angle={seg.angle}
            />
          </BrightGrade>
        </Sequence>
      ))}

      {/* DUOTONE FLASHES at cut points */}
      {cuts.filter(c => c > hookEnd && c < setEnd).map((cutFrame, i) => (
        <Sequence key={`df-${i}`} from={cutFrame - 1} durationInFrames={5}>
          <DuotoneFlash accent={GENRE_TOKENS[genre]?.accent || '#34d399'} />
        </Sequence>
      ))}

      {/* SPEED RAMP */}
      <Sequence from={setEnd} durationInFrames={rampEnd - setEnd}>
        <SpeedRamp durationFrames={rampEnd - setEnd}>
          <BrightGrade>
            <VideoBackgroundMilo src={lastSrc} startFromSec={videoStartSec + setEnd / fps} />
          </BrightGrade>
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

/** Bright, near-original grade with light teal tint */
const BrightGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill>
    <AbsoluteFill style={{
      filter: 'brightness(0.95) contrast(1.15) saturate(0.82)',
    }}>
      {children}
    </AbsoluteFill>
    <AbsoluteFill style={{
      background: 'rgba(52,211,153,0.06)',
      mixBlendMode: 'overlay',
      pointerEvents: 'none',
    }} />
  </AbsoluteFill>
);

/** 5-frame duotone flash: cyan blast → fade out */
const DuotoneFlash: React.FC<{ accent: string }> = ({ accent }) => {
  const frame = useCurrentFrame();

  // Frame 0: white flash
  // Frame 1-2: strong duotone (cyan over everything)
  // Frame 3-4: fade out
  const flashOpacity = interpolate(frame, [0, 1, 2, 4], [0.85, 0.7, 0.4, 0], {
    extrapolateRight: 'clamp',
  });

  const whiteFlash = interpolate(frame, [0, 1], [0.6, 0], {
    extrapolateRight: 'clamp',
  });

  return (
    <AbsoluteFill style={{ zIndex: 50, pointerEvents: 'none' }}>
      {/* White flash on first frame */}
      <AbsoluteFill style={{
        backgroundColor: '#ffffff',
        opacity: whiteFlash,
      }} />
      {/* Duotone wash */}
      <AbsoluteFill style={{
        background: `linear-gradient(180deg, ${accent} 0%, #8b5cf6 100%)`,
        opacity: flashOpacity,
        mixBlendMode: 'color',
      }} />
      {/* Brightness push */}
      <AbsoluteFill style={{
        backgroundColor: accent,
        opacity: flashOpacity * 0.3,
        mixBlendMode: 'screen',
      }} />
    </AbsoluteFill>
  );
};
