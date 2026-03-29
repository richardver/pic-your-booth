import { Config } from "@remotion/cli/config";

// Maximum quality settings
Config.setVideoImageFormat("png");       // PNG frames (lossless) instead of JPEG
Config.setOverwriteOutput(true);
Config.setPixelFormat("yuv420p");        // Standard pixel format for compatibility
Config.setCrf(18);                       // Near-lossless quality (lower = better, 0-51 scale)
Config.setCodec("h264");                 // H.264 for TikTok compatibility
