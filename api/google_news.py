import requests

# Fetch Google News
class GoogleNewsAPI:
    def __init__(self, api_key,location="United States"):
        self.api_key = api_key
        self.location = location
        self.url = "https://www.searchapi.io/api/v1/search"

    def fetch_news(self, query):
        params = {
            "engine": "google_news",
            "q": query,  # 예시: "stock market", "crypto news"
            "time_period": "last_day", 
            "location": self.location,
            "api_key": self.api_key

        }

        response = requests.get(self.url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data['organic_results']
        else:
            print("Error fetching news")
            return []
