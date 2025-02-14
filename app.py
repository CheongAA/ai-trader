import json
import streamlit as st
import google.generativeai as genai

from api.fear_and_greed_index import FearAndGreedIndex
from api.google_news import GoogleNewsAPI

from service.exchange.Binance import Binance
from service.exchange.Bithumb import Bithumb
from service.exchange.Upbit import Upbit

from service.ChartImageCollector import ChartImageCollector
from service.ChartDataCollector import ChartDataCollector
from service.TradingSystem import TradingSystem

from db.TradingDatabase import TradingDatabase
from ui.DecisionHistory import DecisionHistory

from config.AppConfig import AppConfig
from prompt import prompt

def initialize_app() -> TradingSystem:
    
    config = AppConfig.load_config()

    # ai
    genai.configure(api_key=config.gemini.key)
    ai_model = genai.GenerativeModel(config.gemini.model)

    # exchange
    binance = Binance(
        symbol=config.symbol,
        api_access_key=config.binance.api_access_key,
        api_secret_key=config.binance.api_secret_key
    )
    bithumb = Bithumb(
        symbol=config.symbol,
        api_access_key=config.bithumb.api_access_key,
        api_secret_key=config.bithumb.api_secret_key
    )
    upbit = Upbit(
        symbol=config.symbol,
        api_access_key=config.upbit.api_access_key,
        api_secret_key=config.upbit.api_secret_key
    )
    
    # data collector
    google_news_api = GoogleNewsAPI(api_key=config.serpapi_key)
    fear_and_greed = FearAndGreedIndex()
    chart_image_collector = ChartImageCollector(
        exchange=upbit)
    chart_data_collector = ChartDataCollector(
        exchange=upbit)
    
    # db
    db = TradingDatabase(db_path="trading_decisions.db")

    # trading system
    trading_system = TradingSystem(
        symbol=config.symbol,
        db=db,
        google_news_api=google_news_api,
        fear_and_greed=fear_and_greed,
        image_collector=chart_image_collector,
        data_collector=chart_data_collector,
        ai_model=ai_model
    )

    return trading_system

def main():
    st.set_page_config(
        page_title="AI Trading Decision System",
        layout="wide"
    )
    st.title("💹 AI Trading Decision System")
    st.info("Click the button to get AI Trading Decision.")
    
    # Initialize service
    trader = initialize_app()
    
    # Render decision history
    decisions_container = st.container()
    with decisions_container:
        decisions = trader.db.get_recent_decisions(
            symbol=trader.symbol,
            limit=10
        )
        DecisionHistory.render_table(decisions)
    
    # Handle trading decision
    if st.button("🔮 Get Trading Decision"):
        with st.spinner("Collecting Data and Making Decision..."):
            data = trader.collect_chart_data()
            image_data = trader.collect_chart_image()
            youtube_data = trader.collect_youtube_transcript('6flHiM5-n50')
            fear_and_greed_data = trader.collect_fear_and_greed_data()
            # news_data = trader.collect_news_data()

            # 데이터를 dict로 묶어서 JSON 직렬화
            indicators = {
                "chart_data": data,
                "youtube_data": youtube_data,
                "fear_and_greed_data": fear_and_greed_data,
                # "news_data": news_data,
                "image_data": image_data  # image_data도 dict에 포함
            }

            # JSON 직렬화
            indicators = json.dumps(indicators)
            
            # get ai decision
            decision = trader.get_ai_decision(
                prompt=prompt.text,
                data=indicators, 
            )
            DecisionHistory.render_single_decision(decision)
            st.rerun()

if __name__ == "__main__":
    main()
