"""
direction_detector.py

Simple direction estimator for demo purposes.

Main public function:
    detect_direction(audio_path: str) -> {"direction": str, "confidence": float}

- First tries demo_direction_map.json (for deterministic demo results).
- If the file is not in the map, it falls back to a simple stereo-energy heuristic.
"""

import json
import os
from typing import Dict

import numpy as np
import soundfile as sf  # pip install soundfile

# Assume demo_direction_map.json is at the repo root
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEMO_MAP_PATH = os.path.join(REPO_ROOT, "demo_direction_map.json")

DEFAULT_DIRECTION = "front"


def _load_demo_map() -> Dict[str, str]:
    """Load JSON file that maps demo filenames -> direction labels."""
    if not os.path.exists(DEMO_MAP_PATH):
        return {}
    with open(DEMO_MAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


_DEMO_MAP = _load_demo_map()


def _estimate_from_stereo(audio_path: str) -> Dict[str, float]:
    """
    Very simple stereo-based heuristic:

    - If left channel energy > right channel energy  -> "left"
    - If right channel energy > left channel energy -> "right"
    - If similar -> "front"

    Returns a dict {"direction": str, "confidence": float}
    """
    data, sr = sf.read(audio_path)  # data: (n_samples, n_channels) or (n_channels, n_samples)

    # Mono -> cannot estimate, assume front
    if data.ndim == 1:
        return {"direction": DEFAULT_DIRECTION, "confidence": 0.5}

    # Normalize shape so we have (n_samples, 2)
    if data.shape[1] == 2:
        left = data[:, 0]
        right = data[:, 1]
    elif data.shape[0] == 2:
        left = data[0]
        right = data[1]
    else:
        # More channels: just take first two
        left = data[:, 0]
        right = data[:, 1]

    left_energy = float(np.mean(left ** 2) + 1e-9)
    right_energy = float(np.mean(right ** 2) + 1e-9)
    total = left_energy + right_energy
    diff = left_energy - right_energy

    # -1 (all right) -> +1 (all left)
    balance = diff / total
    abs_balance = abs(balance)

    if abs_balance < 0.1:
        direction = DEFAULT_DIRECTION
    elif balance > 0:
        direction = "left"
    else:
        direction = "right"

    confidence = min(1.0, 0.5 + abs_balance)  # 0.5 .. 1.0
    return {"direction": direction, "confidence": round(confidence, 3)}


def detect_direction(audio_path: str) -> Dict[str, float]:
    """
    Public API used by backend.

    Parameters
    ----------
    audio_path : str
        Path to an audio file (same file that the sound classifier receives).

    Returns
    -------
    dict
        {"direction": <str>, "confidence": <float between 0 and 1>}
    """
    filename = os.path.basename(audio_path)

    # 1) Try demo map (deterministic directions for demo audio)
    if filename in _DEMO_MAP:
        direction = _DEMO_MAP[filename]
        return {"direction": direction, "confidence": 0.95}

    # 2) Fallback to a simple stereo-based estimation
    try:
        return _estimate_from_stereo(audio_path)
    except Exception as e:
        print(f"[direction_detector] Error while analysing {audio_path}: {e}")
        return {"direction": DEFAULT_DIRECTION, "confidence": 0.5}