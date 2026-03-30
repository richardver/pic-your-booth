import React from 'react';
import {
  AbsoluteFill, Audio, Sequence, staticFile,
  useCurrentFrame, interpolate,
} from 'remotion';
import { ReleaseClipProps } from '../lib/types';
import { TOKENS } from '../lib/tokens';
import { VideoBackgroundMilo } from '../components/VideoBackgroundMilo';
import { EndCard } from '../components/EndCard';
import { FilmGrain } from '../components/effects/FilmGrain';
import { LumaRevealText } from '../components/effects/LumaRevealText';
import { SpeedRamp } from '../components/effects/SpeedRamp';

/**
 * Variant 3: LUMA SILHOUETTE
 *
 * High-contrast footage layered over an animated cyan/violet gradient.
 * The gradient bleeds through dark areas via screen blend, creating
 * a silhouette effect where Milø's figure is lit by moving color.
 */
export const MiloLumaSilhouette: React.FC<ReleaseClipProps> = (props) => {
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

      {/* HOOK */}
      <Sequence from={0} durationInFrames={hookEnd}>
        <SilhouetteGrade>
          <VideoBackgroundMilo src={videoSrc1} startFromSec={videoStartSec} angle={1} />
        </SilhouetteGrade>
      </Sequence>
      <Sequence from={0} durationInFrames={hookEnd}>
        <LumaRevealText text={hookText} djName={djName} />
      </Sequence>

      {/* SET */}
      {segments.map((seg, i) => (
        <Sequence key={i} from={seg.from} durationInFrames={seg.duration}>
          <SilhouetteGrade>
            <VideoBackgroundMilo
              src={seg.src}
              startFromSec={videoStartSec + seg.from / fps}
              angle={i % 2 === 0 ? 1 : 2}
            />
          </SilhouetteGrade>
        </Sequence>
      ))}

      {/* SPEED RAMP */}
      <Sequence from={setEnd} durationInFrames={rampEnd - setEnd}>
        <SpeedRamp durationFrames={rampEnd - setEnd}>
          <SilhouetteGrade>
            <VideoBackgroundMilo src={lastSrc} startFromSec={videoStartSec + setEnd / fps} />
          </SilhouetteGrade>
        </SpeedRamp>
      </Sequence>

      {/* END CARD */}
      <Sequence from={rampEnd} durationInFrames={totalFrames - rampEnd}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      <FilmGrain opacity={0.05} />
    </AbsoluteFill>
  );
};

/** Animated gradient background + high-contrast footage via screen blend */
const SilhouetteGrade: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();

  // Slowly rotating gradient position
  const gradAngle = interpolate(frame, [0, 750], [135, 315], {
    extrapolateRight: 'clamp',
  });
  const shift = Math.sin(frame * 0.03) * 10;

  return (
    <AbsoluteFill>
      {/* Animated cyan/violet gradient background */}
      <AbsoluteFill style={{
        background: `linear-gradient(${gradAngle}deg,
          #0f172a 0%,
          rgba(52,211,153,0.5) ${30 + shift}%,
          rgba(139,92,246,0.4) ${60 + shift}%,
          #0f172a 100%)`,
      }} />

      {/* High-contrast footage — screen blend lets gradient bleed through darks */}
      <AbsoluteFill style={{
        filter: 'brightness(1.3) contrast(1.8) saturate(0.3)',
        mixBlendMode: 'screen',
      }}>
        {children}
      </AbsoluteFill>

      {/* Extra luminosity push to keep highlights visible */}
      <AbsoluteFill style={{
        filter: 'brightness(0.7) contrast(1.6) saturate(0.2)',
        mixBlendMode: 'luminosity',
        opacity: 0.3,
      }}>
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
