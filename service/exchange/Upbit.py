import pyupbit
from service.TechnicalAnalysis import TechnicalAnalysis

class Upbit:
    def __init__(self, api_access_key=None, api_secret_key=None, symbol="BTC"):
        self.symbol = "KRW-" + symbol
        self.exchange = pyupbit.Upbit(api_access_key, api_secret_key)
    
    def prepare_dataframe(self, df):
        """DataFrame을 JSON 직렬화 가능한 형태로 변환"""
        if df is None:
            return None
        
        # NaN 값 처리
        df = df.ffill().bfill()
        
        # 인덱스를 문자열로 변환
        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')
        df.index.name = 'time'
        return df.reset_index().to_dict('records')

    def get_daily_data(self):
        df = pyupbit.get_ohlcv(self.symbol, interval="day", count=30)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
    def get_4h_data(self):
        df = pyupbit.get_ohlcv(self.symbol, interval="minute240", count=30)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
    def get_1h_data(self):
        df = pyupbit.get_ohlcv(self.symbol, interval="minute60", count=30)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
    def get_tickers(self):
        return pyupbit.get_ticker()

    def get_current_price(self):
        return pyupbit.get_current_price(self.symbol)
    
    def get_market_detail(self):
        df = pyupbit.get_ohlcv(self.symbol, count=1)
        return df.tail(1) if not df.empty else None
    
    def get_orderbook(self, limit=5):
        orderbook = pyupbit.get_orderbook(ticker=self.symbol)
        if orderbook:
            return {
                'timestamp': orderbook['timestamp'],
                'total_ask_size': orderbook['total_ask_size'],
                'total_bid_size': orderbook['total_bid_size'],
                'orderbook_units': orderbook['orderbook_units'][:limit]  # Limiting to top 'limit' entries
            }
        return None
    
    def get_candlestick(self, interval="1h", count=10):
        df = pyupbit.get_ohlcv(self.symbol, interval=interval, count=count)

        if df is not None:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
    def get_trading_fee(self):
        """수수료 조회 (업비트에서 직접적으로 수수료 조회는 불가)"""
        return None
    
    def get_balance(self):
        balance = self.exchange.get_balances()
        return {item['currency']: item['balance'] for item in balance}
    
    def place_order(self, order_type, price, quantity):
        if order_type == 'buy':
            return self.exchange.buy_limit_order(self.symbol, price, quantity)
        elif order_type == 'sell':
            return self.exchange.sell_limit_order(self.symbol, price, quantity)
        else:
            raise ValueError("Invalid order type. Use 'buy' or 'sell'.")
    
    def cancel_order(self, uuid):
        return self.exchange.cancel_order(uuid)
    
    def get_outstanding_orders(self, uuid=None):
        return self.exchange.get_order(self.symbol) if uuid is None else self.exchange.get_order(uuid)
