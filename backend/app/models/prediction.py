from sqlalchemy import Column, Integer, Float, ForeignKey, String, DateTime, JSON
from datetime import datetime
from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    year = Column(Integer, nullable=False)
    season = Column(String, nullable=False)
    predicted_yield = Column(Float, nullable=False)
    confidence_lower = Column(Float, nullable=True)
    confidence_upper = Column(Float, nullable=True)
    feature_importance = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    model_version = Column(String, nullable=True)
