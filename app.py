from flask import Flask, request, send_file, jsonify
import pandas as pd
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_pivot():
    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': 'Missing credentials'}), 400

    try:
        # Simulate login and downloading Excel from Superset
        session = requests.Session()

        # Simulated login to Superset (Replace with actual login URL and form fields)
        login_url = 'https://superset.youruniversity.edu/login/'
        login_payload = {
            'username': username,
            'password': password
        }
        session.post(login_url, data=login_payload)

        # Simulated file download (Replace with actual file URL)
        file_url = 'https://superset.youruniversity.edu/downloads/placement_file.xlsx'
        response = session.get(file_url)

        # Save Excel content in memory
        input_excel = BytesIO(response.content)

        # Read Excel file using pandas
        df = pd.read_excel(input_excel)

        # Extract required columns (adjust based on your Excel structure)
        columns_needed = ['Company', 'Status', 'Roll No', 'Name']
        columns_needed = ['Company', 'Status', 'Roll No', 'Name']
        df_filtered = df[columns_needed]
        if isinstance(df_filtered, pd.Series):
            df_filtered = pd.DataFrame(df_filtered)

        # Pivot the table
        pivot_df = pd.pivot_table(
            df_filtered,
            index=['Roll No', 'Name'],
            columns='Status',
            aggfunc='size',
            fill_value=0
        ).reset_index()

        # Save processed pivot to memory
        output = BytesIO()
        pivot_df.to_excel(output, index=False)
        output.seek(0)

        return send_file(output, download_name="pivoted.xlsx", as_attachment=True)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
