import pandas as pd
import requests
import zipfile
import io
import os

# 1. SETUP PATHS
URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/00222/bank-additional.zip"
DATA_DIR = "data"
CSV_PATH = os.path.join(DATA_DIR, "bank-additional", "bank-additional-full.csv")

# 2. DOWNLOAD & EXTRACT (The Fix)
if not os.path.exists(CSV_PATH):
    print("--- Phase 1: Downloading & Extracting Data ---")
    try:
        response = requests.get(URL, timeout=20)
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(DATA_DIR)
        print("Successfully extracted files to /data.")
    except Exception as e:
        print(f"FAILED to download: {e}")
else:
    print("--- Phase 1: Data already exists. Skipping download. ---")

# 3. LOAD & INSPECT (Step 4)
if os.path.exists(CSV_PATH):
    # This dataset uses ';' as a separator. Standard CSVs use ','. 
    # Noticing this is a 'Senior' level detail.
    df = pd.read_csv(CSV_PATH, sep=';')
    
    print("\n--- Phase 1 Complete ---")
    print(f"Dataset Shape: {df.shape}")
    print("\n--- First 5 Rows ---")
    print(df.head())
else:
    print(f"\nCRITICAL ERROR: File still missing at {CSV_PATH}")
    print("Check your internet connection and folder permissions.")