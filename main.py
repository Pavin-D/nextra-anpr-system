from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime
import psycopg2
import psycopg2.extras
import subprocess
import shutil
import os

app = FastAPI(title="City-Wide ANPR Platform")

app.mount("/assets", StaticFiles(directory="frontend/dist/assets"), name="assets")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PARAMS = {"dbname": "ocr_db", "user": "postgres", "password": "root", "host": "localhost"}

def get_db():
    return psycopg2.connect(**DB_PARAMS)

@app.get("/favicon.ico")
def serve_favicon():
    import os
    if os.path.exists("frontend/public/vite.svg"):
        return FileResponse("frontend/public/vite.svg")
    return {"status": "ok"}

@app.get("/")
def serve_dashboard():
    return FileResponse("frontend/dist/index.html")

@app.get("/tracking")
def serve_tracking():
    return FileResponse("frontend/dist/index.html")

@app.get("/blacklist")
def serve_blacklist():
    return FileResponse("frontend/dist/index.html")

from pydantic import BaseModel

@app.get("/geofence")
def serve_geofence():
    return FileResponse("frontend/dist/index.html")


@app.get("/videos")
def serve_videos():
    return FileResponse("frontend/dist/index.html")

@app.get("/database")
def serve_database():
    return FileResponse("frontend/dist/index.html")

@app.get("/alerts")
def serve_alerts():
    return FileResponse("frontend/dist/index.html")

@app.get("/chat")
def serve_chat():
    return FileResponse("frontend/dist/index.html")

class ChatRequest(BaseModel):
    message: str

import re

@app.post("/api/v1/chat")
def process_chat(req: ChatRequest):
    text = req.message.lower()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    query = "SELECT plate_number, camera_id, timestamp FROM plate_detections WHERE 1=1"
    params = []
    
    # 1. Location / Camera Rules
    if any(x in text for x in ["cam 1", "cam1", "camera 1", "camera1", "connaught"]):
        query += " AND camera_id = %s"
        params.append('CAM_01')
    elif any(x in text for x in ["cam 2", "cam2", "camera 2", "camera2", "mandi"]):
        query += " AND camera_id = %s"
        params.append('CAM_02')
    elif any(x in text for x in ["cam 3", "cam3", "camera 3", "camera3", "india gate"]):
        query += " AND camera_id = %s"
        params.append('CAM_03')
        
    # 2. Extract Plate Numbers (Match dynamically against DB known plates)
    cur.execute("SELECT DISTINCT plate_number FROM plate_detections")
    known_plates = [r['plate_number'].lower() for r in cur.fetchall()]
    detected_plates = [p for p in known_plates if p in text]
    if detected_plates:
        format_strings = ','.join(['%s'] * len(detected_plates))
        query += f" AND LOWER(plate_number) IN ({format_strings})"
        params.extend(detected_plates)
        
    # 3. Date Rules (DD/MM/YYYY or YYYY-MM-DD)
    date_match = re.search(r'(\d{1,4})[/-](\d{1,2})[/-](\d{1,4})', text)
    if date_match:
        p1, p2, p3 = date_match.groups()
        if len(p3) == 4: # DD/MM/YYYY
            query += " AND timestamp::date = %s"
            params.append(f"{p3}-{p2}-{p1}")
        elif len(p1) == 4: # YYYY-MM-DD
            query += " AND timestamp::date = %s"
            params.append(f"{p1}-{p2}-{p3}")
            
    # 4. Time Rules (e.g. "10 am to 2 pm" or "10 to 14")
    times = re.findall(r'(\d{1,2})\s*(am|pm)?', text)
    if len(times) >= 2:
        t1_val, p1 = times[0]
        t2_val, p2 = times[1]
        
        def to_24h(h_str, ampm):
            h = int(h_str)
            if ampm == 'pm' and h < 12: h += 12
            if ampm == 'am' and h == 12: h = 0
            return h
            
        h1 = to_24h(t1_val, p1)
        h2 = to_24h(t2_val, p2)
        
        if h1 > h2: h1, h2 = h2, h1
        query += " AND EXTRACT(HOUR FROM timestamp) >= %s AND EXTRACT(HOUR FROM timestamp) <= %s"
        params.extend([h1, h2])

    query += " ORDER BY timestamp DESC LIMIT 20"
    
    try:
        cur.execute(query, tuple(params))
        results = cur.fetchall()
    except Exception as e:
        cur.close(); conn.close()
        return {"reply": "Sorry, I encountered an error running that query. Please rephrase."}
        
    cur.close(); conn.close()
    
    if not results:
        return {"reply": "I couldn't find any vehicles matching those exact criteria. Try rephrasing your location, plate, or time!"}
        
    reply = f"Found {len(results)} vehicles matching your criteria:\n\n"
    for r in results:
        reply += f"- **{r['plate_number']}** spotted at {r['camera_id']} on {r['timestamp'].strftime('%Y-%m-%d %I:%M %p')}\n"
        
    return {"reply": reply}

