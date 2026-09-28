import re

with open("main.py", "r", encoding="utf-8") as f:
    content = f.read()

new_api = """
# ==========================================
# AUTHENTICATION API
# ==========================================
import jwt
import bcrypt
import datetime
from pydantic import BaseModel
from fastapi.responses import RedirectResponse

JWT_SECRET = "nextra_super_secret_key_2026"

class LoginRequest(BaseModel):
    username: str
    password: str

@app.get("/login")
def serve_login():
    return FileResponse("login.html")

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
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
    
    return {"token": token, "username": user["username"]}
"""

with open("main.py", "a", encoding="utf-8") as f:
    f.write("\n" + new_api + "\n")

print("Added authentication API!")
