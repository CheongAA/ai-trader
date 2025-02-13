import os
import logging
from dotenv import load_dotenv

import google.generativeai as genai

from db.TradingDatabase import TradingDatabase

from api.google_news import GoogleNewsAPI
from api.fear_and_greed_index import FearAndGreedIndex
from service.TradingSystem import TradingSystem

from service.ChartDataCollector import ChartDataCollector
from service.ChartImageCollector import ChartImageCollector

from service.exchange.Bithumb import Bithumb
from service.exchange.Upbit import Upbit
from service.exchange.Binance import Binance

from prompt import prompt
from utils import save_to_excel

# 환경 변수 로드
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
logging.getLogger('absl').setLevel(logging.ERROR)
load_dotenv()

envConfig = {
    "binance": {
        "api_access_key": os.getenv("BINANCE_ACCESS_KEY"),
        "api_secret_key": os.getenv("BINANCE_SECRET_KEY"),
    },
    "bithumb": {
        "api_access_key": os.getenv("BITHUMB_ACCESS_KEY"),
        "api_secret_key": os.getenv("BITHUMB_SECRET_KEY"),
    },
    "upbit": {
        "api_access_key": os.getenv("UPBIT_ACCESS_KEY"),
        "api_secret_key": os.getenv("UPBIT_SECRET_KEY"), 
    },
    "serpapi": {
        "api_key": os.getenv("SERPAPI_API_KEY"),
    },
    'gemini': {
        "api_key": os.getenv("GEMINI_API_KEY"),
        "model": "gemini-1.5-flash"
    },
    'symbol': 'btc'.upper()
}

def main():
    # config
    genai.configure(api_key=envConfig['gemini']['api_key'])
    ai_model = genai.GenerativeModel(envConfig['gemini']['model'])
    fear_and_greed = FearAndGreedIndex()
    google_news_api = GoogleNewsAPI(api_key=envConfig["serpapi"]['api_key'])
    
    exchange_binance = Binance(
            symbol=envConfig['symbol'],
            api_secret_key=envConfig['binance']['api_secret_key'], 
            api_access_key=envConfig['binance']['api_access_key']
    )
    exchange_bithumb = Bithumb(
            symbol=envConfig['symbol'],
            api_secret_key=envConfig['bithumb']['api_secret_key'], 
            api_access_key=envConfig['bithumb']['api_access_key']
    )
    exchange_upbit = Upbit(
            symbol=envConfig['symbol'],
            api_secret_key=envConfig['upbit']['api_secret_key'], 
            api_access_key=envConfig['upbit']['api_access_key']
    )
    chart_collector = ChartDataCollector(exchange_bithumb)
    image_collector = ChartImageCollector(exchange_binance)
    db = TradingDatabase(db_path="trading_decisions.db")


    # trader
    trading_system = TradingSystem(
        symbol=envConfig['symbol'],
        ai_model=ai_model,
        data_collector=chart_collector,
        fear_and_greed=fear_and_greed,
        goolge_news_api=google_news_api,
        image_collector=image_collector,
        db=db
        )


    # indicator
    data = trading_system.collect_chart_data()
    image_data = trading_system.collect_chart_image()
    youtube_data = trading_system.collect_youtube_transcript('6flHiM5-n50')
    fear_and_greed_data = trading_system.collect_fear_and_greed_data()
    news_data = trading_system.collect_news_data()
    indicators = [
        data,
        # youtube_data
        # fear_and_greed_data,
        # news_data,
    ]
    print(indicators)

    # decision
    decision = trading_system.get_ai_decision(
        data=indicators, 
        image_data=image_data,
        prompt=prompt.text
    )
    print(decision)
    

    # execute
    # trading_system.execute_trade(decision)

if __name__ == "__main__":
    main()
