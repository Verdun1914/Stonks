def generate_signals(df, patterns):
    signals = []

    required_cols = ['Date', 'Close', 'Volume', 'SMA', 'RSI', 'MACD', 'MACD_signal']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"❌ Missing columns: {missing_cols}")
        return []

    df = df.dropna(subset=required_cols).reset_index(drop=True)

    # Adjusted rolling windows for shorter data periods
    short_sma = df['SMA']  # 20-day SMA from compute_indicators
    long_sma = df['SMA'].rolling(window=10).mean()  # reduced from 50 to 10
    avg_volume = df['Volume'].rolling(window=10).mean()  # reduced from 20 to 10

    min_window = 10  # smallest window used here
    if len(df) < min_window:
        print("⚠️ Not enough data for signal generation.")
        return []

    for i in range(min_window, len(df)):
        reasons = []
        score = 0

        close = df['Close'].iloc[i]
        rsi = df['RSI'].iloc[i]
        macd = df['MACD'].iloc[i]
        macd_signal = df['MACD_signal'].iloc[i]
        volume = df['Volume'].iloc[i]
        sma = df['SMA'].iloc[i]
        trend = short_sma.iloc[i] > long_sma.iloc[i]

        # Rule-based conditions
        if rsi < 30:
            score += 2
            reasons.append("RSI < 30 (Oversold)")

        if rsi > 70:
            score -= 2
            reasons.append("RSI > 70 (Overbought)")

        if macd > macd_signal:
            score += 1
            reasons.append("MACD Bullish Crossover")

        if macd < macd_signal:
            score -= 1
            reasons.append("MACD Bearish Crossover")

        if close > sma:
            score += 1
            reasons.append("Price > SMA")

        if close < sma:
            score -= 1
            reasons.append("Price < SMA")

        if volume > avg_volume.iloc[i] * 1.5:
            score += 1
            reasons.append("Volume Spike")

        if trend:
            score += 1
            reasons.append("Uptrend")
        else:
            score -= 1
            reasons.append("Downtrend")

        # Pattern-based score
        for ts, pattern in patterns:
            if df['Date'].iloc[i] == ts:
                score += 1
                reasons.append(f"Pattern detected: {pattern}")

        # Final Signal decision
        if score >= 4:
            action = "🔥 HARD BUY"
        elif score >= 2:
            action = "🟢 Light Buy"
        elif score <= -4:
            action = "🔻 HARD SELL"
        elif score <= -2:
            action = "🟠 Light Sell"
        else:
            action = "⚪ HOLD"

        signals.append({
            "time": df.loc[i, 'Date'],
            "signal": action,
            "score": score,
            "reasons": reasons
        })

    return signals