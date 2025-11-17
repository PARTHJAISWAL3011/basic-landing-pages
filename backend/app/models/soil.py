from sqlalchemy import Column, Integer, Float, ForeignKey, String
from app.core.database import Base


class Soil(Base):
    __tablename__ = "soil"
    
    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), nullable=False)
    soil_type = Column(String, nullable=True)
    ph = Column(Float, nullable=True)
    nitrogen = Column(Float, nullable=True)  # kg/ha
    phosphorus = Column(Float, nullable=True)  # kg/ha
    potassium = Column(Float, nullable=True)  # kg/ha
    organic_carbon = Column(Float, nullable=True)  # percentage
