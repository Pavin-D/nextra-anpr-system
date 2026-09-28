import argparse
import os
import cv2
import glob
import torch
from ultralytics import YOLO

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--camera_id", required=True)
    parser.add_argument("--no-show", action="store_true")
    args = parser.parse_args()
    
    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    v_model = YOLO("yolo11n.pt")
    
    plate_model_paths = glob.glob("**/*plate*.pt", recursive=True)
    if plate_model_paths:
        p_model = YOLO(plate_model_paths[0])
    else:
        p_model = YOLO("yolo11n.pt") 
    
    os.makedirs("data/bestplates", exist_ok=True)
    best_plates = {}
    
    cap = cv2.VideoCapture(args.input)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    
    print(f"[INFO] Tracking vehicles in {args.input} (Total Frames: {total_frames}) on {device}...")
    
    frame_count = 0
    
    # 1. Threaded Video Stream (stream=True) prevents I/O blocking
    # 2. Removed half=True because it severely bottlenecks CPU inference
    results = v_model.track(
        source=args.input, 
        classes=[2,3,5,7], 
        persist=True, 
        verbose=False, 
        tracker="bytetrack.yaml", 
        imgsz=320, 
        stream=True,
        device=device
    )
    
    for r in results:
        frame_count += 1
        frame = r.orig_img.copy()
        
        # Save Progress JSON periodically
        if total_frames > 0 and frame_count % 10 == 0:
            progress_pct = min(100, int((frame_count / total_frames) * 100))
            with open(f"data/progress_{args.camera_id}.json", "w") as f:
                import json
                json.dump({"progress": progress_pct, "frame": frame_count, "total": total_frames}, f)
            print(f"  -> [PROGRESS] Processed {frame_count}/{total_frames} frames ({progress_pct}%)...")
            
        if r.boxes.id is not None:
            track_ids = r.boxes.id.int().cpu().tolist()
            boxes = r.boxes.xyxy.cpu().numpy()
            
            v_crops = []
            valid_tids = []
            global_coords = []
            
            for t_id, box in zip(track_ids, boxes):
                x1, y1, x2, y2 = map(int, box)
                
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, f"ID: {t_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
                
                h, w = frame.shape[:2]
                px1, py1 = max(0, x1 - 20), max(0, y1 - 20)
                px2, py2 = min(w, x2 + 20), min(h, y2 + 20)
                v_crop = r.orig_img[py1:py2, px1:px2]
                
                if v_crop.size == 0: continue
                
                v_crops.append(v_crop)
                valid_tids.append(t_id)
                global_coords.append((px1, py1))
                
            # 3. Batch Inference for Plate Detection
            if v_crops:
                # 4. CPU OPTIMIZATION: Removed half=True, drastically reduced imgsz to 160 (since crops are tiny)
                p_results = p_model(v_crops, verbose=False, conf=0.25, imgsz=160, device=device)
                
                for p_res, t_id, v_crop, (px1, py1) in zip(p_results, valid_tids, v_crops, global_coords):
                    if len(p_res.boxes) > 0:
                        best_idx = p_res.boxes.conf.argmax().item()
                        p_box = p_res.boxes.xyxy[best_idx].cpu().numpy()
                        p_conf = p_res.boxes.conf[best_idx].item()
                        
                        cx1, cy1, cx2, cy2 = map(int, p_box)
                        
                        global_px1, global_py1 = px1 + cx1, py1 + cy1
                        global_px2, global_py2 = px1 + cx2, py1 + cy2
                        cv2.rectangle(frame, (global_px1, global_py1), (global_px2, global_py2), (0, 255, 255), 2)
                        
                        pw, ph = cx2 - cx1, cy2 - cy1
                        padx, pady = int(pw * 0.10), int(ph * 0.05)
                        cx1, cy1 = max(0, cx1 - padx), max(0, cy1 - pady)
                        cx2, cy2 = min(v_crop.shape[1], cx2 + padx), min(v_crop.shape[0], cy2 + pady)
                        
                        plate_crop = v_crop[cy1:cy2, cx1:cx2]
                        if plate_crop.size == 0: continue
                        
                        gray = cv2.cvtColor(plate_crop, cv2.COLOR_BGR2GRAY)
                        laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
                        score = p_conf * laplacian_var
                        
                        if t_id not in best_plates or score > best_plates[t_id]['score']:
                            best_plates[t_id] = {"score": score, "image": plate_crop}
                            
        if frame_count % 5 == 0:
            tmp_path = f"data/live_frame_{args.camera_id}_tmp.jpg"
            final_path = f"data/live_frame_{args.camera_id}.jpg"
            cv2.imwrite(tmp_path, frame)
            try:
                os.replace(tmp_path, final_path)
            except PermissionError:
                pass  # Windows locks the file when the browser is actively downloading it. Skip this frame update.
                        
    for v_id, data in best_plates.items():
        cv2.imwrite(f"data/bestplates/plate_v{v_id}.jpg", data["image"])
        
    print(f"[SUCCESS] Saved {len(best_plates)} clearest plates to data/bestplates")

if __name__ == "__main__":
    main()

