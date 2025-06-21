import plotly.graph_objects as go
import pandas as pd

def plot_chart(df, signals):
    # Ensure 'Date' column and signal times are datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    fig = go.Figure(data=[go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name="Candlesticks"
    )])

    fig.add_trace(go.Scatter(x=df['Date'], y=df['SMA'], name='SMA', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['EMA'], name='EMA', line=dict(color='orange')))

    for signal in signals:
        signal_time = pd.to_datetime(signal['time'])
        match_row = df[df['Date'] == signal_time]
        if not match_row.empty:
            y_value = match_row['Close'].values[0]
            fig.add_trace(go.Scatter(
                x=[signal_time],
                y=[y_value],
                mode='markers',
                marker=dict(size=10, color='green' if 'BUY' in signal['signal'] else 'red'),
                name=signal['signal']
            ))

    fig.update_layout(title="SmartTrader Chart", xaxis_title="Date", yaxis_title="Price")
    return fig