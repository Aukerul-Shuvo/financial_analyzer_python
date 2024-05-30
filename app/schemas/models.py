from pydantic import BaseModel
from typing import List, Dict, Optional

class Transaction(BaseModel):
    transaction_id: str
    date: str
    amount: float
    merchant: str
    category: str
    city: str
    region: str
    payment_method: str
    day_of_week: Optional[int] = None
    week_of_month: Optional[int] = None
    month: Optional[int] = None
    uuid: Optional[str] = None


class Analysis(BaseModel):
    historical_average_spending: float
    current_week_spending: float
    spending_comparison: float
    historical_average_earnings: float
    current_week_earnings: float
    earnings_comparison: float
    current_month_spending: float
    current_month_earnings: float
    historical_month_spending: float
    historical_month_earnings: float
    overall_spending: float
    overall_earnings: float

class Comparison(BaseModel):
    current_analysis: Analysis
    differences: Dict[str, Dict[str, float]]

class UUIDRequest(BaseModel):
    uuid: str

class TransactionsAnalysisPayload(BaseModel):
    transactions: List[Transaction]
    analysis: Analysis    

