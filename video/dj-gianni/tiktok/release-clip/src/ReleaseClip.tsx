import React from 'react';
import { AbsoluteFill, Sequence } from 'remotion';
import { ReleaseClipProps } from './lib/types';
import { VideoBackground } from './components/VideoBackground';
import { TextHook } from './components/TextHook';
import { GenrePills } from './components/GenrePills';
import { EQBar } from './components/EQBar';
import { DropMoment } from './components/DropMoment';
import { CTABar } from './components/CTABar';
import { EndCard } from './components/EndCard';
import { HexBadge } from './components/HexBadge';

export const ReleaseClip: React.FC<ReleaseClipProps> = ({
  genre, serieName, hookText, genreTags, videoSrc, videoStartSec, dropTimestamp, coverArtSrc, durationSec,
}) => {
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150; // 5 sec end card

  return (
    <AbsoluteFill style={{ backgroundColor: '#050508' }}>
      {/* Video background — plays throughout until end card */}
      <Sequence durationInFrames={endCardStart}>
        <VideoBackground src={videoSrc} startFromSec={videoStartSec} />
      </Sequence>

      {/* Hex badge — always visible */}
      <div style={{ position: 'absolute', top: 120, right: 130, zIndex: 20 }}>
        <HexBadge genre={genre} />
      </div>

      {/* Hook text + genre pills (0:00 - 0:03) */}
      <Sequence durationInFrames={90}>
        <AbsoluteFill style={{ padding: '140px 48px', zIndex: 10 }}>
          <TextHook text={hookText} genre={genre} />
          <GenrePills tags={genreTags} genre={genre} />
        </AbsoluteFill>
      </Sequence>

      {/* EQ bar during build-up (0:03 - 0:08) */}
      <Sequence from={90} durationInFrames={150}>
        <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 300, zIndex: 10 }}>
          <EQBar genre={genre} height={100} />
        </AbsoluteFill>
      </Sequence>

      {/* THE DROP (0:08 - 0:10) */}
      <Sequence from={240} durationInFrames={60}>
        <DropMoment serieName={serieName} genre={genre} />
      </Sequence>

      {/* CTA bar slides up during vibe (0:12+) */}
      <Sequence from={360} durationInFrames={endCardStart - 360}>
        <CTABar genre={genre} />
      </Sequence>

      {/* EQ bar during vibe */}
      <Sequence from={300} durationInFrames={endCardStart - 300}>
        <AbsoluteFill style={{ justifyContent: 'flex-end', alignItems: 'center', paddingBottom: 420, zIndex: 10 }}>
          <EQBar genre={genre} height={70} />
        </AbsoluteFill>
      </Sequence>

      {/* End card (last 5 sec) */}
      <Sequence from={endCardStart}>
        <EndCard serieName={serieName} genre={genre} coverArtSrc={coverArtSrc} />
      </Sequence>
    </AbsoluteFill>
  );
};
