import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

new_route = """@app.delete("/api/v1/database/clear/{table}")
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

@app.delete("/api/v1/database/data/{table}/{pk_val}")"""

content = content.replace('@app.delete("/api/v1/database/data/{table}/{pk_val}")', new_route)

with open("main.py", "w", encoding="utf-8") as f:
    f.write(content)

print("Backend patched")
