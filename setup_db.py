import psycopg2

def create_tables():
    conn = psycopg2.connect(host="postgres", database="metro_db", user="admin", password="password123", port="5432")
    cur = conn.cursor()
    
    # 1. Existing Passenger Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS passenger_flow (
        id SERIAL PRIMARY KEY,
        event_id VARCHAR(50) UNIQUE,
        event_timestamp TIMESTAMP,
        station_name VARCHAR(100),
        event_type VARCHAR(10),
        passenger_type VARCHAR(20)
    );
    """)
    
    # 2. NEW: Train Log Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS train_log (
        id SERIAL PRIMARY KEY,
        train_id VARCHAR(20),
        event_timestamp TIMESTAMP,
        station_name VARCHAR(100),
        status VARCHAR(20),
        delay_minutes INT
    );
    """)
    
    conn.commit()
    print("✅ Tables 'passenger_flow' and 'train_log' are ready!")
    cur.close()
    conn.close()

if __name__ == "__main__":
    create_tables()