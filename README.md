# SmartTrader 📈

A modular stock trading analysis dashboard using technical indicators, pattern recognition, and strategy rules to suggest trades.

## Features
- Candlestick charts with SMA, EMA, RSI, MACD, Bollinger Bands
- Pattern recognition (simple trends)
- Rule-based strategy decisions
- Backtest and analyze modes
- Interactive Plotly charts in a modern Streamlit GUI

## How to Run

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Run Streamlit app:
    ```bash
    streamlit run app.py
    ```

## Folder Structure



import streamlit as st

st.set_page_config(page_title="Info & Help", layout="wide")
st.title("📚 SmartTrader Information & Help")

# Button to return to dashboard page
if st.button("← Back to Dashboard"):
    st.set_query_params(page="app")

st.header("Signal Explanation")

st.markdown("""
**RSI (Relative Strength Index):**  
- Measures if a stock is overbought (>70) or oversold (<30).  
- Oversold means it might be a good time to buy, overbought means it could be time to sell.

**MACD (Moving Average Convergence Divergence):**  
- Tracks momentum by comparing two moving averages.  
- A bullish crossover (MACD > Signal line) suggests buying opportunity; bearish suggests selling.

**SMA (Simple Moving Average):**  
- The average stock price over a set number of days.  
- If the price is above SMA, it indicates upward momentum; below SMA, downward.

**Volume Spike:**  
- Unusually high trading volume compared to average indicates strong interest, confirming trend moves.

**Trend:**  
- Based on short and long SMAs to identify overall market direction (uptrend or downtrend).

---

### Signal Levels:

- 🔥 **HARD BUY:** Strong indications to buy immediately.  
- 🟢 **Light Buy:** Positive signs, consider buying.  
- ⚪ **HOLD:** No strong signals, best to wait.  
- 🟠 **Light Sell:** Early warning to consider selling.  
- 🔻 **HARD SELL:** Strong indications to sell immediately.

---

### What is Backtesting?

Backtesting is the process of testing a trading strategy using historical data to see how it would have performed.  
This helps traders evaluate the effectiveness of their strategies before risking real money.
""")
