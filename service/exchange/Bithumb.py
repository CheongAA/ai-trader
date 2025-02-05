import pybithumb
from service.TechnicalAnalysis import TechnicalAnalysis

class Bithumb:
    def __init__(self, api_access_key=None, api_secret_key=None, symbol="BTC"):
        self.symbol = symbol
        self.exchange = pybithumb.Bithumb(api_access_key, api_secret_key)

    def prepare_dataframe(self, df):
        """DataFrame을 JSON 직렬화 가능한 형태로 변환"""
        if df is None:
            return None
        
        # NaN 값 처리
        df = df.ffill().bfill()
        
        # 인덱스를 문자열로 변환
        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
        return df.reset_index().to_dict('records')

    def get_daily_data(self):
        df = self.exchange.get_candlestick(self.symbol, chart_intervals="24h").tail(100)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)

    def get_4h_data(self):
        df = self.exchange.get_candlestick(self.symbol, chart_intervals="4h").tail(100)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
    def get_1h_data(self):
        df = self.exchange.get_candlestick(self.symbol, chart_intervals="1h").tail(100)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
    def get_tickers(self):
        return self.exchange.get_tickers()
    
    def get_current_price(self):
        return self.exchange.get_current_price(self.symbol)
    
    def get_market_detail(self):
        return self.exchange.get_market_detail(self.symbol)
    
    def get_orderbook(self, limit=5):
        orderbook = self.exchange.get_orderbook(self.symbol)
        if orderbook:
            return {
                'timestamp': orderbook['timestamp'],
                'bids': orderbook['bids'][:limit],
                'asks': orderbook['asks'][:limit]
            }
        return None
    
    def get_candlestick(self, interval="1h", count=10):
        df = self.exchange.get_candlestick(self.symbol, chart_intervals=interval).tail(count)
        return self.prepare_dataframe(df)
    
    
    def get_trading_fee(self):
        return self.exchange.get_trading_fee(self.symbol)
    
    def get_balance(self):
        balance = {}
        for coin in self.exchange.get_tickers():
            balance[coin] = self.exchange.get_balance(coin)
        return balance
    
    def place_order(self, order_type, price, quantity):
        if order_type == 'buy':
            return self.exchange.buy_limit_order(self.symbol, price, quantity)
        elif order_type == 'sell':
            return self.exchange.sell_limit_order(self.symbol, price, quantity)
        else:
            raise ValueError("Invalid order type. Use 'buy' or 'sell'.")
        
    def cancel_order(self, order_desc):
        return self.exchange.cancel_order(order_desc)
    
    def get_outstanding_orders(self, order_desc):
        return self.exchange.get_outstanding_order(order_desc)
