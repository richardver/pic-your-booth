import React from 'react';
import { AbsoluteFill, Audio, Freeze, Sequence, staticFile } from 'remotion';
import { ReleaseClipProps } from './lib/types';
import { DJ_PROFILES, EffectProfile } from './lib/dj-profiles';
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

export const ReleaseClip: React.FC<ReleaseClipProps> = (props) => {
  const {
    genre, djProfile: djProfileKey, djName, serieName, hookText, genreTags,
    videoSrc1, videoSrc2, videoStartSec, dropTimestamp, energyData,
    coverArtSrc, durationSec,
  } = props;

  const profile = DJ_PROFILES[djProfileKey];
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150;
  const dropFrame = dropTimestamp;
  const preDropStart = dropFrame - 60;
  const vibeStart = dropFrame + 60;

  const safePad = `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`;

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* === AUDIO: full duration (from primary angle) === */}
      {videoSrc1 && (
        <Audio
          src={staticFile(videoSrc1)}
          startFrom={Math.round(videoStartSec * 30)}
        />
      )}

      {/* ========================================== */}
      {/* === VIDEO LAYERS (per section with fx)    === */}
      {/* === Each section has its own camera move  === */}
      {/* === Sections are back-to-back, no gaps    === */}
      {/* ========================================== */}

      {/* HOOK (0 to preDropStart-90): SlowZoomDrift — videoSrc1 */}
      <Sequence from={0} durationInFrames={90}>
        <BeatPulse energyData={energyData} djProfile={djProfileKey}>
          <SlowZoomDrift fromScale={profile.hookZoom[0]} toScale={profile.hookZoom[1]}>
            <VideoBackground src={videoSrc1} startFromSec={videoStartSec} />
          </SlowZoomDrift>
        </BeatPulse>
      </Sequence>

      {/* BUILD-UP (90 to preDropStart): SlowZoomDrift deeper — videoSrc1 */}
      <Sequence from={90} durationInFrames={preDropStart - 90}>
        <BeatPulse energyData={energyData} djProfile={djProfileKey}>
          <SlowZoomDrift fromScale={profile.buildUpZoom[0]} toScale={profile.buildUpZoom[1]}>
            <VideoBackground src={videoSrc1} startFromSec={videoStartSec + 90 / fps} />
          </SlowZoomDrift>
        </BeatPulse>
      </Sequence>

      {/* PRE-DROP (preDropStart to dropFrame): tension — videoSrc2 */}
      <Sequence from={preDropStart} durationInFrames={60}>
        <BeatPulse energyData={energyData} djProfile={djProfileKey}>
          <VideoBackground src={videoSrc2} startFromSec={videoStartSec + preDropStart / fps} />
        </BeatPulse>
      </Sequence>

      {/* DROP (dropFrame): Freeze + ScreenShake + zoom — videoSrc2 */}
      <Sequence from={dropFrame} durationInFrames={6}>
        <Freeze frame={0}>
          <VideoBackground src={videoSrc2} startFromSec={videoStartSec + dropFrame / fps} />
        </Freeze>
      </Sequence>

      <Sequence from={dropFrame + 6} durationInFrames={24}>
        <ScreenShake intensity={profile.screenShakeIntensity} durationFrames={profile.screenShakeDuration}>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            <VideoBackground src={videoSrc2} startFromSec={videoStartSec + (dropFrame + 6) / fps} />
          </BeatPulse>
        </ScreenShake>
      </Sequence>

      {/* POST-DROP settling — videoSrc2 */}
      <Sequence from={dropFrame + 30} durationInFrames={vibeStart - dropFrame - 30}>
        <BeatPulse energyData={energyData} djProfile={djProfileKey}>
          <VideoBackground src={videoSrc2} startFromSec={videoStartSec + (dropFrame + 30) / fps} />
        </BeatPulse>
      </Sequence>

      {/* VIBE (vibeStart to 480): SlowPan + warmer color — videoSrc1 */}
      <Sequence from={vibeStart} durationInFrames={480 - vibeStart}>
        <BeatPulse energyData={energyData} djProfile={djProfileKey}>
          {profile.useSlowPan ? (
            <SlowPan fromX={0} toX={-25}>
              <AbsoluteFill style={profile.warmVibeSection ? { filter: 'saturate(1.15) brightness(1.02)' } : undefined}>
                <VideoBackground src={videoSrc1} startFromSec={videoStartSec + vibeStart / fps} />
              </AbsoluteFill>
            </SlowPan>
          ) : (
            <AbsoluteFill style={profile.warmVibeSection ? { filter: 'saturate(1.15) brightness(1.02)' } : undefined}>
              <VideoBackground src={videoSrc1} startFromSec={videoStartSec + vibeStart / fps} />
            </AbsoluteFill>
          )}
        </BeatPulse>
      </Sequence>

      {/* DECK HITS (480 to endCard): zoom kicks + flashes — videoSrc1 */}
      {/* TODO: pass hitZoomScale to DeckHits when component supports it (profile.hitZoomScale) */}
      <Sequence from={480} durationInFrames={endCardStart - 480}>
        <DeckHits genre={genre} hitInterval={profile.hitInterval} hitCount={profile.hitCount}>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            {profile.useSlowPan ? (
              <SlowPan fromX={-25} toX={-40}>
                <AbsoluteFill style={profile.warmVibeSection ? { filter: 'saturate(1.15) brightness(1.02)' } : undefined}>
                  <VideoBackground src={videoSrc1} startFromSec={videoStartSec + 480 / fps} />
                </AbsoluteFill>
              </SlowPan>
            ) : (
              <AbsoluteFill style={profile.warmVibeSection ? { filter: 'saturate(1.15) brightness(1.02)' } : undefined}>
                <VideoBackground src={videoSrc1} startFromSec={videoStartSec + 480 / fps} />
              </AbsoluteFill>
            )}
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
      {/* TODO: pass bassFlashOpacity to BassFlash when component supports it (profile.bassFlashOpacity) */}
      <Sequence from={dropFrame} durationInFrames={10}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* Drop: particles (only if profile enables them) */}
      {profile.useParticles && (
        <Sequence from={dropFrame} durationInFrames={24}>
          <ParticleBurst genre={genre} />
        </Sequence>
      )}

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
