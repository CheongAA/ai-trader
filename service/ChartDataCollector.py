from service.TechnicalAnalysis import TechnicalAnalysis

class ChartDataCollector:
    def __init__(self,exchange = None,symbol="BTC"):
        self.symbol = symbol
        self.exchange = exchange

    def get_daily_data(self):
        return self.exchange.get_daily_data()

    def get_4h_data(self):
        return self.exchange.get_4h_data()

    def get_1h_data(self):
        return self.exchange.get_1h_data()

    def get_tickers(self):
        # 암호화폐 목록
        return self.exchange.get_tickers()
    
    def get_current_price(self):
        # 최근 체결 가격 조회
        return self.exchange.get_current_price()
    
    def get_market_detail(self):
        # 시가/고가/저가/종가/거래량 정보 조회
        return self.exchange.get_market_detail()
    
    def get_orderbook(self, limit=5):
        # 호가 데이터 조회
        return self.exchange.get_orderbook(limit)
    
    def get_candlestick(self, interval="1h", count=10):
        # 시간별 가격정보 조회
        return self.exchange.get_candlestick(interval, count)
    
    def get_trading_fee(self):
        # 수수료 조회
        return self.exchange.get_trading_fee()
    
    def get_balace(self):
        # 잔고 조회
        return self.exchange.get_balace()
    
    def place_order(self, order_type, price, quantity):
        # 매수/매도 주문
        return self.exchange.place_order(order_type, price, quantity)
    
    def cancel_order(self, order_desc):
        # 매수/매도 주문 취소
        return self.exchange.cancel_order(order_desc)
    
    def get_outstanding_orders(self, order_desc):
        # 매수/매도 잔량 확인
        return self.exchange.get_outstanding_orders(order_desc)
