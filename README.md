Health Equity Insights Dashboard
Intersectional Health Analytics & Cost Burden Tracker

🏗️ Architecture

```
health_equity_insights_dashboard/
├── app/
│   └── main.py              # ← Streamlit UI (Filters, City Selection, Cost Charts)
├── src/
│   ├── data_processor.py    # ← Partitioned Data Recombination & Intersectional Join Logic
│   ├── model_loader.py      # ← ML Serialization (Pickle) & Environment Pathing
│   └── visuals.py           # ← Equity Charts & Geographic Cluster Mapping
├── data/
│   ├── patients.csv         # ← Synthea Demographic Dataset
│   ├── encounters_part_1.csv# ← Partitioned Clinical Records (Part 1)
│   └── encounters_part_2.csv# ← Partitioned Clinical Records (Part 2)
├── models/
│   └── cost_predictor.pkl   # ← Trained Random Forest Regressor (Predictive Engine)
├── requirements.txt         # ← Production Dependencies (Altair 4.2.2 fixed)
└── README.md
```

 Setup (Step-by-Step)

1. Install Python dependencies

```
pip install -r requirements.txt
```

2. Point to your Synthea CSV files
   Ensure your split files are located in the /data directory:

* patients.csv
* encounters_part_1.csv
* encounters_part_2.csv

3. Automated Data Recombination
   The dashboard utilizes a custom backend to bypass GitHub's 25MB file limit. The data_processor.py handles recombination automatically upon launch:

```python
# Function call within app/main.py
data, report = load_and_merge_data()
```

4. Run the Dashboard

```
streamlit run app/main.py
```

Open: Localhost port provided in terminal (standard is http://localhost:8501)

 Dashboard Logic

| Component           | Logic Source      | Description                                                 |
| ------------------- | ----------------- | ----------------------------------------------------------- |
| Data Recombination  | data_processor.py | Combines split CSV chunks to ensure 0 invalid foreign keys  |
| Intersectional Join | data_processor.py | Maps clinical encounters to race/gender/income demographics |
| Predictive Engine   | model_loader.py   | Loads Random Forest weights to forecast future claim costs  |
| Equity Visuals      | visuals.py        | Generates bar charts focused on the Vertical Equity gap     |

 Intersectional Equity Logic

| Metric              | Threshold/Insight                      | Target Policy Action                       |
| ------------------- | -------------------------------------- | ------------------------------------------ |
| Vertical Equity Gap | Avg Cost > $1,350 (Low Income)         | Advocate for 15% Higher Reimbursement      |
| Cost Disparity      | $895 (State Avg) vs $1,350 (High Risk) | Identify targeted funding for Social Needs |
| Disease Clustering  | > 300 Cases per City                   | Deploy specialized mobile health clinics   |

 Workflow Per Analysis

1. Data Merging
   Recombine partitioned files and clean patient records to ensure referential integrity.

2. Intersectional Mapping
   Apply join logic between Race, Gender, and Income datasets to identify marginalized cost burdens.

3. Analysis Pathways:

* Geographic Clusters: Identify cities (e.g., Los Angeles) with high-need comorbidities (e.g., 312 Hypertension cases).
* Financial Burden: Calculate Mean Claim Cost for marginalized segments to quantify the equity gap.

4. Predictive Forecasting
   Random Forest model predicts future financial risk based on input demographic profiles.

 Extending the Data Pipeline

To add new clinical metrics (e.g., Diabetes or Observations data), add the CSV to the data/ folder and update the join logic in src/data_processor.py:

```python
# Example addition to the pipeline
new_data = pd.read_csv('data/observations.csv')
merged_data = pd.merge(data, new_data, on='PATIENT_ID')
```

