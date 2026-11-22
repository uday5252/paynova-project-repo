from threading import Lock

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="PayNova Wallet Service")

# Demo data only. A real project should store wallet data in a database.
wallets = {
    "student1": 1000.0,
    "student2": 500.0,
}
wallet_lock = Lock()


class DeductRequest(BaseModel):
    customer_id: str
    amount: float = Field(gt=0)


@app.post("/deduct")
def deduct_money(request: DeductRequest):
    with wallet_lock:
        if request.customer_id not in wallets:
            return {
                "success": False,
                "message": "Customer wallet not found",
            }

        current_balance = wallets[request.customer_id]

        if current_balance < request.amount:
            return {
                "success": False,
                "message": "Insufficient wallet balance",
                "balance": current_balance,
            }

        wallets[request.customer_id] = round(
            current_balance - request.amount, 2
        )

        return {
            "success": True,
            "message": "Amount deducted",
            "balance": wallets[request.customer_id],
        }


@app.get("/balance/{customer_id}")
def get_balance(customer_id: str):
    with wallet_lock:
        if customer_id not in wallets:
            return {"message": "Customer wallet not found"}

        return {
            "customer_id": customer_id,
            "balance": wallets[customer_id],
        }


@app.get("/health")
def health():
    return {"service": "wallet-service", "status": "healthy"}
