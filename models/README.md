# Models

This folder contains the ML / signal-processing modules used by the backend.

## Direction detection (Person 3)

**Files**

- `direction_detector.py` — exposes `detect_direction(audio_path) -> {"direction", "confidence"}`.
- `audio_capture.py` — helpers to obtain audio from demo files or microphone.
- `run_direction_demo.py` — CLI demo runner for direction detection.
- `../demo_direction_map.json` — mapping from demo filenames to fixed directions (demo mode).

### Public API

```python
from models.direction_detector import detect_direction
from models.audio_capture import get_audio_input

# Demo mode (file-based)
audio_path = get_audio_input(source="file", file_path="demo_audio/Alarm.wav")
direction_info = detect_direction(audio_path)
# direction_info: {"direction": "front", "confidence": 0.95}

# Live mode (mic-based, optional)
# audio_path = get_audio_input(source="mic", duration=3.0)
# direction_info = detect_direction(audio_path)
```

### CLI demo (for testing)

From the repo root:

```bash
python -m models.run_direction_demo --folder demo_audio
# or
python -m models.run_direction_demo --file demo_audio/Alarm.wav
```

### Dependencies

Install these Python packages:

```bash
pip install numpy soundfile sounddevice
```

`sounddevice` is only required if microphone capture is used (`source="mic"`).
```

