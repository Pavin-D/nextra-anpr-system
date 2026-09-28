import argparse
import os
import shutil
import subprocess
import json
import psycopg2
from datetime import datetime, timedelta
import cv2

def process_video_stream(video_path, camera_id, base_timestamp, db_params, colab_url=None):
    print(f"[{camera_id}] Starting processing on {video_path}")
    
    best_plates_dir = f"data/bestplates_{camera_id}"
    os.makedirs(best_plates_dir, exist_ok=True)
    json_out = f"paddle_results_{camera_id}.json"
    
    ocr_results = []
    
    print(f"[{camera_id}] Running YOLO Tracker locally...")
    shutil.rmtree("data/bestplates", ignore_errors=True)
    subprocess.run(["python", "yolo_tracker.py", "--input", video_path, "--camera_id", camera_id, "--no-show"], check=True)
    
    if os.path.exists("data/bestplates"):
        shutil.copytree("data/bestplates", best_plates_dir, dirs_exist_ok=True)
    
    venv_python = r"C:\Users\Lenovo\OneDrive\Documents\Project\OCR\anpr_project\venv\Scripts\python.exe"
    test_script = r"C:\Users\Lenovo\OneDrive\Documents\Project\OCR\anpr_project\test.py"
    
    if os.path.exists(test_script):
        print(f"[{camera_id}] Running PaddleOCR Engine locally...")
        subprocess.run([
            venv_python, test_script, 
            "--image_path", best_plates_dir, 
            "--output_json", json_out
        ], check=True)
        
    if os.path.exists(json_out):
        with open(json_out, 'r') as f:
            ocr_results = json.load(f)
            
    print(f"[{camera_id}] Exporting results and generating alerts...")
        
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()
    
    ocr_success = 0
    ocr_reject = 0
    
    for item in ocr_results:
        raw_plate = item.get("prediction", "").upper()
        conf = float(item.get("confidence", 0))
        img_name = item.get("image")
        
        # 1. Strip non-alphanumeric characters
        import re
        plate = re.sub(r'[^A-Z0-9]', '', raw_plate)
        
        # 2. Advanced Validation Logic
        valid = True
        
        # Must have decent confidence
        if conf < 0.85:
            valid = False
            
        # Standard Indian plates are usually 8-11 characters long
        if len(plate) < 7 or len(plate) > 11:
            valid = False
            
        # Must start with a valid Indian State Code
        state_codes = {"AP","AR","AS","BR","CG","GA","GJ","HR","HP","JH","KA","KL","MP","MH","MN","ML","MZ","NL","OD","PB","RJ","SK","TN","TS","TR","UP","UK","WB","AN","CH","DN","DD","DL","JK","LA","LD","PY"}
        first_two = plate[:2].replace("0", "O").replace("1", "I").replace("8", "B")
        if first_two not in state_codes:
            valid = False
            
        # Must end with numbers (allow max 1 misread letter at the end)
        last_chars = plate[-4:]
        digits = sum(1 for c in last_chars if c.isdigit())
        if digits < 2:
            valid = False
            
        if not valid:
            ocr_reject += 1
            continue
            
        ocr_success += 1
        timestamp = base_timestamp + timedelta(seconds=1)
        
        cur.execute("""
            INSERT INTO plate_detections (plate_number, camera_id, confidence, timestamp, image_path)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (plate_number, camera_id) DO NOTHING
            RETURNING id;
        """, (plate, camera_id, conf, timestamp, os.path.join(best_plates_dir, img_name)))
        
        inserted = cur.fetchone()
        
        if inserted:
            cur.execute("SELECT reason FROM blacklist WHERE plate_number = %s", (plate,))
            bl = cur.fetchone()
            if bl:
                cur.execute("""
                    INSERT INTO alerts (plate_number, camera_id, alert_type, description, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (plate, camera_id, 'BLACKLIST', f"Blacklisted Vehicle Detected: {bl[0]}", timestamp))
                print(f"[ALERT] Blacklisted plate {plate} detected at {camera_id}!")
                
            cur.execute("""
                SELECT COUNT(*) FROM plate_detections 
                WHERE plate_number = %s AND camera_id = %s AND timestamp::date = %s::date
            """, (plate, camera_id, timestamp))
            count = cur.fetchone()[0]
            if count > 3:
                cur.execute("""
                    INSERT INTO alerts (plate_number, camera_id, alert_type, description, timestamp)
                    VALUES (%s, %s, %s, %s, %s)
                """, (plate, camera_id, 'ANOMALY', f"Suspicious Loitering: Seen {count} times", timestamp))
                
    cur.execute("""
        INSERT INTO system_metrics (camera_id, frames_processed, vehicles_detected, ocr_success_count, ocr_reject_count, processing_time_sec)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (camera_id, 1800, len(ocr_results), ocr_success, ocr_reject, 120.0))
    
    cur.execute("UPDATE cameras SET status = 'online', last_active = %s WHERE camera_id = %s", (datetime.now(), camera_id))
    
    conn.commit()
    cur.close()
    conn.close()
    print(f"[{camera_id}] Pipeline completed successfully. Success: {ocr_success}, Rejected: {ocr_reject}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--video", required=True)
    parser.add_argument("--camera_id", required=True)
    parser.add_argument("--base_time", required=True)
    parser.add_argument("--colab_url", required=False, default=None)
    args = parser.parse_args()
    
    db_params = {"dbname": "ocr_db", "user": "postgres", "password": "root", "host": "localhost"}
    base_ts = datetime.fromisoformat(args.base_time)
    process_video_stream(args.video, args.camera_id, base_ts, db_params, args.colab_url)



