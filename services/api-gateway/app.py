import os

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="PayNova API Gateway")

PAYMENT_SERVICE_URL = os.getenv(
    "PAYMENT_SERVICE_URL", "http://localhost:8002"
)
WALLET_SERVICE_URL = os.getenv(
    "WALLET_SERVICE_URL", "http://localhost:8003"
)


class PaymentRequest(BaseModel):
    customer_id: str
    amount: float = Field(gt=0)


@app.post("/pay")
def pay(payment: PaymentRequest):
    try:
        response = requests.post(
            f"{PAYMENT_SERVICE_URL}/pay",
            json=payment.model_dump(),
            timeout=10,
        )
        return response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Payment Service is not available",
        )


@app.get("/balance/{customer_id}")
def balance(customer_id: str):
    try:
        response = requests.get(
            f"{WALLET_SERVICE_URL}/balance/{customer_id}",
            timeout=5,
        )
        return response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Wallet Service is not available",
        )


@app.get("/health")
def health():
    return {"service": "api-gateway", "status": "healthy"}