class GeofenceRequest(BaseModel):
    cameras: list[str]

@app.post("/api/v1/geofence-search")
def geofence_search(req: GeofenceRequest):
    if not req.cameras:
        return {"detections": []}
    
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Securely format the IN clause
    format_strings = ','.join(['%s'] * len(req.cameras))
    query = f"SELECT plate_number, camera_id, timestamp, confidence FROM plate_detections WHERE camera_id IN ({format_strings}) ORDER BY timestamp DESC LIMIT 50"
    
    cur.execute(query, tuple(req.cameras))
    data = cur.fetchall()
    cur.close(); conn.close()
    return {"detections": data}

@app.get("/api/v1/blacklist")
def get_blacklist():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT plate_number, reason, created_at FROM blacklist ORDER BY created_at DESC;")
    data = cur.fetchall()
    cur.close(); conn.close()
    return {"blacklist": data}

from pydantic import BaseModel
class BlacklistRequest(BaseModel):
    plate_number: str
    reason: str

@app.post("/api/v1/blacklist")
def add_blacklist(req: BlacklistRequest):
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO blacklist (plate_number, reason) VALUES (%s, %s)", (req.plate_number.upper(), req.reason))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cur.close(); conn.close()
    return {"status": "success"}

@app.delete("/api/v1/blacklist/{plate}")
def delete_blacklist(plate: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM blacklist WHERE plate_number = %s", (plate.upper(),))
    conn.commit()
    cur.close(); conn.close()
    return {"status": "success"}

def run_pipeline(video_path: str, camera_id: str, base_time: str, colab_url: str = None):
    cmd = [
        "python", "pipeline.py",
        "--video", video_path,
        "--camera_id", camera_id,
        "--base_time", base_time
    ]
    if colab_url:
        cmd.extend(["--colab_url", colab_url])
        
    subprocess.run(cmd)

@app.post("/api/v1/upload-feeds")
async def upload_feeds(
    background_tasks: BackgroundTasks,
    cam1: UploadFile = File(None),
    cam2: UploadFile = File(None),
    cam3: UploadFile = File(None),
    colab_url: str = Form(None)
):
    import glob
    for f in glob.glob("data/progress_*.json"): os.remove(f)
    for f in glob.glob("data/live_frame_*.jpg"): os.remove(f)
    
    os.makedirs("data/uploads", exist_ok=True)
    base_time = datetime.now().isoformat()
    
    files = {"CAM_01": cam1, "CAM_02": cam2, "CAM_03": cam3}
    
    for cam_id, file in files.items():
        if not file:
            continue
        path = f"data/uploads/{cam_id}_{file.filename}"
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Spawn concurrent pipelines via BackgroundTasks
        background_tasks.add_task(run_pipeline, path, cam_id, base_time, colab_url)
        
    return {"message": "All 3 video streams are now being processed concurrently."}

@app.get("/api/v1/trajectory/{plate_number}")
def get_trajectory(plate_number: str):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Query joins detections with cameras to get lat/long chronologically
    cur.execute("""
        SELECT d.timestamp, d.confidence, c.camera_id, c.location_name, c.lat, c.long 
        FROM plate_detections d
        JOIN cameras c ON d.camera_id = c.camera_id
        WHERE d.plate_number = %s
        ORDER BY d.timestamp ASC
    """, (plate_number,))
    
    trajectory = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"plate": plate_number, "trajectory": trajectory}

@app.get("/api/v1/analytics/heatmap")
def get_heatmap():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    cur.execute("""
        SELECT c.camera_id, c.lat, c.long, COUNT(d.id) as detection_count
        FROM cameras c
        LEFT JOIN plate_detections d 
          ON c.camera_id = d.camera_id 
          AND d.timestamp >= NOW() - INTERVAL '3 minutes'
        GROUP BY c.camera_id, c.lat, c.long
    """)
    
    data = cur.fetchall()
    cur.close()
    conn.close()
    
    return {"heatmap": data}

