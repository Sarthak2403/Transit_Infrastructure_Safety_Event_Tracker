import sqlite3
import pandas as pd

DB_FILE = 'transit_safety.db'

# --- Step 1: Connect to DB ---
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

print("🔍 Running SQL Queries on 'safety_events'...\n")

# --- Query 1: Total incidents by mode ---
print("📌 Total Incidents by Mode:")
query1 = """
SELECT [Mode Name], COUNT(*) AS total_incidents
FROM safety_events
GROUP BY [Mode Name]
ORDER BY total_incidents DESC;
"""
print(pd.read_sql_query(query1, conn), "\n")

# --- Query 2: Hazardous events by location type ---
print("⚠️ Hazardous Incidents by Location Type:")
query2 = """
SELECT [Location Type], COUNT(*) AS hazardous_count
FROM safety_events
WHERE hazardous_flag = 1
GROUP BY [Location Type]
ORDER BY hazardous_count DESC
LIMIT 10;
"""
print(pd.read_sql_query(query2, conn), "\n")

# --- Query 3: Monthly incident trend ---
print("📅 Monthly Incidents Over Time:")
query3 = """
SELECT strftime('%Y-%m', [Event Date]) AS month, COUNT(*) AS count
FROM safety_events
GROUP BY month
ORDER BY month ASC;
"""
print(pd.read_sql_query(query3, conn), "\n")

# --- Query 4: Multi-vehicle incidents ---
print("🚗 Incidents Involving Multiple Transit Vehicles:")
query4 = """
SELECT COUNT(*) AS multi_transit_incidents
FROM safety_events
WHERE [Number of Transit Vehicles Involved] > 1;
"""
print(pd.read_sql_query(query4, conn), "\n")

conn.close()
print("✅ Queries complete.")
