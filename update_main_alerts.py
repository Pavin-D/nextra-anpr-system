import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

# Add serve_alerts endpoint
if "@app.get(\"/alerts\")" not in content:
    serve_alerts = """
@app.get("/alerts")
def serve_alerts():
    return FileResponse("alerts.html")
"""
    content = content.replace("@app.get(\"/chat\")", serve_alerts + "\n@app.get(\"/chat\")")

# Add CRUD API endpoints for alerts
if "class AlertCreate(" not in content:
    crud_api = """
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
"""
    content = content + "\n" + crud_api

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Updated main.py with alerts CRUD endpoints.")
