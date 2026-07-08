from __future__ import annotations

import logging
import os
import shutil
from pathlib import Path
from typing import Any, cast

logger = logging.getLogger(__name__)


def resolve_ffmpeg_executable() -> str: # type: ignore
    """
    Resolve the FFmpeg executable.

    Resolution order:
        1. FFMPEG_PATH environment variable
        2. ffmpeg on system PATH
        3. imageio-ffmpeg bundled executable
    """

    # 1. Environment Variable
    
    env_path = os.getenv("FFMPEG_PATH", "").strip().strip('"')

    if env_path:
        candidate = Path(env_path)

        if candidate.is_file():
            logger.info("Using FFmpeg from FFMPEG_PATH")
            return str(candidate)

        logger.warning(
            "FFMPEG_PATH is set but the executable does not exist: %s",
            env_path,
        )

            # ------------------------------------------------------------------
            # 2. System PATH
            # ------------------------------------------------------------------

        system_ffmpeg = shutil.which("ffmpeg")

        if system_ffmpeg is not None:
            logger.info("Using FFmpeg from system PATH")
            return system_ffmpeg

            # ------------------------------------------------------------------
            # 3. imageio-ffmpeg fallback
            # ------------------------------------------------------------------

        try:
            import imageio_ffmpeg  # type: ignore

            get_ffmpeg_exe = cast(Any, imageio_ffmpeg.get_ffmpeg_exe) # pyright: ignore[reportUnknownMemberType]
            bundled = cast(str, get_ffmpeg_exe())

            if Path(bundled).is_file():
                logger.info("Using bundled imageio-ffmpeg executable")
                return bundled

        except ImportError:
            logger.debug("imageio-ffmpeg is not installed.")

        except Exception as exc:
            logger.exception("Failed to locate bundled FFmpeg: %s", exc)

                # ------------------------------------------------------------------
                # Failure
                # ------------------------------------------------------------------

        raise RuntimeError(
            "\nUnable to locate FFmpeg.\n\n"
            "Choose ONE of the following:\n\n"
            "1. Install FFmpeg and add it to your PATH.\n"
            "2. Set the FFMPEG_PATH environment variable.\n"
            "3. Install imageio-ffmpeg:\n\n"
            "       pip install imageio-ffmpeg\n"
        )