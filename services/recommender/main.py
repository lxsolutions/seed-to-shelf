










from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class DemandForecastRequest(BaseModel):
    location: str
    time_horizon_days: int

@app.get("/forecast/demand")
def get_demand_forecast(request: DemandForecastRequest):
    # Mock forecast data - in real implementation would use ARIMA/Prophet
    return {
        "location": request.location,
        "time_horizon_days": request.time_horizon_days,
        "predicted_demand": [
            {"ingredient": "lettuce", "quantity_kg": 15.2},
            {"ingredient": "tomatoes", "quantity_kg": 8.7}
        ]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}










