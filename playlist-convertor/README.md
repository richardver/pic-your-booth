# Playlist Convertor

Convert Spotify playlists into DJ-ready MP3 files with BPM detection, key detection, Camelot notation, and Rekordbox/Serato export. Audio is sourced from YouTube via spotdl, not from Spotify.

## Installation

Requires Python 3.10+ and ffmpeg.

```bash
pip install -e .
```

For BPM and key analysis:

```bash
pip install -e ".[analysis]"
```

For Rekordbox XML export:

```bash
pip install -e ".[rekordbox]"
```

Install everything:

```bash
pip install -e ".[analysis,rekordbox]"
```

### Spotify API Setup

spotdl requires Spotify API credentials for individual track lookups. Register an app in the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and add `http://127.0.0.1:9900/` as a redirect URI.

Configure spotdl with user authentication:

```bash
spotdl --user-auth
```

This creates `~/.spotdl/config.json` with `user_auth: true`.

## Usage

### Interactive Wizard

Run with no arguments to start the interactive wizard:

```bash
playlist-convertor
```

The wizard walks you through each option step by step. Choose between downloading a Spotify playlist or researching a DJ/artist by name.

### Download Command

Download a playlist directly with options:

```bash
playlist-convertor download <SPOTIFY_URL> [OPTIONS]
```

**Arguments:**

| Argument | Description |
|----------|-------------|
| `SPOTIFY_URL` | Spotify playlist URL (e.g. `https://open.spotify.com/playlist/...`) |

**Options:**

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `-t, --target` | `rekordbox`, `serato`, `both` | `rekordbox` | Target DJ software |
| `-b, --bitrate` | `128k`, `192k`, `256k`, `320k` | `192k` | Audio bitrate |
| `-f, --format` | `mp3`, `flac`, `wav` | `mp3` | Audio format |
| `-o, --output` | directory path | `output/` | Output directory |
| `--skip-analysis` | flag | off | Skip BPM and key detection |
| `--analyze-mix-points` | flag | off | Detect mix-in/mix-out points (Rekordbox hot cues) |
| `--analyze-energy` | flag | off | Estimate track energy (1-10 scale for set building) |
| `--camelot-in-comments` | flag | off | Write Camelot key to the Comments ID3 field |
| `--dry-run` | flag | off | Show track listing without downloading |
| `--no-fat32` | flag | off | Disable FAT32 filename sanitization |
| `-v, --verbose` | flag | off | Show detailed output |

**Examples:**

```bash
# Download for Rekordbox at 320kbps MP3 (defaults)
playlist-convertor download "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M"

# Download for Serato at 192kbps FLAC
playlist-convertor download "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" \
  -t serato -b 192k -f flac

# Preview tracks without downloading
playlist-convertor download "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" \
  --dry-run

# Download without BPM/key analysis
playlist-convertor download "https://open.spotify.com/playlist/37i9dQZF1DXcBWIGoYBM5M" \
  --skip-analysis
```

### Output Structure

Downloads are organized into dated folders with Rekordbox XML alongside the audio files:

```
output/
  2026-02-25_Luca_rekordbox_120-128bpm/
    01 - CKay, Olamide - WAHALA.mp3
    02 - SPINALL, Fireboy DML - Sere.mp3
    ...
    Luca.xml
```

## Library Management

All downloaded tracks are tracked in a local library for browsing, searching, and set building.

### List All Songs

```bash
playlist-convertor library list [--sort FIELD]
```

Sort options: `title`, `artist`, `bpm`, `key`, `date` (default: `artist`).

### Search the Library

```bash
playlist-convertor library search "QUERY"
```

Searches by title, artist, or album.

### Library Statistics

```bash
playlist-convertor library stats
```

Shows total songs, analyzed count, unique artists, playlists, and per-playlist track counts.

### Clean Up Missing Files

```bash
playlist-convertor library cleanup
```

Removes library entries for files that no longer exist on disk.

## DJ Set Builder

Build DJ sets from your library by filtering on BPM, Camelot key, search terms, or playlist membership. Songs are copied into a numbered set folder ready for export.

### Workflow

```bash
# 1. Start a new set
playlist-convertor set new --name "Friday Night"

# 2. Add songs using filters
playlist-convertor set add --bpm 120-128
playlist-convertor set add --key 8A
playlist-convertor set add --search "Dua Lipa"
playlist-convertor set add --playlist "Summer Hits"

# 3. Review the set
playlist-convertor set show

# 4. Save when ready
playlist-convertor set save
```

### Commands

#### `set new`

Start a new set, clearing any active set in progress.

```bash
playlist-convertor set new [--name "NAME"]
```

If `--name` is omitted, the set uses an auto-generated name when saved.

#### `set add`

Add songs to the active set. Duplicates are automatically skipped. Specify exactly one filter:

```bash
playlist-convertor set add --search "QUERY"      # Search by title/artist/album
playlist-convertor set add --bpm MIN-MAX          # BPM range (e.g. 120-128)
playlist-convertor set add --key KEY              # Camelot key + compatible keys (e.g. 8A)
playlist-convertor set add --playlist "NAME"      # All songs from a playlist
```

When using `--key`, compatible keys are included automatically: same key, +1/-1 on the Camelot Wheel, and the relative major/minor.

#### `set show`

Display the active set with track numbers, BPM, and Camelot keys.