@app.get("/api/v1/analytics/speeds")
def get_speeds():
    # Placeholder for actual speed calc - calculate haversine between joined routes
    # For prototype, we'll return mock avg speeds for city bottlenecks
    return {
        "bottlenecks": [
            {"route": "Connaught Place -> Mandi House", "avg_speed_kmh": 14.5, "status": "CONGESTED"},
            {"route": "Mandi House -> India Gate", "avg_speed_kmh": 32.1, "status": "CLEAR"}
        ]
    }

@app.get("/api/v1/alerts")
def get_alerts():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT a.*, b.created_at AS blacklist_date, b.reason AS blacklist_reason FROM alerts a LEFT JOIN blacklist b ON a.plate_number = b.plate_number ORDER BY a.timestamp DESC LIMIT 50;")
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return {"alerts": alerts}

@app.get("/api/v1/telemetry")
def get_telemetry():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    # Get overall metrics
    cur.execute("SELECT SUM(ocr_success_count) as total_success, SUM(ocr_reject_count) as total_reject FROM system_metrics;")
    metrics = cur.fetchone()
    
    # Get camera statuses
    cur.execute("SELECT camera_id, status FROM cameras;")
    cams = cur.fetchall()
    
    cur.close()
    conn.close()
    
    total = (metrics['total_success'] or 0) + (metrics['total_reject'] or 0)
    success_rate = round(((metrics['total_success'] or 0) / total * 100), 2) if total > 0 else 0
    
    return {
        "success_rate": success_rate,
        "total_plates_scanned": total,
        "cameras": cams
    }


@app.get("/api/v1/videos")
def list_videos():
    import glob, os, datetime
    files = glob.glob("data/uploads/*.mp4")
    videos = []
    for f in files:
        videos.append({
            "filename": os.path.basename(f),
            "size": f"{os.path.getsize(f) / (1024*1024):.2f} MB",
            "date": datetime.datetime.fromtimestamp(os.path.getmtime(f)).isoformat()
        })
    # sort by date descending
    videos.sort(key=lambda x: x["date"], reverse=True)
    return {"videos": videos}

@app.get("/api/v1/videos/play/{filename}")
def serve_video(filename: str):
    import os
    path = f"data/uploads/{filename}"
    if not os.path.exists(path):
        return {"error": "Not found"}
    return FileResponse(path, media_type="video/mp4")

@app.delete("/api/v1/videos/delete/{filename}")
def delete_video(filename: str):
    import os
    path = f"data/uploads/{filename}"
    if os.path.exists(path):
        os.remove(path)
        return {"success": True}
    return {"error": "Not found"}

@app.get("/api/v1/progress")
def get_progress():
    try:
        import json, glob, os
        files = glob.glob("data/progress_*.json")
        if not files: return {"progress": 0, "frame": 0, "total": 0}
        total_prog = 0
        for f in files:
            with open(f, "r") as json_file:
                total_prog += json.load(json_file).get("progress", 0)
        avg_prog = int(total_prog / len(files))
        return {"progress": avg_prog, "frame": 0, "total": 0}
    except:
        return {"progress": 0, "frame": 0, "total": 0}

@app.get("/api/v1/live-frame")
def get_live_frame():
    try:
        import glob, os
        files = glob.glob("data/live_frame_*.jpg")
        if not files: return FileResponse("data/live_frame.jpg", headers={"Cache-Control": "no-cache"})
        # Return the most recently updated frame
        latest_file = max(files, key=os.path.getmtime)
        return FileResponse(latest_file, headers={"Cache-Control": "no-cache"})
    except:
        return FileResponse("data/live_frame.jpg", headers={"Cache-Control": "no-cache"})

@app.get("/api/v1/plates")
def get_all_plates():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT DISTINCT plate_number FROM plate_detections ORDER BY plate_number;")
    plates = cur.fetchall()
    cur.close()
    conn.close()
    return {"plates": [p['plate_number'] for p in plates]}


class AlertCreate(BaseModel):
    plate_number: str
    camera_id: str
    alert_type: str
    description: str

