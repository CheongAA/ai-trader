from typing import Dict, List
import pandas as pd
import streamlit as st
from datetime import datetime

from models import TradeDecision

class DecisionHistory:
    @staticmethod
    def render_table(decisions: List[TradeDecision]) -> None:
        if not decisions:
            st.warning("저장된 트레이딩 디시젼이 없습니다.")
            return

        df = pd.DataFrame([
            {
                "Date": d.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                "Symbol": d.symbol,
                "Decision": d.decision,
                "Reason": d.reason,
                "Confidence": d.confidence,
                "Current Price": d.current_price,
                "Entry Price": d.entry_price,
                "Exit Price": d.exit_price,
            }
            for d in decisions
        ])

        for col in ['Confidence', 'Current Price', 'Entry Price', 'Exit Price']:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        st.subheader("📊 Previous Trading Decisions")
        st.table(df)

    @staticmethod
    def render_single_decision(decision: Dict) -> None:
        st.success("Decision Completed!")
        st.subheader("📊 Decision Result")
        st.json(decision)
        
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
