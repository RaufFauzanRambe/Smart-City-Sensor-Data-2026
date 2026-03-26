import pandas as pd
from pathlib import Path

def load_csv_or_dummy(file_path: str, sensor_type: str) -> pd.DataFrame:
    """
    Load CSV if exists, otherwise create dummy DataFrame for that sensor type.
    Prints the resulting DataFrame.
    """
    file = Path(file_path)
    if file.exists():
        try:
            df = pd.read_csv(file_path)
            print(f"✅ Loaded {file_path} successfully, shape: {df.shape}")
            print(df)
            return df
        except Exception as e:
            print(f"❌ Error loading {file_path}: {e}")
    print(f"⚠️ {file_path} not found. Creating dummy {sensor_type} DataFrame.")
    
    if sensor_type == "traffic":
        df = pd.DataFrame({
            "timestamp": ["2026-01-01 08:00", "2026-01-01 09:00"],
            "location": ["Zone A", "Zone B"],
            "traffic_count": [120, 95]
        })
    elif sensor_type == "air_quality":
        df = pd.DataFrame({
            "timestamp": ["2026-01-01 08:00", "2026-01-01 09:00"],
            "location": ["Zone A", "Zone B"],
            "pm25": [35.2, 40.5],
            "pm10": [50.1, 55.3]
        })
    elif sensor_type == "weather":
        df = pd.DataFrame({
            "timestamp": ["2026-01-01 08:00", "2026-01-01 09:00"],
            "location": ["Zone A", "Zone B"],
            "temperature": [25.3, 26.1],
            "humidity": [60, 58]
        })
    elif sensor_type == "energy":
        df = pd.DataFrame({
            "timestamp": ["2026-01-01 08:00", "2026-01-01 09:00"],
            "location": ["Zone A", "Zone B"],
            "consumption": [1500, 1600]
        })
    else:
        df = pd.DataFrame()
    
    print(df)
    return df

def load_all_data(data_path: str = "data/processed/") -> dict:
    """
    Load all Smart City sensor CSVs, fallback to dummy data if files are missing.
    Prints summary and resulting dictionary of DataFrames.
    """
    data = {}
    data['traffic'] = load_csv_or_dummy(Path(data_path) / "traffic_sensors_processed.csv", "traffic")
    data['air_quality'] = load_csv_or_dummy(Path(data_path) / "air_quality_sensors_processed.csv", "air_quality")
    data['weather'] = load_csv_or_dummy(Path(data_path) / "weather_station_processed.csv", "weather")
    data['energy'] = load_csv_or_dummy(Path(data_path) / "energy_grid_processed.csv", "energy")
    
    print("\n📊 Summary of loaded datasets:")
    for key, df in data.items():
        print(f"{key}: {df.shape}")
    print("\n✅ All loaded DataFrames:")
    print(data)
    return data
