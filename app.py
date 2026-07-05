from flask import Flask, render_template, request
import pandas as pd
import plotly.graph_objects as go
import base64 # 1. Import the base64 library
from src.predictor import generate_forecast

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        forecast_days = int(request.form.get('forecast_days', 30))
        
        if file:
            raw_data = pd.read_csv(file)
            forecast_df = generate_forecast(raw_data.copy(), forecast_days=forecast_days)
            
            history = raw_data[['Date', 'Items_Sold']].copy()
            history['Date'] = pd.to_datetime(history['Date'])
            
            future = forecast_df.copy()
            future['Date'] = pd.to_datetime(future['Date'])

            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=history['Date'], y=history['Items_Sold'], 
                mode='lines', name='Historical Sales', 
                line=dict(color='#31333F')
            ))
            
            fig.add_trace(go.Scatter(
                x=future['Date'], y=future['Predicted_Demand'], 
                mode='lines', name='Forecasted Demand', 
                line=dict(color='#FF4B4B')
            ))
            
            fig.update_layout(
                margin=dict(l=0, r=0, t=30, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font=dict(family="Space Grotesk, sans-serif"),
                xaxis=dict(showgrid=True, gridcolor='#E6E9EF'),
                yaxis=dict(showgrid=True, gridcolor='#E6E9EF')
            )
            
            chart_html = fig.to_html(full_html=False, include_plotlyjs='cdn')
            total_items_needed = int(forecast_df['Predicted_Demand'].sum())
            
            # 2. Convert dataframe to CSV string and encode it for HTML
            csv_data = forecast_df.to_csv(index=False)
            b64 = base64.b64encode(csv_data.encode()).decode()
            csv_href = f"data:text/csv;base64,{b64}"
            
            # 3. Pass the csv_href to the template
            return render_template(
                'results.html', 
                tables=forecast_df.to_html(classes='data', index=False), 
                total_items=total_items_needed,
                chart=chart_html,
                current_days=forecast_days,
                csv_href=csv_href
            )
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)