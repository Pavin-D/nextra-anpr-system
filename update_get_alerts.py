import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

old_func = """def get_alerts():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 10;")
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return {"alerts": alerts}"""

new_func = """def get_alerts():
    conn = get_db()
    cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cur.execute("SELECT a.*, b.created_at AS blacklist_date, b.reason AS blacklist_reason FROM alerts a LEFT JOIN blacklist b ON a.plate_number = b.plate_number ORDER BY a.timestamp DESC LIMIT 50;")
    alerts = cur.fetchall()
    cur.close()
    conn.close()
    return {"alerts": alerts}"""

if "SELECT a.*, b.created_at" not in content:
    content = content.replace(old_func, new_func)
    with open("main.py", "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated get_alerts in main.py")
else:
    print("Already updated")
