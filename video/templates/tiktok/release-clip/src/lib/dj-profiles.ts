import { DJProfile, Genre } from './types';

export interface EffectProfile {
  // Text entrances
  textEntrance: 'slam' | 'fade';
  textEntranceDuration: number;

  // BeatPulse
  beatScaleMult: number;
  beatBrightnessMult: number;

  // Drop
  bassFlashOpacity: number;
  useParticles: boolean;
  screenShakeIntensity: number;
  screenShakeDuration: number;

  // Camera
  hookZoom: [number, number];
  buildUpZoom: [number, number];
  useSlowPan: boolean;

  // Pre-drop
  preDropShake: number;
  preDropBrightnessDip: number;

  // Post-drop
  postDropShake: number;
  postDropSettleScale: number;
  postDropDuration: number;

  // Hits section
  hitCount: number;
  hitZoomScale: number;
  hitInterval: number;

  // Vignette & color
  vignetteMaxOpacity: number;
  warmVibeSection: boolean;

  // Light leak
  lightLeakOpacity: number;

  // Ken Burns (end card)
  kenBurnsRange: [number, number];

  // CTA
  ctaText: string;
  ctaSubtext: string;
  ctaStyle: 'bold' | 'understated';

  // Hook defaults per genre
  defaultHooks: Partial<Record<Genre, string>>;
}

const GIANNI_PROFILE: EffectProfile = {
  textEntrance: 'slam',
  textEntranceDuration: 8,
  beatScaleMult: 0.08,
  beatBrightnessMult: 0.20,
  bassFlashOpacity: 0.50,
  useParticles: true,
  screenShakeIntensity: 18,
  screenShakeDuration: 18,
  hookZoom: [1.0, 1.04],
  buildUpZoom: [1.0, 1.06],
  useSlowPan: true,
  preDropShake: 4,
  preDropBrightnessDip: 0.30,
  postDropShake: 6,
  postDropSettleScale: 1.03,
  postDropDuration: 45,
  hitCount: 5,
  hitZoomScale: 1.12,
  hitInterval: 28,
  vignetteMaxOpacity: 0.25,
  warmVibeSection: true,
  lightLeakOpacity: 0.30,
  kenBurnsRange: [0.95, 1.05],
  ctaText: 'BOEK DJ GIANNI',
  ctaSubtext: 'Populaire data gaan snel',
  ctaStyle: 'bold',
  defaultHooks: {
    afro: 'POV: *DIT* IS HOE\\nJOUW FEEST KLINKT',
    caribbean: 'POV: *DIT* IS HOE\\nJOUW FEEST KLINKT',
    urban: 'POV: *DIT* IS HOE\\nJOUW FEEST KLINKT',
  },
};

const MILO_PROFILE: EffectProfile = {
  textEntrance: 'fade',
  textEntranceDuration: 12,
  beatScaleMult: 0.06,
  beatBrightnessMult: 0.15,
  bassFlashOpacity: 0.30,
  useParticles: false,
  screenShakeIntensity: 8,
  screenShakeDuration: 12,
  hookZoom: [1.0, 1.03],
  buildUpZoom: [1.0, 1.04],
  useSlowPan: false,
  preDropShake: 2,
  preDropBrightnessDip: 0.15,
  postDropShake: 3,
  postDropSettleScale: 1.02,
  postDropDuration: 30,
  hitCount: 3,
  hitZoomScale: 1.06,
  hitInterval: 40,
  vignetteMaxOpacity: 0.20,
  warmVibeSection: false,
  lightLeakOpacity: 0.25,
  kenBurnsRange: [0.97, 1.03],
  ctaText: 'MILØ',
  ctaSubtext: 'bookings: link in bio',
  ctaStyle: 'understated',
  defaultHooks: {
    house: 'deep in the groove.',
    techno: 'deep in the groove.',
    deep: 'deep in the groove.',
  },
};

export const DJ_PROFILES: Record<DJProfile, EffectProfile> = {
  gianni: GIANNI_PROFILE,
  milo: MILO_PROFILE,
};
