import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { ReleaseClipProps } from './lib/types';
import { TOKENS } from './lib/tokens';
import { VideoBackgroundMilo } from './components/VideoBackgroundMilo';
import { EndCard } from './components/EndCard';
import { FilmGrain } from './components/effects/FilmGrain';
import { LumaRevealText } from './components/effects/LumaRevealText';
import { SpeedRamp } from './components/effects/SpeedRamp';

/**
 * ReleaseClipMilo — DJ Milø release clip composition.
 *
 * Visual approach: CLEAN & BRIGHT — near-original colors with light teal tint,
 * gentle contrast, no heavy dark grades. Let the footage breathe.
 *
 * Timeline (750 frames at 30fps = 25 seconds):
 *   0-150  (0-5s)    HOOK — MILØ name + tagline over clean bright angle 1 video
 *   120-570 (4-19s)  SET  — Beat-synced angle cuts, clean bright grade
 *   570-630 (19-21s) RAMP — SpeedRamp dim-to-black on last angle
 *   630-750 (21-25s) END CARD — EndCard component (reused)
 *   0-750            FilmGrain at 4%
 *
 * NOTE: VideoBackground internally uses `startFrom={Math.round(startFromSec * 24)}`
 * which assumes 24fps. This is a known bug in the shared component — do not change
 * VideoBackground.tsx as it's shared with Gianni's composition.
 */
export const ReleaseClipMilo: React.FC<ReleaseClipProps> = (props) => {
  const {
    genre, djName, serieName, hookText,
    videoSrc1, videoSrc2, videoStartSec, cutPoints = [],
    coverArtSrc, durationSec,
  } = props;

  const fps = 30;
  const totalFrames = durationSec * fps;
  const hookEnd = 150;      // 5s — breathing room for name + tagline
  const setEnd = 570;       // 19s
  const rampEnd = 630;      // 21s
  // endCard: 630-750

  // Build angle segments from cut points
  // Default cuts if none provided
  const cuts = cutPoints.length > 0 ? cutPoints : [180, 300, 420];

  // Create segments: each segment alternates between angle 1 and angle 2
  const segments: Array<{ from: number; duration: number; src: string; angle: 1 | 2 }> = [];
  let segStart = hookEnd; // set section starts after hook

  for (let i = 0; i < cuts.length; i++) {
    const cutFrame = Math.min(cuts[i], setEnd);
    if (cutFrame <= segStart) continue;
    const angle: 1 | 2 = i % 2 === 0 ? 1 : 2;
    segments.push({
      from: segStart,
      duration: cutFrame - segStart,
      src: angle === 1 ? videoSrc1 : videoSrc2,
      angle,
    });
    segStart = cutFrame;
  }
  // Final segment to end of set section
  if (segStart < setEnd) {
    const angle: 1 | 2 = segments.length % 2 === 0 ? 1 : 2;
    segments.push({
      from: segStart,
      duration: setEnd - segStart,
      src: angle === 1 ? videoSrc1 : videoSrc2,
      angle,
    });
  }

  // Last angle used (for speed ramp section)
  const lastSrc = segments.length > 0 ? segments[segments.length - 1].src : videoSrc1;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* === AUDIO from angle 1 === */}
      {videoSrc1 && (
        <Audio
          src={staticFile(videoSrc1)}
          startFrom={Math.round(videoStartSec * fps)}
        />
      )}

      {/* === HOOK (0-5s): Big text over clean bright video (angle 1) === */}
      <Sequence from={0} durationInFrames={hookEnd}>
        <CleanGrade>
          <VideoBackgroundMilo src={videoSrc1} startFromSec={videoStartSec} angle={1} />
        </CleanGrade>
        {/* Soft bottom fade for text readability only */}
        <AbsoluteFill style={{
          background: 'linear-gradient(180deg, transparent 50%, rgba(5,5,8,0.4) 100%)',
          pointerEvents: 'none',
        }} />
      </Sequence>
      <Sequence from={0} durationInFrames={hookEnd}>
        <LumaRevealText text={hookText} djName={djName} />
      </Sequence>

      {/* === SET (3-19s): Beat-synced angle segments, clean bright === */}
      {segments.map((seg, i) => (
        <Sequence key={i} from={seg.from} durationInFrames={seg.duration}>
          <CleanGrade>
            <VideoBackgroundMilo
              src={seg.src}
              startFromSec={videoStartSec + seg.from / fps}
              angle={seg.angle}
            />
          </CleanGrade>
        </Sequence>
      ))}

      {/* Hard cuts only — clean and precise */}

      {/* === SPEED RAMP (19-21s): Dim to black === */}
      <Sequence from={setEnd} durationInFrames={rampEnd - setEnd}>
        <SpeedRamp durationFrames={rampEnd - setEnd}>
          <CleanGrade>
            <VideoBackgroundMilo
              src={lastSrc}
              startFromSec={videoStartSec + setEnd / fps}
            />
          </CleanGrade>
        </SpeedRamp>
      </Sequence>

      {/* === END CARD (21-25s) === */}
      <Sequence from={rampEnd} durationInFrames={totalFrames - rampEnd}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      {/* === FILM GRAIN (always, 4% — subtle, clean default) === */}
      <FilmGrain opacity={0.04} />
    </AbsoluteFill>
  );
};

/** Clean & Bright grade: light teal tint, gentle contrast, near-original colors */
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
