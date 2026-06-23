# 🚇 Mumbai Metro Digital Twin: Real-Time Data Pipeline

![Mumbai Metro Dashboard Demo](demo.gif)

## 📖 What is this project?
Imagine trying to track millions of people and dozens of trains moving across Mumbai in real-time. This project is a **"Digital Twin"**—a live, virtual simulation of the Mumbai Metro Aqua Line. It generates realistic, real-time data for passengers entering/exiting stations and trains moving along the tracks. 

It processes this high-speed data instantly to power a live dashboard, allowing simulated operations teams to monitor station congestion and train delays the moment they happen.

---

## 🧠 How it Works (The Architecture)
Building a system that handles thousands of events a second requires specialized decoupling. Here is how the data flows:

1. **The Sensors (Python Simulator):** Acts like IoT turnstiles and train GPS, generating continuous JSON payloads.
2. **The Buffer (Apache Kafka):** A distributed event streaming platform that acts as a shock absorber. It safely holds high-velocity data spikes (like rush hour) in a queue so downstream systems don't crash.
3. **The Sorter (Python Consumer):** An ETL script that constantly polls Kafka, cleans the data, and routes it to the correct storage tables.
4. **The Data Warehouse (PostgreSQL):** A relational database storing the cleaned time-series data.
5. **The Monitor (Streamlit):** A live operational dashboard executing SQL aggregations to visualize the data in real-time.

---

## 🛠️ Technical Implementation
* **Micro-batching & Upserts:** The ETL consumer handles duplicate data using idempotent `ON CONFLICT DO NOTHING` SQL logic to maintain data integrity.
* **Topic Decoupling:** Passenger events and Train telemetry are separated into distinct Kafka topics (`passenger_events` and `train_events`).
* **Containerization:** The entire distributed system (Zookeeper, Kafka, Postgres, Python generators, and Streamlit) is managed via a unified `docker-compose` network.

**Tech Stack:**
* **Streaming:** Apache Kafka, Confluent-Kafka
* **Storage:** PostgreSQL
* **Processing:** Python 3.9, Pandas
* **UI & DevOps:** Streamlit, Docker

---

## 🚧 Architectural Trade-offs & Production Scaling
This project was built as a local proof-of-concept to master the fundamentals of streaming data pipelines. However, to deploy this to the actual Mumbai Metro handling millions of daily events, the following enterprise-grade upgrades would be necessary:

1. **Stream Processing:** The single-threaded Python consumer would become a bottleneck during heavy traffic. In production, this would be replaced with a distributed processing framework like **Apache Flink** or **Spark Streaming** for parallel, fault-tolerant processing.
2. **Analytical Database:** PostgreSQL is an OLTP database optimized for transactions. For heavy analytical queries across millions of rows, it would be replaced with a columnar OLAP Data Warehouse like **Snowflake**, **Google BigQuery**, or a real-time database like **ClickHouse**.
3. **Cluster Resilience:** The single-node local Kafka setup would be replaced with a fully managed, multi-broker distributed cluster (e.g., **Amazon MSK** or **Confluent Cloud**) to ensure zero data loss during hardware failures.
4. **Cloud Hosting:** The Docker Compose infrastructure would be migrated to the Cloud, orchestrating containers via **Kubernetes (EKS/GKE)**.

---

## 🚀 Run it Yourself in 1 Command
Ensure you have [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed.

1. Clone this repository.
2. Open your terminal in the project folder.
3. Start the entire infrastructure:
   ```bash
   docker compose up --build -d
   ```
4.	Access the live dashboard at: http://localhost:8501
5.	To gracefully shut down the cluster and clean up:
   ```bash
   docker compose down
   ```

    
