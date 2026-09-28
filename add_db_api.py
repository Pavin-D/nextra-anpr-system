import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

new_api = """
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
        cur.execute(f"SELECT COUNT(*) as count FROM {t['name']};")
        t["count"] = cur.fetchone()["count"]
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
    cur.execute(f"SELECT * FROM {table} ORDER BY {order_by} LIMIT 100;")
    rows = cur.fetchall()
    # Convert datetimes to strings for JSON
    for r in rows:
        for k, v in r.items():
            if hasattr(v, 'isoformat'):
                r[k] = v.isoformat()
    cur.close()
    conn.close()
    return {"rows": rows}

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

"""

if "DATABASE MANAGEMENT API" not in content:
    # Insert before if __name__ == '__main__':
    content = content.replace("if __name__ == '__main__':", new_api + "\nif __name__ == '__main__':")
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Added DB Management API!")
else:
    print("API already exists")
