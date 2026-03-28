# Video Editor Agent - Release Clip POC Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a working Remotion Release Clip that takes DJ Gianni footage + props and renders a branded 9:16 TikTok video.

**Architecture:** Remotion React project at `video/dj-gianni/tiktok/release-clip/`. Main composition `<ReleaseClip>` orchestrates 5 `<Sequence>` blocks (Hook, Build-up, Drop, Vibe, End Card). Each visual element is a standalone component. Design tokens drive genre-based accent colors.

**Tech Stack:** Remotion 4.x, React 19, TypeScript, Google Fonts (Bebas Neue + Space Grotesk)

---

## Task 1: Scaffold Remotion Project

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/package.json`
- Create: `video/dj-gianni/tiktok/release-clip/tsconfig.json`
- Create: `video/dj-gianni/tiktok/release-clip/remotion.config.ts`
- Create: `video/dj-gianni/tiktok/release-clip/src/Root.tsx`
- Create: `video/dj-gianni/tiktok/release-clip/src/index.ts`

**Step 1: Init Remotion project**

```bash
cd video/dj-gianni/tiktok/release-clip
npm init -y
npm i remotion @remotion/cli @remotion/player react react-dom
npm i -D @types/react typescript @remotion/bundler
```

**Step 2: Create tsconfig.json**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ES2022",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "outDir": "dist",
    "rootDir": "src",
    "baseUrl": ".",
    "paths": { "@/*": ["src/*"] }
  },
  "include": ["src/**/*", "remotion.config.ts"]
}
```

**Step 3: Create remotion.config.ts**

```typescript
import { Config } from "@remotion/cli/config";
Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
```

**Step 4: Create src/index.ts**

```typescript
import { registerRoot } from "remotion";
import { RemotionRoot } from "./Root";
registerRoot(RemotionRoot);
```

**Step 5: Create src/Root.tsx with placeholder composition**

```tsx
import { Composition } from "remotion";

export const RemotionRoot: React.FC = () => {
  return (
    <Composition
      id="ReleaseClip"
      component={() => <div style={{ background: '#050508', width: '100%', height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#f0654a', fontFamily: 'Impact', fontSize: 48 }}>RELEASE CLIP</div>}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        genre: 'afro' as const,
        serieName: 'AFRO BEATS VOL. 2',
        hookText: 'Nieuwe Afro Beats mix is LIVE',
        genreTags: ['Afro Beats', 'Amapiano', 'Afro House'],
        videoSrc: '',
        dropTimestamp: 240,
        coverArtSrc: '',
        durationSec: 25,
      }}
    />
  );
};
```

**Step 6: Verify Remotion Studio opens**

```bash
cd video/dj-gianni/tiktok/release-clip
npx remotion studio
```

Expected: Browser opens, shows "RELEASE CLIP" text on dark background at 1080x1920.

**Step 7: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/
git commit -m "feat(video): scaffold Remotion project for Release Clip POC"
```

---

## Task 2: Design Tokens + Types

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/src/lib/tokens.ts`
- Create: `video/dj-gianni/tiktok/release-clip/src/lib/types.ts`

**Step 1: Create types.ts**

```typescript
export type Genre = 'afro' | 'caribbean' | 'urban';

export interface ReleaseClipProps {
  genre: Genre;
  serieName: string;
  hookText: string;
  genreTags: string[];
  videoSrc: string;
  dropTimestamp: number;
  coverArtSrc: string;
  durationSec: number;
}
```

**Step 2: Create tokens.ts**

```typescript
import { Genre } from './types';

export const GENRE_TOKENS: Record<Genre, { accent: string; dim: string; name: string }> = {
  afro:      { accent: '#f0654a', dim: 'rgba(240,101,74,0.10)', name: 'Afro Beats' },
  caribbean: { accent: '#f5b731', dim: 'rgba(245,183,49,0.10)', name: 'Caribbean' },
  urban:     { accent: '#c084fc', dim: 'rgba(192,132,252,0.10)', name: 'NL Urban' },
};

export const TOKENS = {
  void: '#050508',
  white: '#ededf0',
  muted: 'rgba(237,237,240,0.45)',
  fontDisplay: "'Bebas Neue', Impact, sans-serif",
  fontBody: "'Space Grotesk', system-ui, sans-serif",
};
```

