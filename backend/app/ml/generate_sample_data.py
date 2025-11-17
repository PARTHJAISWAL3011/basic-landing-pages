import pandas as pd
import numpy as np
from pathlib import Path

# Set random seed for reproducibility
np.random.seed(42)

# Define Indian states and districts
REGIONS = [
    # Punjab
    ("Punjab", "Ludhiana", 30.9010, 75.8573),
    ("Punjab", "Amritsar", 31.6340, 74.8723),
    ("Punjab", "Patiala", 30.3398, 76.3869),
    ("Punjab", "Jalandhar", 31.3260, 75.5762),
    
    # Haryana
    ("Haryana", "Karnal", 29.6857, 76.9905),
    ("Haryana", "Hisar", 29.1492, 75.7217),
    ("Haryana", "Ambala", 30.3782, 76.7767),
    
    # Uttar Pradesh
    ("Uttar Pradesh", "Meerut", 28.9845, 77.7064),
    ("Uttar Pradesh", "Lucknow", 26.8467, 80.9462),
    ("Uttar Pradesh", "Varanasi", 25.3176, 82.9739),
    ("Uttar Pradesh", "Agra", 27.1767, 78.0081),
    
    # Maharashtra
    ("Maharashtra", "Pune", 18.5204, 73.8567),
    ("Maharashtra", "Nashik", 19.9975, 73.7898),
    ("Maharashtra", "Nagpur", 21.1458, 79.0882),
    ("Maharashtra", "Ahmednagar", 19.0948, 74.7480),
    
    # Karnataka
    ("Karnataka", "Bengaluru", 12.9716, 77.5946),
    ("Karnataka", "Mysuru", 12.2958, 76.6394),
    ("Karnataka", "Belgaum", 15.8497, 74.4977),
    ("Karnataka", "Mandya", 12.5244, 76.8958),
    
    # Tamil Nadu
    ("Tamil Nadu", "Coimbatore", 11.0168, 76.9558),
    ("Tamil Nadu", "Thanjavur", 10.7870, 79.1378),
    ("Tamil Nadu", "Salem", 11.6643, 78.1460),
    ("Tamil Nadu", "Tirunelveli", 8.7139, 77.7567),
    
    # West Bengal
    ("West Bengal", "Kolkata", 22.5726, 88.3639),
    ("West Bengal", "Bardhaman", 23.2324, 87.8615),
    ("West Bengal", "Murshidabad", 24.1833, 88.2833),
    
    # Andhra Pradesh
    ("Andhra Pradesh", "Guntur", 16.3067, 80.4365),
    ("Andhra Pradesh", "Krishna", 16.5193, 80.6305),
    ("Andhra Pradesh", "Visakhapatnam", 17.6868, 83.2185),
    
    # Telangana
    ("Telangana", "Hyderabad", 17.3850, 78.4867),
    ("Telangana", "Warangal", 17.9689, 79.5941),
    
    # Madhya Pradesh
    ("Madhya Pradesh", "Indore", 22.7196, 75.8577),
    ("Madhya Pradesh", "Bhopal", 23.2599, 77.4126),
    ("Madhya Pradesh", "Jabalpur", 23.1815, 79.9864),
    
    # Gujarat
    ("Gujarat", "Ahmedabad", 23.0225, 72.5714),
    ("Gujarat", "Surat", 21.1702, 72.8311),
    ("Gujarat", "Rajkot", 22.3039, 70.8022),
    
    # Rajasthan
    ("Rajasthan", "Jaipur", 26.9124, 75.7873),
    ("Rajasthan", "Jodhpur", 26.2389, 73.0243),
    ("Rajasthan", "Kota", 25.2138, 75.8648),
    
    # Bihar
    ("Bihar", "Patna", 25.5941, 85.1376),
    ("Bihar", "Gaya", 24.7955, 85.0002),
    ("Bihar", "Muzaffarpur", 26.1225, 85.3906),
    
    # Odisha
    ("Odisha", "Bhubaneswar", 20.2961, 85.8245),
    ("Odisha", "Cuttack", 20.4625, 85.8830),
]

# Define crops with their characteristics
CROPS = [
    ("Rice", "staple", "kharif", "Major cereal crop"),
    ("Wheat", "staple", "rabi", "Major cereal crop"),
    ("Maize", "staple", "kharif", "Cereal crop"),
    ("Cotton", "cash", "kharif", "Fiber crop"),
    ("Sugarcane", "cash", "kharif", "Cash crop"),
    ("Pulses", "pulse", "rabi", "Protein-rich legumes"),
    ("Groundnut", "oilseed", "kharif", "Oilseed crop"),
    ("Soybean", "oilseed", "kharif", "Oilseed crop"),
]

YEARS = [2019, 2020, 2021, 2022, 2023, 2024]
SEASONS = ["kharif", "rabi"]

# Crop-specific yield ranges (tonnes/ha)
CROP_YIELD_RANGES = {
    "Rice": (2.5, 5.5),
    "Wheat": (3.0, 5.0),
    "Maize": (2.0, 4.5),
    "Cotton": (1.5, 3.0),
    "Sugarcane": (60.0, 90.0),
    "Pulses": (0.8, 1.5),
    "Groundnut": (1.2, 2.5),
    "Soybean": (1.0, 2.0),
}

def generate_regions():
    """Generate regions data"""
    regions = []
    for idx, (state, district, lat, lon) in enumerate(REGIONS, 1):
        regions.append({
            "id": idx,
            "state": state,
            "district": district,
            "city": district,  # Using district as city for simplicity
            "latitude": lat,
            "longitude": lon,
            "area_hectares": np.random.uniform(50000, 200000)
        })
    return pd.DataFrame(regions)

