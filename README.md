# .env

```
UPBIT_ACCESS_KEY=""
UPBIT_SECRET_KEY=""

BITHUMB_ACCESS_KEY=""
BITHUMB_SECRET_KEY=""


GEMINI_API_KEY=""
SERPAPI_API_KEY=""


```

# run

```
pip install -r requirements.txt

python -m streamlit run app.py

```

# Bollinger Bands

## 기본 설정

- **기간 (window):** 기본적으로 14 (주식 및 일반적인 금융 데이터에서 많이 사용)
- **표준 편차 (window_dev):** 2 (일반적으로 2로 설정)

# Exponential Moving Average (EMA)

## 기본 설정

- **단기 EMA**: 9일, 12일, 20일
- **장기 EMA**: 50일, 200일

# Moving Average Convergence Divergence (MACD)

## 기본 설정

- **단기 EMA (빠른 EMA)**: 12일
- **장기 EMA (느린 EMA)**: 26일
- **신호선**: 9일 (MACD 선의 EMA)

# Relative Strength Index (RSI)

## 기본 설정

- **기간**: 10일

# VWAP

# ATR