**Step 3: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/src/lib/
git commit -m "feat(video): add design tokens and types for Release Clip"
```

---

## Task 3: VideoBackground Component

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/src/components/VideoBackground.tsx`

**Step 1: Create VideoBackground**

Uses `<OffthreadVideo>` for the behind-the-decks footage with a gradient overlay. Falls back to a dark placeholder when no video is provided (for development).

```tsx
import { AbsoluteFill, OffthreadVideo, staticFile } from 'remotion';
import { TOKENS } from '../lib/tokens';

export const VideoBackground: React.FC<{ src: string }> = ({ src }) => {
  return (
    <AbsoluteFill>
      {src ? (
        <OffthreadVideo
          src={staticFile(src)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      ) : (
        <AbsoluteFill style={{ backgroundColor: TOKENS.void }} />
      )}
      <AbsoluteFill
        style={{
          background: `linear-gradient(180deg, rgba(5,5,8,0.15) 0%, rgba(5,5,8,0.5) 50%, rgba(5,5,8,0.85) 100%)`,
        }}
      />
    </AbsoluteFill>
  );
};
```

**Step 2: Verify in Remotion Studio** — Replace placeholder in Root.tsx with VideoBackground.

**Step 3: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/src/components/VideoBackground.tsx
git commit -m "feat(video): add VideoBackground component with gradient overlay"
```

---

## Task 4: TextHook + GenrePills Components

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/src/components/TextHook.tsx`
- Create: `video/dj-gianni/tiktok/release-clip/src/components/GenrePills.tsx`

**Step 1: Create TextHook** — Spring fade-in text overlay.

```tsx
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const TextHook: React.FC<{ text: string; genre: Genre }> = ({ text, genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const enter = spring({ fps, frame, config: { damping: 200 } });
  const exit = spring({ fps, frame: frame - 60, config: { damping: 200 } });
  const opacity = enter - exit;

  return (
    <div style={{
      fontSize: 62,
      fontWeight: 700,
      fontFamily: TOKENS.fontBody,
      color: TOKENS.white,
      textShadow: '0 4px 20px rgba(0,0,0,0.9)',
      lineHeight: 1.2,
      maxWidth: 800,
      opacity,
      transform: `translateY(${interpolate(enter, [0, 1], [20, 0])}px)`,
    }}>
      {text}
    </div>
  );
};
```

**Step 2: Create GenrePills** — Row of genre tag badges.

```tsx
import { spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const GenrePills: React.FC<{ tags: string[]; genre: Genre }> = ({ tags, genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent, dim } = GENRE_TOKENS[genre];

  return (
    <div style={{ display: 'flex', gap: 16, marginTop: 24 }}>
      {tags.map((tag, i) => {
        const enter = spring({ fps, frame: frame - i * 4, config: { damping: 200 } });
        return (
          <div key={tag} style={{
            fontSize: 28,
            fontWeight: 700,
            letterSpacing: '0.08em',
            textTransform: 'uppercase' as const,
            padding: '8px 24px',
            borderRadius: 999,
            background: dim,
            color: accent,
            backdropFilter: 'blur(8px)',
            opacity: enter,
            transform: `translateY(${(1 - enter) * 10}px)`,
          }}>
            {tag}
          </div>
        );
      })}
    </div>
  );
};
```

**Step 3: Preview in Remotion Studio**

**Step 4: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/src/components/TextHook.tsx video/dj-gianni/tiktok/release-clip/src/components/GenrePills.tsx
git commit -m "feat(video): add TextHook and GenrePills components"
```

---

## Task 5: EQBar + HexBadge Components

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/src/components/EQBar.tsx`
- Create: `video/dj-gianni/tiktok/release-clip/src/components/HexBadge.tsx`

