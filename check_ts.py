import psycopg2

conn = psycopg2.connect(dbname="ocr_db", user="postgres", password="root", host="localhost")
cur = conn.cursor()
cur.execute("SELECT MAX(timestamp), MIN(timestamp), COUNT(*) FROM plate_detections")
res = cur.fetchone()
print("Max TS:", res[0])
print("Min TS:", res[1])
print("Total rows:", res[2])

cur.execute("SELECT NOW()")
print("Current DB Time:", cur.fetchone()[0])

cur.close()
conn.close()
