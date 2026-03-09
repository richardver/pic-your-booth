"""Rich progress display for the pipeline."""

from rich.console import Console
from rich.progress import (
    BarColumn,
    MofNCompleteColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
)
from rich.table import Table
from rich.panel import Panel

console = Console()


def create_progress() -> Progress:
    """Create a Rich progress bar for track processing."""
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(bar_width=40),
        MofNCompleteColumn(),
        TimeElapsedColumn(),
        TimeRemainingColumn(),
        console=console,
    )


def print_playlist_info(name: str, owner: str, track_count: int) -> None:
    """Display playlist information."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold cyan")
    table.add_column()
    table.add_row("Playlist", name)
    if owner:
        table.add_row("Owner", owner)
    table.add_row("Tracks", str(track_count))
    console.print(Panel(table, title="[bold]Spotify Playlist", border_style="blue"))


def print_track_list(tracks: list[dict]) -> None:
    """Display track listing."""
    table = Table(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title")
    table.add_column("Artist")
    table.add_column("Duration", justify="right")

    for i, track in enumerate(tracks, 1):
        duration_s = track["duration_ms"] // 1000
        mins, secs = divmod(duration_s, 60)
        table.add_row(str(i), track["title"], track["artist"], f"{mins}:{secs:02d}")

    console.print(table)


def _format_time(seconds: float) -> str:
    """Format seconds as m:ss."""
    mins, secs = divmod(int(seconds), 60)
    return f"{mins}:{secs:02d}"


def print_analysis_results(results: list[tuple]) -> None:
    """Display BPM/key analysis results."""
    has_mix_points = any(
        a and a.get("mix_in") is not None
        for _, _, a in results
    )

    table = Table(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title")
    table.add_column("BPM", justify="right")
    table.add_column("Key")
    table.add_column("Camelot", style="bold cyan")
    table.add_column("Confidence", justify="right")
    if has_mix_points:
        table.add_column("Mix In", justify="right", style="green")
        table.add_column("Mix Out", justify="right", style="blue")

    for i, (file_path, track, analysis) in enumerate(results, 1):
        if analysis:
            conf = analysis["key_confidence"]
            conf_style = "green" if conf > 0.75 else "yellow" if conf > 0.6 else "red"
            row = [
                str(i),
                track["title"],
                str(analysis["bpm"]),
                analysis["key"],
                analysis["camelot_key"],
                f"[{conf_style}]{conf:.0%}[/{conf_style}]",
            ]
            if has_mix_points:
                mix_in = analysis.get("mix_in")
                mix_out = analysis.get("mix_out")
                row.append(_format_time(mix_in) if mix_in is not None else "-")
                row.append(_format_time(mix_out) if mix_out is not None else "-")
            table.add_row(*row)
        else:
            row = [str(i), track["title"], "-", "-", "-", "[red]failed[/red]"]
            if has_mix_points:
                row.extend(["-", "-"])
            table.add_row(*row)

    console.print(Panel(table, title="[bold]Analysis Results", border_style="magenta"))


def print_serato_warnings(report: dict) -> None:
    """Display Serato compatibility warnings."""
    table = Table(show_header=True, header_style="bold")
    table.add_column("File")
    table.add_column("Issue", style="yellow")

    for detail in report["details"]:
        for issue in detail["issues"]:
            table.add_row(detail["file"], issue)

    console.print(Panel(table, title="[bold]Serato Compatibility", border_style="yellow"))


import random

# Fun opener reactions
_OPENER_LINES = [
    "OPENER. Sets the vibe. No pressure.",
    "First track. Make or break. Let's go.",
    "Opening move. The crowd is watching.",
    "Track one. This is where legends begin.",
    "The warm-up starts HERE.",
]

# Fun transition reactions by rating
_GREEN_LINES = [
    "smooth as butter",
    "silk transition",
    "chef's kiss",
    "textbook mix",
    "crowd won't even notice",
    "butter smooth",
    "like it was meant to be",
    "harmonic perfection",
]

_YELLOW_LINES = [
    "bit spicy, but works",
    "creative choice",
    "DJ's call",
    "trust the process",
    "a bold move",
    "keep it moving",
    "they'll forgive you",
]

_RED_LINES = [
    "hold on tight",
    "plot twist!",
    "surprise element",
    "reset the vibe",
    "brave choice",
    "genre switch incoming",
]

# Fun peak track reactions
_PEAK_LINES = [
    "PEAK ENERGY. Hands up!",
    "THIS is the moment.",
    "Main stage energy right here.",
    "The crowd is LOSING IT.",
    "Drop it. NOW.",
]

# Fun closer reactions
_CLOSER_LINES = [
    "Last dance. Make it count.",
    "The closer. Lights coming on soon.",
    "One more memory before the night ends.",
    "Wrap it up, legend.",
    "Final track. Leave them wanting more.",
]


def print_auto_set(tracks: list[dict], transitions: list[dict], preset_name: str, estimated_minutes: float) -> None:
    """Display the auto-sequenced set with color-coded transitions and DJ commentary."""
    table = Table(show_header=True, header_style="bold")
    table.add_column("#", style="dim", width=4)
    table.add_column("Title")
    table.add_column("Artist")
    table.add_column("BPM", justify="right")
    table.add_column("Camelot", style="bold cyan")
    table.add_column("Energy", justify="right")
    table.add_column("Transition")

    # Find peak energy track
    peak_idx = 0
    peak_energy = 0
    for i, track in enumerate(tracks):
        e = track.get("energy") or 0
        if e > peak_energy:
            peak_energy = e
            peak_idx = i

    for i, track in enumerate(tracks):
        energy = track.get("energy") or "-"
        if isinstance(energy, (int, float)):
            energy_bar = "█" * int(energy) + "░" * (10 - int(energy))
            energy_str = f"{energy_bar} {energy}"
        else:
            energy_str = str(energy)

        # Transition info for all but first track
        trans_str = ""
        if i == 0:
            trans_str = f"[bold magenta]{random.choice(_OPENER_LINES)}[/bold magenta]"
        elif i == len(tracks) - 1 and i > 0:
            # Last track gets closer line + transition
            t = transitions[i - 1]
            color = {"green": "green", "yellow": "yellow", "red": "red"}[t["rating"]]
            tier_label = {1: "perfect", 2: "ok", 3: "dramatic", 4: "clash"}[t["harmonic_tier"]]
            trans_str = f"[{color}]● {t['from_key']}→{t['to_key']} Δ{t['bpm_jump']}bpm[/{color}] [dim]{random.choice(_CLOSER_LINES)}[/dim]"
        elif i == peak_idx and i > 0:
            # Peak track
            t = transitions[i - 1]
            color = {"green": "green", "yellow": "yellow", "red": "red"}[t["rating"]]
            trans_str = f"[{color}]● {t['from_key']}→{t['to_key']} Δ{t['bpm_jump']}bpm[/{color}] [bold yellow]{random.choice(_PEAK_LINES)}[/bold yellow]"
        elif i > 0 and i - 1 < len(transitions):
            t = transitions[i - 1]
            color = {"green": "green", "yellow": "yellow", "red": "red"}[t["rating"]]
            tier_label = {1: "perfect", 2: "ok", 3: "dramatic", 4: "clash"}[t["harmonic_tier"]]
            fun_lines = {"green": _GREEN_LINES, "yellow": _YELLOW_LINES, "red": _RED_LINES}
            quip = random.choice(fun_lines[t["rating"]])
            trans_str = f"[{color}]● {t['from_key']}→{t['to_key']} Δ{t['bpm_jump']}bpm[/{color}] [dim]{quip}[/dim]"
            # Vocal transition indicators
            if t.get("vocal_warning"):
                trans_str += " [yellow]vocals may clash[/yellow]"
            elif t.get("vocal_boost"):
                trans_str += " [green]clean transition[/green]"

        table.add_row(
            str(i + 1),
            track["title"],
            track["artist"],
            str(int(track["bpm"])) if track.get("bpm") else "-",
            track.get("camelot_key") or "-",
            energy_str,
            trans_str,
        )

    console.print(Panel(
        table,
        title=f"[bold]Auto Set — {preset_name} ({estimated_minutes:.0f} min)",
        border_style="magenta",
    ))


def print_energy_curve(tracks: list[dict], preset_name: str) -> None:
    """Display a text sparkline showing target vs actual energy across the set."""
    from .arc_presets import get_target_energy

    if not tracks:
        return

    spark_chars = " ▁▂▃▄▅▆▇█"

    target_line = ""
    actual_line = ""
    for i, track in enumerate(tracks):
        position = i / max(1, len(tracks) - 1)
        target_e = get_target_energy(preset_name, position)
        actual_e = track.get("energy") or 0

        t_idx = max(0, min(len(spark_chars) - 1, int(target_e * (len(spark_chars) - 1) / 10)))
        a_idx = max(0, min(len(spark_chars) - 1, int(actual_e * (len(spark_chars) - 1) / 10)))
        target_line += spark_chars[t_idx]
        actual_line += spark_chars[a_idx]

    console.print(f"  [dim]Target:[/dim]  [cyan]{target_line}[/cyan]")
    console.print(f"  [dim]Actual:[/dim]  [magenta]{actual_line}[/magenta]")
    console.print(f"  [dim]         {''.join(str(i + 1)[-1] for i in range(len(tracks)))}[/dim]")


def print_set_summary(result) -> None:
    """Display summary panel for an auto-built set."""
    green = sum(1 for t in result.transitions if t["rating"] == "green")
    yellow = sum(1 for t in result.transitions if t["rating"] == "yellow")
    red = sum(1 for t in result.transitions if t["rating"] == "red")

    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_row("Preset", result.preset)
    table.add_row("Duration", f"~{result.estimated_minutes:.0f} min")
    table.add_row("Tracks", f"{len(result.tracks)} / {result.candidates_available} candidates")
    table.add_row(
        "Transitions",
        f"[green]{green} smooth[/green]  [yellow]{yellow} workable[/yellow]  [red]{red} rough[/red]",
    )

    console.print(Panel(table, title="[bold]Set Summary", border_style="green"))


def print_summary(total: int, success: int, skipped: int, failed: int, output_dir: str) -> None:
    """Display download summary."""
    table = Table(show_header=False, box=None, padding=(0, 2))
    table.add_column(style="bold")
    table.add_column()
    table.add_row("Total", str(total))
    table.add_row("[green]Downloaded", str(success))
    if skipped > 0:
        table.add_row("[cyan]Skipped", str(skipped))
    if failed > 0:
        table.add_row("[red]Failed", str(failed))
    table.add_row("Output", output_dir)
    console.print(Panel(table, title="[bold]Summary", border_style="green"))