**Step 1: Create EQBar** — 7 animated bars that pulse with a sin wave.

```tsx
import { useCurrentFrame } from 'remotion';
import { GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

const BAR_HEIGHTS = [0.35, 0.65, 1.0, 0.5, 0.8, 0.4, 0.7];

export const EQBar: React.FC<{ genre: Genre; height?: number }> = ({ genre, height = 80 }) => {
  const frame = useCurrentFrame();
  const { accent } = GENRE_TOKENS[genre];

  return (
    <div style={{ display: 'flex', gap: 8, alignItems: 'flex-end', height }}>
      {BAR_HEIGHTS.map((h, i) => {
        const pulse = Math.sin((frame + i * 4) * 0.15) * 0.3 + 0.7;
        return (
          <div key={i} style={{
            width: 8,
            height: `${h * pulse * 100}%`,
            borderRadius: 4,
            background: accent,
            opacity: 0.8,
          }} />
        );
      })}
    </div>
  );
};
```

**Step 2: Create HexBadge** — Hexagonal G logo.

```tsx
import { GENRE_TOKENS, TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const HexBadge: React.FC<{ genre: Genre; size?: number }> = ({ genre, size = 72 }) => {
  const { accent } = GENRE_TOKENS[genre];
  return (
    <div style={{
      width: size,
      height: size,
      clipPath: 'polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%)',
      background: accent,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      fontFamily: TOKENS.fontDisplay,
      fontSize: size * 0.45,
      color: TOKENS.void,
    }}>
      G
    </div>
  );
};
```

**Step 3: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/src/components/EQBar.tsx video/dj-gianni/tiktok/release-clip/src/components/HexBadge.tsx
git commit -m "feat(video): add EQBar and HexBadge components"
```

---

## Task 6: DropMoment Component

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/src/components/DropMoment.tsx`

**Step 1: Create DropMoment** — DJ name flash with spring scale and coral glow.

```tsx
import { AbsoluteFill, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const DropMoment: React.FC<{ serieName: string; genre: Genre }> = ({ serieName, genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent } = GENRE_TOKENS[genre];

  const scale = spring({ fps, frame, config: { damping: 12, stiffness: 200 } });
  const glow = spring({ fps, frame, config: { damping: 200 } });

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      background: `radial-gradient(ellipse at 50% 50%, ${accent}33 0%, transparent 60%)`,
      opacity: glow,
    }}>
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 140,
        letterSpacing: '0.06em',
        color: TOKENS.white,
        textShadow: `0 4px 30px rgba(0,0,0,0.9), 0 0 80px ${accent}66`,
        textAlign: 'center',
        transform: `scale(${scale})`,
      }}>
        DJ GIANNI
      </div>
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 52,
        letterSpacing: '0.1em',
        color: accent,
        textShadow: '0 2px 12px rgba(0,0,0,0.9)',
        marginTop: -8,
        opacity: scale,
      }}>
        {serieName}
      </div>
    </AbsoluteFill>
  );
};
```

**Step 2: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/src/components/DropMoment.tsx
git commit -m "feat(video): add DropMoment component with spring scale and glow"
```

---

## Task 7: CTABar + EndCard Components

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/src/components/CTABar.tsx`
- Create: `video/dj-gianni/tiktok/release-clip/src/components/EndCard.tsx`

**Step 1: Create CTABar** — Slide-up CTA bar.

```tsx
import { interpolate, spring, useCurrentFrame, useVideoConfig } from 'remotion';
import { GENRE_TOKENS, TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';

export const CTABar: React.FC<{ genre: Genre }> = ({ genre }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent, dim } = GENRE_TOKENS[genre];
  const enter = spring({ fps, frame, config: { damping: 200 } });
  const y = interpolate(enter, [0, 1], [100, 0]);

  return (
    <div style={{
      position: 'absolute',
      bottom: 160,
      left: 40,
      right: 180,
      background: `${accent}26`,
      backdropFilter: 'blur(12px)',
      border: `2px solid ${accent}44`,
      borderRadius: 28,
      padding: '28px 40px',
      display: 'flex',
      alignItems: 'center',
      gap: 20,
      transform: `translateY(${y}px)`,
      opacity: enter,
    }}>
      <div>
        <div style={{ fontSize: 32, fontWeight: 700, color: TOKENS.white }}>
          Volledige set op SoundCloud
        </div>
        <div style={{ fontSize: 24, color: TOKENS.muted, marginTop: 4 }}>
          Link in bio
        </div>
      </div>
      <div style={{ marginLeft: 'auto', fontSize: 48, color: accent }}>&#10148;</div>
    </div>
  );
};
```

