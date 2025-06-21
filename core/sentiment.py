import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import datetime

API_KEY = "b08c53811f3241d5a4f9fe21fa414af6"

def fetch_news(ticker, days=3):
    """
    Fetch recent news for ticker using NewsAPI.
    """
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=days)
    url = (
        f"https://newsapi.org/v2/everything?"
        f"q={ticker}&"
        f"from={start_date}&"
        f"to={end_date}&"
        f"language=en&"
        f"sortBy=relevancy&"
        f"apiKey={API_KEY}"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return []
    articles = response.json().get("articles", [])
    return [a['title'] + ". " + (a['description'] or '') for a in articles]

def analyze_sentiment(texts):
    """
    Analyze sentiment of list of texts and return average compound score.
    """
    analyzer = SentimentIntensityAnalyzer()
    scores = [analyzer.polarity_scores(text)['compound'] for text in texts if text]
    if not scores:
        return 0.0
    return sum(scores) / len(scores)
