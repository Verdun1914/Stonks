from core.patterns import detect_patterns
from core.sentiment import fetch_news, analyze_sentiment

def combined_analysis(df, ticker):
    # Detect patterns
    patterns = detect_patterns(df)

    # Get news sentiment
    news_texts = fetch_news(ticker)
    sentiment_score = analyze_sentiment(news_texts)

    # Define sentiment thresholds
    positive_thresh = 0.2
    negative_thresh = -0.2

    # Combine signals
    enhanced_signals = []
    for date, pattern in patterns:
        signal_strength = 1.0
        # Boost signal if sentiment is positive and pattern bullish
        if sentiment_score > positive_thresh and 'Bullish' in pattern:
            signal_strength += 0.5
        # Weaken signal if sentiment is negative and pattern bullish
        elif sentiment_score < negative_thresh and 'Bullish' in pattern:
            signal_strength -= 0.5
        # Inverse for bearish patterns
        if sentiment_score < negative_thresh and 'Bearish' in pattern:
            signal_strength += 0.5
        elif sentiment_score > positive_thresh and 'Bearish' in pattern:
            signal_strength -= 0.5
        enhanced_signals.append({'date': date, 'pattern': pattern, 'strength': signal_strength})

    return enhanced_signals, sentiment_score
