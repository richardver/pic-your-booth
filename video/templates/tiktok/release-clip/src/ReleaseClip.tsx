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
import { ZoomPunch } from './components/effects/ZoomPunch';
import { ParticleBurst } from './components/effects/ParticleBurst';
import { CoralVignette } from './components/effects/CoralVignette';
import { FilmGrain } from './components/effects/FilmGrain';
import { ScreenShake } from './components/effects/ScreenShake';
import { LightLeak } from './components/effects/LightLeak';

export const ReleaseClip: React.FC<ReleaseClipProps> = ({
  genre, djName, serieName, hookText, genreTags, videoSrc, videoStartSec, dropTimestamp, coverArtSrc, durationSec,
}) => {
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150;
  const dropFrame = 240;

  const safePad = `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* === AUDIO: full duration including end card === */}
      {videoSrc && (
        <Audio
          src={staticFile(videoSrc)}
          startFrom={Math.round(videoStartSec * 24)}
        />
      )}

      {/* === LAYER 1: Video background === */}
      <Sequence durationInFrames={endCardStart}>
        <VideoBackground src={videoSrc} startFromSec={videoStartSec} />
      </Sequence>

      {/* === LAYER 2: Vignette builds tension during build-up === */}
      <Sequence from={90} durationInFrames={dropFrame - 90}>
        <CoralVignette genre={genre} />
      </Sequence>

      {/* === LAYER 3: Hook — text + pills only, no SoundCloud text === */}
      <Sequence durationInFrames={90}>
        <HookSection hookText={hookText} genreTags={genreTags} genre={genre} />
      </Sequence>

      {/* === LAYER 4: Light leak sweep at hook exit === */}
      <Sequence from={82} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* === LAYER 5: THE DROP — everything fires at once === */}

      {/* 5a: Freeze frame — time stops for 6 frames */}
      <Sequence from={dropFrame} durationInFrames={6}>
        <Freeze frame={0}>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + dropFrame / fps} />
        </Freeze>
      </Sequence>

      {/* 5b: Bass flash — full screen coral blast */}
      <Sequence from={dropFrame} durationInFrames={10}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* 5c: Screen shake + zoom punch — the physical impact */}
      <Sequence from={dropFrame} durationInFrames={20}>
        <ScreenShake intensity={18} durationFrames={18}>
          <ZoomPunch>
            <VideoBackground src={videoSrc} startFromSec={videoStartSec + dropFrame / fps} />
          </ZoomPunch>
        </ScreenShake>
      </Sequence>

      {/* 5d: Particle explosion */}
      <Sequence from={dropFrame} durationInFrames={24}>
        <ParticleBurst genre={genre} />
      </Sequence>

      {/* 5e: DJ name slam */}
      <Sequence from={dropFrame} durationInFrames={60}>
        <DropMoment djName={djName} serieName={serieName} genre={genre} />
      </Sequence>

      {/* 5f: Second bass flash at drop + 0.5s for double-hit feel */}
      <Sequence from={dropFrame + 15} durationInFrames={8}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* === LAYER 6: Light leak at drop exit === */}
      <Sequence from={290} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* === LAYER 7: CTA bar during vibe === */}
      <Sequence from={360} durationInFrames={endCardStart - 360}>
        <AbsoluteFill style={{ padding: safePad, justifyContent: 'flex-end', zIndex: 10 }}>
          <CTABar genre={genre} />
        </AbsoluteFill>
      </Sequence>

      {/* === LAYER 8: Light leak at vibe → end card transition === */}
      <Sequence from={endCardStart - 10} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* === LAYER 9: End card === */}
      <Sequence from={endCardStart}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      {/* === LAYER 10: Film grain (always) === */}
      <FilmGrain opacity={0.05} />
    </AbsoluteFill>
  );
};
