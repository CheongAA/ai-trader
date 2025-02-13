from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class TradeDecision:
    decision: str
    reason: str
    created_at: datetime
    symbol: str
    confidence: Optional[float] = None
    current_price: Optional[float] = None
    entry_price: Optional[float] = None
    exit_price: Optional[float] = None
