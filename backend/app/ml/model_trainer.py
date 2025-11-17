import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from xgboost import XGBRegressor
import joblib
import json


class CropYieldModel:
    def __init__(self):
        self.rf_model = None
        self.xgb_model = None
        self.scaler = StandardScaler()
        self.feature_names = []
        self.model_version = "1.0.0"
        
    def prepare_features(self, yield_df, weather_df, soil_df):
        """Prepare features for training"""
        # Merge all data
        data = yield_df.merge(weather_df, on=["region_id", "year", "season"], how="left")
        data = data.merge(soil_df, on="region_id", how="left")
        
        # Select features
        feature_cols = [
            "year",
            "avg_temperature",
            "total_rainfall",
            "avg_humidity",
            "rainy_days",
            "ph",
            "nitrogen",
            "phosphorus",
            "potassium",
            "organic_carbon"
        ]
        
        # Handle missing values
        data = data.dropna(subset=feature_cols + ["yield_value"])
        
        X = data[feature_cols]
        y = data["yield_value"]
        
        self.feature_names = feature_cols
        
        return X, y, data
    
    def train(self, X, y):
        """Train ensemble model"""
        print("Splitting data...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        print("Scaling features...")
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        print("Training Random Forest...")
        self.rf_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=15,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            n_jobs=-1
        )
        self.rf_model.fit(X_train_scaled, y_train)
        rf_score = self.rf_model.score(X_test_scaled, y_test)
        print(f"Random Forest R² Score: {rf_score:.4f}")
        
        print("Training XGBoost...")
        self.xgb_model = XGBRegressor(
            n_estimators=100,
            max_depth=6,
            learning_rate=0.1,
            random_state=42,
            n_jobs=-1
        )
        self.xgb_model.fit(X_train_scaled, y_train)
        xgb_score = self.xgb_model.score(X_test_scaled, y_test)
        print(f"XGBoost R² Score: {xgb_score:.4f}")
        
        return rf_score, xgb_score
    
    def predict(self, X):
        """Make ensemble prediction"""
        X_scaled = self.scaler.transform(X)
        
        # Ensemble: average of both models
        rf_pred = self.rf_model.predict(X_scaled)
        xgb_pred = self.xgb_model.predict(X_scaled)
        
        ensemble_pred = (rf_pred + xgb_pred) / 2
        
        # Calculate confidence interval (using RF prediction intervals)
        # Simplified approach: use standard deviation of predictions
        std_dev = np.std([rf_pred, xgb_pred], axis=0)
        confidence_lower = ensemble_pred - 1.96 * std_dev
        confidence_upper = ensemble_pred + 1.96 * std_dev
        
        return ensemble_pred, confidence_lower, confidence_upper
    
    def get_feature_importance(self):
        """Get feature importance from Random Forest"""
        if self.rf_model is None:
            return {}
        
        importance = self.rf_model.feature_importances_
        feature_importance = dict(zip(self.feature_names, importance.tolist()))
        
        # Sort by importance
        feature_importance = dict(
            sorted(feature_importance.items(), key=lambda x: x[1], reverse=True)
        )
        
        return feature_importance
    
    def save(self, model_dir):
        """Save model and scaler"""
        model_dir = Path(model_dir)
        model_dir.mkdir(exist_ok=True, parents=True)
        
        joblib.dump(self.rf_model, model_dir / "rf_model.pkl")
        joblib.dump(self.xgb_model, model_dir / "xgb_model.pkl")
        joblib.dump(self.scaler, model_dir / "scaler.pkl")
        
        # Save metadata
        metadata = {
            "version": self.model_version,
            "feature_names": self.feature_names,
            "feature_importance": self.get_feature_importance()
        }
        
        with open(model_dir / "metadata.json", "w") as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Model saved to {model_dir}")
    
    def load(self, model_dir):
        """Load model and scaler"""
        model_dir = Path(model_dir)
        
        self.rf_model = joblib.load(model_dir / "rf_model.pkl")
        self.xgb_model = joblib.load(model_dir / "xgb_model.pkl")
        self.scaler = joblib.load(model_dir / "scaler.pkl")
        
        with open(model_dir / "metadata.json", "r") as f:
            metadata = json.load(f)
            self.model_version = metadata["version"]
            self.feature_names = metadata["feature_names"]
        
        print(f"Model loaded from {model_dir}")


def main():
    """Train and save the model"""
    print("Loading data...")
    data_dir = Path(__file__).parent.parent / "data"
    
    yield_df = pd.read_csv(data_dir / "yield_data.csv")
    weather_df = pd.read_csv(data_dir / "weather.csv")
    soil_df = pd.read_csv(data_dir / "soil.csv")
    
    print(f"Loaded {len(yield_df)} yield records")
    
    # Initialize model
    model = CropYieldModel()
    
    # Prepare features
    print("Preparing features...")
    X, y, data = model.prepare_features(yield_df, weather_df, soil_df)
    print(f"Features shape: {X.shape}")
    print(f"Target shape: {y.shape}")
    
    # Train model
    print("\nTraining models...")
    rf_score, xgb_score = model.train(X, y)
    
    # Get feature importance
    print("\nFeature Importance:")
    for feature, importance in model.get_feature_importance().items():
        print(f"  {feature}: {importance:.4f}")
    
    # Save model
    model_dir = Path(__file__).parent.parent / "models"
    model.save(model_dir)
    
    print("\nModel training complete!")
    print(f"Random Forest R² Score: {rf_score:.4f}")
    print(f"XGBoost R² Score: {xgb_score:.4f}")


if __name__ == "__main__":
    main()
