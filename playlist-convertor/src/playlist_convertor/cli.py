"""CLI entry point using Click."""

from pathlib import Path

import click

from .config import (
    DEFAULT_BITRATE,
    DEFAULT_DJ_SOFTWARE,
    DEFAULT_FORMAT,
    DEFAULT_OUTPUT_DIR,
    DEFAULT_STEM_MODEL,
    VALID_BITRATES,
    VALID_DJ_SOFTWARE,
    VALID_STEM_MODELS,
)
from .pipeline import run_pipeline, run_pipeline_from_tracks


@click.group(invoke_without_command=True)
@click.version_option()
@click.pass_context
def cli(ctx):
    """Convert Spotify playlists to DJ-ready MP3s."""
    if ctx.invoked_subcommand is None:
        _interactive_wizard()


def _interactive_wizard():
    """Interactive wizard - asks questions step by step."""
    import os
    from rich.panel import Panel
    from rich.prompt import Prompt, Confirm
    from .progress import console

    os.system("clear" if os.name != "nt" else "cls")

    BANNER = (
        "\n"
        "[bold magenta]"
        "     ___  _____   __  __ _ _         ___    ___  _____   _\n"
        "    |   \\\\|_   _| |  \\\\/  (_) |___    ( _ )  |   \\\\|_   _| | |   _  _ __ __ _\n"
        "    | |) | | |   | |\\\\/| | | / _ \\\\   / _ \\\\  | |) | | |   | |__| || / _/ _` |\n"
        "    |___/  |_|   |_|  |_|_|_\\\\___/   \\\\___/  |___/  |_|   |____|\\\\_,_\\\\__\\\\__,_|\n"
        "[/bold magenta]\n"
        "[dim]"
        "        ______________________________________________________\n"
        "       |  .----.  |  .----.  |    _____                      |\n"
        "       | | /--\\\\ | | | /--\\\\ | |   / ___ \\\\   Spotify Playlist  |\n"
        "       | ||    || | ||    || |  | /   \\\\ |  to DJ-Ready MP3s  |\n"
        "       | | \\\\--/ | | | \\\\--/ | |  | \\\\___/ |                    |\n"
        "       |  .----.  |  .----.  |   \\\\_____/   [/dim][bold cyan]v0.1.0[/bold cyan][dim]            |\n"
        "       |__________|__________|____________________________ __|\n"
        "[/dim]"
    )
    console.print(BANNER)

    # 1. Mode selection
    console.print("\n[bold cyan]How would you like to start?[/bold cyan]")
    console.print("  [dim]1[/dim] Spotify Playlist URL")
    console.print("  [dim]2[/dim] DJ / Artist Research")
    mode_choice = Prompt.ask("  Choose", choices=["1", "2"], default="1")

    # Mode-specific input
    spotify_url = None
    research_tracks = None
    research_name = None

    if mode_choice == "1":
        spotify_url = Prompt.ask("\n[bold cyan]Spotify playlist URL[/bold cyan]")
        if not spotify_url or "spotify" not in spotify_url.lower():
            console.print("[red]Invalid Spotify URL[/red]")
            return

    else:
        import json
        from rich.table import Table
        from .library import make_synthetic_uri
        from .track_search import search_artist_top_tracks, search_tracks

        research_name = Prompt.ask("\n[bold cyan]Artist / DJ name[/bold cyan]")
        if not research_name.strip():
            console.print("[red]Name is required.[/red]")
            return

        track_count = int(Prompt.ask(
            "[bold cyan]How many tracks?[/bold cyan]",
            default="30",
        ))

        # Try Spotify artist search first
        console.print()
        with console.status(f"[bold blue]Searching Spotify for {research_name}..."):
            research_tracks = search_artist_top_tracks(research_name.strip(), limit=track_count)

        if not research_tracks:
            # Artist not found — fall back to track list JSON
            console.print(f"[yellow]'{research_name}' not found as a Spotify artist.[/yellow]")
            console.print("  [dim]This DJ may play other artists' music. Load a track list instead.[/dim]\n")

            tracklist_path = Prompt.ask(
                "[bold cyan]Path to track list JSON[/bold cyan] [dim](or Enter to cancel)[/dim]",
                default="",
            )
            if not tracklist_path:
                console.print("[dim]Cancelled.[/dim]")
                return

            tracklist_file = Path(tracklist_path)
            if not tracklist_file.exists():
                console.print(f"[red]File not found: {tracklist_file}[/red]")
                return

            try:
                raw = json.loads(tracklist_file.read_text())
            except json.JSONDecodeError as e:
                console.print(f"[red]Invalid JSON: {e}[/red]")
                return

            if not isinstance(raw, list) or not raw:
                console.print("[red]JSON must contain a non-empty array of {\"artist\", \"title\"} objects.[/red]")
                return

            # Look up Spotify URLs for each track
            console.print(f"\n  Searching Spotify for {len(raw)} tracks...")
            with console.status("[bold blue]Searching Spotify..."):
                found, not_found = search_tracks(raw)

            # Build pipeline dicts for not-found tracks
            not_found_dicts = []
            for item in not_found:
                artist, title = item["artist"], item["title"]
                not_found_dicts.append({
                    "title": title,
                    "artist": artist,
                    "album": "",
                    "track_number": 0,
                    "year": "",
                    "duration_ms": 0,
                    "artwork_url": None,
                    "spotify_uri": make_synthetic_uri(artist, title),
                    "spotify_url": f"{artist} - {title}",
                })

            research_tracks = found + not_found_dicts
            for i, track in enumerate(research_tracks, 1):
                track["track_number"] = i

            # Show results table
            table = Table(show_header=True, header_style="bold")
            table.add_column("#", style="dim", width=4)
            table.add_column("Artist")
            table.add_column("Title")
            table.add_column("Source", style="dim")
            for i, track in enumerate(research_tracks, 1):
                source = "Spotify" if track["spotify_uri"].startswith("spotify:") else "YouTube search"
                table.add_row(str(i), track["artist"], track["title"], source)
            console.print(table)
            console.print(
                f"\n  [green]{len(found)}[/green] found on Spotify, "
                f"[yellow]{len(not_found_dicts)}[/yellow] will use YouTube search"
            )
        else:
            # Artist found — show top tracks
            table = Table(show_header=True, header_style="bold")
            table.add_column("#", style="dim", width=4)
            table.add_column("Title")
            table.add_column("Album", style="dim")
            for i, track in enumerate(research_tracks, 1):
                table.add_row(str(i), track["title"], track["album"])
            console.print(table)
            console.print(f"\n  [green]{len(research_tracks)}[/green] tracks found for [bold]{research_name}[/bold]")

        if not Confirm.ask("\n[bold]Use these tracks?[/bold]", default=True):
            console.print("[dim]Cancelled.[/dim]")
            return

    # 2. Target DJ software
    console.print("\n[bold cyan]Target DJ software[/bold cyan]")
    console.print("  [dim]1[/dim] Rekordbox")
    console.print("  [dim]2[/dim] Serato")
    console.print("  [dim]3[/dim] Both")
    target_choice = Prompt.ask("  Choose", choices=["1", "2", "3"], default="1")
    target = {"1": "rekordbox", "2": "serato", "3": "both"}[target_choice]

    # Audio quality and format — fixed defaults
    bitrate = DEFAULT_BITRATE
    audio_format = DEFAULT_FORMAT

    # 3. Output directory (always use default)
    output_dir = DEFAULT_OUTPUT_DIR

    # 4. BPM/Key analysis
    analyze = Confirm.ask("\n[bold cyan]Analyze BPM & key?[/bold cyan]", default=True)

    # 5. Mix point detection (only when analysis is enabled)
    analyze_mix = False
    if analyze:
        analyze_mix = Confirm.ask(
            "[bold cyan]Detect mix-in/mix-out points?[/bold cyan] [dim](hot cues for Rekordbox)[/dim]",
            default=False,
        )

    # 6. Stem separation (only when analysis is enabled AND demucs installed)
    analyze_stems = False
    if analyze:
        try:
            import demucs.pretrained  # noqa: F401
            analyze_stems = Confirm.ask(
                "[bold cyan]Separate stems?[/bold cyan] [dim](vocals/drums/bass/other)[/dim]",
                default=False,
            )
        except ImportError:
            console.print("  [dim]Stem separation not available (install with: pip install -e \".[stems]\")[/dim]")

    # Summary
    analyze_label = "yes + mix points" if analyze_mix else "yes" if analyze else "no"

    if mode_choice == "1":
        source_label = spotify_url
    else:
        source_label = f"{research_name} ({len(research_tracks)} tracks)"

    summary_lines = [
        f"[bold]Source:[/bold]  {source_label}",
        f"[bold]Target:[/bold]  {target}",
        f"[bold]Quality:[/bold] {bitrate} {audio_format}",
        f"[bold]Output:[/bold]  {output_dir}",
        f"[bold]Analyze:[/bold] {analyze_label}",
    ]
    if analyze_stems:
        summary_lines.append("[bold]Stems:[/bold]   yes")

    console.print()
    console.print(Panel(
        "\n".join(summary_lines),
        title="[bold]Ready to download",
        border_style="green",
    ))

    if not Confirm.ask("\n[bold]Start download?[/bold]", default=True):
        console.print("[dim]Cancelled.[/dim]")
        return

    console.print()
    if mode_choice == "1":
        run_pipeline(
            spotify_url=spotify_url,
            output_dir=output_dir,
            audio_format=audio_format,
            bitrate=bitrate,
            target=target,
            skip_analysis=not analyze,
            analyze_mix_points=analyze_mix,
            analyze_stems=analyze_stems,
        )
    else:
        run_pipeline_from_tracks(
            playlist_name=research_name,
            tracks=research_tracks,
            output_dir=output_dir,
            audio_format=audio_format,
            bitrate=bitrate,
            target=target,
            skip_analysis=not analyze,
            analyze_mix_points=analyze_mix,
            analyze_stems=analyze_stems,
        )


