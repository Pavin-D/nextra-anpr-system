import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

old_query = """    cur.execute(\"\"\"
        SELECT c.camera_id, c.lat, c.long, COUNT(d.id) as detection_count
        FROM cameras c
        LEFT JOIN plate_detections d ON c.camera_id = d.camera_id
        GROUP BY c.camera_id, c.lat, c.long
    \"\"\")"""

# We'll use a 15 minute sliding window for "live" traffic
new_query = """    cur.execute(\"\"\"
        SELECT c.camera_id, c.lat, c.long, COUNT(d.id) as detection_count
        FROM cameras c
        LEFT JOIN plate_detections d 
          ON c.camera_id = d.camera_id 
          AND d.timestamp >= NOW() - INTERVAL '15 minutes'
        GROUP BY c.camera_id, c.lat, c.long
    \"\"\")"""

if old_query in content:
    content = content.replace(old_query, new_query)
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated heatmap query to use recent time window!")
else:
    print("Could not find the exact query string. Please check formatting.")
