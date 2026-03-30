import React from 'react';
import {
  AbsoluteFill, Audio, Sequence, staticFile,
  OffthreadVideo, useCurrentFrame, interpolate, spring, useVideoConfig,
} from 'remotion';
import { ReleaseClipProps } from '../lib/types';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { EndCard } from '../components/EndCard';
import { FilmGrain } from '../components/effects/FilmGrain';
import { LumaRevealText } from '../components/effects/LumaRevealText';
import { SpeedRamp } from '../components/effects/SpeedRamp';

/**
 * Variant 2: SPLIT SCREEN
 *
 * Both angles visible simultaneously. Main angle fills the screen,
 * secondary angle in a floating PiP frame with accent border.
 * At each cut point they swap — the PiP becomes full and vice versa.
 */
export const MiloSplitScreen: React.FC<ReleaseClipProps> = (props) => {
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

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>
      {videoSrc1 && (
        <Audio src={staticFile(videoSrc1)} startFrom={Math.round(videoStartSec * fps)} />
      )}

      {/* HOOK: Full angle 1 */}
      <Sequence from={0} durationInFrames={hookEnd}>
        <BrightVideo src={videoSrc1} startFromSec={videoStartSec} />
        <AbsoluteFill style={{
          background: 'linear-gradient(180deg, transparent 40%, rgba(5,5,8,0.5) 100%)',
          pointerEvents: 'none',
        }} />
      </Sequence>
      <Sequence from={0} durationInFrames={hookEnd}>
        <LumaRevealText text={hookText} djName={djName} />
      </Sequence>

      {/* SET: Split screen with PiP */}
      <Sequence from={hookEnd} durationInFrames={setEnd - hookEnd}>
        <SplitScreenLayer
          src1={videoSrc1}
          src2={videoSrc2}
          startFromSec={videoStartSec}
          hookEnd={hookEnd}
          cuts={cutPoints.length > 0 ? cutPoints : [180, 300, 420]}
          setEnd={setEnd}
          genre={genre}
          fps={fps}
        />
      </Sequence>

      {/* SPEED RAMP */}
      <Sequence from={setEnd} durationInFrames={rampEnd - setEnd}>
        <SpeedRamp durationFrames={rampEnd - setEnd}>
          <BrightVideo src={videoSrc1} startFromSec={videoStartSec + setEnd / fps} />
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

const SplitScreenLayer: React.FC<{
  src1: string;
  src2: string;
  startFromSec: number;
  hookEnd: number;
  cuts: number[];
  setEnd: number;
  genre: string;
  fps: number;
}> = ({ src1, src2, startFromSec, hookEnd, cuts, setEnd, genre, fps }) => {
  const frame = useCurrentFrame();
  const { fps: videoFps } = useVideoConfig();
  const absFrame = frame + hookEnd;
  const accent = GENRE_TOKENS[genre as keyof typeof GENRE_TOKENS]?.accent || '#34d399';

  // Determine which angle is main based on cut points
  let mainIsAngle1 = true;
  for (const cut of cuts) {
    if (absFrame >= cut && cut <= setEnd) mainIsAngle1 = !mainIsAngle1;
  }

  const mainSrc = mainIsAngle1 ? src1 : src2;
  const pipSrc = mainIsAngle1 ? src2 : src1;
  const currentTimeSec = startFromSec + absFrame / fps;

  // PiP entrance spring
  const pipEnter = spring({
    fps: videoFps,
    frame: Math.min(frame, 15),
    config: { damping: 14, stiffness: 160 },
  });

  return (
    <AbsoluteFill>
      {/* Main — full screen, bright */}
      <AbsoluteFill style={{ filter: 'brightness(0.92) contrast(1.1) saturate(0.9)' }}>
        <OffthreadVideo
          src={staticFile(mainSrc)}
          startFrom={Math.round(currentTimeSec * 30)}
          volume={0}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </AbsoluteFill>

      {/* Light teal wash */}
      <AbsoluteFill style={{
        background: 'rgba(52,211,153,0.05)',
        mixBlendMode: 'overlay',
        pointerEvents: 'none',
      }} />

      {/* PiP — floating frame, top-right */}
      <div style={{
        position: 'absolute',
        top: 180,
        right: 40,
        width: 320,
        height: 420,
        borderRadius: 20,
        overflow: 'hidden',
        border: `3px solid ${accent}`,
        boxShadow: `0 8px 32px rgba(0,0,0,0.5), 0 0 20px ${accent}44`,
        transform: `scale(${pipEnter})`,
        zIndex: 20,
      }}>
        <OffthreadVideo
          src={staticFile(pipSrc)}
          startFrom={Math.round(currentTimeSec * 30)}
          volume={0}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </div>
    </AbsoluteFill>
  );
};

const BrightVideo: React.FC<{ src: string; startFromSec: number }> = ({ src, startFromSec }) => (
  <AbsoluteFill style={{ filter: 'brightness(0.92) contrast(1.1) saturate(0.9)' }}>
    {src ? (
      <OffthreadVideo
        src={staticFile(src)}
        startFrom={Math.round(startFromSec * 30)}
        volume={0}
        style={{ width: '100%', height: '100%', objectFit: 'cover' }}
      />
    ) : (
      <AbsoluteFill style={{ backgroundColor: TOKENS.void }} />
    )}
  </AbsoluteFill>
);
