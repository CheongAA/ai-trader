import typing_extensions as typing
import google.generativeai as genai
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

    def collect_news_data(self, headlines):
        """구글 뉴스에서 최신 뉴스 헤드라인을 가져오기"""
        news_data = self.google_news_api.fetch_news(headlines)
        headlines = [article['title'] for article in news_data]
        print(f"Headlines: {headlines}")
        return {
            'news_headlines': headlines
        }
    
    def collect_fear_and_greed_data(self):
        """Fear and Greed Index 데이터 수집"""
        fear_and_greed_data = self.fear_and_greed.fetch_fear_and_greed_index()
        print(f"Fear and Greed Index: {fear_and_greed_data}")
        return {
            'fear_and_greed_index': fear_and_greed_data
        }
    
    def collect_chart_image(self, wait_time = 3):
        """차트 이미지 수집"""
        return self.image_collector.capture_chart(wait_time)
        
    def collect_chart_data(self, enabled_api = False):
        """모든 데이터 수집"""
        if self.data_collector is None:
            raise ValueError("DataCollector is not initialized.")

        data = {
            'daily_candles': self.data_collector.get_daily_data(),
            '4h_candles': self.data_collector.get_4h_data(),
            '1h_candles': self.data_collector.get_1h_data(),
            'orderbook': self.data_collector.get_orderbook(),
            'current_price': self.data_collector.get_current_price(),
        }

        if enabled_api:
            data['news_data'] = self.collect_news_data(self.symbol)
            data['fear_and_greed_data'] = self.collect_fear_and_greed_data()

        return data
    
    def get_ai_decision_by_image(self):
        """AI 분석 및 결정"""

        image_path = self.collect_chart_image()
        image_file = PIL.Image.open(image_path)
        prompt = [
            """
                Given a chart image, analyze the data and provide a trading decision based on the following criteria:

                Decision (decision): Choose between "hold", "buy", or "sell".
                Confidence (confidence): Provide a confidence level for the decision, ranging from 0.0 to 1.0.
                Current Price (current_price): State the current market price of the cryptocurrency.
                Entry Price (entry_price): If it's a "buy" signal, suggest the optimal entry price.
                Exit Price (exit_price): If it's a "sell" signal, suggest the optimal exit price.
                Reason (reason): Provide a detailed explanation for the decision, mentioning specific indicators used (e.g., Moving Averages, RSI, MACD, or any patterns observed in the chart).
                Important: Please make sure to consider all relevant technical indicators while making the decision.

                Note: While the decision and other values should be in English, please provide the explanation (reason) in Korean.

            """,
            image_file
        ]
        result = self.ai_model.generate_content(prompt,
            generation_config=genai.GenerationConfig(
            response_mime_type="application/json", response_schema=Decision
        ))  


        return json.loads(result.candidates[0].content.parts[0].text)
    

    def get_ai_decision(self, data):
        """AI 분석 및 결정"""
        prompt = [
            """
                You are a professional trading assistant specialized in cryptocurrency trading. Based on the provided data and technical indicators, analyze and make a decision using the following approach:

                ---

                ### Data Provided:
                1. **Candles**: Includes OHLC data and the following indicators:
                - Bollinger Bands
                - EMA
                - MACD
                - RSI
                - VWAP
                - ATR
                2. **Orderbook**: Current buy/sell orderbook data.
                3. **Current Price**: The latest market price.

                ---

                ### Analysis Guidelines:
                1. **Trend Analysis**: Use EMA crossovers to evaluate overall price trends.
                2. **Momentum**: Analyze RSI and MACD to determine the strength of current trends.
                3. **Volatility**: Evaluate Bollinger Bands and ATR to gauge market conditions.
                4. **Volume Analysis**: Use VWAP and orderbook data to assess market participation.
                5. **Timeframe Consistency**: Check for alignment of signals across candle.

                ---

                ### Output Format:
                Return a JSON object with the following fields:
                - decision (string): Either `"hold"`, `"buy"`, or `"sell"`.
                - confidence (float): Confidence level for the decision, ranging from 0.0 to 1.0.
                - current_price (float): Current market price.
                - entry_price (float): Suggested optimal entry price for a "buy" signal.
                - exit_price (float): Suggested optimal exit price for a "sell" signal.
                - reason (string): A detailed explanation of the decision. Mention the specific indicators used and their significance in Korean.

            """,
            json.dumps(data)
        ]

        data_result = self.ai_model.generate_content(prompt,
        generation_config=genai.GenerationConfig(
        response_mime_type="application/json", response_schema=Decision
        ))
        data_decision = json.loads(data_result.candidates[0].content.parts[0].text)

        if self.image_collector is not None :
            image_decision = self.get_ai_decision_by_image()
            return {
                "image_decision": image_decision,
                "data_decision": data_decision
            }
        
        return data_decision
    
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
