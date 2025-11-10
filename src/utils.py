from typing import Any, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime

class MarketSummary(BaseModel):
    company: str
    as_of: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    price_snapshot: Dict[str, Any]
    top_news: List[Dict[str, Any]]
    analysis: str
    risks: List[str]
    recommendations: List[str]
