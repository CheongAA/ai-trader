import pybithumb
from service.TechnicalAnalysis import TechnicalAnalysis

class BithumbCryptoDataCollector:
    def __init__(self, api_access_key=None, api_secret_key=None, symbol="BTC"):
        self.symbol = symbol
        self.bithumb = pybithumb.Bithumb(api_access_key, api_secret_key)
    
    def get_daily_data(self):
        df = self.bithumb.get_candlestick(self.symbol, chart_intervals="24h").tail(30)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)

    def get_4h_data(self):
        df = self.bithumb.get_candlestick(self.symbol, chart_intervals="4h").tail(30)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
    def get_1h_data(self):
        df = self.bithumb.get_candlestick(self.symbol, chart_intervals="1h").tail(30)
        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
        
    def get_tickers(self):
        """빗썸에서 지원하는 암호화폐 목록"""
        return self.bithumb.get_tickers()
    
    def get_current_price(self):
        """최근 체결 가격 조회"""
        return self.bithumb.get_current_price(self.symbol)
    
    def get_market_detail(self):
        """시가/고가/저가/종가/거래량 정보 조회"""
        return self.bithumb.get_market_detail(self.symbol)
    
    def get_orderbook(self, limit=5):
        """호가 데이터 조회"""
        orderbook = self.bithumb.get_orderbook(self.symbol)
        if orderbook:
            return {
                'timestamp': orderbook['timestamp'],
                'bids': orderbook['bids'][:limit],
                'asks': orderbook['asks'][:limit]
            }
        return None
    
    def get_candlestick(self, interval="1h", count=10):
        """시간별 가격정보 조회"""
        df = self.bithumb.get_candlestick(self.symbol, chart_intervals=interval)
        return self.prepare_dataframe(df.tail(count))
    
    def prepare_dataframe(self, df):
        """DataFrame을 JSON 직렬화 가능한 형태로 변환"""
        if df is None:
            return None
        
        # NaN 값 처리
        df = df.ffill().bfill()
        
        # 인덱스를 문자열로 변환
        df.index = df.index.strftime('%Y-%m-%d %H:%M:%S')

        return df.reset_index().to_dict('records')
    
    def get_trading_fee(self):
        """수수료 조회"""
        return self.bithumb.get_trading_fee()
    
    def get_balance(self):
        """잔고 조회"""
        balance = {}
        for coin in self.bithumb.get_tickers():
            balance[coin] = self.bithumb.get_balance(coin)
        return balance
    
    def place_order(self, order_type, price, quantity):
        """매수/매도 주문"""
        if order_type == 'buy':
            return self.bithumb.buy_limit_order(self.symbol, price, quantity)
        elif order_type == 'sell':
            return self.bithumb.sell_limit_order(self.symbol, price, quantity)
        else:
            raise ValueError("Invalid order type. Use 'buy' or 'sell'.")
    
    def cancel_order(self, order_desc):
        """매수/매도 주문 취소"""
        return self.bithumb.cancel_order(order_desc)
    
    def get_outstanding_orders(self, order_desc):
        """매수/매도 잔량 확인"""
        return self.bithumb.get_outstanding_order(order_desc)

