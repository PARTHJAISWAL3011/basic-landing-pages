from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import distinct
from typing import List, Optional
from app.core.database import get_db
from app.schemas.region import RegionResponse
from app.schemas.crop import CropResponse
from app.models import Region, Crop

router = APIRouter()


@router.get("/metadata/crops", response_model=List[CropResponse])
async def get_crops(
    season: Optional[str] = Query(None, description="Filter by season"),
    category: Optional[str] = Query(None, description="Filter by category"),
    db: Session = Depends(get_db)
):
    """
    Get list of all supported crops
    """
    query = db.query(Crop)
    
    if season:
        query = query.filter(Crop.season == season)
    if category:
        query = query.filter(Crop.category == category)
    
    crops = query.all()
    return crops


@router.get("/metadata/regions", response_model=List[RegionResponse])
async def get_regions(
    state: Optional[str] = Query(None, description="Filter by state"),
    district: Optional[str] = Query(None, description="Filter by district"),
    db: Session = Depends(get_db)
):
    """
    Get list of regions (states/districts)
    """
    query = db.query(Region)
    
    if state:
        query = query.filter(Region.state == state)
    if district:
        query = query.filter(Region.district == district)
    
    regions = query.all()
    return regions


@router.get("/metadata/states", response_model=List[str])
async def get_states(db: Session = Depends(get_db)):
    """
    Get list of all states
    """
    states = db.query(distinct(Region.state)).order_by(Region.state).all()
    return [state[0] for state in states]


@router.get("/metadata/districts", response_model=List[str])
async def get_districts(
    state: str = Query(..., description="State name"),
    db: Session = Depends(get_db)
):
    """
    Get list of districts for a given state
    """
    districts = db.query(distinct(Region.district)).filter(
        Region.state == state
    ).order_by(Region.district).all()
    
    return [district[0] for district in districts]