def generate_crops():
    """Generate crops data"""
    crops = []
    for idx, (name, category, season, description) in enumerate(CROPS, 1):
        crops.append({
            "id": idx,
            "name": name,
            "category": category,
            "season": season,
            "description": description
        })
    return pd.DataFrame(crops)

def generate_weather(regions_df):
    """Generate weather data"""
    weather_data = []
    weather_id = 1
    
    for _, region in regions_df.iterrows():
        for year in YEARS:
            for season in SEASONS:
                # Season-specific weather patterns
                if season == "kharif":  # Monsoon season
                    temp = np.random.uniform(25, 35)
                    rainfall = np.random.uniform(600, 1200)
                    humidity = np.random.uniform(70, 90)
                    rainy_days = np.random.randint(60, 100)
                else:  # rabi - winter season
                    temp = np.random.uniform(15, 25)
                    rainfall = np.random.uniform(50, 200)
                    humidity = np.random.uniform(50, 70)
                    rainy_days = np.random.randint(10, 30)
                
                weather_data.append({
                    "id": weather_id,
                    "region_id": region["id"],
                    "year": year,
                    "season": season,
                    "avg_temperature": round(temp, 2),
                    "total_rainfall": round(rainfall, 2),
                    "avg_humidity": round(humidity, 2),
                    "rainy_days": rainy_days
                })
                weather_id += 1
    
    return pd.DataFrame(weather_data)

def generate_soil(regions_df):
    """Generate soil data"""
    soil_data = []
    soil_types = ["Alluvial", "Black", "Red", "Laterite", "Sandy"]
    
    for idx, region in regions_df.iterrows():
        soil_data.append({
            "id": idx + 1,
            "region_id": region["id"],
            "soil_type": np.random.choice(soil_types),
            "ph": round(np.random.uniform(5.5, 8.5), 2),
            "nitrogen": round(np.random.uniform(150, 350), 2),
            "phosphorus": round(np.random.uniform(10, 50), 2),
            "potassium": round(np.random.uniform(100, 300), 2),
            "organic_carbon": round(np.random.uniform(0.3, 1.5), 2)
        })
    
    return pd.DataFrame(soil_data)

def generate_yield_data(regions_df, crops_df, weather_df, soil_df):
    """Generate historical yield data with realistic patterns"""
    yield_data = []
    yield_id = 1
    
    for _, region in regions_df.iterrows():
        for _, crop in crops_df.iterrows():
            # Only generate data for matching seasons
            crop_season = crop["season"]
            
            for year in YEARS:
                # Get weather and soil data for this region
                weather = weather_df[
                    (weather_df["region_id"] == region["id"]) & 
                    (weather_df["year"] == year) & 
                    (weather_df["season"] == crop_season)
                ].iloc[0]
                
                soil = soil_df[soil_df["region_id"] == region["id"]].iloc[0]
                
                # Base yield from crop range
                min_yield, max_yield = CROP_YIELD_RANGES[crop["name"]]
                base_yield = np.random.uniform(min_yield, max_yield)
                
                # Weather impact
                rainfall_factor = 1.0
                if crop_season == "kharif":
                    # Kharif crops need good rainfall
                    if weather["total_rainfall"] < 700:
                        rainfall_factor = 0.8
                    elif weather["total_rainfall"] > 1000:
                        rainfall_factor = 1.1
                
                temp_factor = 1.0
                if weather["avg_temperature"] > 32:
                    temp_factor = 0.95
                elif weather["avg_temperature"] < 20:
                    temp_factor = 0.9
                
                # Soil impact
                soil_factor = 1.0
                if 6.0 <= soil["ph"] <= 7.5:
                    soil_factor = 1.1
                if soil["nitrogen"] > 250:
                    soil_factor *= 1.05
                
                # Calculate final yield
                final_yield = base_yield * rainfall_factor * temp_factor * soil_factor
                final_yield = round(final_yield, 2)
                
                area = np.random.uniform(5000, 50000)
                production = round(final_yield * area, 2)
                
                yield_data.append({
                    "id": yield_id,
                    "region_id": region["id"],
                    "crop_id": crop["id"],
                    "year": year,
                    "season": crop_season,
                    "yield_value": final_yield,
                    "area_cultivated": round(area, 2),
                    "production": production
                })
                yield_id += 1
    
    return pd.DataFrame(yield_data)

def main():
    """Generate all sample data"""
    print("Generating sample data...")
    
    # Create data directory
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)
    
    # Generate data
    print("Generating regions...")
    regions_df = generate_regions()
    regions_df.to_csv(data_dir / "regions.csv", index=False)
    
    print("Generating crops...")
    crops_df = generate_crops()
    crops_df.to_csv(data_dir / "crops.csv", index=False)
    
    print("Generating weather data...")
    weather_df = generate_weather(regions_df)
    weather_df.to_csv(data_dir / "weather.csv", index=False)
    
    print("Generating soil data...")
    soil_df = generate_soil(regions_df)
    soil_df.to_csv(data_dir / "soil.csv", index=False)
    
    print("Generating yield data...")
    yield_df = generate_yield_data(regions_df, crops_df, weather_df, soil_df)
    yield_df.to_csv(data_dir / "yield_data.csv", index=False)
    
    print(f"\nData generation complete!")
    print(f"Regions: {len(regions_df)}")
    print(f"Crops: {len(crops_df)}")
    print(f"Weather records: {len(weather_df)}")
    print(f"Soil records: {len(soil_df)}")
    print(f"Yield records: {len(yield_df)}")

if __name__ == "__main__":
    main()