@cli.command()
@click.argument("spotify_url")
@click.option("-o", "--output", type=click.Path(path_type=Path), default=DEFAULT_OUTPUT_DIR, help="Output directory")
@click.option("-f", "--format", "audio_format", type=click.Choice(["mp3", "flac", "wav"]), default=DEFAULT_FORMAT, help="Audio format")
@click.option("-b", "--bitrate", type=click.Choice(list(VALID_BITRATES)), default=DEFAULT_BITRATE, help="Audio bitrate")
@click.option("-t", "--target", type=click.Choice(list(VALID_DJ_SOFTWARE)), default=DEFAULT_DJ_SOFTWARE, help="DJ software target")
@click.option("--skip-analysis", is_flag=True, help="Skip BPM/key detection")
@click.option("--analyze-mix-points", is_flag=True, help="Detect mix-in/mix-out points (Rekordbox hot cues)")
@click.option("--camelot-in-comments", is_flag=True, help="Write Camelot key to Comments field")
@click.option("--dry-run", is_flag=True, help="Show tracks without downloading")
@click.option("--no-fat32", is_flag=True, help="Disable FAT32 filename sanitization")
@click.option("--stems", "analyze_stems", is_flag=True, help="Separate stems (vocals/drums/bass/other)")
@click.option("--model", "stem_model", type=click.Choice(list(VALID_STEM_MODELS)), default=DEFAULT_STEM_MODEL, help="Demucs model")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed output")
def download(
    spotify_url: str,
    output: Path,
    audio_format: str,
    bitrate: str,
    target: str,
    skip_analysis: bool,
    analyze_mix_points: bool,
    camelot_in_comments: bool,
    dry_run: bool,
    no_fat32: bool,
    analyze_stems: bool,
    stem_model: str,
    verbose: bool,
):
    """Download a Spotify playlist as DJ-ready audio files."""
    run_pipeline(
        spotify_url=spotify_url,
        output_dir=output,
        audio_format=audio_format,
        bitrate=bitrate,
        target=target,
        fat32_safe=not no_fat32,
        skip_analysis=skip_analysis,
        analyze_mix_points=analyze_mix_points,
        camelot_in_comments=camelot_in_comments,
        dry_run=dry_run,
        verbose=verbose,
        analyze_stems=analyze_stems,
        stem_model=stem_model,
    )


