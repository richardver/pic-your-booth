"""Pipeline orchestrator - ties all stages together."""

import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import threading

from .config import (
    DEFAULT_BITRATE,
    DEFAULT_DJ_SOFTWARE,
    DEFAULT_FORMAT,
    DEFAULT_MAX_CONCURRENT,
    DEFAULT_STEM_MODEL,
    STEMS_SUBFOLDER,
)
from .downloader import check_dependencies, download_track
from .library import add_playlist, add_song, is_downloaded
from .log_setup import setup_logging
from .organizer import build_track_filename, create_output_dir, rename_with_bpm
from .progress import (
    console,
    create_progress,
    print_analysis_results,
    print_playlist_info,
    print_serato_warnings,
    print_summary,
    print_track_list,
)
from .spotify_client import fetch_tracks

logger = logging.getLogger(__name__)


def run_pipeline(
    spotify_url: str,
    output_dir: Path,
    audio_format: str = DEFAULT_FORMAT,
    bitrate: str = DEFAULT_BITRATE,
    target: str = DEFAULT_DJ_SOFTWARE,
    fat32_safe: bool = True,
    skip_analysis: bool = False,
    camelot_in_comments: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
    analyze_mix_points: bool = False,
    analyze_energy: bool = False,
    analyze_stems: bool = False,
    stem_model: str = DEFAULT_STEM_MODEL,
) -> None:
    """Run the full download pipeline from a Spotify playlist URL."""
    # Check external tools
    if not dry_run:
        check_dependencies()

    # Fetch playlist metadata
    with console.status("[bold blue]Fetching playlist info..."):
        playlist_name, tracks = fetch_tracks(spotify_url)

    _run_pipeline_core(
        playlist_name=playlist_name,
        tracks=tracks,
        spotify_url=spotify_url,
        output_dir=output_dir,
        audio_format=audio_format,
        bitrate=bitrate,
        target=target,
        fat32_safe=fat32_safe,
        skip_analysis=skip_analysis,
        camelot_in_comments=camelot_in_comments,
        dry_run=dry_run,
        verbose=verbose,
        analyze_mix_points=analyze_mix_points,
        analyze_energy=analyze_energy,
        analyze_stems=analyze_stems,
        stem_model=stem_model,
    )


def run_pipeline_from_tracks(
    playlist_name: str,
    tracks: list[dict],
    output_dir: Path,
    audio_format: str = DEFAULT_FORMAT,
    bitrate: str = DEFAULT_BITRATE,
    target: str = DEFAULT_DJ_SOFTWARE,
    fat32_safe: bool = True,
    skip_analysis: bool = False,
    camelot_in_comments: bool = False,
    dry_run: bool = False,
    verbose: bool = False,
    analyze_mix_points: bool = False,
    analyze_energy: bool = False,
    analyze_stems: bool = False,
    stem_model: str = DEFAULT_STEM_MODEL,
) -> None:
    """Run the download pipeline from a pre-built track list.

    Used by the research flow where tracks are already resolved
    (with Spotify URLs or 'Artist - Title' search queries).
    """
    if not dry_run:
        check_dependencies()

    _run_pipeline_core(
        playlist_name=playlist_name,
        tracks=tracks,
        spotify_url=f"research://{playlist_name}",
        output_dir=output_dir,
        audio_format=audio_format,
        bitrate=bitrate,
        target=target,
        fat32_safe=fat32_safe,
        skip_analysis=skip_analysis,
        camelot_in_comments=camelot_in_comments,
        dry_run=dry_run,
        verbose=verbose,
        analyze_mix_points=analyze_mix_points,
        analyze_energy=analyze_energy,
        analyze_stems=analyze_stems,
        stem_model=stem_model,
    )


