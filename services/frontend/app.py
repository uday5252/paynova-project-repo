import os

import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="PayNova Frontend")
API_GATEWAY_URL = os.getenv("API_GATEWAY_URL", "http://localhost:8001")


class PaymentForm(BaseModel):
    customer_id: str
    amount: float = Field(gt=0)


@app.get("/", response_class=HTMLResponse)
def home():
    return '''
    <!doctype html>
    <html>
    <head>
      <title>PayNova Demo</title>
      <style>
        body { font-family: Arial; max-width: 520px; margin: 50px auto; padding: 20px; }
        input, button { padding: 10px; margin: 7px 0; width: 100%; box-sizing: border-box; }
        button { background: #1456cc; color: white; border: 0; cursor: pointer; }
        pre { background: #f2f2f2; padding: 12px; white-space: pre-wrap; }
      </style>
    </head>
    <body>
      <h1>PayNova - Payment Demo</h1>
      <p>Demo customer: <b>student1</b> | Starting balance: ₹1000</p>
      <label>Customer ID</label>
      <input id="customer" value="student1">
      <label>Amount</label>
      <input id="amount" type="number" min="1" step="0.01" value="250">
      <button onclick="pay()">Make payment</button>
      <pre id="result">Payment result will appear here.</pre>
      <script>
        async function pay() {
          const result = document.getElementById("result");
          result.textContent = "Processing...";
          try {
            const response = await fetch("/pay", {
              method: "POST",
              headers: {"Content-Type": "application/json"},
              body: JSON.stringify({
                customer_id: document.getElementById("customer").value,
                amount: Number(document.getElementById("amount").value)
              })
            });
            const data = await response.json();
            result.textContent = JSON.stringify(data, null, 2);
          } catch (error) {
            result.textContent = "Could not contact the application: " + error;
          }
        }
      </script>
    </body>
    </html>
    '''


@app.post("/pay")
def make_payment(payment: PaymentForm):
    response = requests.post(
        f"{API_GATEWAY_URL}/pay",
        json=payment.model_dump(),
        timeout=10,
    )
    return response.json()


@app.get("/health")
def health():
    return {"service": "frontend", "status": "healthy"}
