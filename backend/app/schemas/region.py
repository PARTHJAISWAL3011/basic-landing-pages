from pydantic import BaseModel
from typing import Optional


class RegionResponse(BaseModel):
    id: int
    state: str
    district: str
    city: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    
    class Config:
        from_attributes = True
