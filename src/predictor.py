import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression

def generate_forecast(df, forecast_days=30):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values('Date')
    
    start_date = df['Date'].min()
    df['Days_Since'] = (df['Date'] - start_date).dt.days
    
    X = df[['Days_Since']]
    y = df['Items_Sold']
    
    model = LinearRegression()
    model.fit(X, y)
    
    max_day = df['Days_Since'].max()
    future_days = np.array(range(max_day + 1, max_day + 1 + forecast_days)).reshape(-1, 1)
    
    predictions = model.predict(future_days)
    
    last_date = df['Date'].max()
    future_dates = [last_date + pd.Timedelta(days=i) for i in range(1, forecast_days + 1)]
    
    forecast_df = pd.DataFrame({
        'Date': future_dates,
        'Predicted_Demand': np.round(predictions, 0).astype(int)
    })
    
    forecast_df['Predicted_Demand'] = forecast_df['Predicted_Demand'].clip(lower=0)
    
    return forecast_df