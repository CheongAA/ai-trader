
class Binance:
    def __init__(self, api_access_key=None, api_secret_key=None, symbol="BTC"):
        self.symbol = symbol
        # self.exchange = ccxt.binance({
        #     'apiKey': api_access_key,
        #     'secret': api_secret_key,
        # })
        self.url = "https://www.binance.com/en/trade/{}_USDT?type=spot".format(symbol)
        self.xpath_list = [
            '//*[@id="1h"]'
        ]

    def get_url(self):
        return self.url
    
    def get_chart_xpath_list(self):
        return self.xpath_list
