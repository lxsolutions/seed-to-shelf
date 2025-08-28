










from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    nutrient_ec: float
    ph_level: float

@app.post("/sensors")
def record_sensor_data(data: SensorData):
    # In a real implementation, this would store in database
    return {
        "status": "recorded",
        "temperature_celsius": data.temperature,
        "nutrient_ec_mS_per_cm": data.nutrient_ec,
        "ph_level": data.ph_level
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}










