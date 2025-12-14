import os
import warnings

# Suppress TF INFO & DEPRECATION messages
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # 0=all, 1=info, 2=warning, 3=error
warnings.filterwarnings('ignore', category=FutureWarning)  # ignore future warnings

import numpy as np
import librosa
import soundfile as sf
import csv
from models.yamnet_model import yamnet_instance


def classify_sound(audio_path):
    yamnet = yamnet_instance.get_model()
    class_map_path = yamnet_instance.get_class_map_path()

    # Load audio
    waveform, sample_rate = sf.read(audio_path, dtype='float32')

    # Resample to 16k
    if sample_rate != 16000:
        waveform = librosa.resample(waveform, orig_sr=sample_rate, target_sr=16000)

    # Convert stereo → mono
    if len(waveform.shape) > 1:
        waveform = np.mean(waveform, axis=1)

    # Run inference (YAMNet expects 1D waveform)
    scores, embeddings, spectrogram = yamnet(waveform)
    avg_scores = scores.numpy().mean(axis=0)

    class_index = np.argmax(avg_scores)
    confidence = float(avg_scores[class_index])

    # Load class names
    labels = []
    with open(class_map_path, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            labels.append(row['display_name'])

    return labels[class_index], confidence
