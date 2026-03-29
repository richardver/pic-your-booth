import React from 'react';
import { AbsoluteFill, Audio, Freeze, Sequence, staticFile } from 'remotion';
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
import { ScreenShake } from './components/effects/ScreenShake';
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
      {/* === VIDEO LAYERS (per section with fx)    === */}
      {/* === Each section has its own camera move  === */}
      {/* === Sections are back-to-back, no gaps    === */}
      {/* ========================================== */}

      {/* HOOK (0-3s): SlowZoomDrift */}
      <Sequence from={0} durationInFrames={90}>
        <BeatPulse>
          <SlowZoomDrift fromScale={1.0} toScale={1.04}>
            <VideoBackground src={videoSrc} startFromSec={videoStartSec} />
          </SlowZoomDrift>
        </BeatPulse>
      </Sequence>

      {/* BUILD-UP (3-6s): SlowZoomDrift deeper */}
      <Sequence from={90} durationInFrames={preDropStart - 90}>
        <BeatPulse>
          <SlowZoomDrift fromScale={1.0} toScale={1.06}>
            <VideoBackground src={videoSrc} startFromSec={videoStartSec + 90 / fps} />
          </SlowZoomDrift>
        </BeatPulse>
      </Sequence>

      {/* PRE-DROP (6-8s): tension video */}
      <Sequence from={preDropStart} durationInFrames={60}>
        <BeatPulse>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + preDropStart / fps} />
        </BeatPulse>
      </Sequence>

      {/* DROP (8s): Freeze + ScreenShake + zoom */}
      <Sequence from={dropFrame} durationInFrames={6}>
        <Freeze frame={0}>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + dropFrame / fps} />
        </Freeze>
      </Sequence>

      <Sequence from={dropFrame + 6} durationInFrames={24}>
        <ScreenShake intensity={18} durationFrames={18}>
          <BeatPulse>
            <VideoBackground src={videoSrc} startFromSec={videoStartSec + (dropFrame + 6) / fps} />
          </BeatPulse>
        </ScreenShake>
      </Sequence>

      {/* POST-DROP (9-10s): settling video */}
      <Sequence from={dropFrame + 30} durationInFrames={vibeStart - dropFrame - 30}>
        <BeatPulse>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + (dropFrame + 30) / fps} />
        </BeatPulse>
      </Sequence>

      {/* VIBE (10-16s): SlowPan + warmer color */}
      <Sequence from={vibeStart} durationInFrames={480 - vibeStart}>
        <BeatPulse>
          <SlowPan fromX={0} toX={-25}>
            <AbsoluteFill style={{ filter: 'saturate(1.15) brightness(1.02)' }}>
              <VideoBackground src={videoSrc} startFromSec={videoStartSec + vibeStart / fps} />
            </AbsoluteFill>
          </SlowPan>
        </BeatPulse>
      </Sequence>

      {/* DECK HITS (16-20s): zoom kicks + flashes */}
      <Sequence from={480} durationInFrames={endCardStart - 480}>
        <DeckHits genre={genre} hitInterval={28} hitCount={5}>
          <BeatPulse>
            <SlowPan fromX={-25} toX={-40}>
              <AbsoluteFill style={{ filter: 'saturate(1.15) brightness(1.02)' }}>
                <VideoBackground src={videoSrc} startFromSec={videoStartSec + 480 / fps} />
              </AbsoluteFill>
            </SlowPan>
          </BeatPulse>
        </DeckHits>
      </Sequence>

      {/* ========================================== */}
      {/* === OVERLAY EFFECTS                       === */}
      {/* ========================================== */}

      {/* Vignette during build-up */}
      <Sequence from={90} durationInFrames={preDropStart - 90}>
        <CoralVignette genre={genre} />
      </Sequence>

      {/* Pre-drop overlay: brightness dip + vignette */}
      <Sequence from={preDropStart} durationInFrames={60}>
        <PreDropBuild genre={genre} />
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

      {/* Post-drop: brightness recovery */}
      <Sequence from={dropFrame + 20} durationInFrames={45}>
        <PostDropDecay />
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

      {/* Drop: DJ name */}
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
      {/* === END CARD                              === */}
      {/* ========================================== */}
      <Sequence from={endCardStart}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      {/* === Film grain (always) === */}
      <FilmGrain opacity={0.05} />
    </AbsoluteFill>
  );
};
