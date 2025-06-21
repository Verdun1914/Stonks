import pandas as pd
import numpy as np

def detect_patterns(df):
    """
    Detects up to 50 popular candlestick and chart patterns.
    Returns list of tuples: (timestamp, pattern_name)
    """
    patterns = []

    # Validate columns
    required_cols = ['Date', 'Open', 'High', 'Low', 'Close']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"DataFrame must have '{col}' column")

    df = df.dropna(subset=required_cols).reset_index(drop=True)
    length = len(df)

    # Helper functions
    def is_bullish(i): return df.loc[i, 'Close'] > df.loc[i, 'Open']
    def is_bearish(i): return df.loc[i, 'Close'] < df.loc[i, 'Open']
    def body_size(i): return abs(df.loc[i, 'Close'] - df.loc[i, 'Open'])
    def candle_range(i): return df.loc[i, 'High'] - df.loc[i, 'Low']
    def upper_shadow(i): return df.loc[i, 'High'] - max(df.loc[i, 'Close'], df.loc[i, 'Open'])
    def lower_shadow(i): return min(df.loc[i, 'Close'], df.loc[i, 'Open']) - df.loc[i, 'Low']
    def is_doji(i): return abs(df.loc[i, 'Close'] - df.loc[i, 'Open']) <= 0.001 * df.loc[i, 'Close']

    for i in range(5, length):

        date = df.loc[i, 'Date']
        o, h, l, c = df.loc[i, ['Open', 'High', 'Low', 'Close']]
        o1, h1, l1, c1 = df.loc[i-1, ['Open', 'High', 'Low', 'Close']]
        o2, h2, l2, c2 = df.loc[i-2, ['Open', 'High', 'Low', 'Close']]
        o3, h3, l3, c3 = df.loc[i-3, ['Open', 'High', 'Low', 'Close']]
        o4, h4, l4, c4 = df.loc[i-4, ['Open', 'High', 'Low', 'Close']]
        o5, h5, l5, c5 = df.loc[i-5, ['Open', 'High', 'Low', 'Close']]

        body = body_size(i)
        ls = lower_shadow(i)
        us = upper_shadow(i)

        # 1. Hammer
        if body > 0 and ls > 2 * body and us < 0.1 * body and is_bullish(i):
            patterns.append((date, 'Hammer'))

        # 2. Hanging Man
        if body > 0 and ls > 2 * body and us < 0.1 * body and is_bearish(i):
            patterns.append((date, 'Hanging Man'))

        # 3. Inverted Hammer
        if body > 0 and us > 2 * body and ls < 0.1 * body and is_bullish(i):
            patterns.append((date, 'Inverted Hammer'))

        # 4. Shooting Star
        if body > 0 and us > 2 * body and ls < 0.1 * body and is_bearish(i):
            patterns.append((date, 'Shooting Star'))

        # 5. Bullish Engulfing
        if is_bearish(i-1) and is_bullish(i) and o < c1 and c > o1:
            patterns.append((date, 'Bullish Engulfing'))

        # 6. Bearish Engulfing
        if is_bullish(i-1) and is_bearish(i) and o > c1 and c < o1:
            patterns.append((date, 'Bearish Engulfing'))

        # 7. Morning Star
        cond1 = is_bearish(i-2)
        cond2 = body_size(i-1) < body_size(i-2) * 0.5
        cond3 = is_bullish(i)
        cond4 = c > (o2 + c2) / 2
        if cond1 and cond2 and cond3 and cond4:
            patterns.append((date, 'Morning Star'))

        # 8. Evening Star
        cond1 = is_bullish(i-2)
        cond2 = body_size(i-1) < body_size(i-2) * 0.5
        cond3 = is_bearish(i)
        cond4 = c < (o2 + c2) / 2
        if cond1 and cond2 and cond3 and cond4:
            patterns.append((date, 'Evening Star'))

        # 9. Doji
        if is_doji(i):
            patterns.append((date, 'Doji'))

        # 10. Three White Soldiers
        if all(is_bullish(j) for j in [i-2, i-1, i]) and \
           df.loc[i-2:i, 'Close'].is_monotonic_increasing:
            patterns.append((date, 'Three White Soldiers'))

        # 11. Three Black Crows
        if all(is_bearish(j) for j in [i-2, i-1, i]) and \
           df.loc[i-2:i, 'Close'].is_monotonic_decreasing:
            patterns.append((date, 'Three Black Crows'))

        # 12. Piercing Line
        if is_bearish(i-1) and is_bullish(i):
            midpoint = (o1 + c1) / 2
            if c > midpoint and o < c1:
                patterns.append((date, 'Piercing Line'))

        # 13. Dark Cloud Cover
        if is_bullish(i-1) and is_bearish(i):
            midpoint = (o1 + c1) / 2
            if c < midpoint and o > c1:
                patterns.append((date, 'Dark Cloud Cover'))

        # 14. Bullish Harami
        if is_bearish(i-1) and is_bullish(i) and o > c1 and c < o1:
            patterns.append((date, 'Bullish Harami'))

        # 15. Bearish Harami
        if is_bullish(i-1) and is_bearish(i) and o < c1 and c > o1:
            patterns.append((date, 'Bearish Harami'))

        # 16. Rising Three Methods
        if i >= 5:
            cond1 = is_bullish(i-5)
            cond2 = all(is_bearish(j) for j in range(i-4, i-1))
            cond3 = all(df.loc[j, 'Close'] > df.loc[i-5, 'Open'] and df.loc[j, 'Open'] < df.loc[i-5, 'Close'] for j in range(i-4, i-1))
            cond4 = is_bullish(i)
            cond5 = c > df.loc[i-5, 'Close']
            if cond1 and cond2 and cond3 and cond4 and cond5:
                patterns.append((date, 'Rising Three Methods'))

        # 17. Falling Three Methods
        if i >= 5:
            cond1 = is_bearish(i-5)
            cond2 = all(is_bullish(j) for j in range(i-4, i-1))
            cond3 = all(df.loc[j, 'Close'] < df.loc[i-5, 'Open'] and df.loc[j, 'Open'] > df.loc[i-5, 'Close'] for j in range(i-4, i-1))
            cond4 = is_bearish(i)
            cond5 = c < df.loc[i-5, 'Close']
            if cond1 and cond2 and cond3 and cond4 and cond5:
                patterns.append((date, 'Falling Three Methods'))

        # 18. Bullish Belt Hold
        if is_bullish(i) and o == l and c > o and (h - c) < 0.1 * body:
            patterns.append((date, 'Bullish Belt Hold'))

        # 19. Bearish Belt Hold
        if is_bearish(i) and o == h and c < o and (c - l) < 0.1 * body:
            patterns.append((date, 'Bearish Belt Hold'))

        # 20. Tweezer Bottom
        if i >= 1 and l == l1 and is_bearish(i-1) and is_bullish(i):
            patterns.append((date, 'Tweezer Bottom'))

        # 21. Tweezer Top
        if i >= 1 and h == h1 and is_bullish(i-1) and is_bearish(i):
            patterns.append((date, 'Tweezer Top'))

        # 22. Marubozu Bullish
        if o == l and c == h and is_bullish(i):
            patterns.append((date, 'Bullish Marubozu'))

        # 23. Marubozu Bearish
        if o == h and c == l and is_bearish(i):
            patterns.append((date, 'Bearish Marubozu'))

        # 24. Long Legged Doji
        if is_doji(i) and (h - l) > 3 * body:
            patterns.append((date, 'Long Legged Doji'))

        # 25. Dragonfly Doji
        if is_doji(i) and l == o == c:
            patterns.append((date, 'Dragonfly Doji'))

        # 26. Gravestone Doji
        if is_doji(i) and h == o == c:
            patterns.append((date, 'Gravestone Doji'))

        # 27. Mat Hold
        # Complex pattern - simplified example of 5 candles with 3 small pullbacks
        if i >= 5 and all(is_bullish(j) for j in [i-5, i-1, i]):
            mid_bears = all(is_bearish(j) and body_size(j) < body_size(i-5)*0.5 for j in [i-4, i-3, i-2])
            if mid_bears:
                patterns.append((date, 'Mat Hold'))

        # 28. Homing Pigeon
        if is_bearish(i-1) and is_bearish(i) and o > o1 and c < c1:
            patterns.append((date, 'Homing Pigeon'))

        # 29. Matching Low
        if i >= 1 and l == l1:
            patterns.append((date, 'Matching Low'))

        # 30. On Neck Line
        if i >= 1 and is_bearish(i-1) and is_bearish(i) and c > l1 and abs(c - l1) < 0.001*c:
            patterns.append((date, 'On Neck Line'))

        # 31. In Neck Line
        if i >= 1 and is_bearish(i-1) and is_bearish(i) and c < l1 and c > l1 * 0.99:
            patterns.append((date, 'In Neck Line'))

        # 32. Thrusting Line
        if i >= 1 and is_bearish(i-1) and is_bullish(i) and c > c1 and c < o1:
            patterns.append((date, 'Thrusting Line'))

        # 33. Deliberation Line
        if i >= 2 and is_bearish(i-2) and is_bearish(i-1) and is_bullish(i) and o > c2 and c < o2:
            patterns.append((date, 'Deliberation Line'))

        # 34. Advance Block
        if i >= 2 and all(is_bullish(j) for j in [i-2, i-1, i]):
            if df.loc[i-1, 'Close'] < df.loc[i-2, 'Close'] and df.loc[i, 'Close'] < df.loc[i-1, 'Close']:
                patterns.append((date, 'Advance Block'))

        # 35. Evening Doji Star
        if i >= 2 and is_bullish(i-2) and is_doji(i-1) and is_bearish(i) and c < (o2 + c2) / 2:
            patterns.append((date, 'Evening Doji Star'))

        # 36. Morning Doji Star
        if i >= 2 and is_bearish(i-2) and is_doji(i-1) and is_bullish(i) and c > (o2 + c2) / 2:
            patterns.append((date, 'Morning Doji Star'))

        # 37. Bullish Kicker
        if i >= 1 and is_bearish(i-1) and is_bullish(i) and o > c1:
            patterns.append((date, 'Bullish Kicker'))

        # 38. Bearish Kicker
        if i >= 1 and is_bullish(i-1) and is_bearish(i) and o < c1:
            patterns.append((date, 'Bearish Kicker'))

        # 39. Upside Gap Two Crows
        if i >= 2 and is_bearish(i-2) and is_bullish(i-1) and is_bearish(i) and o1 > h2 and o < c1 and c > o:
            patterns.append((date, 'Upside Gap Two Crows'))

        # 40. Downside Gap Three Methods
        if i >= 4 and is_bearish(i-4) and all(is_bullish(j) for j in range(i-3, i-1)) and is_bearish(i):
            if all(df.loc[j, 'Close'] < df.loc[i-4, 'Open'] and df.loc[j, 'Open'] > df.loc[i-4, 'Close'] for j in range(i-3, i-1)):
                patterns.append((date, 'Downside Gap Three Methods'))

        # 41. Bearish Separating Lines
        if i >= 1 and is_bearish(i) and is_bearish(i-1) and o == o1 and c < c1:
            patterns.append((date, 'Bearish Separating Lines'))

        # 42. Bullish Separating Lines
        if i >= 1 and is_bullish(i) and is_bullish(i-1) and o == o1 and c > c1:
            patterns.append((date, 'Bullish Separating Lines'))

        # 43. Stick Sandwich
        if i >= 2 and is_bearish(i-2) and is_bullish(i-1) and is_bearish(i):
            if abs(c2 - c) <= (0.001 * c) and c1 < c2 and c1 < c:
                patterns.append((date, 'Stick Sandwich'))

        # 44. Tasuki Gap
        if i >= 2 and is_bullish(i-2) and is_bullish(i-1) and is_bearish(i):
            if o < c1 and o1 > c2 and c > o1:
                patterns.append((date, 'Tasuki Gap'))

        # 45. Abandoned Baby
        if i >= 2 and is_bearish(i-2) and is_doji(i-1) and is_bullish(i):
            if (l1 > h2) and (o > c1):
                patterns.append((date, 'Abandoned Baby'))

        # 46. Kicking (Bullish)
        if i >= 1 and is_bearish(i-1) and is_bullish(i) and o > c1 and o1 == h1:
            patterns.append((date, 'Kicking (Bullish)'))

        # 47. Kicking (Bearish)
        if i >= 1 and is_bullish(i-1) and is_bearish(i) and o < c1 and o1 == l1:
            patterns.append((date, 'Kicking (Bearish)'))

        # 48. Long Black Candle
        if is_bearish(i) and body > 1.5 * np.mean([body_size(j) for j in range(i-5, i)]):
            patterns.append((date, 'Long Black Candle'))

        # 49. Long White Candle
        if is_bullish(i) and body > 1.5 * np.mean([body_size(j) for j in range(i-5, i)]):
            patterns.append((date, 'Long White Candle'))

        # 50. Spinning Top
        if body <= 0.3 * candle_range(i) and lower_shadow(i) > 0.3 * candle_range(i) and upper_shadow(i) > 0.3 * candle_range(i):
            patterns.append((date, 'Spinning Top'))

    return patterns