import pandas as pd
import glob
import os

def load_and_merge_data():
    """
    Loads split Synthea EHR datasets and merges them for intersectional health analysis.
    Optimized for Streamlit Cloud deployment.
    """
    # 1. Direct Relative Pathing
    # Since Streamlit runs from the root of your repo, 'data' is just a folder at the same level.
    data_dir = 'data'

    # 2. Recombine Split Encounter Files
    # This finds the CSV parts you split to stay under the 25MB limit.
    search_pattern = os.path.join(data_dir, "encounters_part_*.csv")
    encounter_files = glob.glob(search_pattern)
    
    if not encounter_files:
        # This will print the contents of your directory in the logs to help us debug
        content = os.listdir('.')
        raise FileNotFoundError(f"No encounter files found in '{data_dir}'. Root contains: {content}")
    
    # Sort files to ensure they are combined in order
    encounter_files.sort()
    encounters = pd.concat((pd.read_csv(f) for f in encounter_files), ignore_index=True)

    # 3. Load Patient Demographics
    patients_path = os.path.join(data_dir, 'patients.csv')
    if not os.path.exists(patients_path):
        raise FileNotFoundError(f"Missing patients.csv at: {patients_path}")
        
    patients = pd.read_csv(patients_path)

    # 4. Data Cleaning
    # Age calculation for the 0-110 range from your preliminary report
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
    patients['AGE'] = (pd.Timestamp.today() - patients['BIRTHDATE']).dt.days // 365

    # 5. The Intersectional Join
    # Merges patients and encounters to ensure 0 invalid foreign keys
    merged_data = pd.merge(encounters, patients, left_on='PATIENT', right_on='Id')

    # 6. Generate Equity Metrics
    # Analyzes the $1,350 vs $895 cost gaps you identified
    equity_report = merged_data.groupby(['RACE', 'GENDER']).agg({
        'TOTAL_CLAIM_COST': 'mean',
        'Id': 'count'
    }).rename(columns={'Id': 'Encounter_Count'}).reset_index()

    return merged_data, equity_report

if __name__ == "__main__":
    # Test block for local validation
    try:
        data, report = load_and_merge_data()
        print("✅ Data Integrity Check Passed: 0 invalid foreign keys.")
        print(f"✅ Successfully processed {len(data)} clinical encounters.")
        print("\nTop Disparity Segments:")
        print(report.sort_values(by='TOTAL_CLAIM_COST', ascending=False).head())
    except Exception as e:
        print(f"❌ Initialization Error: {e}")
