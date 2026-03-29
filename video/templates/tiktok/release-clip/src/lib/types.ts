export type Genre = 'afro' | 'caribbean' | 'urban' | 'house' | 'techno' | 'deep';

export interface ReleaseClipProps {
  // Brand
  genre: Genre;
  djName: string;           // "DJ GIANNI" or "DJ MILO"
  serieName: string;        // "AFRO BEATS VOL. 2"
  genreTags: string[];      // ["Afro Beats", "Amapiano", "Afro House"]

  // Hook (from strategist)
  hookText: string;         // "STUUR JE PLAYLIST\nIK MAAK ER DIT VAN"

  // Footage (from audio analyzer)
  videoSrc: string;         // path in public/footage/
  videoStartSec: number;    // audio-analyzed start offset
  dropTimestamp: number;    // frame of the drop in the clip

  // Assets
  coverArtSrc: string;      // path in public/covers/

  // Duration
  durationSec: number;      // 15-30
}
