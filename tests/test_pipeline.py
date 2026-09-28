import sys
import os
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
import cv2
from pipeline.vehicle_detector import VehicleDetector
from pipeline.plate_detector import PlateDetector
from pipeline.visualizer import Visualizer


def test_pipeline_smoke():
    # 1. Create a dummy test frame
    frame = np.full((720, 1280, 3), 40, dtype=np.uint8)

    # 2. Draw mock vehicle-like shape and text
    cv2.rectangle(frame, (300, 200), (900, 600), (120, 120, 120), -1)
    # mock plate
    cv2.rectangle(frame, (500, 480), (700, 540), (240, 240, 240), -1)
    cv2.putText(frame, "DL 01 AB 1234", (510, 520), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 2)

    # 3. Test vehicle detector
    v_model = "weights/yolo11n.pt" if os.path.exists("weights/yolo11n.pt") else "yolo11n.pt"
    p_model = "weights/plate_model_v11n.pt" if os.path.exists("weights/plate_model_v11n.pt") else "plate_model_v11n.pt"

    v_detector = VehicleDetector(model_path=v_model, conf_threshold=0.25)
    vehicles = v_detector.detect(frame, track=False)

    # 4. Test plate detector
    p_detector = PlateDetector(model_path=p_model, conf_threshold=0.2)
    # Test crop-based and full-frame
    plates_crop = p_detector.detect_in_vehicle_crops(frame, vehicles)
    plates_full = p_detector.detect_in_full_frame(frame, vehicles)

    # 5. Test visualizer
    vis = Visualizer(show_plate_zoom=True)
    annotated = vis.annotate(frame, vehicles, plates_full, fps=30.0)

    assert annotated.shape == frame.shape
    print("[SUCCESS] Smoke test passed! Frame annotated successfully.")


if __name__ == "__main__":
    test_pipeline_smoke()
