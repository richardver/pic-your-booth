import React from 'react';
import { AbsoluteFill, Audio, Sequence, staticFile } from 'remotion';
import { ReleaseClipProps } from './lib/types';
import { TOKENS, SAFE } from './lib/tokens';
import { VideoBackground } from './components/VideoBackground';
import { HookSection } from './components/HookSection';
import { DropMoment } from './components/DropMoment';
import { CTABar } from './components/CTABar';
import { EndCard } from './components/EndCard';
import { BassFlash } from './components/effects/BassFlash';
import { ParticleBurst } from './components/effects/ParticleBurst';
import { CoralVignette } from './components/effects/CoralVignette';
import { FilmGrain } from './components/effects/FilmGrain';
import { BeatPulse } from './components/effects/BeatPulse';
import { LightLeak } from './components/effects/LightLeak';
import { PreDropBuild } from './components/effects/PreDropBuild';
import { PostDropDecay } from './components/effects/PostDropDecay';
import { DeckHits } from './components/effects/DeckHits';

export const ReleaseClip: React.FC<ReleaseClipProps> = ({
  genre, djName, serieName, hookText, genreTags, videoSrc, videoStartSec, dropTimestamp, coverArtSrc, durationSec,
}) => {
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150;
  const dropFrame = 240;
  const preDropStart = dropFrame - 60;

  const safePad = `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* ========================================== */}
      {/* === BASE: Audio (full duration)           === */}
      {/* ========================================== */}
      {videoSrc && (
        <Audio
          src={staticFile(videoSrc)}
          startFrom={Math.round(videoStartSec * 24)}
        />
      )}

      {/* ========================================== */}
      {/* === BASE: ONE continuous video layer      === */}
      {/* === Runs the ENTIRE clip until end card   === */}
      {/* === Everything else is OVERLAY on top     === */}
      {/* ========================================== */}
      <Sequence durationInFrames={endCardStart}>
        <BeatPulse>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec} />
        </BeatPulse>
      </Sequence>

      {/* ========================================== */}
      {/* === OVERLAY EFFECTS (on top of video)     === */}
      {/* ========================================== */}

      {/* Vignette during build-up */}
      <Sequence from={90} durationInFrames={preDropStart - 90}>
        <CoralVignette genre={genre} />
      </Sequence>

      {/* Pre-drop: growing shake overlay + brightness dip */}
      <Sequence from={preDropStart} durationInFrames={60}>
        <PreDropBuild genre={genre}>
          <div />
        </PreDropBuild>
      </Sequence>

      {/* Drop: bass flash */}
      <Sequence from={dropFrame} durationInFrames={10}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* Drop: particles */}
      <Sequence from={dropFrame} durationInFrames={24}>
        <ParticleBurst genre={genre} />
      </Sequence>

      {/* Drop: second bass flash */}
      <Sequence from={dropFrame + 18} durationInFrames={8}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* Post-drop decay overlay */}
      <Sequence from={dropFrame + 20} durationInFrames={45}>
        <PostDropDecay>
          <div />
        </PostDropDecay>
      </Sequence>

      {/* Deck hits — overlay flashes at 16-20s */}
      <Sequence from={480} durationInFrames={140}>
        <DeckHits genre={genre} hitInterval={28} hitCount={5} />
      </Sequence>

      {/* Light leaks at transitions */}
      <Sequence from={82} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>
      <Sequence from={290} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>
      <Sequence from={endCardStart - 10} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* ========================================== */}
      {/* === TEXT OVERLAYS                         === */}
      {/* ========================================== */}

      {/* Hook: text + pills */}
      <Sequence durationInFrames={90}>
        <HookSection hookText={hookText} genreTags={genreTags} genre={genre} />
      </Sequence>

      {/* Drop: DJ name (overlay on video, NOT replacing it) */}
      <Sequence from={dropFrame + 2} durationInFrames={120}>
        <DropMoment djName={djName} serieName={serieName} genre={genre} />
      </Sequence>

      {/* Vibe: booking CTA */}
      <Sequence from={360} durationInFrames={endCardStart - 360}>
        <AbsoluteFill style={{ padding: safePad, justifyContent: 'flex-end', zIndex: 10 }}>
          <CTABar genre={genre} djName={djName} />
        </AbsoluteFill>
      </Sequence>

      {/* ========================================== */}
      {/* === END CARD (replaces video)             === */}
      {/* ========================================== */}
      <Sequence from={endCardStart}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      {/* ========================================== */}
      {/* === TOP: Film grain (always)              === */}
      {/* ========================================== */}
      <FilmGrain opacity={0.05} />
    </AbsoluteFill>
  );
};
