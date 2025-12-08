# Sound Classification Module

This module provides **automatic sound classification** using **YAMNet**, including audio validation, conversion, and prediction. It is designed to be integrated into projects or called from scripts.

---

## Folder Structure

```
models/
├── sound_classifier.py        # Main classification workflow
├── yamnet_model.py            # Loads YAMNet once
├── audio_preprocessor.py      # Validates and converts audio to YAMNet format
├── app.py                     # Example script demonstrating workflow
└── README.md                  # Documentation

demo_audio/                    # Sample audio files for testing
├── dog_bark.wav
├── ambulance.wav
└── ... 

uploads/                       # Temporary folder for converted audio files
```

---

## Dependencies

Install the required packages:

```bash
pip install tensorflow tensorflow-hub librosa soundfile numpy
```

Optional: suppress warnings in your script:

```python
import os, warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
warnings.filterwarnings('ignore')
```

---

## Files Overview

- **`sound_classifier.py`**  
  - Main function `classify_sound(audio_path)`  
  - Validates audio, converts if necessary, runs YAMNet, returns label and confidence  

- **`yamnet_model.py`**  
  - Loads YAMNet from TensorFlow Hub once  
  - Provides access to model and class labels  

- **`audio_preprocessor.py`**  
  - Checks if audio is mono and 16kHz  
  - Converts mp3/wav/m4a to 16kHz mono WAV  
  - Returns converted file path  

- **`app.py`**  
  - Demonstrates usage of `classify_sound()` with example audio files  
  - Can be run directly to test predictions  

- **`demo_audio/`**  
  - 4–8 labeled audio files to test the classifier  

---

## Usage Example

```python
from models.sound_classifier import classify_sound

audio_file = "../demo_audio/old-telephone-ringing-362034.mp3"
label, confidence = classify_sound(audio_file)

print(f"Predicted Sound: {label}, Confidence: {confidence:.3f}")
```

---

## Workflow

1. User provides an audio file.  
2. `audio_preprocessor.py` checks format and converts if needed.  
3. `sound_classifier.py` sends the validated audio to YAMNet.  
4. YAMNet predicts the sound class.  
5. Returns human-readable label and confidence score.  

---

## Deliverables for the Company

- `models/sound_classifier.py`  
- `models/yamnet_model.py`  
- `models/audio_preprocessor.py`  
- `models/app.py` (example usage script)  
- `demo_audio/` (labeled audio clips)  
- `models/README.md`  

---

## Notes

- Supported audio formats: `.wav`, `.mp3`, `.m4a`  
- YAMNet expects **mono 16kHz WAV**, but this module handles conversion automatically  
- Confidence scores range from `0.0` to `1.0`