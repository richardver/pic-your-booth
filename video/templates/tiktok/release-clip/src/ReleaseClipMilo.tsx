import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { ReleaseClipProps } from './lib/types';
import { TOKENS } from './lib/tokens';
import { VideoBackgroundMilo } from './components/VideoBackgroundMilo';
import { EndCard } from './components/EndCard';
import { FilmGrain } from './components/effects/FilmGrain';
import { ColorGradeFilter } from './components/effects/ColorGradeFilter';
import { BlackoutLumaTransition } from './components/effects/BlackoutLumaTransition';
import { LumaRevealText } from './components/effects/LumaRevealText';
import { SpeedRamp } from './components/effects/SpeedRamp';

/**
 * ReleaseClipMilo — DJ Milø release clip composition.
 *
 * Timeline (750 frames at 30fps = 25 seconds):
 *   0-90   (0-3s)    HOOK — LumaRevealText over ColorGraded angle 1 video
 *   90-570 (3-19s)   SET  — Beat-synced angle cuts with BlackoutLumaTransition, ColorGraded
 *   570-630 (19-21s) RAMP — SpeedRamp dim-to-black on last angle
 *   630-750 (21-25s) END CARD — EndCard component (reused)
 *   0-750            FilmGrain at 7%
 *
 * NOTE: VideoBackground internally uses `startFrom={Math.round(startFromSec * 24)}`
 * which assumes 24fps. This is a known bug in the shared component — do not change
 * VideoBackground.tsx as it's shared with Gianni's composition.
 */
export const ReleaseClipMilo: React.FC<ReleaseClipProps> = (props) => {
  const {
    genre, djName, serieName, hookText, genreTags,
    videoSrc1, videoSrc2, videoStartSec, cutPoints = [],
    coverArtSrc, durationSec,
  } = props;

  const fps = 30;
  const totalFrames = durationSec * fps;
  const hookEnd = 90;       // 3s
  const setEnd = 570;       // 19s
  const rampEnd = 630;      // 21s
  // endCard: 630-750

  // Build angle segments from cut points
  // Default cuts if none provided
  const cuts = cutPoints.length > 0 ? cutPoints : [180, 300, 420];

  // Create segments: each segment alternates between angle 1 and angle 2
  const segments: Array<{ from: number; duration: number; src: string }> = [];
  let segStart = hookEnd; // set section starts after hook

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
  // Final segment to end of set section
  if (segStart < setEnd) {
    segments.push({
      from: segStart,
      duration: setEnd - segStart,
      src: segments.length % 2 === 0 ? videoSrc1 : videoSrc2,
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

      {/* === HOOK (0-3s): Big text over color-graded video === */}
      <Sequence from={0} durationInFrames={hookEnd}>
        <ColorGradeFilter>
          <VideoBackgroundMilo src={videoSrc1} startFromSec={videoStartSec} />
        </ColorGradeFilter>
      </Sequence>
      <Sequence from={0} durationInFrames={hookEnd}>
        <LumaRevealText text={hookText} genreTags={genreTags} />
      </Sequence>

      {/* === SET (3-19s): Beat-synced angle segments === */}
      {segments.map((seg, i) => (
        <Sequence key={i} from={seg.from} durationInFrames={seg.duration}>
          <ColorGradeFilter>
            <VideoBackgroundMilo
              src={seg.src}
              startFromSec={videoStartSec + seg.from / fps}
            />
          </ColorGradeFilter>
        </Sequence>
      ))}

      {/* === BLACKOUT TRANSITIONS at each cut point === */}
      {cuts.filter(c => c > hookEnd && c < setEnd).map((cutFrame, i) => (
        <Sequence key={`t-${i}`} from={cutFrame - 2} durationInFrames={7}>
          <BlackoutLumaTransition startFrame={2} />
        </Sequence>
      ))}

      {/* === SPEED RAMP (19-21s): Dim to black === */}
      <Sequence from={setEnd} durationInFrames={rampEnd - setEnd}>
        <SpeedRamp durationFrames={rampEnd - setEnd}>
          <ColorGradeFilter>
            <VideoBackgroundMilo
              src={lastSrc}
              startFromSec={videoStartSec + setEnd / fps}
            />
          </ColorGradeFilter>
        </SpeedRamp>
      </Sequence>

      {/* === END CARD (21-25s) === */}
      <Sequence from={rampEnd} durationInFrames={totalFrames - rampEnd}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      {/* === FILM GRAIN (always, 7%) === */}
      <FilmGrain opacity={0.07} />
    </AbsoluteFill>
  );
};
