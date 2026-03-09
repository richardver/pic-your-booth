"""Stem separation using Meta's Demucs."""

import logging
import subprocess
from pathlib import Path

from .config import DEFAULT_STEM_MODEL, STEMS_ANALYSIS_SECONDS

logger = logging.getLogger(__name__)


def _check_demucs():
    """Raise ImportError with install hint if demucs is not available."""
    try:
        import demucs.pretrained  # noqa: F401
    except ImportError:
        raise ImportError(
            "Stem separation requires the stems extra.\n"
            'Install with: pip install -e ".[stems]"'
        )


def separate_track(
    file_path: Path,
    output_dir: Path,
    model_name: str = DEFAULT_STEM_MODEL,
    bitrate: str = "192k",
) -> dict:
    """Separate a track into vocals and instrumental using Demucs.

    Only processes the middle 60 seconds of the track to save time.
    Outputs only vocals.mp3 and instrumental.mp3.

    Args:
        file_path: Path to the input audio file.
        output_dir: Directory for stem output (e.g. stems/track_name/).
        model_name: Demucs model name.
        bitrate: MP3 bitrate for stem encoding.

    Returns:
        Dict with keys: stems_path, vocals, instrumental.
    """
    _check_demucs()

    from demucs.pretrained import get_model
    from demucs.audio import AudioFile
    from demucs.apply import apply_model
    import torch

    output_dir.mkdir(parents=True, exist_ok=True)

    logger.info("Separating stems: %s (model=%s)", file_path.name, model_name)

    # Load model and audio
    model = get_model(model_name)
    model.eval()
    sample_rate = model.samplerate

    wav = AudioFile(file_path).read(streams=0, samplerate=sample_rate, channels=model.audio_channels)

    # Trim to middle 60 seconds to save processing time
    max_samples = STEMS_ANALYSIS_SECONDS * sample_rate
    total_samples = wav.shape[-1]
    if total_samples > max_samples:
        start = (total_samples - max_samples) // 2
        wav = wav[..., start:start + max_samples]
        logger.info("Trimmed to %ds (middle of track)", STEMS_ANALYSIS_SECONDS)

    ref = wav.mean(0)
    wav = (wav - ref.mean()) / ref.std()

    # Run separation
    with torch.no_grad():
        sources = apply_model(model, wav[None], progress=False)[0]

    # sources shape: (num_sources, channels, samples)
    source_names = model.sources

    source_dict = {}
    for i, name in enumerate(source_names):
        source_dict[name] = sources[i] * ref.std() + ref.mean()

    # Save vocals
    vocals_path = output_dir / "vocals.mp3"
    if "vocals" in source_dict:
        _save_stem_as_mp3(source_dict["vocals"], sample_rate, vocals_path, bitrate)
        logger.debug("Saved vocals: %s", vocals_path)

    # Save instrumental (everything except vocals mixed together)
    instrumental_path = output_dir / "instrumental.mp3"
    instrumental_parts = [source_dict[n] for n in source_names if n != "vocals" and n in source_dict]
    if instrumental_parts:
        instrumental_mix = torch.stack(instrumental_parts).sum(dim=0)
        _save_stem_as_mp3(instrumental_mix, sample_rate, instrumental_path, bitrate)
        logger.debug("Saved instrumental: %s", instrumental_path)

    result = {
        "stems_path": str(output_dir),
        "vocals": str(vocals_path) if "vocals" in source_dict else "",
        "instrumental": str(instrumental_path) if instrumental_parts else "",
    }

    logger.info("Stem separation complete: %s -> %s", file_path.name, output_dir)
    return result


def _save_stem_as_mp3(tensor, sample_rate: int, output_path: Path, bitrate: str) -> None:
    """Save a torch tensor as MP3 via torchaudio, with ffmpeg subprocess fallback."""
    try:
        import torchaudio

        # torchaudio expects (channels, samples)
        torchaudio.save(
            str(output_path),
            tensor.cpu(),
            sample_rate,
            format="mp3",
            compression=_bitrate_to_compression(bitrate),
        )
    except Exception as e:
        logger.debug("torchaudio MP3 save failed (%s), trying ffmpeg fallback", e)
        _save_via_ffmpeg(tensor, sample_rate, output_path, bitrate)


def _bitrate_to_compression(bitrate: str) -> float:
    """Convert bitrate string to torchaudio compression parameter."""
    # torchaudio uses compression as kbps for MP3
    return float(bitrate.rstrip("k"))


def _save_via_ffmpeg(tensor, sample_rate: int, output_path: Path, bitrate: str) -> None:
    """Save tensor as MP3 using ffmpeg subprocess (fallback)."""
    # Write as WAV first, then convert
    wav_path = output_path.with_suffix(".wav")
    try:
        import torchaudio
        torchaudio.save(str(wav_path), tensor.cpu(), sample_rate, format="wav")
    except Exception:
        # Last resort: write raw PCM via numpy
        import numpy as np
        import wave

        audio_np = tensor.cpu().numpy()
        if audio_np.ndim == 2:
            audio_np = audio_np.T  # (samples, channels)
        audio_int16 = (audio_np * 32767).astype(np.int16)

        with wave.open(str(wav_path), "w") as wf:
            channels = audio_int16.shape[1] if audio_int16.ndim == 2 else 1
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())

    # Convert WAV to MP3 via ffmpeg
    try:
        subprocess.run(
            ["ffmpeg", "-y", "-i", str(wav_path), "-b:a", bitrate, str(output_path)],
            capture_output=True,
            check=True,
        )
    finally:
        wav_path.unlink(missing_ok=True)
