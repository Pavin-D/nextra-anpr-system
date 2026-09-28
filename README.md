# Indian Vehicle & License Plate Detection (YOLO11)

A two-stage computer vision pipeline designed to detect vehicles and locate Indian number plates from video streams.

---

## 📁 Project Directory Structure

```
OCR/
├── data/
│   ├── videos/              # Place input videos here (e.g. traffic_sample.mp4)
│   ├── output/              # Annotated output videos saved here
│   └── crops/               # Extracted license plate image crops for OCR
├── weights/
│   ├── yolo11n.pt           # YOLO11 vehicle detector (cars, bikes, buses, trucks)
│   └── plate_model_v11n.pt  # Fine-tuned YOLO11 license plate detector
├── pipeline/
│   ├── __init__.py
│   ├── vehicle_detector.py  # Stage 1: Vehicle detection & persistent ByteTrack tracking
│   ├── plate_detector.py    # Stage 2: Plate localization (vehicle-crop or full-frame)
│   └── visualizer.py        # Visual overlays, HUD metrics & plate zoom PIP
├── tests/
│   └── test_pipeline.py     # Pipeline smoke test
├── main.py                  # CLI runner for video, webcam, or images
├── requirements.txt         # Project dependencies
└── README.md
```

---

## 🚀 Quick Start

### 1. Run Detection on the Sample Video
If no input is specified, the script automatically picks up any video inside `data/videos/`:
```powershell
python main.py
```

### 2. Run with Interactive Preview Window
```powershell
python main.py --input data/videos/traffic_sample.mp4
```

### 3. Run in Headless Mode (Faster Processing)
To process in the background without opening the GUI window:
```powershell
python main.py --input data/videos/traffic_sample.mp4 --no-show
```

### 4. Save Detected Plate Crops for OCR
To automatically export cropped license plate images into `data/crops/`:
```powershell
python main.py --input data/videos/traffic_sample.mp4 --save-crops data/crops
```

---

## ⌨️ Interactive Controls (During Video Playback)

| Key | Action |
|---|---|
| **SPACE** | Pause / Resume video playback |
| **S** | Save a snapshot image of the current annotated frame |
| **Q** / **ESC** | Quit gracefully and finalize the output video |

---

## ⚙️ Advanced Arguments

| Argument | Default | Description |
|---|---|---|
| `--input`, `-i` | Auto (`data/videos/*.mp4`) | Path to video file, image, or webcam index (`0`). |
| `--output`, `-o` | `data/output/annotated_<name>.mp4` | Output path for annotated video. |
| `--detection-mode` | `crop` | `crop` (vehicle-focused), `full` (whole frame), or `both`. |
| `--conf-vehicle` | `0.35` | Confidence threshold for vehicle detection. |
| `--conf-plate` | `0.25` | Confidence threshold for plate detection. |
| `--save-crops` | `""` | Directory to save cropped license plates. |
| `--max-frames` | `0` | Process up to N frames (`0` = full video). |
| `--no-track` | `False` | Disable persistent vehicle tracking. |
| `--no-show` | `False` | Disable preview display window. |
