import pyupbit
from service.TechnicalAnalysis import TechnicalAnalysis

class UpbitCryptoDataCollector:
    def __init__(self, api_access_key=None, api_secret_key=None, symbol="KRW-BTC"):
        self.symbol = "KRW-" + symbol
        self.upbit = pyupbit.Upbit(api_access_key, api_secret_key)

    def get_daily_data(self):
        """일별 가격정보 조회"""
        df = pyupbit.get_ohlcv(self.symbol, interval="day", count=30)

        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)

        return self.prepare_dataframe(df)

    def get_4h_data(self):
        """4시간봉 가격정보 조회"""
        df = pyupbit.get_ohlcv(self.symbol, interval="minute240", count=30)

        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)

        return self.prepare_dataframe(df)

    def get_1h_data(self):
        """1시간봉 가격정보 조회"""
        df = pyupbit.get_ohlcv(self.symbol, interval="minute60", count=30)

        if df is not None and len(df) > 20:
            df = TechnicalAnalysis.add_indicators(df)

        return self.prepare_dataframe(df)
    
    def get_tickers(self):
        """업비트에서 지원하는 암호화폐 목록"""
        return pyupbit.get_tickers()
    
    def get_current_price(self):
        """최근 체결 가격 조회"""
        return pyupbit.get_current_price(self.symbol)
    
    def get_market_detail(self):
        """시가/고가/저가/종가/거래량 정보 조회"""
        df = pyupbit.get_ohlcv(self.symbol, count=1)
        return df.tail(1) if not df.empty else None
    
    def get_orderbook(self, limit=5):
        """호가 데이터 조회"""
        orderbook = pyupbit.get_orderbook(ticker=self.symbol)
        if orderbook:
            return {
                'timestamp': orderbook['timestamp'],
                'total_ask_size': orderbook['total_ask_size'],
                'total_bid_size': orderbook['total_bid_size'],
                'orderbook_units': orderbook['orderbook_units'][:limit]  # Limiting to top 'limit' entries
            }
        return None
    
    def get_candlestick(self, interval="minute1", count=10):
        """시간별 가격정보 조회"""
        df = pyupbit.get_ohlcv(self.symbol, interval=interval, count=count)

        if df is not None:
            df = TechnicalAnalysis.add_indicators(df)
        return self.prepare_dataframe(df)
    
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
    
    def get_trading_fee(self):
        """수수료 조회 (업비트에서 직접적으로 수수료 조회는 불가)"""
        return None
    
    def get_balance(self):
        """잔고 조회"""
        balance = self.upbit.get_balances()
        return {item['currency']: item['balance'] for item in balance}
    
    def place_order(self, order_type, price, quantity):
        """매수/매도 주문"""
        if order_type == 'buy':
            return self.upbit.buy_limit_order(self.symbol, price, quantity)
        elif order_type == 'sell':
            return self.upbit.sell_limit_order(self.symbol, price, quantity)
        else:
            raise ValueError("Invalid order type. Use 'buy' or 'sell'.")
    
    def cancel_order(self, uuid):
        """매수/매도 주문 취소"""
        return self.upbit.cancel_order(uuid)
    
    def get_outstanding_orders(self, uuid=None):
        """미체결 주문 조회"""
        return self.upbit.get_order(self.symbol) if uuid is None else self.upbit.get_order(uuid)
