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
import { SlowZoomDrift } from './components/effects/SlowZoomDrift';
import { SlowPan } from './components/effects/SlowPan';
import { DeckHits } from './components/effects/DeckHits';

export const ReleaseClip: React.FC<ReleaseClipProps> = ({
  genre, djName, serieName, hookText, genreTags, videoSrc, videoStartSec, dropTimestamp, coverArtSrc, durationSec,
}) => {
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150;
  const dropFrame = 240;
  const preDropStart = dropFrame - 60;
  const vibeStart = dropFrame + 60;

  const safePad = `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* === AUDIO: full duration === */}
      {videoSrc && (
        <Audio
          src={staticFile(videoSrc)}
          startFrom={Math.round(videoStartSec * 24)}
        />
      )}

      {/* ========================================== */}
      {/* === HOOK SECTION (0-3s) — zoom drift       */}
      {/* ========================================== */}
      <Sequence durationInFrames={90}>
        <BeatPulse>
          <SlowZoomDrift fromScale={1.0} toScale={1.04}>
            <VideoBackground src={videoSrc} startFromSec={videoStartSec} />
          </SlowZoomDrift>
        </BeatPulse>
      </Sequence>

      <Sequence durationInFrames={90}>
        <HookSection hookText={hookText} genreTags={genreTags} genre={genre} />
      </Sequence>

      {/* === Light leak at hook exit === */}
      <Sequence from={82} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* ========================================== */}
      {/* === BUILD-UP (3-6s) — slow zoom drift      */}
      {/* ========================================== */}
      <Sequence from={90} durationInFrames={preDropStart - 90}>
        <BeatPulse>
          <SlowZoomDrift fromScale={1.0} toScale={1.06}>
            <VideoBackground src={videoSrc} startFromSec={videoStartSec + 90 / fps} />
          </SlowZoomDrift>
        </BeatPulse>
      </Sequence>

      <Sequence from={90} durationInFrames={preDropStart - 90}>
        <CoralVignette genre={genre} />
      </Sequence>

      {/* ========================================== */}
      {/* === PRE-DROP (6-8s) — tension builds        */}
      {/* ========================================== */}
      <Sequence from={preDropStart} durationInFrames={60}>
        <PreDropBuild genre={genre}>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + preDropStart / fps} />
        </PreDropBuild>
      </Sequence>

      {/* ========================================== */}
      {/* === THE DROP (8s)                          */}
      {/* ========================================== */}

      {/* Bass flash */}
      <Sequence from={dropFrame} durationInFrames={10}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* Particles */}
      <Sequence from={dropFrame} durationInFrames={24}>
        <ParticleBurst genre={genre} />
      </Sequence>

      {/* DJ name — appears 2 frames after flash, stays 4 seconds */}
      <Sequence from={dropFrame + 2} durationInFrames={120}>
        <DropMoment djName={djName} serieName={serieName} genre={genre} />
      </Sequence>

      {/* Second bass flash */}
      <Sequence from={dropFrame + 18} durationInFrames={8}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* ========================================== */}
      {/* === POST-DROP DECAY (8.7-10s)              */}
      {/* ========================================== */}
      <Sequence from={dropFrame + 20} durationInFrames={45}>
        <PostDropDecay>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + (dropFrame + 20) / fps} />
        </PostDropDecay>
      </Sequence>

      {/* Light leak at drop exit */}
      <Sequence from={290} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* ========================================== */}
      {/* === VIBE (10-20s) — slow pan + warmer color */}
      {/* ========================================== */}
      <Sequence from={vibeStart} durationInFrames={endCardStart - vibeStart}>
        <BeatPulse>
          <SlowPan fromX={0} toX={-25}>
            {/* Warmer color during vibe — energy feels different from build-up */}
            <AbsoluteFill style={{ filter: 'saturate(1.15) brightness(1.02)' }}>
              <VideoBackground src={videoSrc} startFromSec={videoStartSec + vibeStart / fps} />
            </AbsoluteFill>
          </SlowPan>
        </BeatPulse>
      </Sequence>

      {/* Deck hits — repeating zoom + flash during deck action (16-20s) */}
      <Sequence from={480} durationInFrames={140}>
        <DeckHits genre={genre} hitInterval={28} hitCount={5}>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + 480 / fps} />
        </DeckHits>
      </Sequence>

      {/* CTA bar during vibe */}
      <Sequence from={360} durationInFrames={endCardStart - 360}>
        <AbsoluteFill style={{ padding: safePad, justifyContent: 'flex-end', zIndex: 10 }}>
          <CTABar genre={genre} djName={djName} />
        </AbsoluteFill>
      </Sequence>

      {/* === Light leak at vibe → end card === */}
      <Sequence from={endCardStart - 10} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* ========================================== */}
      {/* === END CARD (20-25s)                      */}
      {/* ========================================== */}
      <Sequence from={endCardStart}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      {/* === Film grain (always) === */}
      <FilmGrain opacity={0.05} />
    </AbsoluteFill>
  );
};
