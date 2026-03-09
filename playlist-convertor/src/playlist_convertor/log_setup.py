"""Logging configuration for playlist-convertor.

Sets up file logging (DEBUG level) in the output folder and
console logging (WARNING+) to stderr so it doesn't interfere with Rich.
"""

import logging
from pathlib import Path

LOG_FILENAME = "playlist-convertor.log"


def setup_logging(output_dir: Path) -> None:
    """Configure logging for a pipeline run.

    Args:
        output_dir: The playlist output folder. The log file is created here.
    """
    root = logging.getLogger("playlist_convertor")
    root.setLevel(logging.DEBUG)

    # Remove any handlers from a previous run (e.g. interactive re-runs)
    root.handlers.clear()

    # File handler: DEBUG level, full detail
    log_path = output_dir / LOG_FILENAME
    fh = logging.FileHandler(str(log_path), encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s %(levelname)-8s [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    ))
    root.addHandler(fh)

    # Console handler: WARNING+ to stderr (won't pollute Rich output)
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)
    ch.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    root.addHandler(ch)