**Step 2: Create EndCard** — Cover art with glow + CTA.

```tsx
import { AbsoluteFill, Img, spring, useCurrentFrame, useVideoConfig, staticFile } from 'remotion';
import { TOKENS, GENRE_TOKENS } from '../lib/tokens';
import { Genre } from '../lib/types';
import { EQBar } from './EQBar';
import { HexBadge } from './HexBadge';

export const EndCard: React.FC<{
  serieName: string;
  genre: Genre;
  coverArtSrc: string;
}> = ({ serieName, genre, coverArtSrc }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const { accent } = GENRE_TOKENS[genre];
  const enter = spring({ fps, frame, config: { damping: 15, stiffness: 120 } });

  return (
    <AbsoluteFill style={{
      justifyContent: 'center',
      alignItems: 'center',
      background: `radial-gradient(ellipse at 50% 55%, ${accent}33 0%, transparent 55%), ${TOKENS.void}`,
    }}>
      <div style={{ position: 'absolute', top: 120, right: 48 }}>
        <HexBadge genre={genre} />
      </div>
      {coverArtSrc && (
        <Img
          src={staticFile(coverArtSrc)}
          style={{
            width: 540,
            height: 540,
            borderRadius: 48,
            border: `3px solid ${accent}55`,
            boxShadow: `0 20px 60px rgba(0,0,0,0.6), 0 0 40px ${accent}33`,
            transform: `scale(${enter})`,
          }}
        />
      )}
      <div style={{
        fontFamily: TOKENS.fontDisplay,
        fontSize: 80,
        letterSpacing: '0.06em',
        color: TOKENS.white,
        textAlign: 'center',
        marginTop: 48,
        opacity: enter,
      }}>
        {serieName}
      </div>
      <div style={{
        fontSize: 40,
        color: TOKENS.muted,
        marginTop: 12,
        opacity: enter,
      }}>
        Volledige set op SoundCloud
      </div>
      <div style={{
        fontSize: 40,
        fontWeight: 700,
        color: accent,
        letterSpacing: '0.1em',
        textTransform: 'uppercase' as const,
        marginTop: 32,
        display: 'flex',
        alignItems: 'center',
        gap: 16,
        opacity: enter,
      }}>
        LINK IN BIO &#10148;
      </div>
      <div style={{ marginTop: 48 }}>
        <EQBar genre={genre} height={60} />
      </div>
    </AbsoluteFill>
  );
};
```

**Step 3: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/src/components/CTABar.tsx video/dj-gianni/tiktok/release-clip/src/components/EndCard.tsx
git commit -m "feat(video): add CTABar and EndCard components"
```

---

## Task 8: Assemble ReleaseClip Composition

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/src/ReleaseClip.tsx`
- Modify: `video/dj-gianni/tiktok/release-clip/src/Root.tsx`

**Step 1: Create ReleaseClip.tsx** — Main composition that orchestrates all sequences.

```tsx
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
  genre, serieName, hookText, genreTags, videoSrc, dropTimestamp, coverArtSrc, durationSec,
}) => {
  const fps = 30;
  const totalFrames = durationSec * fps;
  const endCardStart = totalFrames - 150; // 5 sec end card

  return (
    <AbsoluteFill style={{ backgroundColor: '#050508' }}>
      {/* Video background — plays throughout until end card */}
      <Sequence durationInFrames={endCardStart}>
        <VideoBackground src={videoSrc} />
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

      {/* THE DROP (0:08 - 0:09) */}
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
```

