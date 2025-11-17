from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.core.database import Base


class Weather(Base):
    __tablename__ = "weather"
    
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    year = Column(Integer, nullable=False, index=True)
    season = Column(String, nullable=False)
    avg_temperature = Column(Float, nullable=True)  # Celsius
    total_rainfall = Column(Float, nullable=True)  # mm
    avg_humidity = Column(Float, nullable=True)  # percentage
    rainy_days = Column(Integer, nullable=True)
