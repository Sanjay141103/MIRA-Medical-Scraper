import os
import sys
import pandas as pd
from app import scrape_and_extract

test_url = "https://www.robina7daydoctors.com.au/our-doctors"
if len(sys.argv) > 1:
    test_url = sys.argv[1]

print("=== Starting Medical Data Extraction Test ===")
print("Target URL:", test_url)

df, csv_path = scrape_and_extract(test_url)

print("\n=== Extraction Results ===")
if "Error" in df.columns:
    print("FAILED with Error:")
    print(df["Error"].iloc[0])
else:
    print(f"SUCCESS! Extracted {len(df)} doctor records:\n")
    print(df.to_string(index=False))
    if csv_path and os.path.exists(csv_path):
        print(f"\nSaved to CSV: {csv_path}")
