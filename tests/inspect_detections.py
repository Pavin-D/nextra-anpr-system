import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
from pipeline import VehicleDetector, PlateDetector

cap = cv2.VideoCapture('data/videos/traffic_sample.mp4')
vd = VehicleDetector('weights/yolo11n.pt', conf_threshold=0.3)
pd = PlateDetector('weights/plate_model_v11n.pt', conf_threshold=0.2)

for fn in range(0, 500, 25):
    cap.set(cv2.CAP_PROP_POS_FRAMES, fn)
    ret, frame = cap.read()
    if not ret:
        break
    vehs = vd.detect(frame, track=False)
    plates = pd.merge_detections(
        pd.detect_in_vehicle_crops(frame, vehs),
        pd.detect_in_full_frame(frame, vehs)
    )
    for p in plates:
        bx1, by1, bx2, by2 = p['bbox']
        bw = bx2 - bx1
        bh = by2 - by1
        aspect = bw / float(bh) if bh > 0 else 0
        conf = p['conf']
        v_type = p.get('vehicle_type')
        print(f"Frame {fn:3d}: bbox=[{bx1},{by1},{bx2},{by2}] size={bw}x{bh} aspect={aspect:.2f} conf={conf:.2f} veh={v_type}")

cap.release()
