"""Settings and constants."""

from pathlib import Path

DEFAULT_OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "output"
PLAYLISTS_DIR = "playlists"
SETS_DIR = "sets"
ACTIVE_SET_DIR = "active-set"
DEFAULT_FORMAT = "mp3"
DEFAULT_BITRATE = "192k"
VALID_BITRATES = ("128k", "192k", "256k", "320k")
DEFAULT_DJ_SOFTWARE = "rekordbox"
VALID_DJ_SOFTWARE = ("rekordbox", "serato", "both")
DEFAULT_MAX_CONCURRENT = 4
DURATION_TOLERANCE_SECONDS = 5

# FAT32 illegal characters
FAT32_ILLEGAL_CHARS = r'\/:*?"<>|'

# Max path length for FAT32
MAX_PATH_LENGTH = 255

# Spotify API scopes (read-only)
SPOTIFY_SCOPES = "playlist-read-private playlist-read-collaborative"

# Artwork size from Spotify
ARTWORK_SIZE = 640

# Mix point detection
MIX_POINT_ENERGY_THRESHOLD = 0.70    # fraction of body median energy
MIX_POINT_SUSTAIN_BEATS = 8          # beats of sustained energy to confirm
MIX_POINT_SMOOTHING_SECONDS = 4.0    # RMS smoothing window
MIX_POINT_MIN_TRACK_DURATION = 60    # skip for tracks under 60s
MIX_POINT_FALLBACK_BEATS = 16        # default intro/outro length
MIX_IN_MAX_POSITION = 0.33           # mix-in must be in first third
MIX_OUT_MIN_POSITION = 0.67          # mix-out must be in last third

# Energy estimation
ENERGY_RMS_CEILING = 0.15
ENERGY_CENTROID_CEILING = 5000.0
ENERGY_ONSET_CEILING = 6.0
ENERGY_WEIGHT_RMS = 0.40
ENERGY_WEIGHT_CENTROID = 0.30
ENERGY_WEIGHT_ONSET = 0.30

# Stem separation
DEFAULT_STEM_MODEL = "htdemucs"
VALID_STEM_MODELS = ("htdemucs", "htdemucs_ft")
STEMS_SUBFOLDER = "stems"
STEMS_ANALYSIS_SECONDS = 60          # only process middle 60s of track

# Vocal activity detection
VOCAL_RMS_THRESHOLD = 0.01
VOCAL_MIN_SEGMENT_SECONDS = 2.0
VOCAL_HEAD_SECONDS = 30.0
VOCAL_TAIL_SECONDS = 30.0

# Stem-enhanced energy weights (drums vs bass)
STEM_ENERGY_WEIGHT_DRUMS = 0.55
STEM_ENERGY_WEIGHT_BASS = 0.45

# Auto set builder
DEFAULT_TRANSITION_OVERLAP = 30     # seconds between tracks
DEFAULT_TRACK_DURATION = 210        # 3.5 min fallback
DEFAULT_SET_PRESET = "peak-time"
