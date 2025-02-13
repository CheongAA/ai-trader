import pandas as pd
import ta
from ta.volatility import BollingerBands
from ta.trend import EMAIndicator, MACD, SMAIndicator
from ta.momentum import RSIIndicator
from ta.volume import VolumeWeightedAveragePrice
from ta.momentum import StochasticOscillator
import numpy as np

class TechnicalAnalysis:
    @staticmethod
    def add_indicators(df):
        """기술적 지표 추가 - 크립토 마켓에 최적화된 설정"""
        close = df['close']
        high = df['high']
        low = df['low']
        volume = df['volume']
        
        # Bollinger Bands
        bb = BollingerBands(close=close, window=14, window_dev=2)  
        df['bollinger_bands_upper'] = bb.bollinger_hband()
        df['bollinger_bands_middle'] = bb.bollinger_mavg()
        df['bollinger_bands_lower'] = bb.bollinger_lband()
        
        # MA
        df['ma5'] = SMAIndicator(close=close, window=5).sma_indicator()
        df['ma7'] = SMAIndicator(close=close, window=7).sma_indicator()
        df['ma20'] = SMAIndicator(close=close, window=20).sma_indicator()
        df['ma60'] = SMAIndicator(close=close, window=60).sma_indicator()
        df['ma122'] = SMAIndicator(close=close, window=122).sma_indicator()
        df['ma244'] = SMAIndicator(close=close, window=244).sma_indicator()
        
        # MACD
        macd = MACD(close=close, window_slow=26, window_fast=12, window_sign=9)
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        
        # RSI
        df['rsi'] = RSIIndicator(close=close, window=10).rsi()
        
        # VWAP
        df['vwap'] = VolumeWeightedAveragePrice(
            high=high, low=low, close=close, volume=volume
        ).volume_weighted_average_price()
        
        # 추가: ATR (Average True Range) - 변동성 측정
        high_low = high - low
        high_close = np.abs(high - close.shift())
        low_close = np.abs(low - close.shift())
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = np.max(ranges, axis=1)
        df['atr'] = true_range.rolling(window=14).mean()

        # # Stochastic Oscillator (Stochastic)
        # # %K와 %D 값을 계산
        # stoch = StochasticOscillator(high=high, low=low, close=close, window=14, smooth_window=3)
        # df['stoch_k'] = stoch.stoch()
        # df['stoch_d'] = stoch.stoch_signal()

        # # Ichimoku Cloud 계산
        # df['tenkan_sen'] = (high.rolling(window=9).max() + low.rolling(window=9).min()) / 2
        # df['kijun_sen'] = (high.rolling(window=26).max() + low.rolling(window=26).min()) / 2
        # df['senkou_span_a'] = ((df['tenkan_sen'] + df['kijun_sen']) / 2).shift(26)
        # df['senkou_span_b'] = ((high.rolling(window=52).max() + low.rolling(window=52).min()) / 2).shift(26)
        # df['chikou_span'] = close.shift(-26)

        return df
