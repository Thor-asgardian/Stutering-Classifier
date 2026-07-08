from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from audio.ffmpeg_utils import resolve_ffmpeg_executable

logger = logging.getLogger(__name__)


SUPPORTED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".avi",
    ".mov",
    ".mkv",
    ".wmv",
    ".flv",
    ".webm",
    ".mpeg",
    ".mpg",
}


def is_video_file(file_path: str | Path) -> bool:
    """
    Check whether the file is a supported video.
    """
    return Path(file_path).suffix.lower() in SUPPORTED_VIDEO_EXTENSIONS


def extract_audio(
    video_path: str | Path,
    output_path: str | Path,
    sample_rate: int = 16000,
) -> str:
    """
    Extract mono WAV audio from a video.

    Parameters
    ----------
    video_path : str | Path
    Input video file.

    output_path : str | Path
    Output WAV path.

    sample_rate : int
    Target sampling rate.

    Returns
    -------
    str
    Path to extracted WAV file.
    """

    video_path = Path(video_path)
    output_path = Path(output_path)

    if not video_path.is_file():
        raise FileNotFoundError(video_path)

    ffmpeg = resolve_ffmpeg_executable()

    cmd = [
        ffmpeg,
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        str(sample_rate),
        "-acodec",
        "pcm_s16le",
        str(output_path),
    ]

    logger.info("Extracting audio from %s", video_path.name)

    try:
        subprocess.run(
            cmd,
            check=True,
            capture_output=True,
            text=True,
        )

    except subprocess.CalledProcessError as exc:
        raise RuntimeError(
    f"Failed to extract audio from '{video_path}'."
) from exc

    logger.info("Saved audio to %s", output_path)

    return str(output_path)