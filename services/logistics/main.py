








from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RouteRequest(BaseModel):
    pickup_location: str
    dropoff_location: str
    delivery_mode: str  # PICKUP|DRIVER|DRONE

@app.post("/route/quote")
def get_route_quote(request: RouteRequest):
    return {
        "delivery_mode": request.delivery_mode,
        "estimated_time_minutes": 30 if request.delivery_mode == "DRIVER" else 15,
        "cost": 7.99 if request.delivery_mode == "DRIVER" else 2.99
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}








