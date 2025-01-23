import os
import logging
from dotenv import load_dotenv

import google.generativeai as genai

from api.google_news import GoogleNewsAPI
from api.fear_and_greed_index import FearAndGreedIndex
from service.TradingSystem import TradingSystem
from service.UpbitCryptoDataCollector import UpbitCryptoDataCollector
from service.BithumbCryptoDataCollector import BithumbCryptoDataCollector
from service.ChartImageCollector import ChartImageCollector


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
    'symbol': 'etc'.upper()
}

def main():
    # 객체 생성
    genai.configure(api_key=envConfig['gemini']['api_key'])
    ai_model = genai.GenerativeModel(envConfig['gemini']['model'])
    fear_and_greed = FearAndGreedIndex()
    google_news_api = GoogleNewsAPI(api_key=envConfig["serpapi"]['api_key'])
    upbit_data_collector = UpbitCryptoDataCollector(
            symbol=envConfig['symbol'],
            api_secret_key=envConfig['upbit']['api_secret_key'], 
            api_access_key=envConfig['upbit']['api_access_key']
        )
    bithumb_data_collector = BithumbCryptoDataCollector(
            symbol=envConfig['symbol'],
            api_secret_key=envConfig['bithumb']['api_secret_key'], 
            api_access_key=envConfig['bithumb']['api_access_key']
        )
    image_collector = ChartImageCollector()

    # 트레이딩 시스템 초기화
    trading_system = TradingSystem(
        symbol=envConfig['symbol'],
        ai_model=ai_model
        ,data_collector=bithumb_data_collector,
        fear_and_greed=fear_and_greed,
        goolge_news_api=google_news_api,
        image_collector=image_collector)

    # 데이터 수집
    url = "https://upbit.com/full_chart?code=CRIX.UPBIT.KRW-"+envConfig['symbol']
    chart_id = "fullChartiq"
    period_xpath = '//cq-menu[1]'
    period_interval_xpath = '//cq-menu[1]//cq-item[contains(., "1시간")]'
    studies_xpath = '//cq-menu[contains(.,"지표")]'
    bb_xpath = '//cq-menu[3]//cq-item[contains(., "볼린저 밴드")]'

    image_path = trading_system.collect_chart_image(
        url= url,
        chart_id=chart_id,
        xpath_list=[
            period_xpath, 
            period_interval_xpath,
            studies_xpath, 
            bb_xpath
        ],
        wait_time=1
    )
    data = trading_system.collect_all_data()

    # AI 분석 및 결정
    decision = trading_system.get_ai_decision(data)
    image_decision = trading_system.get_ai_decision_by_image(image_path=image_path)
    
    # 거래 실행
    trading_system.execute_trade(decision)
    trading_system.execute_trade(image_decision)

if __name__ == "__main__":
    main()
