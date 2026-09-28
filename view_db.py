import psycopg2
import pandas as pd

def main():
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host="localhost",
            port="5432",
            dbname="ocr_db",
            user="postgres",
            password="root"
        )
        
        # Fetch the data into a Pandas DataFrame for a nice printed table
        query = "SELECT id, plate_number, confidence, image_path, extracted_at FROM vehicle_plates"
        df = pd.read_sql_query(query, conn)
        
        print("\n=== VEHICLE PLATES IN POSTGRESQL DATABASE ===")
        if df.empty:
            print("The database is currently empty.")
        else:
            # Print the dataframe
            print(df.to_string(index=False))
            
        conn.close()
        
    except Exception as e:
        print(f"[ERROR] Could not connect or read from PostgreSQL: {e}")

if __name__ == "__main__":
    main()
