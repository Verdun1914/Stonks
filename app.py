import streamlit as st
import pandas as pd
import yfinance as yf
from core.indicators import compute_indicators
from core.patterns import detect_patterns
from core.strategy import generate_signals
from core.visualize import plot_chart
from core.analysis import combined_analysis  # your combined pattern + sentiment function
import datetime
from streamlit_autorefresh import st_autorefresh

# Auto-refresh every minute (60000 ms)
st_autorefresh(interval=60 * 1000, key="datarefresh")

# Default start date 90 days ago
default_start = datetime.date.today() - datetime.timedelta(days=90)

# Common popular tickers dropdown list
COMMON_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA",
    "META", "NVDA", "BRK-B", "JPM", "V",
    "JNJ", "WMT", "PG", "DIS", "MA",
    "BAC", "XOM", "NFLX", "ADBE", "CSCO"
]

st.set_page_config(page_title="SmartTrader", layout="wide")

# Title and overall action layout
col1, col2 = st.columns([3, 2])
with col1:
    st.title("📈 SmartTrader Dashboard")
with col2:
    overall_action_placeholder = st.empty()

# Sidebar inputs
ticker = st.sidebar.selectbox("Select Stock Ticker", COMMON_TICKERS, index=0)
start_date = st.sidebar.date_input("Start Date", default_start)
end_date = st.sidebar.date_input("End Date", pd.to_datetime("today"))
mode = st.sidebar.selectbox("Mode", ["Analyze", "Backtest"])

# Run analysis automatically when ticker or dates change
def load_and_analyze(ticker, start_date, end_date, mode):
    data = yf.download(ticker, start=start_date, end=end_date, auto_adjust=True)

    # Fix multiindex columns if present
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = [col[0] for col in data.columns]

    # Rename Adj Close if exists
    if 'Adj Close' in data.columns:
        data.rename(columns={'Adj Close': 'Close'}, inplace=True)

    data.reset_index(inplace=True)

    if data.empty:
        st.warning("No data returned.")
        overall_action_placeholder.markdown("## Overall Action: **No Data**")
        return

    data = compute_indicators(data)
    patterns = detect_patterns(data)
    signals = generate_signals(data, patterns)

    # Combined analysis includes sentiment
    enhanced_signals, sentiment_score = combined_analysis(data, ticker)

    # Derive overall action from enhanced_signals
    # Aggregate by adding strength, simple heuristic
    total_strength = sum(signal['strength'] for signal in enhanced_signals) if enhanced_signals else 0

    if total_strength >= 4:
        overall_action = "🔥 HARD BUY"
    elif total_strength >= 2:
        overall_action = "🟢 Light Buy"
    elif total_strength <= -4:
        overall_action = "🔻 HARD SELL"
    elif total_strength <= -2:
        overall_action = "🟠 Light Sell"
    else:
        overall_action = "⚪ HOLD"

    # Display overall action and sentiment near top
    overall_action_placeholder.markdown(f"### Sentiment Score: {sentiment_score:.2f}")

    # Plot chart with signals
    fig = plot_chart(data, signals)
    st.plotly_chart(fig, use_container_width=True)

    # Latest signal details
    st.subheader("Latest Signal")
    if signals:
        latest = signals[-1]
        st.markdown(f"### {latest['signal']}")
        st.write("Reasons:")
        for reason in latest['reasons']:
            st.write(f"- {reason}")
        st.write(f"Score: {latest['score']}")
    else:
        st.write("No signal generated.")

    # Raw data table
    st.subheader("Raw Data")
    st.dataframe(data.tail(10))

    # Beginner-friendly explanation section
    with st.expander("📚 What do the signals mean?"):
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
        """)

if ticker and start_date and end_date:
    load_and_analyze(ticker, start_date, end_date, mode)
