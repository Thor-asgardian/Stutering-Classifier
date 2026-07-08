from __future__ import annotations

import logging
from pathlib import Path

import numpy as np
import soundfile as sf

logger = logging.getLogger(__name__)


def generate_silent_audio(
    output_path: str | Path,
    duration_seconds: float = 60.0,
    sample_rate: int = 16000,
) -> str:
    """
    Generate a silent WAV audio file.

    Parameters
    ----------
    output_path : str | Path
    Destination WAV file.

    duration_seconds : float
    Length of the silent audio.

    sample_rate : int
    Sampling rate in Hz.

    Returns
    -------
    str
    Path to the generated WAV file.
    """

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    num_samples = int(duration_seconds * sample_rate)

    silence = np.zeros(num_samples, dtype=np.float32)

    sf.write(
        str(output_path),
        silence,
        sample_rate,
    )

    logger.info(
        "Generated %.2f seconds of silence at %s",
        duration_seconds,
        output_path,
    )

    return str(output_path)


if __name__ == "__main__":
    generate_silent_audio(
        output_path="audio/silent_60s.wav",
        duration_seconds=60,
    )