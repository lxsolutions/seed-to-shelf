


from fastapi import FastAPI
from src.api.v1.router import router as v1_router

app = FastAPI(
    title="Seed to Chef API",
    description="API for the Seed to Chef platform",
    version="0.1.0"
)

app.include_router(v1_router, prefix="/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to Seed to Chef API"}

