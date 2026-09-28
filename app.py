from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import shutil
import os
import subprocess

from fastapi.responses import FileResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

def process_video(video_path: str):
    print(f"\n[API] Started processing {video_path}")
    
    # 1. Clean previous bestplates
    if os.path.exists("data/bestplates"):
        shutil.rmtree("data/bestplates", ignore_errors=True)
    os.makedirs("data/bestplates", exist_ok=True)
    
    try:
        # 2. Run YOLO pipeline
        print("[API] Running YOLO Pipeline...")
        subprocess.run(["python", "main.py", "--input", video_path, "--no-show"], check=True)
        
        # 3. Run Custom PaddleOCR Test
        print("[API] Running PaddleOCR Model...")
        venv_python = r"C:\Users\Lenovo\OneDrive\Documents\Project\OCR\anpr_project\venv\Scripts\python.exe"
        test_script = r"C:\Users\Lenovo\OneDrive\Documents\Project\OCR\anpr_project\test.py"
        subprocess.run([
            venv_python, test_script, 
            "--image_path", "data/bestplates", 
            "--output_json", "paddle_results.json"
        ], check=True)
        
        # 4. Export to DB
        print("[API] Exporting to Database...")
        subprocess.run(["python", "export_to_db.py", "--db-name", "ocr_db", "--db-user", "postgres", "--db-pass", "root"], check=True)
        
        print(f"[API] Successfully finished processing {video_path}")
    except subprocess.CalledProcessError as e:
        print(f"[API] Error occurred during processing: {e}")

@app.post("/upload")
async def upload_video(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    os.makedirs("data/videos", exist_ok=True)
    file_path = f"data/videos/{file.filename}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    # Process video in the background so the UI doesn't freeze
    background_tasks.add_task(process_video, file_path)
    
    return {"filename": file.filename, "message": "Video uploaded successfully! The pipeline is processing it in the background."}