class AlertUpdate(BaseModel):
    plate_number: str
    camera_id: str
    alert_type: str
    description: str

@app.post("/api/v1/alerts")
def create_alert(alert: AlertCreate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO alerts (plate_number, camera_id, alert_type, description, timestamp) VALUES (%s, %s, %s, %s, NOW())",
        (alert.plate_number, alert.camera_id, alert.alert_type, alert.description)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Alert created successfully"}

@app.delete("/api/v1/alerts/{alert_id}")
def delete_alert(alert_id: int):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM alerts WHERE id = %s", (alert_id,))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Alert deleted successfully"}

@app.put("/api/v1/alerts/{alert_id}")
def update_alert(alert_id: int, alert: AlertUpdate):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE alerts SET plate_number=%s, camera_id=%s, alert_type=%s, description=%s WHERE id = %s",
        (alert.plate_number, alert.camera_id, alert.alert_type, alert.description, alert_id)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"message": "Alert updated successfully"}


# ==========================================
# DATABASE MANAGEMENT API
# ==========================================

@app.get("/api/v1/database/tables")
def get_tables():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    tables = [
        {"name": "plate_detections", "pk": "id"},
        {"name": "blacklist", "pk": "plate_number"},
        {"name": "alerts", "pk": "id"},
        {"name": "cameras", "pk": "camera_id"}
    ]
    for t in tables:
        try:
            cur.execute(f"SELECT COUNT(*) as count FROM {t['name']};")
            t["count"] = cur.fetchone()["count"]
        except Exception as e:
            conn.rollback()
            t["count"] = 0
    cur.close()
    conn.close()
    return {"tables": tables}

@app.get("/api/v1/database/data/{table}")
def get_table_data(table: str):
    allowed_tables = ["plate_detections", "blacklist", "alerts", "cameras"]
    if table not in allowed_tables:
        return {"error": "Invalid table"}
    
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    order_by = "id DESC" if table in ["plate_detections", "alerts"] else "plate_number ASC" if table == "blacklist" else "camera_id ASC"
    try:
        cur.execute(f"SELECT * FROM {table} ORDER BY {order_by} LIMIT 100;")
        rows = cur.fetchall()
        # Convert datetimes to strings for JSON
        for r in rows:
            for k, v in r.items():
                if hasattr(v, 'isoformat'):
                    r[k] = v.isoformat()
    except Exception as e:
        conn.rollback()
        rows = []
    finally:
        cur.close()
        conn.close()
    return {"rows": rows}

@app.delete("/api/v1/database/clear/{table}")
def clear_table_data(table: str):
    allowed_tables = {"plate_detections", "blacklist", "alerts"}
    if table not in allowed_tables:
        return {"error": "Invalid or protected table"}
    
    conn = get_db()
    cur = conn.cursor()
    try:
        cur.execute(f"DELETE FROM {table}")
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()
    return {"success": True}

@app.delete("/api/v1/database/data/{table}/{pk_val}")
def delete_table_data(table: str, pk_val: str):
    allowed_tables = {"plate_detections": "id", "blacklist": "plate_number", "alerts": "id", "cameras": "camera_id"}
    if table not in allowed_tables:
        return {"error": "Invalid table"}
    
    pk_col = allowed_tables[table]
    conn = get_db()
    cur = conn.cursor()
    try:
        if pk_col == "id":
            cur.execute(f"DELETE FROM {table} WHERE {pk_col} = %s", (int(pk_val),))
        else:
            cur.execute(f"DELETE FROM {table} WHERE {pk_col} = %s", (pk_val,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}
    finally:
        cur.close()
        conn.close()
    return {"success": True}



# ==========================================
# AUTHENTICATION API
# ==========================================
import jwt
import bcrypt
import datetime as dt
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

JWT_SECRET = "nextra_super_secret_key_2026"

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/login")
def serve_login():
    return FileResponse("frontend/dist/index.html")

@app.post("/api/v1/auth/login")
def login(req: LoginRequest):
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM users WHERE username = %s", (req.username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return {"error": "Invalid username or password"}

    if not bcrypt.checkpw(req.password.encode('utf-8'), user["password_hash"].encode('utf-8')):
        return {"error": "Invalid username or password"}

    # Generate JWT
    payload = {
        "sub": user["username"],
        "exp": dt.datetime.utcnow() + dt.timedelta(days=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    return {"token": token, "username": user["username"]}



