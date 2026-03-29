import React from 'react';
import { AbsoluteFill, Audio, Freeze, Sequence, staticFile } from 'remotion';
import { ReleaseClipProps } from './lib/types';
import { TOKENS, SAFE } from './lib/tokens';
import { VideoBackground } from './components/VideoBackground';
import { TextHook } from './components/TextHook';
import { GenrePills } from './components/GenrePills';
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
  const endCardStart = totalFrames - 150; // 5 sec end card
  const dropFrame = 240; // 8 seconds in

  const safePad = `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* === AUDIO: plays the ENTIRE duration (including end card) === */}
      {videoSrc && (
        <Audio
          src={staticFile(videoSrc)}
          startFrom={Math.round(videoStartSec * 24)}
        />
      )}

      {/* === LAYER 1: Video background (visual only, until end card) === */}
      <Sequence durationInFrames={endCardStart}>
        <VideoBackground src={videoSrc} startFromSec={videoStartSec} />
      </Sequence>

      {/* === LAYER 2: Coral vignette builds during build-up === */}
      <Sequence from={90} durationInFrames={dropFrame - 90}>
        <CoralVignette genre={genre} />
      </Sequence>

      {/* === LAYER 3: Hook sequence — staggered reveal === */}
      {/* 3a: Hook text ONLY (0:00-0:03) — the scroll stopper */}
      <Sequence durationInFrames={90}>
        <AbsoluteFill style={{
          padding: safePad,
          zIndex: 10,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}>
          <TextHook text={hookText} genre={genre} />
        </AbsoluteFill>
      </Sequence>

      {/* 3b: Genre pills appear AFTER hook lands (0:01-0:03) */}
      <Sequence from={30} durationInFrames={60}>
        <AbsoluteFill style={{
          padding: safePad,
          zIndex: 10,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          paddingTop: SAFE.top + 240,
        }}>
          <GenrePills tags={genreTags} genre={genre} />
        </AbsoluteFill>
      </Sequence>

      {/* 3c: Sub-hook last (0:02-0:03) */}
      <Sequence from={55} durationInFrames={35}>
        <AbsoluteFill style={{
          padding: safePad,
          zIndex: 10,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          paddingTop: SAFE.top + 300,
        }}>
          <div style={{
            fontFamily: TOKENS.fontBody,
            fontSize: 32,
            color: 'rgba(255,255,255,0.6)',
            textShadow: '0 2px 8px rgba(0,0,0,0.9)',
            textAlign: 'center',
          }}>
            {serieName} is live op SoundCloud
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* === LAYER 4: Build-up — clean footage, no overlays === */}

      {/* === LAYER 4.5: Light leak at hook → build-up transition === */}
      <Sequence from={85} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* === LAYER 5: THE DROP effects (0:08) === */}
      {/* Freeze frame on drop for "time stops" effect */}
      <Sequence from={dropFrame} durationInFrames={6}>
        <Freeze frame={0}>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + dropFrame / fps} />
        </Freeze>
      </Sequence>

      <Sequence from={dropFrame} durationInFrames={8}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* Screen shake + zoom punch on bass hit */}
      <Sequence from={dropFrame} durationInFrames={15}>
        <ScreenShake intensity={8}>
          <ZoomPunch>
            <VideoBackground src={videoSrc} startFromSec={videoStartSec + dropFrame / fps} />
          </ZoomPunch>
        </ScreenShake>
      </Sequence>

      <Sequence from={dropFrame} durationInFrames={20}>
        <ParticleBurst genre={genre} />
      </Sequence>

      {/* === LAYER 6: DJ name flash on drop === */}
      <Sequence from={dropFrame} durationInFrames={60}>
        <DropMoment djName={djName} serieName={serieName} genre={genre} />
      </Sequence>

      {/* === LAYER 7: CTA bar during vibe === */}
      <Sequence from={360} durationInFrames={endCardStart - 360}>
        <AbsoluteFill style={{ padding: safePad, justifyContent: 'flex-end', zIndex: 10 }}>
          <CTABar genre={genre} />
        </AbsoluteFill>
      </Sequence>

      {/* === LAYER 7.5: Light leak at drop → vibe transition === */}
      <Sequence from={295} durationInFrames={30}>
        <LightLeak genre={genre} />
      </Sequence>

      {/* === LAYER 8: End card (last 5 sec) — audio continues === */}
      <Sequence from={endCardStart}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>

      {/* === LAYER 9: Film grain overlay (always visible) === */}
      <FilmGrain opacity={0.04} />
    </AbsoluteFill>
  );
};
