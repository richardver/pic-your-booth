import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ReleaseClipProps } from './lib/types';
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
import { TOKENS } from './lib/tokens';

// Safe zone padding
const SAFE = { top: 160, right: 110, bottom: 280, left: 40 };

export const ReleaseClip: React.FC<ReleaseClipProps> = ({
  genre, serieName, hookText, genreTags, videoSrc, videoStartSec, dropTimestamp, coverArtSrc, durationSec,
}) => {
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150; // 5 sec end card
  const dropFrame = 240; // 8 seconds in

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* === LAYER 1: Video background (until end card) === */}
      <Sequence durationInFrames={endCardStart}>
        <VideoBackground src={videoSrc} startFromSec={videoStartSec} />
      </Sequence>

      {/* === LAYER 2: Coral vignette builds during build-up === */}
      <Sequence from={90} durationInFrames={dropFrame - 90}>
        <CoralVignette genre={genre} />
      </Sequence>

      {/* === LAYER 3: Hook text + genre pills (0:00-0:03) === */}
      <Sequence durationInFrames={90}>
        <AbsoluteFill style={{
          padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
          zIndex: 10,
        }}>
          <TextHook text={hookText} genre={genre} />
          <GenrePills tags={genreTags} genre={genre} />
          <div style={{
            fontFamily: TOKENS.fontBody,
            fontSize: 32,
            color: 'rgba(255,255,255,0.7)',
            marginTop: 16,
            textShadow: '0 2px 8px rgba(0,0,0,0.9)',
          }}>
            {serieName} is live op SoundCloud
          </div>
        </AbsoluteFill>
      </Sequence>

      {/* === LAYER 4: Build-up (0:03-0:08) — clean, no overlays === */}
      {/* Footage + coral vignette only. Let the music build tension. */}

      {/* === LAYER 5: THE DROP effects (0:08) === */}
      <Sequence from={dropFrame} durationInFrames={8}>
        <BassFlash genre={genre} />
      </Sequence>

      <Sequence from={dropFrame} durationInFrames={20}>
        <ZoomPunch>
          <VideoBackground src={videoSrc} startFromSec={videoStartSec + dropFrame / fps} />
        </ZoomPunch>
      </Sequence>

      <Sequence from={dropFrame} durationInFrames={20}>
        <ParticleBurst genre={genre} />
      </Sequence>

      {/* === LAYER 6: DJ name flash on drop === */}
      <Sequence from={dropFrame} durationInFrames={60}>
        <DropMoment serieName={serieName} genre={genre} />
      </Sequence>

      {/* === LAYER 7: CTA bar slides up during vibe === */}
      <Sequence from={360} durationInFrames={endCardStart - 360}>
        <AbsoluteFill style={{
          padding: `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`,
          justifyContent: 'flex-end',
          zIndex: 10,
        }}>
          <CTABar genre={genre} />
        </AbsoluteFill>
      </Sequence>

      {/* === LAYER 8: End card (last 5 sec) === */}
      <Sequence from={endCardStart}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>
    </AbsoluteFill>
  );
};
