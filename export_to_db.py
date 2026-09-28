import os
import argparse
import re
try:
    import psycopg2
except ImportError:
    print("[ERROR] psycopg2 is not installed. Please install it using: pip install psycopg2-binary")
    exit(1)

# Disable oneDNN to prevent PaddlePaddle crashes on CPU
import easyocr

import json

def main():
    parser = argparse.ArgumentParser(description="Export PaddleOCR JSON results to PostgreSQL")
    parser.add_argument("--db-host", default="localhost", help="Database host (default: localhost)")
    parser.add_argument("--db-port", default="5432", help="Database port (default: 5432)")
    parser.add_argument("--db-name", default="ocr_db", help="Database name (default: ocr_db)")
    parser.add_argument("--db-user", default="postgres", help="Database user (default: postgres)")
    parser.add_argument("--db-pass", default="postgres", help="Database password (default: postgres)")
    parser.add_argument("--json-file", default="paddle_results.json", help="JSON results file")
    parser.add_argument("--img-dir", default="data/bestplates", help="Directory of best plates")
    args = parser.parse_args()
    
    # Connect to PostgreSQL
    print(f"[INFO] Connecting to PostgreSQL at {args.db_host}:{args.db_port} (db: {args.db_name})...")
    try:
        conn = psycopg2.connect(
            host=args.db_host,
            port=args.db_port,
            dbname=args.db_name,
            user=args.db_user,
            password=args.db_pass
        )
        cur = conn.cursor()
        
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vehicle_plates (
                id SERIAL PRIMARY KEY,
                plate_number VARCHAR(20) UNIQUE NOT NULL,
                image_path VARCHAR(255) NOT NULL,
                confidence FLOAT,
                extracted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
    except Exception as e:
        print(f"[ERROR] Could not connect to PostgreSQL: {e}")
        return

    # Parse JSON
    if not os.path.exists(args.json_file):
        print(f"[ERROR] {args.json_file} not found.")
        return
        
    with open(args.json_file, 'r') as f:
        results = json.load(f)

    print(f"\n[INFO] Saving {len(results)} perfect plates to Database...")
    processed_count = 0
    
    for item in results:
        img_name = item.get("image")
        plate_num = item.get("prediction")
        conf = float(item.get("confidence", 0.0))
        
        # Skip plates with confidence below 0.85 (85%)
        if conf < 0.85:
            print(f"[WARN] Skipping {plate_num} due to low confidence ({conf:.4f})")
            continue
            
        # VALIDATION: A valid Indian plate must have at least 6 characters
        if len(plate_num) < 6:
            print(f"[WARN] Skipping {plate_num}: Too short")
            continue
            
        # VALIDATION: Must contain at least 2 letters and 2 digits
        letters = sum(1 for c in plate_num if c.isalpha())
        digits = sum(1 for c in plate_num if c.isdigit())
        if letters < 2 or digits < 2:
            print(f"[WARN] Skipping {plate_num}: Invalid format (needs 2 letters, 2 digits)")
            continue
            
        # VALIDATION: Indian State Code check
        valid_states = {
            "AP","AR","AS","BR","CG","GA","GJ","HR","HP","JH","KA","KL","MP","MH","MN","ML","MZ",
            "NL","OD","PB","RJ","SK","TN","TS","TR","UP","UK","WB","AN","CH","DN","DD","DL","JK","LA","LD","PY"
        }
        
        first_two_letters = "".join([c for c in plate_num if c.isalpha()])[:2]
        first_two_letters = first_two_letters.replace("0", "O").replace("1", "I").replace("8", "B")
        
        if first_two_letters not in valid_states:
            print(f"[WARN] Skipping {plate_num}: '{first_two_letters}' is not a valid Indian state code")
            continue
            
        filepath = os.path.join(args.img_dir, img_name)
        
        try:
            cur.execute("""
                INSERT INTO vehicle_plates (plate_number, image_path, confidence)
                VALUES (%s, %s, %s)
                ON CONFLICT (plate_number) DO UPDATE 
                SET image_path = EXCLUDED.image_path,
                    confidence = EXCLUDED.confidence,
                    extracted_at = CURRENT_TIMESTAMP
            """, (plate_num, filepath, conf))
            conn.commit()
            print(f"[SUCCESS] Stored {plate_num} (Conf: {conf:.4f}) -> {img_name}")
            processed_count += 1
        except Exception as e:
            conn.rollback()
            print(f"[ERROR] Failed to insert {plate_num}: {e}")
            
    cur.close()
    conn.close()
    print(f"\n[INFO] Database export complete. Successfully stored {processed_count} plates.")

if __name__ == "__main__":
    main()
