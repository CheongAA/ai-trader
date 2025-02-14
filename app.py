import os
from datetime import datetime
from dotenv import load_dotenv

import streamlit as st
import google.generativeai as genai

from db.TradingDatabase import TradingDatabase
from api.google_news import GoogleNewsAPI
from api.fear_and_greed_index import FearAndGreedIndex
from service.TradingSystem import TradingSystem
from service.ChartDataCollector import ChartDataCollector
from service.ChartImageCollector import ChartImageCollector
from service.exchange.Bithumb import Bithumb
from service.exchange.Binance import Binance
from service.exchange.Upbit import Upbit
from prompt import prompt

# 환경 변수 로드
load_dotenv()

# 환경 설정
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


# Streamlit 페이지 설정
st.set_page_config(
    page_title="AI Trading Decision System",
    layout="wide"
)
st.title("💹 AI Trading Decision System")

@st.cache_resource
def initialize_system():
    """트레이딩 시스템 초기화"""
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
    chart_collector = ChartDataCollector(exchange_upbit)
    image_collector = ChartImageCollector(exchange_upbit)
    db = TradingDatabase(db_path="trading_decisions.db")

    trading_system = TradingSystem(
        symbol=envConfig['symbol'],
        ai_model=ai_model,
        data_collector=chart_collector,
        fear_and_greed=fear_and_greed,
        goolge_news_api=google_news_api,
        image_collector=image_collector,
        db=db
    )
    return trading_system

def load_decision_history(trading_system):
    """기존 트레이딩 디시젼 로드"""
    db = trading_system.db
    decisions = db.get_recent_decisions(symbol=envConfig['symbol'], limit=10)
    return decisions

def get_previous_decisions(trading_system):
    """이전 디시젼을 테이블 형식으로 반환"""
    decisions = load_decision_history(trading_system)

    if not decisions:
        st.warning("저장된 트레이딩 디시젼이 없습니다.")
        return
    
    # 테이블 데이터 생성
    table_data = []
    for decision in decisions:
        table_data.append({
            "Date": decision.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "Symbol": decision.symbol,
            "Decision": decision.decision,
            "Reason": decision.reason,
            "Current Price": decision.current_price if decision.current_price else 'N/A',
            "Entry Price": decision.entry_price if decision.entry_price else 'N/A',
            "Exit Price": decision.exit_price if decision.exit_price else 'N/A',
        })
    
    st.subheader("📊 Previous Trading Decisions")
    st.table(table_data)

def update_ui(decision):
    """UI 업데이트 - 결과 출력"""
    st.success("Decision Completed!")
    st.subheader("📊 Decision Result")
    st.json(decision)
    
    # 테이블 형태로 결과 출력
    decision_table = {
        "Decision": [decision['decision']],
        "Reason": [decision['reason']],
        "Confidence": [decision.get('confidence', 'N/A')],
        "Current Price": [decision.get('current_price', 'N/A')],
        "Entry Price": [decision.get('entry_price', 'N/A')],
        "Exit Price": [decision.get('exit_price', 'N/A')],
        "Date": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
    }
    st.table(decision_table)

def main():
    """Streamlit 메인 함수"""
    st.info("Click the button to get AI Trading Decision.")
    
    # 시스템 초기화
    trading_system = initialize_system()
    
    # 데이터베이스 보여주기
    get_previous_decisions(trading_system=trading_system)

    # 버튼 클릭 시 트레이딩 의견 얻기 실행
    if st.button("🔮 Get Trading Decision"):
        with st.spinner("Collecting Data and Making Decision..."):
            data = trading_system.collect_chart_data()
            # image_data = trading_system.collect_chart_image()
            # youtube_data = trading_system.collect_youtube_transcript('6flHiM5-n50')
            # fear_and_greed_data = trading_system.collect_fear_and_greed_data()
            # news_data = trading_system.collect_news_data()
            indicators = [
                data,
                # youtube_data
                # fear_and_greed_data,
                # news_data,
            ]
            decision = trading_system.get_ai_decision(
                prompt=prompt.text,
                data=indicators, 
                # image_data=image_data,
            )
            update_ui(decision)

            # 테이블 업데이트를 위해 페이지 리렌더링
            get_previous_decisions(trading_system=trading_system)

if __name__ == "__main__":
    main()
