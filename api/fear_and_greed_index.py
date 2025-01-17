import requests

# Fetch Fear and Greed Index
class FearAndGreedIndex:
    def __init__(self):
        self.url = "https://api.alternative.me/fng/"
    
    def fetch_fear_and_greed_index(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            data = response.json()
            index = data['data'][0]['value']
            return index
        else:
            print("Error fetching Fear and Greed Index")
            return None

