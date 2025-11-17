import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, Tuple, Optional
from .model_trainer import CropYieldModel


class YieldPredictor:
    def __init__(self):
        self.model = CropYieldModel()
        self.model_loaded = False
        
    def load_model(self):
        """Load the trained model"""
        if not self.model_loaded:
            model_dir = Path(__file__).parent.parent / "models"
            if model_dir.exists():
                self.model.load(model_dir)
                self.model_loaded = True
            else:
                raise FileNotFoundError("Model not found. Please train the model first.")
    
    def predict_yield(
        self,
        year: int,
        temperature: float,
        rainfall: float,
        humidity: float,
        rainy_days: int,
        ph: float,
        nitrogen: float,
        phosphorus: float,
        potassium: float,
        organic_carbon: float
    ) -> Tuple[float, float, float, Dict[str, float]]:
        """
        Predict crop yield based on input features
        
        Returns:
            predicted_yield, confidence_lower, confidence_upper, feature_importance
        """
        if not self.model_loaded:
            self.load_model()
        
        # Prepare input features
        features = pd.DataFrame([{
            "year": year,
            "avg_temperature": temperature,
            "total_rainfall": rainfall,
            "avg_humidity": humidity,
            "rainy_days": rainy_days,
            "ph": ph,
            "nitrogen": nitrogen,
            "phosphorus": phosphorus,
            "potassium": potassium,
            "organic_carbon": organic_carbon
        }])
        
        # Make prediction
        pred, lower, upper = self.model.predict(features)
        
        # Get feature importance
        feature_importance = self.model.get_feature_importance()
        
        return (
            float(pred[0]),
            float(lower[0]),
            float(upper[0]),
            feature_importance
        )
    
    def predict_from_database(
        self,
        region_id: int,
        crop_id: int,
        year: int,
        season: str,
        weather_data: Dict,
        soil_data: Dict,
        custom_inputs: Optional[Dict] = None
    ) -> Tuple[float, float, float, Dict[str, float]]:
        """
        Predict yield using database data with optional custom inputs
        """
        # Use custom inputs if provided, otherwise use database values
        temperature = custom_inputs.get("temperature") if custom_inputs else weather_data.get("avg_temperature")
        rainfall = custom_inputs.get("rainfall") if custom_inputs else weather_data.get("total_rainfall")
        humidity = custom_inputs.get("humidity") if custom_inputs else weather_data.get("avg_humidity")
        rainy_days = weather_data.get("rainy_days", 50)
        
        ph = custom_inputs.get("soil_ph") if custom_inputs else soil_data.get("ph")
        nitrogen = custom_inputs.get("nitrogen") if custom_inputs else soil_data.get("nitrogen")
        phosphorus = custom_inputs.get("phosphorus") if custom_inputs else soil_data.get("phosphorus")
        potassium = custom_inputs.get("potassium") if custom_inputs else soil_data.get("potassium")
        organic_carbon = soil_data.get("organic_carbon", 0.8)
        
        # Apply fertilizer and irrigation adjustments if provided
        if custom_inputs:
            if custom_inputs.get("fertilizer_usage"):
                # Increase NPK based on fertilizer usage
                nitrogen *= (1 + custom_inputs["fertilizer_usage"] * 0.1)
                phosphorus *= (1 + custom_inputs["fertilizer_usage"] * 0.1)
                potassium *= (1 + custom_inputs["fertilizer_usage"] * 0.1)
            
            if custom_inputs.get("irrigation"):
                # Irrigation increases effective rainfall
                rainfall *= 1.2
        
        return self.predict_yield(
            year=year,
            temperature=temperature,
            rainfall=rainfall,
            humidity=humidity,
            rainy_days=rainy_days,
            ph=ph,
            nitrogen=nitrogen,
            phosphorus=phosphorus,
            potassium=potassium,
            organic_carbon=organic_carbon
        )


# Global predictor instance
predictor = YieldPredictor()
