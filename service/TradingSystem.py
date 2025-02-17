import typing_extensions as typing
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi

import json
import PIL.Image
from datetime import datetime

from models import TradeDecision
from db import TradingDatabase

class Decision(BaseModel):
    decision: str
    confidence: float
    current_price: float
    entry_price: float
    exit_price: float
    reason: str

class TradingSystem:
    def __init__(self, google_news_api, fear_and_greed, data_collector , ai_model, db:TradingDatabase,symbol="KRW-BTC", image_collector = None):
        self.symbol = symbol
        self.google_news_api = google_news_api
        self.fear_and_greed = fear_and_greed
        self.data_collector = data_collector
        self.image_collector = image_collector
        self.ai_model = ai_model
        self.db = db

    def collect_news_data(self):
        """구글 뉴스에서 최신 뉴스 헤드라인을 가져오기"""
        news_data = self.google_news_api.fetch_news(self.symbol)
        headlines = [article['title'] for article in news_data]
        return {
            'news_data': headlines
        }
    
    def collect_fear_and_greed_data(self):
        """Fear and Greed Index 데이터 수집"""
        fear_and_greed_data = self.fear_and_greed.fetch_fear_and_greed_index()
        return {
            'fear_and_greed_data': fear_and_greed_data
        }
    
    def collect_youtube_transcript(self, video_id):
        """YouTube 트랜스크립트 수집"""
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        combined_transcript = " ".join([item['text'] for item in transcript])
        return {
            'youtube_transcript': combined_transcript
        }
    
    def collect_chart_image(self, wait_time = 3):
        """차트 이미지 수집"""
        if self.image_collector is None:
            raise ValueError("ImageCollector is not initialized.")
        image_path = self.image_collector.capture_chart(wait_time)

        return PIL.Image.open(image_path)
        
    def collect_chart_data(self):
        """모든 데이터 수집"""
        if self.data_collector is None:
            raise ValueError("DataCollector is not initialized.")
        return {
            'daily_candles': self.data_collector.get_daily_data(),
            '4h_candles': self.data_collector.get_4h_data(),
            '1h_candles': self.data_collector.get_1h_data(),
            'orderbook': self.data_collector.get_orderbook(),
            'current_price': self.data_collector.get_current_price(),
        }
    
    def get_ai_decision(self, prompt, data):
        """AI 분석 및 결정"""
        decision_data = self.ai_model.generate_content(
            prompt=prompt,
            data=data,
            schema=Decision
        )

        # 예외 처리: JSON 디코딩 및 데이터 형식 검사
        try:
            # 필수 키 확인
            required_keys = ['decision', 'reason']
            if not all(key in decision_data for key in required_keys):
                raise ValueError("응답 데이터에 필요한 키가 없습니다.")
            
        except Exception as e:
            print("예외 발생:", e)
            # 디폴트 값 설정
            decision_data = {
                'decision': 'HOLD',
                'reason': '잘못된 응답 데이터 형식',
            }

        # 결정을 데이터베이스에 저장 (옵셔널 필드는 get()으로 처리)
        trade_decision = TradeDecision(
            symbol=self.symbol,
            decision=decision_data['decision'],
            reason=decision_data['reason'],
            confidence=decision_data.get('confidence'),
            current_price=decision_data.get('current_price'),
            entry_price=decision_data.get('entry_price'),
            exit_price=decision_data.get('exit_price'),
            created_at=datetime.now(),
        )

        
        self.db.save_decision(trade_decision)
        return decision_data
    
    def execute_trade(self, decision):
        """거래 실행"""
        # if decision['confidence'] < 0.7:
        #     print(f"Low confidence ({decision['confidence']}): No trade executed")
        #     return
            
        # if decision["decision"] == "buy":
        #     krw_balance = self.data_collector.upbit.get_balance("KRW")
        #     if krw_balance > 5000:
        #         print(f"Executing BUY order with {krw_balance} KRW")
        #         # print(self.data_collector.upbit.buy_market_order(self.symbol, krw_balance*0.9995))
        
        # elif decision["decision"] == "sell":
        #     coin_balance = self.data_collector.upbit.get_balance(self.symbol)
        #     if coin_balance > 0:
        #         print(f"Executing SELL order with {coin_balance} {self.symbol}")
        #         # print(self.data_collector.upbit.sell_market_order(self.symbol, coin_balance))
                
        print(decision)
