import os
import uuid

import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="PayNova Payment Service")

WALLET_SERVICE_URL = os.getenv(
    "WALLET_SERVICE_URL", "http://localhost:8003"
)
NOTIFICATION_SERVICE_URL = os.getenv(
    "NOTIFICATION_SERVICE_URL", "http://localhost:8004"
)


class PaymentRequest(BaseModel):
    customer_id: str
    amount: float = Field(gt=0)


@app.post("/pay")
def make_payment(payment: PaymentRequest):
    payment_id = str(uuid.uuid4())

    # Step 1: Ask Wallet Service to deduct the amount.
    try:
        wallet_response = requests.post(
            f"{WALLET_SERVICE_URL}/deduct",
            json={
                "customer_id": payment.customer_id,
                "amount": payment.amount,
            },
            timeout=5,
        )
        wallet_result = wallet_response.json()
    except requests.RequestException:
        raise HTTPException(
            status_code=503,
            detail="Wallet Service is not available",
        )

    # Step 2: Decide whether the payment succeeded.
    if not wallet_result.get("success"):
        result = {
            "payment_id": payment_id,
            "status": "FAILED",
            "message": wallet_result.get("message", "Payment failed"),
        }
    else:
        result = {
            "payment_id": payment_id,
            "status": "SUCCESS",
            "message": "Payment completed",
            "remaining_balance": wallet_result["balance"],
        }

    # Step 3: Ask Notification Service to print the result.
    try:
        requests.post(
            f"{NOTIFICATION_SERVICE_URL}/send",
            json={
                "customer_id": payment.customer_id,
                "message": result["message"],
                "status": result["status"],
            },
            timeout=5,
        )
    except requests.RequestException:
        # Payment result is still returned; notification failure is separate.
        result["notification"] = "Notification service unavailable"

    return result


@app.get("/health")
def health():
    return {"service": "payment-service", "status": "healthy"}
