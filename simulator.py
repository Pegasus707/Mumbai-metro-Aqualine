import json
import random
import time
from datetime import datetime, timezone
from confluent_kafka import Producer

STATIONS = [
    "Aarey JVLR", "SEEPZ", "MIDC", "Marol Naka", "CSMIA Terminal 2",
    "CSMIA Terminal 1", "Santacruz", "BKC", "Acharya Atre Chowk",
    "Worli", "Siddhivinayak", "Dadar", "Shitaladevi", "Dharavi", "Bandra Colony"
]

conf = {'bootstrap.servers': 'kafka:29092'}
producer = Producer(conf)

def generate_passenger_event():
    return {
        "event_id": f"evt_{random.randint(100000, 999999)}",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "station_name": random.choice(STATIONS),
        "event_type": random.choice(["ENTRY", "EXIT"]),
        "passenger_type": random.choice(["ADULT", "STUDENT", "SENIOR"])
    }

# NEW: Train Event Generator
def generate_train_event():
    return {
        "train_id": f"TRN-{random.randint(101, 120)}", # Simulating 20 active trains
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "station_name": random.choice(STATIONS),
        "status": random.choice(["ARRIVED", "DEPARTED"]),
        "delay_minutes": random.choices([0, 2, 5, 12], weights=[70, 15, 10, 5])[0] # 70% chance of being on time
    }

if __name__ == "__main__":
    print("🚀 Starting Dual-Stream Simulator (Passengers & Trains)...")
    try:
        while True:
            # Always generate a passenger event
            p_data = generate_passenger_event()
            producer.produce('passenger_events', value=json.dumps(p_data).encode('utf-8'))
            print(f"🧍 Passenger: {p_data['station_name']} ({p_data['event_type']})")
            
            # 20% chance to also generate a train event in this same second
            if random.random() < 0.20:
                t_data = generate_train_event()
                # Notice we send this to a completely different Kafka Topic!
                producer.produce('train_events', value=json.dumps(t_data).encode('utf-8'))
                print(f"🚆 Train {t_data['train_id']}: {t_data['status']} at {t_data['station_name']} (Delay: {t_data['delay_minutes']}m)")

            producer.poll(0)
            time.sleep(random.uniform(0.5, 1.5))
            
    except KeyboardInterrupt:
        producer.flush()