import typing_extensions as typing
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

import json
import PIL.Image

class Decision(typing.TypedDict):
    decision: str
    confidence: float
    current_price: float
    entry_price: float
    exit_price: float
    reason: str

class TradingSystem:
    def __init__(self, goolge_news_api, fear_and_greed, data_collector , image_collector,ai_model,symbol="KRW-BTC"):
        self.symbol = symbol
        self.google_news_api = goolge_news_api
        self.fear_and_greed = fear_and_greed
        self.data_collector = data_collector
        self.image_collector = image_collector
        self.ai_model = ai_model

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
        return {'chart_image': PIL.Image.open(image_path)}
        
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
    
    def get_ai_decision(self, prompt, data, image_data = None):
        """AI 분석 및 결정"""
        prompt_req = [prompt, json.dumps(data), image_data]
        result = self.ai_model.generate_content(prompt_req,
        generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Decision
        ))
        
        return json.loads(result.candidates[0].content.parts[0].text)
    
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
