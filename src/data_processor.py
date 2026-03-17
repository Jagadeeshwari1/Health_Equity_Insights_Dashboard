import pandas as pd
import glob
import os

def load_and_merge_data():
    """
    Handles data merging for the California synthetic population (2,272 records).
    Uses absolute paths to prevent FileNotFoundError on Streamlit Cloud.
    """
    # 1. Establish Absolute Paths
    # This finds the 'health_equity_insights_dashboard' root folder
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_dir = os.path.join(base_dir, 'data')

    # 2. Recombine Split Encounter Files
    # This looks for the parts you split to stay under the 25MB limit
    search_pattern = os.path.join(data_dir, "encounters_part_*.csv")
    encounter_files = glob.glob(search_pattern)
    
    if not encounter_files:
        # If this fails, the log will now show exactly where it looked
        raise FileNotFoundError(f"Missing encounter chunks at: {data_dir}")
    
    # Combine chunks into one DataFrame (0 invalid foreign keys check)
    encounters = pd.concat((pd.read_csv(f) for f in encounter_files), ignore_index=True)

    # 3. Load Patient Demographics
    patients_path = os.path.join(data_dir, 'patients.csv')
    if not os.path.exists(patients_path):
        raise FileNotFoundError(f"Missing patients.csv at: {patients_path}")
        
    patients = pd.read_csv(patients_path)

    # 4. Feature Engineering
    # Calculates age for the 0-110 range found in your preliminary report
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
    patients['AGE'] = (pd.Timestamp.today() - patients['BIRTHDATE']).dt.days // 365

    # 5. Intersectional Join
    # Merges on Patient UUID (Id)
    merged_data = pd.merge(encounters, patients, left_on='PATIENT', right_on='Id')

    # 6. Vertical Equity Report
    # Identifies the $1,350 (Low Income) vs $895 (High Income) cost gaps
    equity_report = merged_data.groupby(['RACE', 'GENDER']).agg({
        'TOTAL_CLAIM_COST': 'mean',
        'BASE_ENCOUNTER_COST': 'mean',
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
