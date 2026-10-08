import json
import math
import shutil
from pathlib import Path

import numpy as np

from Data_Collection import load_data
from Data_Processing import process_data
from Model_Development import train_and_forecast
from Evaluation import evaluate_model
from Advisory_Engine import generate_economic_advisory

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
DATA_DIR = PUBLIC / "data"


def clean(value):
    if isinstance(value, dict):
        return {str(k): clean(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [clean(v) for v in value]
    if isinstance(value, np.generic):
        return clean(value.item())
    if isinstance(value, float):
        return None if math.isnan(value) or math.isinf(value) else value
    return value


def main():
    raw_df = load_data()
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    metrics = evaluate_model(
        forecast["model"],
        forecast["X_hist"],
        forecast["y_hist"],
    )
    insights = generate_economic_advisory(processed, forecast)

    industry_rows = raw_df.to_dict(orient="records")

    industry_forecasts = []
    for item in forecast["industry_forecasts"]:
        row = dict(item)
        matching = raw_df[raw_df["code"] == item["code"]]
        if not matching.empty:
            latest_year = processed["latest_year"]
            if latest_year in matching.columns:
                row[latest_year] = float(matching[latest_year].values[0])
        industry_forecasts.append(row)

    payload = {
        "metadata": {
            "province": "Zamboanga del Norte",
            "platform": "Provincial Product Accounts & AI Platform",
            "deployment": "Netlify Static Build",
        },
        "selected_year": None,
        "processed": {
            "years": processed["years"],
            "latest_year": processed["latest_year"],
            "prev_year": processed["prev_year"],
            "total_gdp": processed["total_gdp"],
            "sector_gdp": processed["sector_gdp"],
            "yearly_df": processed["yearly_df"].to_dict(orient="records"),
            "industry_rows": industry_rows,
            "latest_gdp_2024": processed["latest_gdp_2024"],
            "latest_growth_2024": processed["latest_growth_2024"],
            "major_analytics": processed.get("major_analytics", {}),
            "all_ind_analytics": processed.get("all_ind_analytics", {}),
            "province_results": processed.get("province_results", {}),
        },
        "forecast": {
            "forecast_total": forecast["forecast_total"],
            "sector_forecasts": forecast["sector_forecasts"],
            "industry_forecasts": industry_forecasts,
        },
        "metrics": metrics,
        "insights": insights,
    }

    PUBLIC.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "templates" / "index.html", PUBLIC / "index.html")

    with open(DATA_DIR / "dashboard.json", "w", encoding="utf-8") as f:
        json.dump(clean(payload), f, ensure_ascii=False, separators=(",", ":"))

    print(f"Dashboard build complete: {DATA_DIR / 'dashboard.json'}")
    print(f"Years: {processed['years']}")
    print(f"Latest year: {processed['latest_year']}")


if __name__ == "__main__":
    main()
