import pandas as pd
import os

# --- Step 1: Load Cleaned Data ---
DATA_DIR = os.path.join('data')
INPUT_FILE = os.path.join(DATA_DIR, 'cleaned_data.csv')
OUTPUT_FILE = os.path.join(DATA_DIR, 'processed_data.csv')

print(f"📂 Loading data from {INPUT_FILE}...")
df = pd.read_csv(INPUT_FILE)

# --- Step 2: Basic Cleaning ---
print("🧹 Converting Event Date to datetime...")
df['Event Date'] = pd.to_datetime(df['Event Date'], errors='coerce')

# --- Step 3: Flag Hazardous Events ---
print("⚠️ Flagging hazardous events...")

def is_hazardous(row):
    if (row['Total Injuries'] > 0) or (row['Total Fatalities'] > 0) or (row['Total Serious Injuries'] > 0):
        return 1
    return 0

df['hazardous_flag'] = df.apply(is_hazardous, axis=1)

# --- Step 4: Save Processed Data ---
print(f"💾 Saving processed data to {OUTPUT_FILE}...")
df.to_csv(OUTPUT_FILE, index=False)

print("✅ Done! Processed data saved at 'data/processed_data.csv'")