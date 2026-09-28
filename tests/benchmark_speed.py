import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
import torch
from pipeline.vehicle_detector import VehicleDetector
from pipeline.plate_detector import PlateDetector

torch.set_num_threads(torch.get_num_threads())

cap = cv2.VideoCapture('data/videos/traffic_sample1.mp4')
frames = []
for _ in range(30):
    ret, f = cap.read()
    if not ret: break
    frames.append(f)
cap.release()

# 1. Baseline (BoT-SORT / default track)
vd_default = VehicleDetector('weights/yolo11n.pt', conf_threshold=0.35)
t0 = time.time()
for f in frames:
    vd_default.detect(f, track=True)
t_default = time.time() - t0
fps_default = len(frames) / t_default

# 2. ByteTrack explicitly
vd_byte = VehicleDetector('weights/yolo11n.pt', conf_threshold=0.35)
t0 = time.time()
for f in frames:
    vd_byte.model.track(source=f, persist=True, tracker="bytetrack.yaml", classes=[2,3,5,7], conf=0.35, verbose=False)
t_byte = time.time() - t0
fps_byte = len(frames) / t_byte

print(f"Default tracker: {fps_default:.2f} FPS ({t_default:.2f}s)")
print(f"ByteTrack tracker: {fps_byte:.2f} FPS ({t_byte:.2f}s)")