@cli.command()
@click.argument("tracklist", type=click.Path(exists=True, path_type=Path))
@click.option("--name", required=True, help="Name for the playlist/collection (e.g. DJ name)")
@click.option("-o", "--output", type=click.Path(path_type=Path), default=DEFAULT_OUTPUT_DIR, help="Output directory")
@click.option("-t", "--target", type=click.Choice(list(VALID_DJ_SOFTWARE)), default=DEFAULT_DJ_SOFTWARE, help="DJ software target")
@click.option("--skip-analysis", is_flag=True, help="Skip BPM/key detection")
@click.option("--analyze-mix-points", is_flag=True, help="Detect mix-in/mix-out points")
@click.option("--analyze-energy", is_flag=True, help="Run energy analysis")
@click.option("--dry-run", is_flag=True, help="Show tracks without downloading")
@click.option("-v", "--verbose", is_flag=True, help="Show detailed output")
def research(
    tracklist: Path,
    name: str,
    output: Path,
    target: str,
    skip_analysis: bool,
    analyze_mix_points: bool,
    analyze_energy: bool,
    dry_run: bool,
    verbose: bool,
):
    """Download tracks from a research JSON file.

    TRACKLIST is a JSON file with an array of {"artist": "...", "title": "..."} objects.
    Spotify URLs are looked up automatically. Tracks not found on Spotify are
    downloaded via YouTube search using 'Artist - Title' as the query.
    """
    import json
    from rich.table import Table
    from rich.prompt import Confirm
    from .library import make_synthetic_uri
    from .track_search import search_tracks
    from .progress import console

    # Load track list
    raw = json.loads(tracklist.read_text())
    if not isinstance(raw, list) or not raw:
        console.print("[red]JSON file must contain a non-empty array of track objects.[/red]")
        return

    console.print(f"\n[bold]{name}[/bold] — {len(raw)} tracks from {tracklist.name}")

    # Look up Spotify URLs
    with console.status("[bold blue]Searching Spotify..."):
        found, not_found = search_tracks(raw)

    # Build pipeline-ready track dicts for not-found tracks
    not_found_dicts = []
    for item in not_found:
        artist = item["artist"]
        title = item["title"]
        not_found_dicts.append({
            "title": title,
            "artist": artist,
            "album": "",
            "track_number": 0,
            "year": "",
            "duration_ms": 0,
            "artwork_url": None,
            "spotify_uri": make_synthetic_uri(artist, title),
            "spotify_url": f"{artist} - {title}",
        })

    # Combine and assign track numbers
    all_tracks = found + not_found_dicts
    for i, track in enumerate(all_tracks, 1):
        track["track_number"] = i

    # Show summary table
    table = Table(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=4)
    table.add_column("Artist")
    table.add_column("Title")
    table.add_column("Source", style="dim")

    for i, track in enumerate(all_tracks, 1):
        source = "Spotify" if track["spotify_uri"].startswith("spotify:") else "YouTube search"
        table.add_row(str(i), track["artist"], track["title"], source)

    console.print(table)
    console.print(
        f"\n  [green]{len(found)}[/green] found on Spotify, "
        f"[yellow]{len(not_found_dicts)}[/yellow] will use YouTube search"
    )

    if not dry_run and not Confirm.ask("\n[bold]Start download?[/bold]", default=True):
        console.print("[dim]Cancelled.[/dim]")
        return

    console.print()
    run_pipeline_from_tracks(
        playlist_name=name,
        tracks=all_tracks,
        output_dir=output,
        target=target,
        skip_analysis=skip_analysis,
        analyze_mix_points=analyze_mix_points,
        analyze_energy=analyze_energy,
        dry_run=dry_run,
        verbose=verbose,
    )


