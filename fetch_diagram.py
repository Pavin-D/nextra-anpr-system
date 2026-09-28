import urllib.request
import base64
import json
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

mermaid_code = """
graph TD
    classDef hardware fill:#0f172a,stroke:#38bdf8,stroke-width:2px,color:#fff
    classDef ai fill:#312e81,stroke:#818cf8,stroke-width:2px,color:#fff
    classDef database fill:#064e3b,stroke:#34d399,stroke-width:2px,color:#fff
    classDef backend fill:#701a75,stroke:#f472b6,stroke-width:2px,color:#fff
    classDef frontend fill:#1e3a8a,stroke:#60a5fa,stroke-width:2px,color:#fff

    A[Live Cameras / Video Files] -->|Upload| B{pipeline.py Orchestrator}
    B -->|Spawns Subprocess| C[YOLO11n + ByteTrack]
    C -->|10-Frame Skip| D[Cropped Vehicle Image]
    D -->|Base64 Image| E[PaddleOCR]
    E -->|SVTR_HGNet Backbone| F[Plate Text & Confidence]
    F --> G{Confidence > 0.85?}
    G -- Yes --> H[(PostgreSQL DB)]
    G -- No --> Z[Discard Plate]
    H --> I{In Blacklist?}
    I -- Match Found! --> J[Threat Alert]
    H --> K[[main.py / FastAPI Server]]
    J --> K
    K -->|/api/v1/telemetry| L[Dashboard]
    K -->|/api/v1/trajectory| M[OSRM Routing]
    K -->|/api/v1/geofence-search| N[Geofence Map]
    K -->|/api/v1/chat| O[AI Chat Search]

    class A,D,F,Z hardware
    class B,C,E ai
    class H,G,I,J database
    class K backend
    class L,M,N,O frontend
"""

payload = json.dumps({"code": mermaid_code, "mermaid": {"theme": "default"}})
b64 = base64.urlsafe_b64encode(payload.encode('utf-8')).decode('utf-8').rstrip('=')
url = "https://mermaid.ink/img/" + b64

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
try:
    with urllib.request.urlopen(req, context=ctx) as response:
        with open(r'C:\Users\Lenovo\OneDrive\Documents\Project\OCR\NEXTRA_Workflow.png', 'wb') as out_file:
            out_file.write(response.read())
    print("Success")
except Exception as e:
    print("Error:", e)
