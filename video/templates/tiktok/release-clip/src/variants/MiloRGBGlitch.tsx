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
 * Variant 5: RGB GLITCH
 *
 * Bright footage with RGB channel separation + horizontal scan lines
 * at each beat cut. Techy, modern, fits the tech house aesthetic.
 * Between cuts: clean bright footage. At cuts: 6-frame glitch burst.
 */
export const MiloRGBGlitch: React.FC<ReleaseClipProps> = (props) => {
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

      {/* RGB GLITCH at cut points */}
      {cuts.filter(c => c > hookEnd && c < setEnd).map((cutFrame, i) => (
        <Sequence key={`gl-${i}`} from={cutFrame - 2} durationInFrames={8}>
          <RGBGlitchEffect />
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

/** Bright grade — same as DuotoneFlash variant */
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

/** 8-frame RGB glitch burst: channel split + scan lines + noise */
const RGBGlitchEffect: React.FC = () => {
  const frame = useCurrentFrame();

  const intensity = interpolate(frame, [0, 2, 5, 7], [0, 1, 0.6, 0], {
    extrapolateRight: 'clamp',
  });

  // RGB channel offsets — different per frame for jitter
  const rOffset = Math.sin(frame * 4.7) * 12 * intensity;
  const gOffset = Math.cos(frame * 3.2) * 8 * intensity;
  const bOffset = Math.sin(frame * 5.1) * 15 * intensity;

  // Scan line density
  const scanOpacity = intensity * 0.35;

  // Random block displacement
  const blockShift = Math.sin(frame * 7.3) * 30 * intensity;

  return (
    <AbsoluteFill style={{ zIndex: 50, pointerEvents: 'none' }}>
      {/* Red channel offset */}
      <AbsoluteFill style={{
        backgroundColor: `rgba(255,50,50,${0.15 * intensity})`,
        transform: `translateX(${rOffset}px)`,
        mixBlendMode: 'screen',
      }} />

      {/* Cyan channel offset (opposite direction) */}
      <AbsoluteFill style={{
        backgroundColor: `rgba(52,211,153,${0.12 * intensity})`,
        transform: `translateX(${-bOffset}px) translateY(${gOffset}px)`,
        mixBlendMode: 'screen',
      }} />

      {/* Horizontal scan lines */}
      <AbsoluteFill style={{
        backgroundImage: `repeating-linear-gradient(
          0deg,
          transparent,
          transparent 3px,
          rgba(5,5,8,${scanOpacity}) 3px,
          rgba(5,5,8,${scanOpacity}) 4px
        )`,
      }} />

      {/* Glitch block — displaced horizontal bar */}
      <div style={{
        position: 'absolute',
        left: 0,
        right: 0,
        top: `${35 + Math.sin(frame * 2.1) * 15}%`,
        height: `${3 + intensity * 5}%`,
        transform: `translateX(${blockShift}px)`,
        backgroundColor: `rgba(52,211,153,${0.08 * intensity})`,
        mixBlendMode: 'screen',
      }} />

      {/* Brief white flash on first frame */}
      {frame < 1 && (
        <AbsoluteFill style={{
          backgroundColor: 'rgba(255,255,255,0.3)',
        }} />
      )}
    </AbsoluteFill>
  );
};
