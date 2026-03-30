import React from 'react';
import { AbsoluteFill, Audio, Freeze, Sequence, staticFile, interpolate, useCurrentFrame } from 'remotion';
import { ReleaseClipProps } from './lib/types';
import { DJ_PROFILES } from './lib/dj-profiles';
import { TOKENS, GENRE_TOKENS, SAFE } from './lib/tokens';
import { VideoBackground } from './components/VideoBackground';
import { TextHookUrban } from './components/TextHookUrban';
import { DropMomentUrban } from './components/DropMomentUrban';
import { CTABar } from './components/CTABar';
import { EndCard } from './components/EndCard';
import { BassFlash } from './components/effects/BassFlash';
import { BeatPulse } from './components/effects/BeatPulse';
import { PreDropBuild } from './components/effects/PreDropBuild';
import { PostDropDecay } from './components/effects/PostDropDecay';
import { SlowZoomDrift } from './components/effects/SlowZoomDrift';
import { ScreenShake } from './components/effects/ScreenShake';

/**
 * ReleaseClipGianniUrban — Urban NL template for DJ Gianni
 *
 * Visual identity: cool purple grade, letterbox bars, fast cuts,
 * B-roll cutaways, zoom punch drop, black frame tension.
 *
 * Differences from GianniAfro:
 * - Cool color grade (purple shadows) instead of warm saturation
 * - Letterbox bars (cinematic 2.35:1 feel)
 * - Faster text slam (word-by-word, shorter delays)
 * - Black frame before drop (3 frames of void = tension)
 * - Zoom punch on drop instead of particle burst
 * - B-roll close-up cutaways during build-up
 * - Stronger vignette throughout
 * - No GenrePills
 */

// ─── Letterbox Bars ───
const LetterboxBars: React.FC = () => (
  <>
    <div style={{
      position: 'absolute', top: 0, left: 0, right: 0, height: 90,
      background: 'linear-gradient(180deg, #050508 60%, transparent)',
      zIndex: 20,
    }} />
    <div style={{
      position: 'absolute', bottom: 0, left: 0, right: 0, height: 90,
      background: 'linear-gradient(0deg, #050508 60%, transparent)',
      zIndex: 20,
    }} />
  </>
);

// Grade is baked into footage via ffmpeg (teal shadows + purple mids + warm highlights)
// Only a subtle Remotion polish layer for final contrast punch
const GradePolish: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <AbsoluteFill style={{
    filter: 'contrast(1.04) brightness(1.06)',
  }}>
    {children}
  </AbsoluteFill>
);

// ─── Strong Urban Vignette ───
const UrbanVignette: React.FC = () => (
  <AbsoluteFill style={{
    background: 'radial-gradient(ellipse at 50% 50%, transparent 45%, rgba(5,5,8,0.55) 100%)',
    zIndex: 8,
    pointerEvents: 'none' as const,
  }} />
);

// ─── Zoom Punch (replaces particles on drop) ───
const ZoomPunch: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const frame = useCurrentFrame();
  const scale = interpolate(frame, [0, 3, 12], [1.0, 1.18, 1.02], {
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{ transform: `scale(${scale})` }}>
      {children}
    </AbsoluteFill>
  );
};

// ─── Black Flash (tension before drop) ───
const BlackFlash: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 2, 3], [1, 1, 0], {
    extrapolateRight: 'clamp',
  });
  return (
    <AbsoluteFill style={{
      backgroundColor: TOKENS.void,
      opacity,
      zIndex: 15,
    }} />
  );
};

