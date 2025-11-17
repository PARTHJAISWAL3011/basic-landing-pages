from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base


class Region(Base):
    __tablename__ = "regions"
    
    id = Column(Integer, primary_key=True, index=True)
    state = Column(String, index=True, nullable=False)
    district = Column(String, index=True, nullable=False)
    city = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    area_hectares = Column(Float, nullable=True)
