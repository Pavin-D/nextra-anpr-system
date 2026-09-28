import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import cv2
from pipeline import VehicleDetector, PlateDetector

def test_analyze():
    cap = cv2.VideoCapture("data/videos/traffic_sample1.mp4")
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"Analyzing {total_frames} frames of traffic_sample1.mp4...")

    vd = VehicleDetector("weights/yolo11n.pt", conf_threshold=0.3)
    pd = PlateDetector("weights/plate_model_v11n.pt", conf_threshold=0.2)

    plates_found = 0
    frames_with_plates = 0
    all_plate_confs = []
    suspicious_plates = []

    for fn in range(total_frames):
        ret, frame = cap.read()
        if not ret:
            break

        vehs = vd.detect(frame, track=True)
        crop_plates = pd.detect_in_vehicle_crops(frame, vehs)
        full_plates = pd.detect_in_full_frame(frame, vehs)
        merged = pd.merge_detections(crop_plates, full_plates)

        if merged:
            frames_with_plates += 1
            plates_found += len(merged)
            for p in merged:
                all_plate_confs.append(p['conf'])
                # Check for suspicious bounding boxes (aspect ratio too tall, or too huge)
                bw = p['bbox'][2] - p['bbox'][0]
                bh = p['bbox'][3] - p['bbox'][1]
                aspect = bw / float(bh) if bh > 0 else 0
                if aspect < 1.0 or aspect > 6.0 or bh > 150:
                    suspicious_plates.append((fn, p['bbox'], p['conf'], round(aspect, 2)))

        if fn % 60 == 0:
            print(f"Frame {fn}/{total_frames} - Current plates in frame: {len(merged)}")

    cap.release()
    print("\n--- Analysis Results ---")
    print(f"Total frames: {total_frames}")
    print(f"Frames with at least 1 plate: {frames_with_plates} ({frames_with_plates/total_frames*100:.1f}%)")
    print(f"Total plate detections: {plates_found}")
    print(f"Average plate confidence: {sum(all_plate_confs)/len(all_plate_confs):.2f}" if all_plate_confs else "No plates")
    print(f"Suspicious aspect/size plates: {len(suspicious_plates)}")
    if suspicious_plates:
        print("Sample suspicious:", suspicious_plates[:5])

if __name__ == "__main__":
    test_analyze()
