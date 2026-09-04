from flask import Flask, render_template, request, jsonify, Response
import math
import pandas as pd
import numpy as np
import io
from database import (
    export_db_to_csv, import_df_to_db, fetch_gdp_by_industry_db,
    create_industry, get_industry_by_code, update_industry, delete_industry
)
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
    Fetches GDP data dynamically from SQLite database and supports full CRUD & CSV upload/export.
    """
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_template('index.html', metadata=PROVINCE_METADATA)

    @app.route('/api/data', methods=['GET'])
    def get_dashboard_data():
        selected_year = request.args.get('year', None)
        raw_df = load_data()
        processed = process_data(raw_df)
        forecast = train_and_forecast(processed)
        metrics = evaluate_model(forecast['model'], forecast['X_hist'], forecast['y_hist'])
        insights = generate_economic_advisory(processed, forecast)

        yearly_dict = processed['yearly_df'].to_dict(orient='records')
        industry_rows = raw_df.to_dict(orient='records')

        if selected_year and selected_year in processed['years']:
            yr_str = str(selected_year)
            total_yr_gdp = processed['total_gdp'].get(yr_str, 0)
            for row in industry_rows:
                gva = row.get(yr_str, 0)
                row['selected_year_gva'] = gva
                row['selected_year_share'] = (gva / total_yr_gdp * 100) if total_yr_gdp else 0

        ind_forecasts = []
        for ind in forecast['industry_forecasts']:
            matching_row = raw_df[raw_df['code'] == ind['code']]
            if not matching_row.empty:
                latest_y = processed['latest_year']
                if latest_y in matching_row.columns:
                    ind[latest_y] = float(matching_row[latest_y].values[0])
            ind_forecasts.append(ind)

        actual_selected_year = selected_year if (selected_year and selected_year in processed['years']) else None

        payload = {
            'metadata': PROVINCE_METADATA,
            'selected_year': actual_selected_year,
            'processed': {
                'years': processed['years'],
                'latest_year': processed['latest_year'],
                'prev_year': processed['prev_year'],
                'total_gdp': processed['total_gdp'],
                'sector_gdp': processed['sector_gdp'],
                'yearly_df': yearly_dict,
                'industry_rows': industry_rows,
                'latest_gdp_2024': processed['latest_gdp_2024'],
                'latest_growth_2024': processed['latest_growth_2024'],
                'major_analytics': processed.get('major_analytics', {}),
                'all_ind_analytics': processed.get('all_ind_analytics', {}),
                'province_results': processed.get('province_results', {})
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

    # CRUD API Endpoints
    @app.route('/api/gdp', methods=['POST'])
    def api_create_gdp():
        """CREATE: Adds a new industry sector record."""
        data = request.get_json() or {}
        code = data.get('code')
        industry = data.get('industry')
        category = data.get('category')
        year_values = data.get('year_values', {})

        if not code or not industry or not category:
            return jsonify({'error': 'Missing required fields: code, industry, category'}), 400

        existing = get_industry_by_code(code)
        if existing:
            return jsonify({'error': f'Industry record with code {code} already exists'}), 400

        create_industry(code, industry, category, year_values)
        return jsonify({'message': f'Industry {code} created successfully'}), 201

    @app.route('/api/gdp/<code_id>', methods=['GET'])
    def api_read_gdp(code_id):
        """READ: Gets a single industry sector record."""
        row = get_industry_by_code(code_id)
        if not row:
            return jsonify({'error': f'Industry record with code {code_id} not found'}), 404
        return jsonify(convert_types(row))

    @app.route('/api/gdp/<code_id>', methods=['PUT'])
    def api_update_gdp(code_id):
        """UPDATE: Modifies an existing industry sector record and yearly figures."""
        data = request.get_json() or {}
        existing = get_industry_by_code(code_id)
        if not existing:
            return jsonify({'error': f'Industry record with code {code_id} not found'}), 404

        industry = data.get('industry')
        category = data.get('category')
        year_values = data.get('year_values', {})

        update_industry(code_id, industry=industry, category=category, year_values=year_values)
        return jsonify({'message': f'Industry {code_id} updated successfully'})

    @app.route('/api/gdp/<code_id>', methods=['DELETE'])
    def api_delete_gdp(code_id):
        """DELETE: Deletes an industry sector record."""
        existing = get_industry_by_code(code_id)
        if not existing:
            return jsonify({'error': f'Industry record with code {code_id} not found'}), 404

        delete_industry(code_id)
        return jsonify({'message': f'Industry {code_id} deleted successfully'})

    @app.route('/api/upload', methods=['POST'])
    def upload_data():
        """
        Endpoint to upload and import new/updated GDP CSV dataset into SQLite database.
        Supports adding future years (e.g. 2025 data).
        """
        try:
            if 'file' in request.files:
                file = request.files['file']
                if file.filename == '':
                    return jsonify({'error': 'No file selected'}), 400
                df = pd.read_csv(file)
            elif request.is_json:
                json_data = request.get_json()
                if isinstance(json_data, list):
                    df = pd.DataFrame(json_data)
                elif isinstance(json_data, dict) and 'rows' in json_data:
                    df = pd.DataFrame(json_data['rows'])
                else:
                    return jsonify({'error': 'Invalid JSON structure'}), 400
            else:
                return jsonify({'error': 'No CSV file or JSON body provided'}), 400

            required_cols = {'code', 'industry', 'category'}
            if not required_cols.issubset(df.columns):
                return jsonify({'error': f'Dataset missing required columns: {required_cols - set(df.columns)}'}), 400

            import_df_to_db(df)
            return jsonify({
                'message': 'Database updated successfully with imported dataset.',
                'rows_imported': len(df),
                'columns': list(df.columns)
            })
        except Exception as e:
            return jsonify({'error': f'Failed to process upload: {str(e)}'}), 500

    @app.route('/api/export', methods=['GET'])
    def export_data():
        """
        Endpoint to export database GDP data as CSV download or JSON.
        """
        fmt = request.args.get('format', 'csv')
        if fmt == 'json':
            df = fetch_gdp_by_industry_db()
            return jsonify(convert_types(df.to_dict(orient='records')))
        else:
            csv_content = export_db_to_csv()
            return Response(
                csv_content,
                mimetype="text/csv",
                headers={"Content-disposition": "attachment; filename=zamboanga_del_norte_gdp_export.csv"}
            )

    @app.route('/api/predict', methods=['POST'])
    def predict():
        raw_df = load_data()
        processed = process_data(raw_df)
        forecast = train_and_forecast(processed)
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
        raw_df = load_data()
        processed = process_data(raw_df)
        forecast = train_and_forecast(processed)
        return jsonify(convert_types(forecast['forecast_total']))

    @app.route('/api/insights', methods=['GET'])
    def get_insights():
        raw_df = load_data()
        processed = process_data(raw_df)
        forecast = train_and_forecast(processed)
        insights = generate_economic_advisory(processed, forecast)
        return jsonify(convert_types(insights))

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
