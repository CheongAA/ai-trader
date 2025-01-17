import pandas as pd
import ta
from ta.volatility import BollingerBands
from ta.trend import EMAIndicator, MACD
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
        
        # Bollinger Bands (15일)
        # 변동성이 큰 크립토 시장에서는 좀 더 짧은 기간이 효과적
        bb = BollingerBands(close=close, window=15, window_dev=2.5)  
        df['bb_upper'] = bb.bollinger_hband()
        df['bb_middle'] = bb.bollinger_mavg()
        df['bb_lower'] = bb.bollinger_lband()
        
        # EMA (7일, 21일)
        # 단기간 추세를 더 빠르게 포착하기 위해 기간 단축
        df['ema7'] = EMAIndicator(close=close, window=7).ema_indicator()
        df['ema21'] = EMAIndicator(close=close, window=21).ema_indicator()
        
        # 추가 EMA (30일) - 주요 추세 확인용
        df['ema30'] = EMAIndicator(close=close, window=30).ema_indicator()
        
        # MACD (8, 17, 9)
        # 전통적인 (12, 26, 9) 대신 크립토에 최적화된 설정
        macd = MACD(close=close, window_slow=17, window_fast=8, window_sign=9)
        df['macd'] = macd.macd()
        df['macd_signal'] = macd.macd_signal()
        df['macd_diff'] = macd.macd_diff()
        
        # RSI (10일)
        # 변동성이 큰 시장에서 더 민감하게 반응하도록 기간 단축
        df['rsi'] = RSIIndicator(close=close, window=10).rsi()
        
        # VWAP 계산 (일중 거래에 더 효과적)
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
