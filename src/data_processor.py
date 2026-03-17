import os
import pandas as pd
import glob

def load_and_merge_data():
    # 1. Identify the project root directory dynamically
    # This finds the folder containing 'src' and 'data'
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    # 2. Recombine split encounter files using the absolute path
    encounter_files = glob.glob(os.path.join(data_dir, "encounters_part_*.csv"))
    
    if not encounter_files:
        # This provides a more helpful error if the folder is still missing
        raise FileNotFoundError(f"Critical Error: No split encounter files found in {data_dir}")
    
    print(f"Combining {len(encounter_files)} encounter chunks...")
    encounters = pd.concat((pd.read_csv(f) for f in encounter_files), ignore_index=True)

    # 3. Load Patient data using the same absolute path
    patients = pd.read_csv(os.path.join(data_dir, 'patients.csv'))
    
    
    # 4. Load Patient data using the same absolute path
    patients = pd.read_csv(os.path.join(data_dir, 'patients.csv'))

    # 5. Data Cleaning: Age Calculation
    # Aligns with your finding of ages 0-110
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
    today = pd.Timestamp.today()
    patients['AGE'] = (today - patients['BIRTHDATE']).dt.days // 365

    # 6. The Intersectional Join
    # Merges on Patient UUID (Id in patients, PATIENT in encounters)
    merged_data = pd.merge(encounters, patients, left_on='PATIENT', right_on='Id')

    # 7. Calculate Disparity Metrics (Vertical Equity)
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