**Step 2: Update Root.tsx** — Wire up the real composition.

```tsx
import { Composition } from 'remotion';
import { ReleaseClip } from './ReleaseClip';
import { ReleaseClipProps } from './lib/types';

export const RemotionRoot: React.FC = () => {
  return (
    <Composition<ReleaseClipProps>
      id="ReleaseClip"
      component={ReleaseClip}
      durationInFrames={750}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        genre: 'afro',
        serieName: 'AFRO BEATS VOL. 2',
        hookText: 'Nieuwe Afro Beats mix is LIVE',
        genreTags: ['Afro Beats', 'Amapiano', 'Afro House'],
        videoSrc: '',
        dropTimestamp: 240,
        coverArtSrc: '',
        durationSec: 25,
      }}
    />
  );
};
```

**Step 3: Open Remotion Studio and verify all sequences render**

```bash
cd video/dj-gianni/tiktok/release-clip
npx remotion studio
```

Expected: Full clip plays with all 5 sequences in order. No video/cover art yet (empty strings), but all overlays, animations, and transitions should work.

**Step 4: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/src/
git commit -m "feat(video): assemble ReleaseClip composition with all sequences"
```

---

## Task 9: Add Test Assets + Render

**Files:**
- Create: `video/dj-gianni/tiktok/release-clip/public/covers/` (symlink or copy cover art)

**Step 1: Copy a cover art for testing**

```bash
cp docs/images/dj-gianni/mixtape/afro-mixtape-cover.png video/dj-gianni/tiktok/release-clip/public/covers/afro-mixtape-cover.png
```

**Step 2: Update Root.tsx defaultProps with cover art path**

Set `coverArtSrc: 'covers/afro-mixtape-cover.png'`

**Step 3: Verify in Remotion Studio** — End card should now show the actual cover art.

**Step 4: Render to MP4**

```bash
cd video/dj-gianni/tiktok/release-clip
npx remotion render ReleaseClip out/release-clip-afro.mp4
```

Expected: MP4 file created at `out/release-clip-afro.mp4`, 25 seconds, 1080x1920.

**Step 5: Verify genre switching** — Change `genre` to `'caribbean'` in defaultProps, check accent color changes to golden amber in Studio.

**Step 6: Commit**

```bash
git add video/dj-gianni/tiktok/release-clip/
git commit -m "feat(video): add test assets and verify render output"
```

---

## Task 10: Create Video Editor Agent + Knowledge

**Files:**
- Create: `.claude/agents/video-editor.md`
- Create: `.claude/agents/video-editor/knowledge-remotion.md`
- Create: `.claude/agents/video-editor/_index.md`
- Modify: `.claude/agents/_registry.md`
- Modify: `CLAUDE.md`

**Step 1: Create agent definition** (`.claude/agents/video-editor.md`)

Agent frontmatter with name, description, tools. Identity section. Scope boundaries. Collaboration pattern with strategist, social-media, dj-promoter.

**Step 2: Create knowledge-remotion.md**

Remotion API reference, TikTok specs, rendering commands, component patterns, DJ Gianni design tokens. Use Remotion MCP docs as source.

**Step 3: Create _index.md router**

Sub-topic router pointing to knowledge-remotion.md.

**Step 4: Add to registry** — New row in master routing table.

**Step 5: Update CLAUDE.md** — Add video-editor to project structure.

**Step 6: Commit**

```bash
git add .claude/agents/video-editor.md .claude/agents/video-editor/ .claude/agents/_registry.md CLAUDE.md
git commit -m "feat: add video-editor agent with Remotion knowledge"
```

---

## Success Checklist

- [ ] `npx remotion studio` opens at 1080x1920
- [ ] Genre prop switches accent colors (coral / amber / purple)
- [ ] All 5 sequences play in order
- [ ] Cover art shows in end card
- [ ] `npx remotion render` exports working MP4
- [ ] Video-editor agent registered and routable
- [ ] Output matches design storyboard
