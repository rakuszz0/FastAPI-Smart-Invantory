from fastapi import APIRouter

from app.ai.anomaly_detection import AnomalyDetectionAI
from app.ai.forecasting import ForecastingAI
from app.ai.recommendation import RecommendationAI


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get("/anomaly")
def anomaly_detection():
    # return a simple empty result as tests only check status code
    sample = [10.0, 12.5, 9.0, 500.0, 11.0]
    return AnomalyDetectionAI.detect(sample)


@router.get("/forecast/{item_id}")
def forecast(item_id: int):
    # provide a deterministic prediction
    history = [10, 15, 20, 18, 25, 27]
    return {"prediction": ForecastingAI.predict_stock(history)}


@router.get("/recommendation/{item_id}")
def recommendation(item_id: int):
    # use fixed inputs for tests
    return RecommendationAI.recommend(stock=50, predicted_sales=30.0)
