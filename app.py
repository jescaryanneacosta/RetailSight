from flask import Flask, render_template, request
import pandas as pd
from src.predictor import generate_forecast

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # 1. Handle the uploaded CSV file
        file = request.files['file']
        raw_data = pd.read_csv(file)
        
        # 2. Run your existing predictor logic
        forecast_df = generate_forecast(raw_data, forecast_days=30)
        
        # 3. Pass the results to the HTML page
        return render_template(
            'results.html', 
            tables=[forecast_df.to_html(classes='data')], 
            titles=forecast_df.columns.values
        )
        
    # If it's just a standard visit (GET request), show the upload form
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)