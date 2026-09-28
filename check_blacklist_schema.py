import psycopg2
conn = psycopg2.connect(dbname="ocr_db", user="postgres", password="root", host="localhost")
cur = conn.cursor()
cur.execute("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'blacklist';")
print(cur.fetchall())
