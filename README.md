# Health_Equity_Insights_Dashboard
Intersectional Health Analytics & Cost Burden Tracker

# Architecture

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

# Setup (Step-by-Step)
# 1. Environment Configuration
Install the required analytics libraries:
pip install -r requirements.txt
