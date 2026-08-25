from flask import Flask, render_template, request, jsonify
import math
import pandas as pd
import numpy as np
from Data_Collection import load_data
from Data_Processing import process_data
from Model_Development import train_and_forecast
from Evaluation import evaluate_model
from Advisory_Engine import generate_economic_advisory
from data_dict import PROVINCE_METADATA

def convert_types(obj):
    if isinstance(obj, (np.int64, np.int32)):
        return int(obj)
    elif isinstance(obj, (np.float64, np.float32, float)):
        if math.isnan(obj):
            return None
        return float(obj)
    elif isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_types(v) for v in obj]
    return obj

def create_app():
    """
    Flask Application Factory for Zamboanga del Norte Economic Advisory Platform.
    """
    app = Flask(__name__)

    # Pre-compute pipeline data
    raw_df = load_data()
    processed = process_data(raw_df)
    forecast = train_and_forecast(processed)
    metrics = evaluate_model(forecast['model'], forecast['X_hist'], forecast['y_hist'])
    insights = generate_economic_advisory(processed, forecast)

    @app.route('/')
    def index():
        return render_template('index.html', metadata=PROVINCE_METADATA)

    @app.route('/api/data', methods=['GET'])
    def get_dashboard_data():
        yearly_dict = processed['yearly_df'].to_dict(orient='records')

        # Add 2023 values to industry forecasts if missing
        ind_forecasts = []
        for ind in forecast['industry_forecasts']:
            matching_row = processed['raw_df'][processed['raw_df']['code'] == ind['code']]
            if not matching_row.empty:
                ind['2023'] = float(matching_row['2023'].values[0])
            ind_forecasts.append(ind)

        payload = {
            'metadata': PROVINCE_METADATA,
            'processed': {
                'years': processed['years'],
                'total_gdp': processed['total_gdp'],
                'sector_gdp': processed['sector_gdp'],
                'yearly_df': yearly_dict,
                'latest_gdp_2024': processed['latest_gdp_2024'],
                'latest_growth_2024': processed['latest_growth_2024']
            },
            'forecast': {
                'forecast_total': forecast['forecast_total'],
                'sector_forecasts': forecast['sector_forecasts'],
                'industry_forecasts': ind_forecasts
            },
            'metrics': metrics,
            'insights': insights
        }

        return jsonify(convert_types(payload))

    @app.route('/api/predict', methods=['POST'])
    def predict():
        data = request.get_json() or {}
        year = data.get('year', 2028)
        try:
            year_val = float(year)
            pred = forecast['model'].predict([[year_val]])[0]
            return jsonify({'year': year_val, 'predicted_gdp': round(float(pred), 2)})
        except Exception as e:
            return jsonify({'error': str(e)}), 400

    @app.route('/api/forecast', methods=['GET'])
    def get_forecast():
        return jsonify(convert_types(forecast['forecast_total']))

    @app.route('/api/insights', methods=['GET'])
    def get_insights():
        return jsonify(convert_types(insights))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
