import os
import logging
from dotenv import load_dotenv

import google.generativeai as genai

from api.google_news import GoogleNewsAPI
from api.fear_and_greed_index import FearAndGreedIndex
from service.TradingSystem import TradingSystem
from service.UpbitCryptoDataCollector import UpbitCryptoDataCollector


from utils import save_to_excel

# 환경 변수 로드
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('absl').setLevel(logging.ERROR)
load_dotenv()

envConfig = {
    "upbit": {
        "api_access_key": os.getenv("UPBIT_ACCESS_KEY"),
        "api_secret_key": os.getenv("UPBIT_SECRET_KEY"),
    },
    "bithumb": {
        "api_access_key": os.getenv("BITHUMB_ACCESS_KEY"),
        "api_secret_key": os.getenv("BITHUMB_SECRET_KEY"),
    },
    "serpapi": {
        "api_key": os.getenv("SERPAPI_API_KEY"),
    },
    'gemini': {
        "api_key": os.getenv("GEMINI_API_KEY"),
        "model": "gemini-1.5-flash"
    },
    'symbol': 'BTC'
}

def main():
    # 객체 생성
    genai.configure(api_key=envConfig['gemini']['api_key'])
    ai_model = genai.GenerativeModel(envConfig['gemini']['model'])
    upbit_data_collector = UpbitCryptoDataCollector(
            symbol=envConfig['symbol'],
            api_secret_key=envConfig['upbit']['api_secret_key'], 
            api_access_key=envConfig['upbit']['api_access_key']
        )
    fear_and_greed = FearAndGreedIndex()
    google_news_api = GoogleNewsAPI(api_key=envConfig["serpapi"]['api_key'])

    # 트레이딩 시스템 초기화
    trading_system = TradingSystem(
        symbol=envConfig['symbol'],
        ai_model=ai_model
        ,data_collector=upbit_data_collector,
        fear_and_greed=fear_and_greed,
        goolge_news_api=google_news_api)

    # 데이터 수집
    data = trading_system.collect_all_data()

    # AI 분석 및 결정
    decision = trading_system.get_ai_decision(data)
    
    # 거래 실행
    trading_system.execute_trade(decision)

if __name__ == "__main__":
    main()
