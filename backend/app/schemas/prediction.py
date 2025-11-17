from pydantic import BaseModel, Field
from typing import Optional, Dict


class PredictionRequest(BaseModel):
    state: str
    district: str
    crop: str
    season: str
    year: int = Field(default=2025, ge=2020, le=2030)


class CustomPredictionRequest(BaseModel):
    state: str
    district: str
    crop: str
    season: str
    year: int = Field(default=2025, ge=2020, le=2030)
    temperature: Optional[float] = None
    rainfall: Optional[float] = None
    humidity: Optional[float] = None
    soil_ph: Optional[float] = None
    nitrogen: Optional[float] = None
    phosphorus: Optional[float] = None
    potassium: Optional[float] = None
    fertilizer_usage: Optional[float] = None
    irrigation: Optional[bool] = None


class PredictionResponse(BaseModel):
    predicted_yield: float
    unit: str = "tonnes/ha"
    confidence_lower: Optional[float] = None
    confidence_upper: Optional[float] = None
    feature_importance: Optional[Dict[str, float]] = None
    state: str
    district: str
    crop: str
    season: str
    year: int
    
    class Config:
        from_attributes = True
