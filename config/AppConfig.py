import os
from dataclasses import dataclass
from dotenv import load_dotenv

@dataclass
class ExchangeConfig:
    api_access_key: str
    api_secret_key: str

@dataclass
class AiConfig:
    key: str
    model: str

@dataclass
class AppConfig:
    binance: ExchangeConfig
    bithumb: ExchangeConfig
    upbit: ExchangeConfig

    gemini: AiConfig
    openai: AiConfig

    serpapi_key: str
    symbol: str

    @classmethod
    def load_config(cls):
        load_dotenv()
        return cls(
            binance=ExchangeConfig(
                api_access_key=os.getenv("BINANCE_ACCESS_KEY"),
                api_secret_key=os.getenv("BINANCE_SECRET_KEY")
            ),
            bithumb=ExchangeConfig(
                api_access_key=os.getenv("BITHUMB_ACCESS_KEY"),
                api_secret_key=os.getenv("BITHUMB_SECRET_KEY")
            ),
            upbit=ExchangeConfig(
                api_access_key=os.getenv("UPBIT_ACCESS_KEY"),
                api_secret_key=os.getenv("UPBIT_SECRET_KEY")
            ),
            gemini=AiConfig(
                key=os.getenv("GEMINI_API_KEY"),
                model="gemini-1.5-flash"
            ),
            openai=AiConfig(
                key=os.getenv("OPENAI_API_KEY"),
                model="gpt-4o"
            ),
            serpapi_key=os.getenv("SERPAPI_API_KEY"),
            symbol='BTC'
        )
