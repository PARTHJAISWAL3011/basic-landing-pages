from pydantic import BaseModel
from typing import Optional


class CropResponse(BaseModel):
    id: int
    name: str
    category: str
    season: str
    description: Optional[str] = None
    
    class Config:
        from_attributes = True