export const ReleaseClipGianniUrban: React.FC<ReleaseClipProps> = (props) => {
  const {
    genre, djProfile: djProfileKey, djName, serieName, hookText,
    videoSrc1, videoSrc2, videoStartSec, dropTimestamp, energyData,
    coverArtSrc, durationSec, brollSources = [],
  } = props;

  const profile = DJ_PROFILES[djProfileKey];
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150;
  const dropFrame = dropTimestamp;
  const preDropStart = dropFrame - 45; // shorter pre-drop (faster pacing)
  const vibeStart = dropFrame + 50;
  const { accent } = GENRE_TOKENS[genre];

  const safePad = `${SAFE.top}px ${SAFE.right}px ${SAFE.bottom}px ${SAFE.left}px`;

  // B-roll cut schedule: quick 1.5s cuts during build-up
  const brollCuts = brollSources.map((src, i) => ({
    src,
    startFrame: 75 + i * 50, // stagger every ~1.7s starting at 2.5s
    duration: 45, // 1.5s each
  })).filter(cut => cut.startFrame + cut.duration < preDropStart);

  return (
    <AbsoluteFill style={{ backgroundColor: TOKENS.void }}>

      {/* === AUDIO === */}
      {videoSrc1 && (
        <Audio
          src={staticFile(videoSrc1)}
          startFrom={Math.round(videoStartSec * fps)}
        />
      )}

      {/* ========================================== */}
      {/* === VIDEO LAYERS WITH COOL GRADE         === */}
      {/* ========================================== */}

      {/* HOOK (0-70): angle 1, zoom drift */}
      <Sequence from={0} durationInFrames={70}>
        <GradePolish>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            <SlowZoomDrift fromScale={1.0} toScale={1.05}>
              <VideoBackground src={videoSrc1} startFromSec={videoStartSec} />
            </SlowZoomDrift>
          </BeatPulse>
        </GradePolish>
      </Sequence>

      {/* BUILD-UP (70 to preDropStart): angle 1 with B-roll cuts */}
      <Sequence from={70} durationInFrames={preDropStart - 70}>
        <GradePolish>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            <SlowZoomDrift fromScale={1.0} toScale={1.08}>
              <VideoBackground src={videoSrc1} startFromSec={videoStartSec + 70 / fps} />
            </SlowZoomDrift>
          </BeatPulse>
        </GradePolish>
      </Sequence>

      {/* B-ROLL CUTS: flash over the build-up */}
      {brollCuts.map((cut, i) => (
        <Sequence key={`broll-${i}`} from={cut.startFrame} durationInFrames={cut.duration}>
          <GradePolish>
            <VideoBackground src={cut.src} startFromSec={0} />
          </GradePolish>
        </Sequence>
      ))}

      {/* PRE-DROP (preDropStart to dropFrame-3): angle 2, tension */}
      <Sequence from={preDropStart} durationInFrames={dropFrame - preDropStart - 3}>
        <GradePolish>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            <VideoBackground src={videoSrc2} startFromSec={videoStartSec + preDropStart / fps} />
          </BeatPulse>
        </GradePolish>
      </Sequence>

      {/* BLACK FLASH: 3 frames of void before drop */}
      <Sequence from={dropFrame - 3} durationInFrames={3}>
        <BlackFlash />
      </Sequence>

      {/* DROP: freeze + zoom punch */}
      <Sequence from={dropFrame} durationInFrames={6}>
        <GradePolish>
          <ZoomPunch>
            <Freeze frame={0}>
              <VideoBackground src={videoSrc2} startFromSec={videoStartSec + dropFrame / fps} />
            </Freeze>
          </ZoomPunch>
        </GradePolish>
      </Sequence>

      {/* DROP IMPACT: screen shake + zoom punch settle */}
      <Sequence from={dropFrame + 6} durationInFrames={24}>
        <GradePolish>
          <ScreenShake intensity={22} durationFrames={20}>
            <BeatPulse energyData={energyData} djProfile={djProfileKey}>
              <VideoBackground src={videoSrc2} startFromSec={videoStartSec + (dropFrame + 6) / fps} />
            </BeatPulse>
          </ScreenShake>
        </GradePolish>
      </Sequence>

      {/* POST-DROP settling */}
      <Sequence from={dropFrame + 30} durationInFrames={vibeStart - dropFrame - 30}>
        <GradePolish>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            <VideoBackground src={videoSrc2} startFromSec={videoStartSec + (dropFrame + 30) / fps} />
          </BeatPulse>
        </GradePolish>
      </Sequence>

      {/* VIBE (vibeStart to 480): angle 1, cool grade */}
      <Sequence from={vibeStart} durationInFrames={480 - vibeStart}>
        <GradePolish>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            <VideoBackground src={videoSrc1} startFromSec={videoStartSec + vibeStart / fps} />
          </BeatPulse>
        </GradePolish>
      </Sequence>

      {/* LATE VIBE (480 to endCard): angle 1 */}
      <Sequence from={480} durationInFrames={endCardStart - 480}>
        <GradePolish>
          <BeatPulse energyData={energyData} djProfile={djProfileKey}>
            <VideoBackground src={videoSrc1} startFromSec={videoStartSec + 480 / fps} />
          </BeatPulse>
        </GradePolish>
      </Sequence>

      {/* ========================================== */}
      {/* === OVERLAY EFFECTS                       === */}
      {/* ========================================== */}

      {/* Urban vignette: always on (stronger than afro) */}
      <Sequence from={0} durationInFrames={endCardStart}>
        <UrbanVignette />
      </Sequence>

      {/* Pre-drop build overlay */}
      <Sequence from={preDropStart} durationInFrames={dropFrame - preDropStart - 3}>
        <PreDropBuild genre={genre} />
      </Sequence>

      {/* Drop: bass flash (purple-tinted) */}
      <Sequence from={dropFrame} durationInFrames={8}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* Second flash */}
      <Sequence from={dropFrame + 15} durationInFrames={6}>
        <BassFlash genre={genre} />
      </Sequence>

      {/* Post-drop recovery */}
      <Sequence from={dropFrame + 18} durationInFrames={40}>
        <PostDropDecay />
      </Sequence>

      {/* ========================================== */}
      {/* === LETTERBOX BARS (always on)            === */}
      {/* ========================================== */}
      <LetterboxBars />

      {/* ========================================== */}
      {/* === TEXT OVERLAYS                         === */}
      {/* ========================================== */}

      {/* Hook: text only, no pills, bigger font via TextHook */}
      <Sequence durationInFrames={70}>
        <AbsoluteFill style={{
          padding: safePad,
          zIndex: 10,
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
        }}>
          <TextHookUrban text={hookText} genre={genre} />
        </AbsoluteFill>
      </Sequence>

      {/* Drop: DJ name slam */}
      <Sequence from={dropFrame + 2} durationInFrames={100}>
        <DropMomentUrban djName={djName} serieName={serieName} genre={genre} />
      </Sequence>

      {/* CTA */}
      <Sequence from={340} durationInFrames={endCardStart - 340}>
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
    </AbsoluteFill>
  );
};
