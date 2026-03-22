import pandas as pd
import glob
from pathlib import Path

def load_and_merge_data():
    root_path = Path(__file__).parents[1]
    data_dir = root_path / "data"

    # Load encounters
    encounter_files = glob.glob(str(data_dir / "encounters_part_*.csv"))
    if not encounter_files:
        raise FileNotFoundError("No encounter files found")

    encounters = pd.concat((pd.read_csv(f) for f in encounter_files), ignore_index=True)

    # Load patients
    patients = pd.read_csv(data_dir / "patients.csv")

    # Create AGE
    patients['BIRTHDATE'] = pd.to_datetime(patients['BIRTHDATE'], errors='coerce')
    patients['AGE'] = (pd.Timestamp.today() - patients['BIRTHDATE']).dt.days // 365

    # Merge
    merged = pd.merge(encounters, patients, left_on='PATIENT', right_on='Id')

    # Clean important columns
    merged['INCOME'] = merged['INCOME'].fillna(0)
    merged['HEALTHCARE_EXPENSES'] = merged['HEALTHCARE_EXPENSES'].fillna(0)
    merged['HEALTHCARE_COVERAGE'] = merged['HEALTHCARE_COVERAGE'].fillna(0)

    # Aggregated report (NEW VARIABLES)
    report = merged.groupby(['CITY', 'STATE', 'COUNTY']).agg({
        'HEALTHCARE_EXPENSES': 'mean',
        'HEALTHCARE_COVERAGE': 'mean',
        'INCOME': 'mean'
    }).reset_index()

    return merged, report
