# AI-Driven-Economic-Advisory-Platform

Overview An advanced AI-driven platform designed to analyze economic data, generate comprehensive reports, provide feedback, and offer actionable recommendations to improve the economic performance of a place or province.

---

## Architecture Overview

The platform is designed around a modular end-to-end data, ML, and web analytics pipeline:

1. **Database Layer (`database.py`)**: SQLite database (`gdp_database.db`) providing dynamic schema management (auto-altering tables when new year columns like 2025+ are added) and data persistence for sector-level Gross Value Added (GVA) / GDP numbers.
2. **Data Collection & Ingestion (`Data_Collection.py`)**: Ingests baseline dataset from the SQLite database dynamically, ensuring real-time economic sync without reliance on static HTML numbers.
3. **Data Processing & Analytics Engine (`Data_Processing.py`)**: Computes 8 core economic matrices across all available years:
   - YoY Growth Rate by Major Industry
   - YoY Growth Rate by All Industries
   - Share of Major Industries in GDP
   - Share of All Industries in GDP
   - Contribution to Growth (in Percentage Points) by Major Industry
   - Contribution to Growth (in Percentage Points) by All Industries
   - Percentage Share by Major Industry
   - Percentage Share by All Industries
4. **Machine Learning & Advisory Engine (`Model_Development.py`, `Advisory_Engine.py`, `Evaluation.py`)**: Predicts future GDP trajectories (2026–2030) using sector-level trend forecasting models, evaluates model performance metrics, and generates strategic policy advisories and simulation scenarios.
5. **REST API & Web Deployment Layer (`Deployment.py`, `main.py`, `templates/index.html`)**: Flask REST application exposing endpoints for interactive data exploration, CSV/JSON data uploads, dynamic CSV export, policy advisory queries, and scenario simulation.

---

## Key Features

- **Dynamic Database Updates**: Fetches provincial/regional GDP data dynamically from SQLite database tables instead of static figures.
- **Upload, Import, and Export Capabilities**: Provides API endpoints and UI buttons for uploading/importing CSV data files and exporting current GDP data into CSV format. Automatically adapts DB schema to support future real datasets (e.g., PSA 2025 real GDP updates).
- **8 Economic Analytics Matrices**: Toggleable views for Growth Rates, GDP Shares, Contribution to Growth (in percentage points), and Percentage Shares across Major Industries and All Industries over all recorded years.
- **AI Policy Advisory & Scenario Simulator**: Interactive interface to simulate policy interventions (e.g., Agricultural Modernization, Industrial Modernization, Digital Infrastructure) and compute projected GDP target impact.
- **Dynamic Frontend Dashboard**: Dark-mode dashboard built with Chart.js and Tailwind CSS featuring dynamic sector tables, dynamic growth charts, target cards, and metric switchers.

---

## Directory Structure

```
AI-Driven-Economic-Advisory-Platform/
├── Advisory_Engine.py         # Policy advisory generation and intervention simulator
├── Data_Collection.py         # Dynamic SQLite database loader module
├── Data_Processing.py         # Analytics engine calculating 8 economic metrics
├── Deployment.py              # Flask REST API routes and application setup
├── Evaluation.py              # ML model evaluation metrics (MAE, RMSE, MAPE)
├── Model_Development.py       # GDP trend forecasting models (2026-2030)
├── Visualization.py           # Matplotlib & Seaborn static visualization helper script
├── database.py                # SQLite DB initialization, query, upsert, schema evolution & CSV export/import
├── data_dict.py               # Sector definitions and metadata dictionary
├── economic_data.csv          # Baseline economic data in CSV format
├── gdp_database.db            # SQLite database file storing economic metrics
├── main.py                    # Primary entry point launching Flask Web Server on port 5000
├── main_2.py                  # Standalone ML pipeline runner script
├── zamboanga_gdp.csv          # Sectoral GVA baseline dataset
├── static/                    # Frontend static assets (CSS/JS)
├── templates/
│   └── index.html             # Dynamic web dashboard HTML template
└── tests/
    └── test_pipeline.py       # Automated pytest test suite covering DB, pipeline, and API endpoints
```

---

## Quickstart Guide

### 1. Local Environment Setup

Ensure Python 3.10+ is installed. Clone the repository and install requirements:

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies (Flask, Pandas, NumPy, Scikit-learn, Pytest)
pip install flask pandas numpy scikit-learn pytest
```

### 2. Seed Database & Run ML Pipeline

To seed the SQLite database (`gdp_database.db`) from CSV files and execute the machine learning workflow:

```bash
python3 main_2.py
```

or

```bash
python main_2.py
```

### 3. Launch REST API Server

Start the Flask REST API server and interactive dashboard:

```bash
python3 main.py
```
or
```bash
python main.py
```

The application will be accessible at `http://localhost:5000`.

### 4. Run Automated Daily Pipeline

To execute the data ingestion, ML forecasting, and database refresh sequence automatically (e.g., via cron or scheduled task):

```bash
python3 -c "import database, Data_Collection, Data_Processing, Model_Development; database.init_db(); df = Data_Collection.load_data(); Data_Processing.process_data(df)"
```
or 

```bash
python -c "import database, Data_Collection, Data_Processing, Model_Development; database.init_db(); df = Data_Collection.load_data(); Data_Processing.process_data(df)"
```

### 5. Run Test Suite

Run the pytest suite to verify all pipeline components, database operations, and API endpoints:

```bash
PYTHONPATH=. pytest tests/test_pipeline.py
```
or

```bash
set PYTHONPATH=.& pytest tests/test_pipeline.py
```
---

## API Endpoints Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/` | Serves the main web dashboard (`index.html`). |
| `GET` | `/api/data` | Returns dynamic historical GDP numbers, sector analytics, 8 economic breakdown matrices, forecasts, and advisory insights in JSON. |
| `POST` | `/api/upload` | Uploads a CSV or JSON payload to dynamically update the SQLite database and add new year columns (e.g. 2025 data). |
| `GET` | `/api/export` | Downloads the current GDP database content as a CSV file. |
| `POST` | `/api/advisory` | Generates strategic recommendations based on target growth rate inputs. |
| `POST` | `/api/simulate` | Evaluates policy intervention scenarios and returns projected GDP gain and growth impact. |

---

## Power BI Dashboard Overview

The platform supports reporting and visual BI integration:
- **CSV Data Connector**: Export the database via `GET /api/export` or click the "Export CSV" button on the dashboard to generate a clean CSV dataset suitable for Power BI.
- **REST API Integration**: Connect Power BI Web Data Source directly to `http://localhost:5000/api/data` for automated dashboard data refreshes.
- **Supported Visualizations**: Sectoral distribution doughnuts, annual growth rate matrices, contribution to growth percentage-point bar charts, and 2026–2030 projected trajectory lines.

---

## Cloud Deployment (Azure)

To deploy the application to Microsoft Azure:

1. **Azure App Service (Linux Web App)**:
   - Create a Web App on Azure App Service with a Python 3.12 runtime stack.
   - Configure the startup command to launch Gunicorn / Flask:
     ```bash
     gunicorn --bind=0.0.0.0:8000 main:app
     ```
   - Set persistent storage options or mount Azure Files if persisting SQLite database state (`gdp_database.db`) across restarts.

2. **Azure Container Instances (ACI)**:
   - Build a Docker container using the project root Dockerfile.
   - Push the container image to Azure Container Registry (ACR).
   - Deploy container instance on ACI mapping port `5000`.