```bash
playlist-convertor set show
```

#### `set save`

Archive the active set to the `output/sets/` folder.

```bash
playlist-convertor set save [--name "Custom Name"]
```

If `--name` is omitted, a name is auto-generated from the creation timestamp, dominant genre, BPM range, and Camelot keys.

#### `set list`

List all saved sets with track counts and creation dates.

```bash
playlist-convertor set list
```

## DJ Research Pipeline

Download tracks by artist or DJ name without needing a Spotify playlist URL. Search Spotify for an artist's top tracks, review the results, and download through the full pipeline.

### Interactive Wizard

```bash
playlist-convertor
# Choose option 2: DJ / Artist Research
# Enter artist name and track count
```

### Command Line

```bash
# From a JSON track list
playlist-convertor research tracklist.json --name "DJ Name"
```

The JSON file should contain an array of `{"artist": "...", "title": "..."}` objects. Tracks are looked up on Spotify; those not found fall back to YouTube search.

## Auto Set Builder

Automatically sequence a DJ set from your library using harmonic mixing, BPM progression, and energy arc presets. The algorithm scores every possible track transition across 4 weighted criteria and selects the optimal sequence.

### How It Works

1. Filters library to analyzed tracks within your BPM range
2. Calculates tracks needed from set duration (with 30-second transition overlaps)
3. For each slot, scores every remaining candidate on: harmonic compatibility (35%), BPM arc (25%), energy arc (25%), BPM smoothness (15%)
4. Rates each transition green (smooth), yellow (workable), or red (rough)
5. Generates a Rekordbox XML and/or Serato M3U8 playlist referencing original file locations (no file copying)

The set display includes fun DJ commentary per transition — opener lines, transition quips rated by quality, peak energy callouts, and closer lines.

### Quick Start

```bash
# One command with all options
playlist-convertor set auto --minutes 60 --preset peak-time --bpm-min 120 --bpm-max 130 -t rekordbox

# Interactive wizard (prompts for each option)
playlist-convertor set auto
```

### Options

| Option | Values | Default | Description |
|--------|--------|---------|-------------|
| `--minutes` | integer | prompted | Set length in minutes |
| `--preset` | `warm-up`, `peak-time`, `marathon`, `chill`, `closer` | `peak-time` | Energy arc preset |
| `--bpm-min` | float | all | Minimum BPM filter |
| `--bpm-max` | float | all | Maximum BPM filter |
| `--start-key` | Camelot key | auto | Starting key (e.g. `8A`) |
| `--playlist` | text (multiple) | all | Filter to specific playlists |
| `-t, --target` | `rekordbox`, `serato`, `both` | `rekordbox` | Target DJ software for export |
| `--analyze-energy` | flag | off | Run energy analysis first |
| `--stems` | flag | off | Use vocal-aware transition scoring |

### Energy Arc Presets

| Preset | Energy Range | Description |
|--------|-------------|-------------|
| `warm-up` | 2-7 | Opening set, gentle build to moderate |
| `peak-time` | 3-10 | Classic 4-act arc, peak at 2/3 |
| `marathon` | 2-10 | Waves with increasing intensity, 3h+ sets |
| `chill` | 2-5 | Lounge / after-party, low throughout |
| `closer` | 7-3 | Last set, start high and wind down |

### Harmonic Distance Tiers

| Tier | Score | Transitions |
|------|-------|-------------|
| 1 (perfect) | 1.0 | Same key, ±1 on wheel, relative major/minor |
| 2 (acceptable) | 0.6 | ±2 on wheel, diagonal (±1 + mode switch) |
| 3 (dramatic) | 0.3 | ±2 + mode switch, ±3 same mode |
| 4 (incompatible) | 0.0 | Everything else |

### Energy Estimation

When `--analyze-energy` is used during download, or tracks have been analyzed with energy data, the set builder uses actual energy scores (1-10) computed from:

- **RMS loudness** (40%) — body median amplitude
- **Spectral centroid** (30%) — brightness / perceived energy
- **Onset density** (30%) — rhythmic intensity (onsets per second)

Without energy data, the algorithm falls back to a BPM-as-energy proxy (70 BPM ≈ 2, 128 BPM ≈ 7, 150 BPM ≈ 9).

## Technical Details

- **Audio source:** YouTube via spotdl (wraps yt-dlp + ffmpeg)
- **Playlist metadata:** Scraped from Spotify embed pages (bypasses restricted Web API)
- **BPM detection:** librosa with automatic 2x/0.5x normalization
- **Key detection:** Krumhansl-Schmuckler algorithm via librosa
- **Key notation:** Classical key in TKEY, Camelot Wheel in TXXX custom field
- **ID3 version:** ID3v2.3 for Serato compatibility
- **Filenames:** FAT32-safe by default for CDJ/controller USB compatibility
- **Mix point detection:** RMS energy analysis, beat-snapped, confidence-scored
- **Energy estimation:** RMS + spectral centroid + onset density → 1-10 scale
- **Auto set building:** Greedy Camelot-guided sequencing with 5 energy arc presets, Rekordbox XML + Serato M3U8 export
- **DJ Research:** Search Spotify by artist name, download top tracks without needing a playlist URL
- **Stem separation:** Optional Demucs-based stem separation with vocal-aware set building
- **Concurrent downloads:** Up to 4 parallel via ThreadPoolExecutor
