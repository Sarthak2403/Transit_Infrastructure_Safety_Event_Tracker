import pandas as pd
import sqlite3
import os

# --- Step 1: Load Processed Data ---
DATA_DIR = os.path.join('data')
INPUT_FILE = os.path.join(DATA_DIR, 'processed_data.csv')
DB_FILE = 'transit_safety.db'

print(f"📂 Loading processed data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)

# --- Step 2: Connect to SQLite ---
print(f"🛢️ Connecting to SQLite DB: {DB_FILE}...")
conn = sqlite3.connect(DB_FILE)

# --- Step 3: Write to Table ---
print("📊 Inserting data into 'safety_events' table...")
df.to_sql('safety_events', conn, if_exists='replace', index=False)

# --- Step 4: Verify and Close ---
print("✅ Done! Data loaded into 'safety_events' table.")
conn.close()