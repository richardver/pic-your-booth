export type Genre = 'afro' | 'caribbean' | 'urban';

export interface ReleaseClipProps {
  genre: Genre;
  serieName: string;
  hookText: string;
  genreTags: string[];
  videoSrc: string;
  videoStartSec: number;
  dropTimestamp: number;
  coverArtSrc: string;
  durationSec: number;
}
