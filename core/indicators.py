import pandas as pd
import ta

def compute_indicators(df):
    df = df.copy()

    # Ensure Close is a flat Series
    close_series = pd.Series(df['Close'].values.flatten(), index=df.index)

    df['SMA'] = close_series.rolling(window=20).mean()
    df['EMA'] = close_series.ewm(span=20, adjust=False).mean()
    df['RSI'] = ta.momentum.RSIIndicator(close=close_series).rsi()

    macd = ta.trend.MACD(close=close_series)
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()

    bb = ta.volatility.BollingerBands(close=close_series)
    df['BB_high'] = bb.bollinger_hband()
    df['BB_low'] = bb.bollinger_lband()

    return df
