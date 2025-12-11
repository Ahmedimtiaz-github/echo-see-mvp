"""
audio_capture.py

Utilities to provide audio input to the backend.

Two main sources:
- "file": use an existing audio file (e.g., from demo_audio/)
- "mic": record a short clip from the microphone
"""

import os
import uuid
from typing import Literal, Optional

# Try to import microphone-related libraries
try:
    import sounddevice as sd  # type: ignore
    import soundfile as sf   # type: ignore

    _HAS_MIC = True
except Exception:
    _HAS_MIC = False

# Folder where temporary microphone recordings will be stored
AUDIO_TMP_DIR = os.path.join(os.path.dirname(__file__), "..", "tmp_audio")
os.makedirs(AUDIO_TMP_DIR, exist_ok=True)

SourceType = Literal["file", "mic"]


def capture_from_mic(
    duration: float = 3.0,
    sample_rate: int = 16000,
    channels: int = 1,
    filename: Optional[str] = None,
) -> str:
    """
    Record `duration` seconds from default microphone and save to a WAV file.

    Returns
    -------
    str
        File path to the saved recording.

    Raises
    ------
    RuntimeError
        If microphone libraries are not available.
    """
    if not _HAS_MIC:
        raise RuntimeError(
            "Microphone capture not available. "
            "Install 'sounddevice' and 'soundfile' and run on a machine with a mic."
        )

    if filename is None:
        filename = f"mic_{uuid.uuid4().hex}.wav"

    file_path = os.path.join(AUDIO_TMP_DIR, filename)

    print(f"[audio_capture] Recording {duration}s from microphone...")
    audio = sd.rec(
        int(duration * sample_rate),
        samplerate=sample_rate,
        channels=channels,
        dtype="float32",
    )
    sd.wait()
    sf.write(file_path, audio, sample_rate)
    print(f"[audio_capture] Saved recording to {file_path}")

    return file_path


def from_file(file_path: str) -> str:
    """
    Validate and normalize the path to an existing audio file.

    Returns
    -------
    str
        Absolute path to the audio file.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(file_path)
    return os.path.abspath(file_path)


def get_audio_input(
    source: SourceType = "file",
    file_path: Optional[str] = None,
    duration: float = 3.0,
) -> str:
    """
    Main helper for backend to get an audio file path.

    Parameters
    ----------
    source : "file" or "mic"
        - "file": use an existing file (demo mode)
        - "mic": record from microphone (live mode)
    file_path : str, optional
        Required when source == "file".
    duration : float, optional
        Duration of microphone recording in seconds (source == "mic").

    Returns
    -------
    str
        Path to an audio file suitable for:
        - models.sound_classifier.classify_sound
        - models.direction_detector.detect_direction
    """
    if source == "file":
        if file_path is None:
            raise ValueError("file_path must be provided when source='file'")
        return from_file(file_path)

    if source == "mic":
        return capture_from_mic(duration=duration)

    raise ValueError(f"Unknown source {source!r}")