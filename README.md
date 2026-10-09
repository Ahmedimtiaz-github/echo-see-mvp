# 🔊 Echo-See MVP

**Echo-See** is an AI-powered sound classification system that identifies environmental sounds in real time. It leverages Google's [YAMNet](https://tfhub.dev/google/yamnet/1) model to classify audio inputs and exposes the functionality through a FastAPI backend.

> 🎯 **Goal:** Help users detect and identify sounds such as alarms, sirens, dog barking, nature sounds, and more — with confidence scores.

---

## ✨ Features

- 🎤 **Automatic Sound Classification** — powered by YAMNet (TensorFlow Hub)
- 🔄 **Audio Preprocessing** — auto-converts audio to mono 16kHz WAV format
- 🌐 **REST API** — FastAPI backend with CORS support for easy integration
- 📁 **Demo Audio Samples** — included for quick testing
- 🧩 **Modular Design** — clean separation of model, preprocessor, and API layers

---

## 📂 Project Structure

```
echo-see-mvp/
├── backend/
│   ├── app.py                  # FastAPI backend server
│   └── requirements.txt        # Backend dependencies
├── models/
│   ├── sound_classifier.py     # Main classification workflow
│   ├── yamnet_model.py         # Loads YAMNet model from TF Hub
│   ├── audio_preprocessor.py   # Validates & converts audio files
│   ├── app.py                  # Standalone demo script
│   └── run_classify_demo.py    # Demo runner script
├── demo_audio/                 # Sample audio files for testing
│   ├── Alarm.wav
│   ├── dog-barking-406629_16k.wav
│   ├── nature-sounds-240504_16k.wav
│   └── sound-effect-uk-ambulance-siren-164354.mp3
├── .gitignore
├── sound_classification_readme.md
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmedimtiaz-github/echo-see-mvp.git
cd echo-see-mvp
```

### 2. Install Dependencies

**Backend dependencies:**

```bash
pip install -r backend/requirements.txt
```

**ML / Sound classification dependencies:**

```bash
pip install tensorflow tensorflow-hub librosa soundfile numpy
```

### 3. Run the API Server

```bash
cd backend
uvicorn app:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## 📡 API Endpoints

| Method | Endpoint         | Description                          | Status      |
|--------|------------------|--------------------------------------|-------------|
| `GET`  | `/`              | Health check — confirms API is live  | ✅ Active   |
| `GET`  | `/health`        | Returns `{"status": "ok"}`           | ✅ Active   |
| `POST` | `/detect_sound`  | Upload a `.wav` file for classification | ✅ Active |
| `POST` | `/direction`     | Sound direction detection            | 🚧 Planned |
| `POST` | `/captions`      | Audio captioning                     | 🚧 Planned |

### Example: Classify a Sound

```bash
curl -X POST http://127.0.0.1:8000/detect_sound \
  -F "file=@demo_audio/Alarm.wav"
```

**Response:**

```json
{
  "label": "Alarm",
  "confidence": 0.87
}
```

---

## 🧪 Standalone Usage (Without API)

You can also use the sound classifier directly as a Python module:

```python
from models.sound_classifier import classify_sound

audio_file = "demo_audio/dog-barking-406629_16k.wav"
label, confidence = classify_sound(audio_file)

print(f"Predicted Sound: {label}, Confidence: {confidence:.3f}")
```

---

## 🔧 How It Works

1. **User uploads an audio file** (via API or script).
2. **`audio_preprocessor.py`** validates the format and converts it to mono 16kHz WAV if needed.
3. **`sound_classifier.py`** sends the processed audio to YAMNet.
4. **YAMNet** predicts the sound class from 521 categories.
5. **Returns** a human-readable label and a confidence score (0.0 – 1.0).

---

## 🎵 Supported Audio Formats

| Format | Supported |
|--------|-----------|
| `.wav` | ✅        |
| `.mp3` | ✅        |
| `.m4a` | ✅        |

> **Note:** YAMNet requires mono 16kHz WAV input. The preprocessor handles conversion automatically.

---

## 🛠️ Tech Stack

- **Python**  Core language
- **TensorFlow / TensorFlow Hub** YAMNet model inference
- **FastAPI** REST API framework
- **Librosa & SoundFile**  Audio loading and processing
- **NumPy**  Numerical operations

---

## 📌 Roadmap

- [x] Sound classification with YAMNet
- [x] Audio preprocessing pipeline
- [x] FastAPI backend with `/detect_sound` endpoint
- [ ] Sound direction detection (`/direction`)
- [ ] Audio captioning (`/captions`)
- [ ] Frontend UI integration
- [ ] Real-time microphone input support

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/my-feature`)
3. Commit your changes (`git commit -m 'Add my feature'`)
4. Push to the branch (`git push origin feature/my-feature`)
5. Open a Pull Request

---

## 📄 License

This project is currently unlicensed. Please add a license if you plan to distribute it.

---

## 👤 Author

**Ahmed Imtiaz** — [@Ahmedimtiaz-github](https://github.com/Ahmedimtiaz-github)