@cli.group()
def library():
    """Manage the song library."""


@library.command("list")
@click.option("--sort", type=click.Choice(["title", "artist", "bpm", "key", "date"]), default="artist", help="Sort by field")
def library_list(sort: str):
    """List all songs in the library."""
    from rich.table import Table
    from .library import get_all_songs
    from .progress import console

    songs = get_all_songs()
    if not songs:
        console.print("[dim]Library is empty. Download a playlist first.[/dim]")
        return

    sort_keys = {
        "title": lambda s: s["title"].lower(),
        "artist": lambda s: s["artist"].lower(),
        "bpm": lambda s: s.get("bpm") or 0,
        "key": lambda s: s.get("camelot_key") or "",
        "date": lambda s: s.get("downloaded_at") or "",
    }
    songs.sort(key=sort_keys[sort])

    table = Table(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title")
    table.add_column("Artist")
    table.add_column("BPM", justify="right")
    table.add_column("Key")
    table.add_column("Camelot", style="bold cyan")
    table.add_column("Stems", justify="center")
    table.add_column("Playlists", style="dim")

    for i, song in enumerate(songs, 1):
        stems_icon = "[green]Y[/green]" if song.get("has_stems") else "-"
        table.add_row(
            str(i),
            song["title"],
            song["artist"],
            str(int(song["bpm"])) if song.get("bpm") else "-",
            song.get("key") or "-",
            song.get("camelot_key") or "-",
            stems_icon,
            ", ".join(song.get("playlists", [])),
        )

    console.print(table)
    console.print(f"\n[dim]{len(songs)} songs in library[/dim]")


@library.command("search")
@click.argument("query")
def library_search(query: str):
    """Search the library by title, artist, or album."""
    from rich.table import Table
    from .library import search
    from .progress import console

    results = search(query)
    if not results:
        console.print(f"[dim]No results for '{query}'[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Title")
    table.add_column("Artist")
    table.add_column("BPM", justify="right")
    table.add_column("Key")
    table.add_column("Camelot", style="bold cyan")
    table.add_column("File", style="dim")

    for song in results:
        table.add_row(
            song["title"],
            song["artist"],
            str(int(song["bpm"])) if song.get("bpm") else "-",
            song.get("key") or "-",
            song.get("camelot_key") or "-",
            Path(song["file_path"]).name,
        )

    console.print(table)
    console.print(f"\n[dim]{len(results)} result(s)[/dim]")


@library.command("stats")
def library_stats():
    """Show library statistics."""
    from rich.panel import Panel
    from rich.table import Table
    from .library import get_stats, get_all_playlists
    from .progress import console

    stats = get_stats()
    playlists = get_all_playlists()

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()
    table.add_row("Total songs", str(stats["total_songs"]))
    table.add_row("Analyzed", str(stats["analyzed"]))
    table.add_row("With stems", str(stats["with_stems"]))
    table.add_row("Unique artists", str(stats["unique_artists"]))
    table.add_row("Playlists", str(stats["total_playlists"]))
    console.print(Panel(table, title="[bold]Library Stats", border_style="blue"))

    if playlists:
        pl_table = Table(show_header=True, header_style="bold")
        pl_table.add_column("Playlist")
        pl_table.add_column("Tracks", justify="right")
        pl_table.add_column("Last synced", style="dim")

        for name, info in playlists.items():
            synced = info.get("last_synced", "")[:10]
            pl_table.add_row(name, str(info["track_count"]), synced)

        console.print(pl_table)


@library.command("cleanup")
def library_cleanup():
    """Remove library entries for files that no longer exist."""
    from .library import remove_missing
    from .progress import console

    removed = remove_missing()
    if removed:
        console.print(f"[yellow]Removed {removed} missing file(s) from library[/yellow]")
    else:
        console.print("[green]Library is clean - all files exist[/green]")


@cli.group("set")
def djset():
    """Build DJ sets from your library."""


@djset.command("new")
@click.option("--name", default="", help="Optional name for the set")
def set_new(name: str):
    """Start a new set (clears active set)."""
    from .setbuilder import new_set
    from .progress import console

    path = new_set(name)
    console.print(f"[green]New set started:[/green] {path}")
    if name:
        console.print(f"  [dim]Name: {name}[/dim]")


@djset.command("add")
@click.option("--search", "query", default="", help="Search by title/artist/album")
@click.option("--bpm", default="", help="BPM range (e.g. 120-128)")
@click.option("--key", "camelot_key", default="", help="Camelot key + compatible (e.g. 5A)")
@click.option("--playlist", "playlist_name", default="", help="Add all songs from a playlist")
def set_add(query: str, bpm: str, camelot_key: str, playlist_name: str):
    """Add songs to the active set."""
    from .setbuilder import add_by_bpm, add_by_key, add_by_playlist, add_by_search
    from .progress import console

    added = []

    if query:
        added = add_by_search(query)
    elif bpm:
        parts = bpm.split("-")
        bpm_min = float(parts[0])
        bpm_max = float(parts[1]) if len(parts) > 1 else bpm_min
        added = add_by_bpm(bpm_min, bpm_max)
    elif camelot_key:
        added = add_by_key(camelot_key.upper())
    elif playlist_name:
        added = add_by_playlist(playlist_name)
    else:
        console.print("[red]Specify --search, --bpm, --key, or --playlist[/red]")
        return

    if added:
        console.print(f"[green]Added {len(added)} song(s) to set:[/green]")
        for song in added:
            bpm_str = f" [{int(song['bpm'])}bpm]" if song.get("bpm") else ""
            key_str = f" [{song['camelot_key']}]" if song.get("camelot_key") else ""
            console.print(f"  {song['artist']} - {song['title']}{bpm_str}{key_str}")
    else:
        console.print("[dim]No new songs added (already in set or no matches)[/dim]")


@djset.command("show")
def set_show():
    """Show songs in the active set."""
    from rich.table import Table
    from rich.panel import Panel
    from .setbuilder import get_set_songs, generate_set_name
    from .progress import console

    songs = get_set_songs()
    if not songs:
        console.print("[dim]Active set is empty. Use 'set new' then 'set add'.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title")
    table.add_column("Artist")
    table.add_column("BPM", justify="right")
    table.add_column("Camelot", style="bold cyan")

    for i, song in enumerate(songs, 1):
        table.add_row(
            str(i),
            song["title"],
            song["artist"],
            str(int(song["bpm"])) if song.get("bpm") else "-",
            song.get("camelot_key") or "-",
        )

    auto_name = generate_set_name()
    console.print(Panel(table, title=f"[bold]Active Set ({len(songs)} tracks)", border_style="magenta"))
    console.print(f"  [dim]Auto-name: {auto_name}[/dim]")


@djset.command("save")
@click.option("--name", default="", help="Custom name (default: auto-generated from tags)")
def set_save(name: str):
    """Save the active set to the sets folder."""
    from .setbuilder import save_set
    from .progress import console

    try:
        path = save_set(name)
        console.print(f"[green]Set saved:[/green] {path}")
    except ValueError as e:
        console.print(f"[red]{e}[/red]")


@djset.command("list")
def set_list():
    """List all saved sets."""
    from rich.table import Table
    from .setbuilder import list_sets
    from .progress import console

    sets = list_sets()
    if not sets:
        console.print("[dim]No saved sets yet.[/dim]")
        return

    table = Table(show_header=True, header_style="bold")
    table.add_column("Name")
    table.add_column("Tracks", justify="right")
    table.add_column("Created", style="dim")

    for s in sets:
        table.add_row(s["name"], str(s["tracks"]), s.get("created", "-"))

    console.print(table)


@djset.command("auto")
@click.option("--minutes", type=int, help="Set length in minutes")
@click.option(
    "--preset",
    type=click.Choice(["warm-up", "peak-time", "marathon", "chill", "closer"]),
    default=None,
    help="Energy arc preset",
)
@click.option("--bpm-min", type=float, help="Minimum BPM")
@click.option("--bpm-max", type=float, help="Maximum BPM")
@click.option("--start-key", help="Starting Camelot key (e.g. 8A)")
@click.option("--playlist", multiple=True, help="Filter to specific playlists")
@click.option("-t", "--target", type=click.Choice(list(VALID_DJ_SOFTWARE)), default=None, help="DJ software target")
@click.option("--analyze-energy", is_flag=True, help="Run energy analysis on library tracks first")
@click.option("--stems", "use_stems", is_flag=True, help="Use vocal-aware transition scoring")
def set_auto(minutes, preset, bpm_min, bpm_max, start_key, playlist, target, analyze_energy, use_stems):
    """Auto-build a DJ set from your library using harmonic mixing."""
    from rich.prompt import Prompt, Confirm
    from .arc_presets import list_presets
    from .setbuilder import auto_build_set
    from .progress import console, print_auto_set, print_energy_curve, print_set_summary

    # Interactive wizard when --minutes is not provided
    if minutes is None:
        minutes = int(Prompt.ask(
            "\n[bold cyan]How long is your set? (minutes)[/bold cyan]",
            default="60",
        ))

    if preset is None:
        console.print("\n[bold cyan]Energy arc preset[/bold cyan]")
        presets = list_presets()
        for i, p in enumerate(presets, 1):
            console.print(f"  [dim]{i}[/dim] {p['name']} — {p['description']} (energy {p['energy_range']})")
        choice = Prompt.ask("  Choose", choices=[str(i) for i in range(1, len(presets) + 1)], default="2")
        preset = presets[int(choice) - 1]["key"]

    if bpm_min is None and bpm_max is None:
        bpm_input = Prompt.ask(
            "\n[bold cyan]BPM range?[/bold cyan] [dim](e.g. 120-130, or press Enter for all)[/dim]",
            default="",
        )
        if bpm_input:
            parts = bpm_input.replace(" ", "").split("-")
            bpm_min = float(parts[0])
            bpm_max = float(parts[1]) if len(parts) > 1 else bpm_min + 10

    if start_key is None:
        start_key_input = Prompt.ask(
            "[bold cyan]Starting Camelot key?[/bold cyan] [dim](e.g. 8A, or press Enter to skip)[/dim]",
            default="",
        )
        if start_key_input:
            start_key = start_key_input.strip().upper()

    playlists = list(playlist) if playlist else None
    if not playlists:
        from .library import get_all_playlists
        available = get_all_playlists()
        if available:
            # Suggest the most recently synced playlist as default
            last_playlist = max(
                available.items(),
                key=lambda x: x[1].get("last_synced", ""),
            )[0]
            for name, info in available.items():
                synced = info.get("last_synced", "")[:10]
                console.print(f"  [dim]- {name} ({info['track_count']} tracks, synced {synced})[/dim]")
            pl_input = Prompt.ask(
                "[bold cyan]Filter to playlists?[/bold cyan] [dim](comma-separated, or Enter for all)[/dim]",
                default=last_playlist,
            )
            if pl_input and pl_input != last_playlist:
                playlists = [p.strip() for p in pl_input.split(",")]
            elif pl_input:
                playlists = [pl_input]

    # Target DJ software
    if target is None:
        console.print("\n[bold cyan]Target DJ software[/bold cyan]")
        console.print("  [dim]1[/dim] Rekordbox")
        console.print("  [dim]2[/dim] Serato")
        console.print("  [dim]3[/dim] Both")
        target_choice = Prompt.ask("  Choose", choices=["1", "2", "3"], default="1")
        target = {"1": "rekordbox", "2": "serato", "3": "both"}[target_choice]

    # Summary
    from rich.panel import Panel
    console.print()
    summary = (
        f"[bold]Duration:[/bold]  {minutes} min\n"
        f"[bold]Preset:[/bold]    {preset}\n"
        f"[bold]BPM:[/bold]       {f'{bpm_min:.0f}-{bpm_max:.0f}' if bpm_min else 'all'}\n"
        f"[bold]Start:[/bold]     {start_key or 'auto'}\n"
        f"[bold]Playlists:[/bold] {', '.join(playlists) if playlists else 'all'}\n"
        f"[bold]Target:[/bold]    {target}"
    )
    console.print(Panel(summary, title="[bold]Auto Set Builder", border_style="magenta"))

    if not Confirm.ask("\n[bold]Build set?[/bold]", default=True):
        console.print("[dim]Cancelled.[/dim]")
        return

    # Build
    console.print()
    with console.status("[bold blue]Building set..."):
        result = auto_build_set(
            set_minutes=minutes,
            preset_name=preset,
            bpm_min=bpm_min,
            bpm_max=bpm_max,
            start_key=start_key,
            playlists=playlists,
            use_vocal_scoring=use_stems,
            target=target,
        )

    if not result.tracks:
        console.print("[red]No tracks matched your filters. Try a wider BPM range or download more music.[/red]")
        return

    # Display results
    print_auto_set(result.tracks, result.transitions, result.preset, result.estimated_minutes)
    print_energy_curve(result.tracks, result.preset)
    console.print()
    print_set_summary(result)
    # Show export paths
    if result.xml_path:
        console.print(f"\n  [green]Rekordbox XML:[/green] {result.xml_path}")
    if result.m3u8_path:
        console.print(f"  [green]Serato M3U8:[/green] {result.m3u8_path}")
    if result.serato_report:
        from .progress import print_serato_warnings
        if result.serato_report["warnings"] > 0:
            print_serato_warnings(result.serato_report)
        else:
            console.print("  [green]Serato compatibility: all tracks OK[/green]")


@cli.group("stems")
def stems_group():
    """Separate tracks into stems (vocals/drums/bass/other)."""


@stems_group.command("playlist")
@click.argument("playlist_ref")
@click.option("--model", type=click.Choice(list(VALID_STEM_MODELS)), default=DEFAULT_STEM_MODEL, help="Demucs model")
def stems_playlist(playlist_ref: str, model: str):
    """Separate stems for all tracks in a downloaded playlist.

    PLAYLIST_REF is the playlist name or Spotify URL.
    """
    from .library import get_all_songs
    from .stems import separate_track
    from .vocal_activity import detect_vocal_activity
    from .library import add_song
    from .config import STEMS_SUBFOLDER
    from .progress import console, create_progress

    # Find tracks for this playlist
    songs = get_all_songs()
    matches = []
    for song in songs:
        playlists = song.get("playlists", [])
        if playlist_ref in playlists or playlist_ref.lower() in [p.lower() for p in playlists]:
            if Path(song["file_path"]).exists():
                matches.append(song)

    if not matches:
        console.print(f"[red]No tracks found for playlist '{playlist_ref}'[/red]")
        console.print("[dim]Use 'pconv library list' to see available playlists.[/dim]")
        return

    console.print(f"\n[bold]Separating stems for {len(matches)} tracks[/bold] from '{playlist_ref}'")

    progress = create_progress()
    with progress:
        task = progress.add_task("Separating stems", total=len(matches))

        for song in matches:
            file_path = Path(song["file_path"])
            progress.update(task, description=f"Stems: {song['artist']} - {song['title']}")

            try:
                stems_dir = file_path.parent / STEMS_SUBFOLDER / file_path.stem
                stem_result = separate_track(file_path, stems_dir, model_name=model)

                # Vocal activity analysis
                vocal_data = {}
                if stem_result["vocals"]:
                    vocal_data = detect_vocal_activity(Path(stem_result["vocals"]))

                # Update library
                add_song(
                    spotify_uri=song["spotify_uri"],
                    file_path=file_path,
                    title=song["title"],
                    artist=song["artist"],
                    stems_path=stem_result["stems_path"],
                    has_stems=True,
                    vocal_segments=vocal_data.get("vocal_segments"),
                    vocal_pct=vocal_data.get("vocal_pct"),
                    vocal_head_pct=vocal_data.get("vocal_head_pct"),
                    vocal_tail_pct=vocal_data.get("vocal_tail_pct"),
                )

                vocal_str = f" (vocals: {vocal_data['vocal_pct']:.0%})" if vocal_data else ""
                console.print(f"  [green]OK[/green] {song['artist']} - {song['title']}{vocal_str}")

            except ImportError as e:
                console.print(f"  [red]{e}[/red]")
                return
            except Exception as e:
                console.print(f"  [yellow]FAILED[/yellow] {song['title']}: {e}")

            progress.advance(task)

    console.print(f"\n[green]Done![/green] Stems saved alongside MP3s in '{STEMS_SUBFOLDER}/' subfolder.")


@stems_group.command("track")
@click.argument("query")
@click.option("--model", type=click.Choice(list(VALID_STEM_MODELS)), default=DEFAULT_STEM_MODEL, help="Demucs model")
def stems_track(query: str, model: str):
    """Separate stems for a single track from the library.

    QUERY is a search term to find the track (title, artist, or album).
    """
    from .library import search, add_song
    from .stems import separate_track
    from .vocal_activity import detect_vocal_activity
    from .config import STEMS_SUBFOLDER
    from .progress import console

    results = search(query)
    if not results:
        console.print(f"[dim]No results for '{query}'[/dim]")
        return

    song = results[0]
    file_path = Path(song["file_path"])
    if not file_path.exists():
        console.print(f"[red]File not found: {file_path}[/red]")
        return

    console.print(f"\n[bold]Separating stems:[/bold] {song['artist']} - {song['title']}")

    try:
        stems_dir = file_path.parent / STEMS_SUBFOLDER / file_path.stem
        with console.status("[bold blue]Running Demucs..."):
            stem_result = separate_track(file_path, stems_dir, model_name=model)

        console.print("  [green]Stems saved:[/green]")
        for name in ("vocals", "instrumental"):
            if stem_result.get(name):
                console.print(f"    {name}.mp3")

        # Vocal activity
        vocal_data = {}
        if stem_result["vocals"]:
            with console.status("[bold blue]Analyzing vocals..."):
                vocal_data = detect_vocal_activity(Path(stem_result["vocals"]))

            console.print(f"\n  [bold]Vocal activity:[/bold]")
            console.print(f"    Total:  {vocal_data['vocal_pct']:.0%}")
            console.print(f"    Head:   {vocal_data['vocal_head_pct']:.0%} (first 30s)")
            console.print(f"    Tail:   {vocal_data['vocal_tail_pct']:.0%} (last 30s)")

        # Update library
        add_song(
            spotify_uri=song["spotify_uri"],
            file_path=file_path,
            title=song["title"],
            artist=song["artist"],
            stems_path=stem_result["stems_path"],
            has_stems=True,
            vocal_segments=vocal_data.get("vocal_segments"),
            vocal_pct=vocal_data.get("vocal_pct"),
            vocal_head_pct=vocal_data.get("vocal_head_pct"),
            vocal_tail_pct=vocal_data.get("vocal_tail_pct"),
        )

        console.print(f"\n[green]Done![/green] Library updated.")

    except ImportError as e:
        console.print(f"[red]{e}[/red]")
    except Exception as e:
        console.print(f"[red]Stem separation failed: {e}[/red]")
