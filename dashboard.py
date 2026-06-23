import streamlit as st
import pandas as pd
import psycopg2
import time

# 1. Configure the Web Page
st.set_page_config(page_title="Mumbai Metro Aqua Line Twin", page_icon="🚇", layout="wide")
st.title("🚇 Mumbai Metro Aqua Line - Real-Time Digital Twin")
st.markdown("Live operational dashboard monitoring passenger flow and train telemetry.")

# 2. Database Connection
def get_db_connection():
    return psycopg2.connect(host="postgres", database="metro_db", user="admin", password="password123", port="5432")

# 3. Fetch Analytics Data
def fetch_data():
    conn = get_db_connection()
    
    # Passengers: Total ridership count
    total_riders = pd.read_sql_query("SELECT COUNT(*) FROM passenger_flow;", conn).iloc[0,0]
    
    # Passengers: Most congested stations
    df_congestion = pd.read_sql_query("""
        SELECT station_name, COUNT(*) as traffic 
        FROM passenger_flow GROUP BY station_name ORDER BY traffic DESC LIMIT 5;
    """, conn)
    
    # Trains: Latest Train Status & Delays
    # We highlight trains that are delayed by more than 0 minutes
    df_trains = pd.read_sql_query("""
        SELECT train_id, station_name, status, delay_minutes, event_timestamp 
        FROM train_log 
        ORDER BY event_timestamp DESC LIMIT 8;
    """, conn)
    
    conn.close()
    return total_riders, df_congestion, df_trains

# 4. Build the UI Layout
placeholder = st.empty()

with placeholder.container():
    total_riders, df_congestion, df_trains = fetch_data()
    
    # Top Metrics
    st.metric(label="Total Passenger Events Today", value=total_riders)
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Station Congestion (Live)")
        if not df_congestion.empty:
            st.bar_chart(data=df_congestion, x='station_name', y='traffic')
            
    with col2:
        st.subheader("🚆 Live Train Telemetry & Delays")
        if not df_trains.empty:
            # Streamlit lets us apply custom styling to pandas dataframes!
            # Let's highlight delayed trains in red for the operators.
            def highlight_delays(val):
                color = 'red' if isinstance(val, int) and val > 0 else ''
                return f'color: {color}'
            
            st.dataframe(df_trains.style.map(highlight_delays, subset=['delay_minutes']), use_container_width=True)
        else:
            st.info("Waiting for train telemetry...")

# 5. Auto-Refresh Logic
time.sleep(2)
st.rerun()