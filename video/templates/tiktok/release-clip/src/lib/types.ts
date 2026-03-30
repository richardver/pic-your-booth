export type Genre = 'afro' | 'caribbean' | 'urban' | 'house' | 'techno' | 'deep';

export type DJProfile = 'gianni' | 'milo';

export interface ReleaseClipProps {
  // Brand
  genre: Genre;
  djProfile: DJProfile;
  djName: string;
  serieName: string;
  genreTags: string[];

  // Hook
  hookText: string;

  // Footage — two angles
  videoSrc1: string;       // angle 1: hook, build-up, vibe
  videoSrc2: string;       // angle 2: pre-drop, drop
  videoStartSec: number;   // audio-analyzed start offset
  dropTimestamp: number;    // frame of the drop

  // Energy data from analyzer
  energyData: number[];    // RMS energy per 0.5s window

  // Beat-synced cut points (Milø v2)
  cutPoints?: number[];      // frame numbers for angle switches

  // B-roll sources (for templates with multi-cut support)
  brollSources?: string[];   // paths to B-roll clips in public/footage/broll/

  // Assets
  coverArtSrc: string;

  // Duration
  durationSec: number;
}
