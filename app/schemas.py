from pydantic import BaseModel
from typing import List

# Single transaction input
class Transaction(BaseModel):
    transaction_type: str
    amount: float
    location: str
    device_type: str
    network_provider: str
    user_type: str
    is_foreign_number: int
    is_sim_recently_swapped: int
    has_multiple_accounts: int

# Response for single transaction
class TransactionResponse(BaseModel):
    is_anomaly: int
    anomaly_score: float

# Batch input
class BatchTransaction(BaseModel):
    transactions: List[Transaction]

# Response for batch transactions
class BatchTransactionResponse(BaseModel):
    results: List[TransactionResponse]
