from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.core.database import Base


class YieldData(Base):
    __tablename__ = "yield_data"
    
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    crop_id = Column(Integer, ForeignKey("crops.id"), nullable=False)
    year = Column(Integer, nullable=False, index=True)
    season = Column(String, nullable=False)
    yield_value = Column(Float, nullable=False)  # tonnes per hectare
    area_cultivated = Column(Float, nullable=True)  # hectares
    production = Column(Float, nullable=True)  # tonnes
