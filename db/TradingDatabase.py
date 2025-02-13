import sqlite3
from datetime import datetime

from models.TradeDecision import TradeDecision

class TradingDatabase:
    def __init__(self, db_path: str = "trading_decisions.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS trade_decisions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    decision TEXT NOT NULL,
                    confidence REAL,  -- Optional 필드 (NULL 허용)
                    current_price REAL,  -- Optional 필드 (NULL 허용)
                    entry_price REAL,  -- Optional 필드 (NULL 허용)
                    exit_price REAL,  -- Optional 필드 (NULL 허용)
                    reason TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # 분석을 위한 인덱스 생성
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_symbol ON trade_decisions(symbol)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_created_at ON trade_decisions(created_at)")

    def save_decision(self, trade_decision: TradeDecision) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO trade_decisions 
                (symbol, decision, confidence, current_price, entry_price, exit_price, reason, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                trade_decision.symbol,
                trade_decision.decision,
                trade_decision.confidence if trade_decision.confidence is not None else None,
                trade_decision.current_price if trade_decision.current_price is not None else None,
                trade_decision.entry_price if trade_decision.entry_price is not None else None,
                trade_decision.exit_price if trade_decision.exit_price is not None else None,
                trade_decision.reason,
                trade_decision.created_at
            ))
            return cursor.lastrowid

    def get_recent_decisions(self, symbol: str, limit: int = 10) -> list[TradeDecision]:
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM trade_decisions 
                WHERE symbol = ? 
                ORDER BY created_at DESC 
                LIMIT ?
            """, (symbol, limit))
            
            return [TradeDecision(
                symbol=row['symbol'],
                decision=row['decision'],
                confidence=row['confidence'],  # Optional
                current_price=row['current_price'],  # Optional
                entry_price=row['entry_price'],  # Optional
                exit_price=row['exit_price'],  # Optional
                reason=row['reason'],
                created_at=datetime.fromisoformat(row['created_at'])
            ) for row in cursor.fetchall()]
