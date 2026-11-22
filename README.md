# PayNova - Beginner Python Microservices Project

A small learning version of the PayNova payment project. It contains five separate
Python/FastAPI services:

1. `frontend` - a simple browser page where a customer enters an amount.
2. `api-gateway` - the single entry point used by the frontend.
3. `payment-service` - coordinates a payment.
4. `wallet-service` - checks a demo wallet balance and deducts money.
5. `notification-service` - prints a success/failure notification in its terminal.

This is a learning/demo project, NOT a real payment system. Wallet balances are
stored in memory, so they reset when the wallet container restarts. It has no
real bank/UPI integration, authentication, database, or production-grade security.

## Architecture

Browser
  |
  v
Frontend (port 8000)
  |
  v
API Gateway (port 8001)
  |
  v
Payment Service (port 8002)
  |                  \
  v                   v
Wallet Service     Notification Service
(port 8003)         (port 8004)

Each service is a separate application and container.

## Requirements

- Docker Desktop (or Docker Engine) with Docker Compose
- A web browser

You do NOT need to install Python packages manually when using Docker Compose.

## Run the project

Open a terminal in this project folder and run:

```bash
docker compose up --build
```

Wait until all five services start. Open:

```text
http://localhost:8000
```

Demo wallet:
- Customer ID: `student1`
- Starting balance: `1000`

Try paying `250`. The expected remaining balance is `750`.

Try paying `2000`. The payment should fail because the balance is too low.

## Useful commands

See running containers:

```bash
docker compose ps
```

See logs from all services:

```bash
docker compose logs -f
```

See logs from one service:

```bash
docker compose logs -f payment-service
```

Stop the project:

```bash
docker compose down
```

## Test the API without the webpage

```bash
curl -X POST http://localhost:8001/pay \
  -H "Content-Type: application/json" \
  -d '{"customer_id":"student1","amount":100}'
```

Check wallet balance:

```bash
curl http://localhost:8001/balance/student1
```

## Understand one payment

1. Customer enters an amount on the frontend.
2. Frontend sends the payment request to the API Gateway.
3. Gateway forwards it to Payment Service.
4. Payment Service asks Wallet Service to deduct the amount.
5. Wallet Service checks the balance. If enough money is available, it deducts it.
6. Payment Service asks Notification Service to print the result.
7. The result is returned to the frontend.

## Folder structure

```text
paynova-python-microservices/
├── docker-compose.yml
├── README.md
└── services/
    ├── frontend/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── Dockerfile
    ├── api-gateway/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── Dockerfile
    ├── payment-service/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── Dockerfile
    ├── wallet-service/
    │   ├── app.py
    │   ├── requirements.txt
    │   └── Dockerfile
    └── notification-service/
        ├── app.py
        ├── requirements.txt
        └── Dockerfile
```

## Next DevOps steps

After understanding this application, you can add the DevOps parts one by one:
1. Build Docker images and push them to Amazon ECR.
2. Deploy the services to Kubernetes (Amazon EKS or local `kind`).
3. Use Helm to manage Kubernetes deployment files.
4. Use Jenkins to test and build images.
5. Use Argo CD to deploy from Git.
6. Use Argo Rollouts for safe canary releases.
7. Use Prometheus and Grafana for metrics and dashboards.
8. Use Loki and Alloy for logs.
9. Use Kyverno for Kubernetes security policies.

Do not start with all these tools at once. First run the five services locally and
understand how one payment request travels between them.
