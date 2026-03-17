import pandas as pd
import glob
import os
from pathlib import Path

def load_and_merge_data():
    # 1. Dynamically find the root directory of your project
    # __file__ is 'src/data_processor.py'. .resolve().parents[1] moves up two levels to the root.
    root_dir = Path(__file__).resolve().parents[1]
    data_dir = root_dir / "data"

    # 2. Recombine split encounter files
    # Use the absolute path to look for the CSV chunks
    encounter_files = glob.glob(str(data_dir / "encounters_part_*.csv"))
    
    if not encounter_files:
        # If this still fails, the error message will now tell us the EXACT path being searched
        raise FileNotFoundError(f"Could not find encounter files in: {data_dir}")
    
    print(f"Combining {len(encounter_files)} encounter chunks from {data_dir}...")
    encounters = pd.concat((pd.read_csv(f) for f in encounter_files), ignore_index=True)

    # 3. Load Patient data
    patients_path = data_dir / "patients.csv"
    if not patients_path.exists():
        raise FileNotFoundError(f"Could not find patients.csv at: {patients_path}")
        
    patients = pd.read_csv(patients_path)
    
    

    # 4. Data Cleaning: Age Calculation
    # Aligns with your finding of ages 0-110
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
    today = pd.Timestamp.today()
    patients['AGE'] = (today - patients['BIRTHDATE']).dt.days // 365

    # 5. The Intersectional Join
    # Merges on Patient UUID (Id in patients, PATIENT in encounters)
    merged_data = pd.merge(encounters, patients, left_on='PATIENT', right_on='Id')

    # 6. Calculate Disparity Metrics (Vertical Equity)
    # This identifies the $1,350 vs $895 cost gap you found
    equity_report = merged_data.groupby(['RACE', 'GENDER']).agg({
        'TOTAL_CLAIM_COST': 'mean',
        'BASE_ENCOUNTER_COST': 'mean',
        'Id': 'count'
    }).rename(columns={'Id': 'Encounter_Count'}).reset_index()

    return merged_data, equity_report

if __name__ == "__main__":
    data, report = load_and_merge_data()
    print("Data Integrity Check: Successfully merged.")
    print("\nSample Intersectional Cost Report:")
    print(report.head())
