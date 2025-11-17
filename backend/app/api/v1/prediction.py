from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.schemas.prediction import PredictionRequest, PredictionResponse, CustomPredictionRequest
from app.models import Region, Crop, Weather, Soil
from app.ml.predictor import predictor

router = APIRouter()


@router.get("/prediction", response_model=PredictionResponse)
async def get_prediction(
    state: str = Query(..., description="State name"),
    district: str = Query(..., description="District name"),
    crop: str = Query(..., description="Crop name"),
    season: str = Query(..., description="Season (kharif/rabi)"),
    year: int = Query(2025, description="Year for prediction"),
    db: Session = Depends(get_db)
):
    """
    Get crop yield prediction for a specific region and crop
    """
    # Find region
    region = db.query(Region).filter(
        Region.state == state,
        Region.district == district
    ).first()
    
    if not region:
        raise HTTPException(status_code=404, detail=f"Region not found: {state}, {district}")
    
    # Find crop
    crop_obj = db.query(Crop).filter(Crop.name == crop).first()
    if not crop_obj:
        raise HTTPException(status_code=404, detail=f"Crop not found: {crop}")
    
    # Check if crop season matches
    if crop_obj.season != season:
        raise HTTPException(
            status_code=400,
            detail=f"{crop} is a {crop_obj.season} crop, not {season}"
        )
    
    # Get weather data (use latest available or average)
    weather = db.query(Weather).filter(
        Weather.region_id == region.id,
        Weather.season == season
    ).order_by(Weather.year.desc()).first()
    
    if not weather:
        raise HTTPException(
            status_code=404,
            detail=f"Weather data not found for {state}, {district}, {season}"
        )
    
    # Get soil data
    soil = db.query(Soil).filter(Soil.region_id == region.id).first()
    if not soil:
        raise HTTPException(
            status_code=404,
            detail=f"Soil data not found for {state}, {district}"
        )
    
    # Make prediction
    try:
        predicted_yield, conf_lower, conf_upper, feature_importance = predictor.predict_from_database(
            region_id=region.id,
            crop_id=crop_obj.id,
            year=year,
            season=season,
            weather_data={
                "avg_temperature": weather.avg_temperature,
                "total_rainfall": weather.total_rainfall,
                "avg_humidity": weather.avg_humidity,
                "rainy_days": weather.rainy_days
            },
            soil_data={
                "ph": soil.ph,
                "nitrogen": soil.nitrogen,
                "phosphorus": soil.phosphorus,
                "potassium": soil.potassium,
                "organic_carbon": soil.organic_carbon
            }
        )
        
        return PredictionResponse(
            predicted_yield=round(predicted_yield, 2),
            confidence_lower=round(conf_lower, 2),
            confidence_upper=round(conf_upper, 2),
            feature_importance=feature_importance,
            state=state,
            district=district,
            crop=crop,
            season=season,
            year=year
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@router.post("/prediction/custom", response_model=PredictionResponse)
async def get_custom_prediction(
    request: CustomPredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Get custom crop yield prediction with user-provided inputs
    """
    # Find region
    region = db.query(Region).filter(
        Region.state == request.state,
        Region.district == request.district
    ).first()
    
    if not region:
        raise HTTPException(
            status_code=404,
            detail=f"Region not found: {request.state}, {request.district}"
        )
    
    # Find crop
    crop_obj = db.query(Crop).filter(Crop.name == request.crop).first()
    if not crop_obj:
        raise HTTPException(status_code=404, detail=f"Crop not found: {request.crop}")
    
    # Get default weather and soil data
    weather = db.query(Weather).filter(
        Weather.region_id == region.id,
        Weather.season == request.season
    ).order_by(Weather.year.desc()).first()
    
    soil = db.query(Soil).filter(Soil.region_id == region.id).first()
    
    if not weather or not soil:
        raise HTTPException(
            status_code=404,
            detail="Base data not found for this region"
        )
    
    # Prepare custom inputs
    custom_inputs = {}
    if request.temperature is not None:
        custom_inputs["temperature"] = request.temperature
    if request.rainfall is not None:
        custom_inputs["rainfall"] = request.rainfall
    if request.humidity is not None:
        custom_inputs["humidity"] = request.humidity
    if request.soil_ph is not None:
        custom_inputs["soil_ph"] = request.soil_ph
    if request.nitrogen is not None:
        custom_inputs["nitrogen"] = request.nitrogen
    if request.phosphorus is not None:
        custom_inputs["phosphorus"] = request.phosphorus
    if request.potassium is not None:
        custom_inputs["potassium"] = request.potassium
    if request.fertilizer_usage is not None:
        custom_inputs["fertilizer_usage"] = request.fertilizer_usage
    if request.irrigation is not None:
        custom_inputs["irrigation"] = request.irrigation
    
    # Make prediction
    try:
        predicted_yield, conf_lower, conf_upper, feature_importance = predictor.predict_from_database(
            region_id=region.id,
            crop_id=crop_obj.id,
            year=request.year,
            season=request.season,
            weather_data={
                "avg_temperature": weather.avg_temperature,
                "total_rainfall": weather.total_rainfall,
                "avg_humidity": weather.avg_humidity,
                "rainy_days": weather.rainy_days
            },
            soil_data={
                "ph": soil.ph,
                "nitrogen": soil.nitrogen,
                "phosphorus": soil.phosphorus,
                "potassium": soil.potassium,
                "organic_carbon": soil.organic_carbon
            },
            custom_inputs=custom_inputs if custom_inputs else None
        )
        
        return PredictionResponse(
            predicted_yield=round(predicted_yield, 2),
            confidence_lower=round(conf_lower, 2),
            confidence_upper=round(conf_upper, 2),
            feature_importance=feature_importance,
            state=request.state,
            district=request.district,
            crop=request.crop,
            season=request.season,
            year=request.year
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
