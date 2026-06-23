import json
import psycopg2
from confluent_kafka import Consumer

print("Connecting to PostgreSQL...")
conn = psycopg2.connect(host="postgres", database="metro_db", user="admin", password="password123", port="5432")
cur = conn.cursor()
print("✅ Connected to Database!")

conf = {
    'bootstrap.servers': 'kafka:29092',
    'group.id': 'metro-dual-loader',
    'auto.offset.reset': 'earliest'
}
consumer = Consumer(conf)

# NEW: Subscribing to BOTH topics
consumer.subscribe(['passenger_events', 'train_events'])

print("🚀 Listening to multiple streams...")

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None or msg.error():
            continue

        topic = msg.topic() # Let's find out which topic this message came from
        event = json.loads(msg.value().decode('utf-8'))

        # ROUTING LOGIC
        if topic == 'passenger_events':
            cur.execute(
                """
                INSERT INTO passenger_flow (event_id, event_timestamp, station_name, event_type, passenger_type) 
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (event_id) DO NOTHING
                """,
                (event['event_id'], event['timestamp'], event['station_name'], event['event_type'], event['passenger_type'])
            )
            print(f"💾 Saved Passenger -> {event['station_name']}")
            
        elif topic == 'train_events':
            cur.execute(
                """
                INSERT INTO train_log (train_id, event_timestamp, station_name, status, delay_minutes) 
                VALUES (%s, %s, %s, %s, %s)
                """,
                (event['train_id'], event['timestamp'], event['station_name'], event['status'], event['delay_minutes'])
            )
            print(f"🚂 Saved Train Log -> {event['train_id']} at {event['station_name']}")
        conn.commit() 

except KeyboardInterrupt:
    cur.close()
    conn.close()
    consumer.close()