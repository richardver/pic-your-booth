# Remotion Knowledge

Remotion API reference and patterns for PYB video production. Use the Remotion MCP server for detailed docs.

---

## Core Concepts

| Concept | What it does |
|---|---|
| `<Composition>` | Defines a video (width, height, fps, duration, component, defaultProps) |
| `<AbsoluteFill>` | Full-size absolute-positioned container |
| `<Sequence>` | Time-shifts children — `from` delays start, `durationInFrames` limits duration |
| `<Series>` | Display contents after another (auto-sequencing) |
| `useCurrentFrame()` | Returns current frame number (drives all animations) |
| `useVideoConfig()` | Returns { fps, durationInFrames, width, height } |
| `interpolate()` | Maps frame ranges to value ranges (e.g. frame 0-30 -> opacity 0-1) |
| `spring()` | Physics-based animation (0 to 1), configurable damping/stiffness |
| `<OffthreadVideo>` | Renders video without blocking main thread |
| `<Img>` | Renders image and waits for load |
| `staticFile()` | References files in public/ folder |

## Animation Patterns

### Fade In
```tsx
const frame = useCurrentFrame();
const opacity = interpolate(frame, [0, 30], [0, 1], { extrapolateRight: 'clamp' });
```

### Spring Scale
```tsx
const { fps } = useVideoConfig();
const scale = spring({ fps, frame, config: { damping: 12, stiffness: 200 } });
```

### Staggered Enter
```tsx
items.map((item, i) => {
  const enter = spring({ fps, frame: frame - i * 4, config: { damping: 200 } });
  return <div style={{ opacity: Math.max(0, enter) }}>{item}</div>;
});
```

### Enter + Exit
```tsx
const enter = spring({ fps, frame });
const exit = spring({ fps, frame: frame - 60 });
const value = enter - exit; // 0 -> 1 -> 0
```

## DJ Gianni Design Tokens

```typescript
const GENRE_TOKENS = {
  afro:      { accent: '#f0654a', dim: 'rgba(240,101,74,0.10)' },
  caribbean: { accent: '#f5b731', dim: 'rgba(245,183,49,0.10)' },
  urban:     { accent: '#c084fc', dim: 'rgba(192,132,252,0.10)' },
};

const TOKENS = {
  void: '#050508',
  white: '#ededf0',
  muted: 'rgba(237,237,240,0.45)',
  fontDisplay: "'Bebas Neue', Impact, sans-serif",
  fontBody: "'Space Grotesk', system-ui, sans-serif",
};
```

## TikTok Specs

| Attribute | Value |
|---|---|
| Aspect ratio | 9:16 |
| Resolution | 1080x1920 |
| FPS | 30 |
| Duration | 15-60 sec |
| Safe zone bottom | 150px (TikTok UI covers this) |

## Rendering

| Command | Use |
|---|---|
| `npx remotion studio` | Preview in browser with live reload |
| `npx remotion still [entry] [id] [output] --frame=N` | Render single frame as PNG |
| `npx remotion render [entry] [id] [output]` | Render full video as MP4 |
| `npx remotion compositions [entry]` | List all compositions |
| `--props='{"key":"value"}'` | Pass custom inputProps |

## Release Clip Components

| Component | Purpose | Key Props |
|---|---|---|
| `VideoBackground` | OffthreadVideo + gradient overlay | src |
| `TextHook` | Animated text overlay (spring enter/exit) | text, genre |
| `GenrePills` | Staggered genre tag badges | tags, genre |
| `EQBar` | Animated EQ visualizer (sin wave) | genre, height |
| `HexBadge` | Hexagonal G logo | genre, size |
| `DropMoment` | DJ name flash + radial glow | serieName, genre |
| `CTABar` | SoundCloud CTA slide-up | genre |
| `EndCard` | Cover art + title + CTA | serieName, genre, coverArtSrc |
