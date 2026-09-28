import os
import psycopg2
import bcrypt

# DB Connection
conn = psycopg2.connect(
    dbname="ocr_db",
    user="postgres",
    password="password",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);
""")

# Insert pavin / pavin123
password = b"pavin123"
salt = bcrypt.gensalt()
hashed = bcrypt.hashpw(password, salt).decode('utf-8')

try:
    cur.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", ("pavin", hashed))
    conn.commit()
    print("User pavin created successfully.")
except Exception as e:
    conn.rollback()
    print("User already exists or error:", e)
    # Update password if exists
    cur.execute("UPDATE users SET password_hash = %s WHERE username = %s", (hashed, "pavin"))
    conn.commit()
    print("Updated password for pavin.")

cur.close()
conn.close()
