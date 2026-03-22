import pandas as pd
import glob
import os
from pathlib import Path

def load_and_merge_data():
    """
    Unified loader for Synthea data. Processes geographic and financial columns.
    """
    root_path = Path(__file__).parents[1]
    data_dir = root_path / "data"

    if not data_dir.exists():
        raise FileNotFoundError(f"Directory 'data' not found at {data_dir}")

    # 1. Load & Recombine Encounters
    search_pattern = str(data_dir / "encounters_part_*.csv")
    encounter_files = glob.glob(search_pattern)
    if not encounter_files:
        raise FileNotFoundError("Missing encounter part files in /data")
    
    encounters = pd.concat((pd.read_csv(f) for f in encounter_files), ignore_index=True)

    # 2. Load Patients
    patients_path = data_dir / "patients.csv"
    patients = pd.read_csv(patients_path)

    # 3. Feature Engineering: Income & Age
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'])
    patients['AGE'] = (pd.Timestamp.today() - patients['BIRTHDATE']).dt.days // 365
    
    # Create Income Brackets for Vertical Equity Analysis
    def get_income_tier(val):
        if val < 35000: return 'Low Income'
        if val < 85000: return 'Middle Income'
        return 'High Income'
    
    patients['INCOME_TIER'] = patients['INCOME'].apply(get_income_tier)

    # 4. Intersectional Merge
    merged_data = pd.merge(encounters, patients, left_on='PATIENT', right_on='Id')

    # 5. Financial Equity Report (City & Income Focus)
    equity_report = merged_data.groupby(['CITY', 'INCOME_TIER']).agg({
        'TOTAL_CLAIM_COST': 'mean',
        'HEALTHCARE_EXPENSES': 'mean',
        'Id': 'count'
    }).rename(columns={'Id': 'Patient_Count'}).reset_index()

    return merged_data, equity_report
