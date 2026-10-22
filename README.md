# Paisabazaar Credit Health Studio

An interactive Streamlit portfolio-analysis dashboard alongside the original Jupyter notebook. It explores score-label patterns, payment behaviour, aggregate customer journeys, and responsible customer-education experiments.

## Run on Windows

1. Keep `dataset-2.csv` beside `app.py` for local use.
2. Double-click `run_dashboard.bat`. It creates `.venv` if needed, installs requirements, starts the app, and opens the browser.
3. Or start it manually: `python -m pip install -r requirements.txt`, then `python -m streamlit run app.py`.
4. Open `http://127.0.0.1:8501` if the browser does not open automatically.

Open notebooks/credit_health_analysis.ipynb in Jupyter. The repository copy has saved outputs removed and its preview omits direct identifiers. Keep the source CSV local; it is excluded from Git. Docker is not required.

## Cloud configuration

`render.yaml` is configured to start the Streamlit app. It does not publish the dataset. For a hosted service, provide an authorized, de-identified dataset through a private mounted storage path and set the `PAISABAZAAR_DATA` environment variable to its CSV path. The source `dataset-2.csv` includes direct identifiers and is ignored by Git; do not add it to a public repository or public demo. The app excludes ID, Name, and SSN as it reads the CSV, and it only renders aggregates. That does not make uploading the original file to an untrusted host safe.

The cloud service is not deployed yet. A Git remote and cloud account/service setup are still needed. Use synthetic or de-identified data for a public showcase.

## Scope and interpretation

This is a descriptive analyst and customer-education project, not a default-risk model, eligibility tool, or automated credit decision service. The dataset has score labels but no verified repayment/default, application, approval, campaign, conversion, or revenue outcomes. Chart relationships are not causal evidence, and units/currency have not been verified. Business impact requires additional outcome data and a carefully measured pilot.