def _run_pipeline_core(
    playlist_name: str,
    tracks: list[dict],
    spotify_url: str,
    output_dir: Path,
    audio_format: str,
    bitrate: str,
    target: str,
    fat32_safe: bool,
    skip_analysis: bool,
    camelot_in_comments: bool,
    dry_run: bool,
    verbose: bool,
    analyze_mix_points: bool,
    analyze_energy: bool,
    analyze_stems: bool = False,
    stem_model: str = DEFAULT_STEM_MODEL,
) -> None:
    """Core pipeline logic shared by URL-based and track-list-based flows."""
    print_playlist_info(playlist_name, "", len(tracks))
    console.print(f"  [dim]Target: {target} | Bitrate: {bitrate}[/dim]")

    # Warn about YouTube audio quality limitations
    bitrate_num = int(bitrate.rstrip("k"))
    if bitrate_num > 256:
        console.print(
            "  [yellow]Note: YouTube source audio caps at ~128-256kbps. "
            f"{bitrate} output is upsampled, not true {bitrate}.[/yellow]"
        )

    if verbose or dry_run:
        print_track_list(tracks)

    if dry_run:
        console.print("\n[yellow]Dry run - no files downloaded.[/yellow]")
        return

    # Set up output directory: output/YYYY-MM-DD_PlaylistName_target/
    playlist_dir = create_output_dir(output_dir, playlist_name, target=target, fat32_safe=fat32_safe)

    # Set up logging into the output folder
    setup_logging(playlist_dir)
    logger.info("Pipeline started: %s (%d tracks)", playlist_name, len(tracks))

    pipeline_start = time.monotonic()

    # Record playlist in library
    add_playlist(playlist_name, spotify_url, len(tracks))

    # Download tracks with parallel workers
    success = 0
    skipped = 0
    failed = 0
    failed_tracks = []
    downloaded_files = []
    lock = threading.Lock()

    # Split into skip list and download list
    to_download = []
    for i, track in enumerate(tracks, 1):
        new_name = build_track_filename(i, track["artist"], track["title"], audio_format, fat32_safe)
        new_path = playlist_dir / new_name

        lib_entry = is_downloaded(track["spotify_uri"])
        if lib_entry or new_path.exists():
            skipped += 1
            if new_path.exists():
                downloaded_files.append((new_path, track))
            elif lib_entry:
                add_song(
                    spotify_uri=track["spotify_uri"],
                    file_path=Path(lib_entry["file_path"]),
                    title=track["title"],
                    artist=track["artist"],
                    album=track.get("album", ""),
                    playlist_name=playlist_name,
                )
        else:
            to_download.append((i, track, new_path))

    if skipped > 0:
        console.print(f"  [dim]Skipped {skipped} track(s) already in library[/dim]")

    def _download_one(item):
        i, track, new_path = item
        t0 = time.monotonic()
        downloaded_file = download_track(
            track["spotify_url"],
            playlist_dir,
            audio_format,
            bitrate,
        )
        elapsed = time.monotonic() - t0
        label = f"{track['artist']} - {track['title']}"
        if downloaded_file:
            logger.info("Downloaded [%d/%d] in %.1fs: %s", i, len(tracks), elapsed, label)
        else:
            logger.warning("Download FAILED [%d/%d] after %.1fs: %s", i, len(tracks), elapsed, label)
        return i, track, new_path, downloaded_file

    if to_download:
        workers = min(DEFAULT_MAX_CONCURRENT, len(to_download))
        console.print(f"  [dim]Downloading {len(to_download)} track(s) with {workers} parallel workers[/dim]")
        logger.info("Download phase: %d tracks, %d workers", len(to_download), workers)

        dl_start = time.monotonic()
        progress = create_progress()
        with progress:
            task = progress.add_task("Downloading", total=len(to_download))

            with ThreadPoolExecutor(max_workers=workers) as executor:
                futures = {executor.submit(_download_one, item): item for item in to_download}

                for future in as_completed(futures):
                    i, track, new_path, downloaded_file = future.result()

                    with lock:
                        if downloaded_file:
                            final_path = new_path
                            if downloaded_file != new_path:
                                try:
                                    downloaded_file.rename(new_path)
                                except OSError:
                                    # Rename failed — use the file where spotdl left it
                                    final_path = downloaded_file
                            downloaded_files.append((final_path, track))
                            success += 1

                            add_song(
                                spotify_uri=track["spotify_uri"],
                                file_path=final_path,
                                title=track["title"],
                                artist=track["artist"],
                                album=track.get("album", ""),
                                playlist_name=playlist_name,
                            )
                        else:
                            failed += 1
                            failed_tracks.append(f"{track['artist']} - {track['title']}")

                    progress.update(task, description=f"{track['artist']} - {track['title']}")
                    progress.advance(task)

        logger.info(
            "Download phase completed in %.1fs (%d ok, %d failed)",
            time.monotonic() - dl_start, success, failed,
        )

    # Phase 2: Analyze and tag
    analysis_results = []

    if not skip_analysis and downloaded_files:
        from .analyzer import analyze_track
        from .tagger import tag_track

        analysis_start = time.monotonic()
        progress = create_progress()
        with progress:
            parts = ["BPM", "Key"]
            if analyze_mix_points:
                parts.append("Mix Points")
            if analyze_stems:
                parts.extend(["Stems", "Energy (stems)", "Vocals"])
            elif analyze_energy:
                parts.append("Energy")
            analysis_label = "Analyzing " + ", ".join(parts)
            task = progress.add_task(analysis_label, total=len(downloaded_files))

            for file_path, track in downloaded_files:
                progress.update(task, description=f"Analyzing {track['artist']} - {track['title']}")

                if not file_path.exists():
                    logger.warning("File missing, skipping analysis: %s", file_path)
                    analysis_results.append((file_path, track, None))
                    progress.advance(task)
                    continue

                t0 = time.monotonic()
                try:
                    stems_output_dir = (
                        playlist_dir / STEMS_SUBFOLDER / file_path.stem
                        if analyze_stems else None
                    )
                    analysis = analyze_track(
                        file_path,
                        analyze_mix_points=analyze_mix_points,
                        analyze_energy=analyze_energy,
                        analyze_stems=analyze_stems,
                        stem_model=stem_model,
                        stems_output_dir=stems_output_dir,
                    )
                    elapsed = time.monotonic() - t0
                    analysis_results.append((file_path, track, analysis))
                    logger.info(
                        "Analyzed in %.1fs: %s (BPM=%s, Key=%s, Camelot=%s)",
                        elapsed, track["title"],
                        analysis["bpm"], analysis["key"], analysis["camelot_key"],
                    )

                    add_song(
                        spotify_uri=track["spotify_uri"],
                        file_path=file_path,
                        title=track["title"],
                        artist=track["artist"],
                        album=track.get("album", ""),
                        playlist_name=playlist_name,
                        bpm=analysis["bpm"],
                        key=analysis["key"],
                        camelot_key=analysis["camelot_key"],
                        mix_in=analysis.get("mix_in"),
                        mix_out=analysis.get("mix_out"),
                        energy=analysis.get("energy"),
                        duration_ms=track.get("duration_ms"),
                        stems_path=analysis.get("stems_path"),
                        has_stems=analysis.get("has_stems", False),
                        vocal_segments=analysis.get("vocal_segments"),
                        vocal_pct=analysis.get("vocal_pct"),
                        vocal_head_pct=analysis.get("vocal_head_pct"),
                        vocal_tail_pct=analysis.get("vocal_tail_pct"),
                    )
                except Exception as e:
                    elapsed = time.monotonic() - t0
                    logger.warning(
                        "Analysis FAILED in %.1fs: %s - %s",
                        elapsed, track["title"], e, exc_info=True,
                    )
                    if verbose:
                        console.print(f"  [yellow]Analysis failed for {track['title']}: {e}[/yellow]")
                    analysis_results.append((file_path, track, None))

                progress.advance(task)

        logger.info("Analysis phase completed in %.1fs", time.monotonic() - analysis_start)

        # Tag all files
        progress = create_progress()
        with progress:
            task = progress.add_task("Tagging", total=len(analysis_results))

            for file_path, track, analysis in analysis_results:
                progress.update(task, description=f"Tagging {track['artist']} - {track['title']}")

                try:
                    tag_track(
                        file_path,
                        metadata=track,
                        analysis=analysis,
                        camelot_in_comments=camelot_in_comments,
                    )
                except Exception as e:
                    if verbose:
                        console.print(f"  [yellow]Tagging failed for {track['title']}: {e}[/yellow]")

                progress.advance(task)

        if verbose:
            print_analysis_results(analysis_results)

        # Rename folder to include BPM range
        bpms = [a["bpm"] for _, _, a in analysis_results if a and a.get("bpm")]
        if bpms:
            bpm_range = (int(min(bpms)), int(max(bpms)))
            old_dir = playlist_dir
            playlist_dir = rename_with_bpm(playlist_dir, bpm_range, playlist_name, target=target, fat32_safe=fat32_safe)

            # Update file paths if folder was renamed
            if playlist_dir != old_dir:
                logger.info("Renamed folder: %s -> %s", old_dir.name, playlist_dir.name)
                downloaded_files = [
                    (playlist_dir / fp.name, track) for fp, track in downloaded_files
                ]
                analysis_results = [
                    (playlist_dir / fp.name, track, analysis)
                    for fp, track, analysis in analysis_results
                ]
                # Update stems_path references in analysis results
                if analyze_stems:
                    for fp, track, analysis in analysis_results:
                        if analysis and analysis.get("stems_path"):
                            old_stems = Path(analysis["stems_path"])
                            analysis["stems_path"] = str(
                                playlist_dir / STEMS_SUBFOLDER / old_stems.name
                            )

    elif skip_analysis and downloaded_files:
        from .tagger import tag_track

        progress = create_progress()
        with progress:
            task = progress.add_task("Tagging", total=len(downloaded_files))

            for file_path, track in downloaded_files:
                progress.update(task, description=f"Tagging {track['artist']} - {track['title']}")

                try:
                    tag_track(file_path, metadata=track)
                except Exception:
                    pass

                progress.advance(task)

    # Phase 3: DJ software export
    if downloaded_files:
        export_tracks = []
        for file_path, track in downloaded_files:
            export_entry = {**track, "file_path": file_path}
            for fp, t, analysis in analysis_results:
                if fp == file_path and analysis:
                    export_entry["bpm"] = analysis["bpm"]
                    export_entry["key"] = analysis["key"]
                    export_entry["camelot_key"] = analysis["camelot_key"]
                    if analysis.get("mix_in") is not None:
                        export_entry["mix_in"] = analysis["mix_in"]
                    if analysis.get("mix_out") is not None:
                        export_entry["mix_out"] = analysis["mix_out"]
                    break
            export_tracks.append(export_entry)

        # Rekordbox XML export (inside the playlist folder)
        if target in ("rekordbox", "both"):
            from .rekordbox_export import generate_xml

            xml_path = playlist_dir / f"{playlist_name}.xml"
            generate_xml(playlist_name, export_tracks, xml_path)
            console.print(f"  [green]Rekordbox XML:[/green] {xml_path}")

        # Serato M3U8 export + compatibility check
        if target in ("serato", "both"):
            from .serato_export import generate_m3u8
            from .serato_compat import check_playlist

            m3u8_path = playlist_dir / f"{playlist_name}.m3u8"
            generate_m3u8(playlist_name, export_tracks, m3u8_path)
            console.print(f"  [green]Serato M3U8:[/green] {m3u8_path}")

            file_paths = [fp for fp, _ in downloaded_files]
            serato_report = check_playlist(file_paths)
            if serato_report["warnings"] > 0:
                print_serato_warnings(serato_report)
            else:
                console.print("  [green]Serato compatibility: all tracks OK[/green]")

    # Print results
    console.print()
    print_summary(len(tracks), success, skipped, failed, str(playlist_dir))

    if failed_tracks:
        console.print("\n[red]Failed tracks:[/red]")
        for name in failed_tracks:
            console.print(f"  [dim]- {name}[/dim]")

    logger.info(
        "Pipeline complete in %.1fs: %d total, %d downloaded, %d skipped, %d failed",
        time.monotonic() - pipeline_start, len(tracks), success, skipped, failed,
    )
