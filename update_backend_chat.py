import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

old_chat = """@app.post("/api/v1/chat")
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
        
    reply = f"Found {len(results)} vehicles matching your criteria:\\n\\n"
    for r in results:
        reply += f"- **{r['plate_number']}** at {r['camera_id']} ({r['timestamp'].strftime('%Y-%m-%d %H:%M:%S')})\\n"
        
    return {"reply": reply}"""

new_chat = """@app.post("/api/v1/chat")
def process_chat(req: ChatRequest):
    text = req.message.lower()
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    
    query = "SELECT plate_number, camera_id, timestamp FROM plate_detections WHERE 1=1"
    params = []
    
    # Check if user wants a count
    is_count = any(x in text for x in ["how many", "count", "total", "number of"])
    
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
    elif "today" in text:
        query += " AND timestamp::date = CURRENT_DATE"
    elif "yesterday" in text:
        query += " AND timestamp::date = CURRENT_DATE - INTERVAL '1 day'"
        
    # 3b. Relative time rules
    if any(x in text for x in ["recent", "latest", "just now", "last hour"]):
        query += " AND timestamp >= NOW() - INTERVAL '1 hour'"
        
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

    # Handle limits based on keywords
    if "all" in text or "every" in text:
        query += " ORDER BY timestamp DESC LIMIT 100"
    elif any(x in text for x in ["recent", "latest"]):
        query += " ORDER BY timestamp DESC LIMIT 5"
    else:
        query += " ORDER BY timestamp DESC LIMIT 20"
    
    try:
        cur.execute(query, tuple(params))
        results = cur.fetchall()
    except Exception as e:
        cur.close(); conn.close()
        return {"reply": "Sorry, I encountered an error running that query. Please rephrase."}
        
    cur.close(); conn.close()
    
    # Respond dynamically based on requested info
    if not results:
        return {"reply": "I couldn't find any vehicles matching those exact criteria. Try rephrasing your location, plate, or time!"}
        
    if is_count:
        return {"reply": f"I found **{len(results)}** detections matching your criteria."}
        
    reply = f"Found {len(results)} vehicles matching your criteria:\\n\\n"
    for r in results:
        reply += f"- **{r['plate_number']}** at {r['camera_id']} ({r['timestamp'].strftime('%Y-%m-%d %H:%M:%S')})\\n"
        
    return {"reply": reply}"""

content = content.replace(old_chat, new_chat)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Updated AI Chat backend with new NLP keywords!")
