from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="PayNova Notification Service")


class NotificationRequest(BaseModel):
    customer_id: str
    message: str
    status: str


@app.post("/send")
def send_notification(notification: NotificationRequest):
    # Learning demo: print a message instead of sending a real SMS/email.
    print(
        f"[NOTIFICATION] Customer={notification.customer_id} "
        f"Status={notification.status} Message={notification.message}",
        flush=True,
    )
    return {"sent": True, "message": "Notification printed in service logs"}


@app.get("/health")
def health():
    return {"service": "notification-service", "status": "healthy"}
