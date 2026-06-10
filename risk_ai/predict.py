import pandas as pd
import joblib
from huggingface_hub import hf_hub_download
from risk_ai.fetch_ai_data import elevation, soil

hfrepo = "robil/siagaai-flood-risk-model"

riskModelpath = hf_hub_download(repo_id=hfrepo, filename="flood_risk_model.pkl")
scalerpath = hf_hub_download(repo_id=hfrepo, filename="feature_scaler.pkl")
encoderPath = hf_hub_download(repo_id=hfrepo, filename="label_encoder.pkl")

encoder = joblib.load(encoderPath)
model = joblib.load(riskModelpath)
scaler = joblib.load(scalerpath)

hydroRankings = {
    "A": 0,
    "B": 1,
    "C": 2,
    "D": 3,
    "A/D": 4,
    "B/D": 5,
    "C/D": 6
}

drainageRankings = {
    "Excessively drained":          1.0,
    "Somewhat excessively drained": 0.85,
    "Well drained":                 0.75,
    "Moderately well drained":      0.55,
    "Somewhat poorly drained":      0.35,
    "Poorly drained":               0.15,
    "Very poorly drained":          0.05
}

# note this is from wtv language they speak in indonasiaa to normal engilsh
risk = {
    "aman":    "Safe", # 1
    "waspada": "Low", # 2
    "siaga":   "Medium", # 3
    "awas":    "High" # 4
}

# sampledata = {
#     "rainfall_1h": 25.5,
#     "rainfall_3h": 60.2,
#     "rainfall_24h": 150.0,
#     "humidity": 88.0,
#     "temperature": 26.5,
#     "wind_speed": 15.0,
#     "month": 11,             
#     "is_rainy_season": 1,   
#     "elevation_m": 12.0,
#     "distance_to_river_km": 0.5,
#     "soil_type_encoded": 3,  
#     "rain_intensity": 8.5,
#     "rain_persistence": 4.0,
#     "saturation_index": 0.85,
#     "drainage_score": 0.4,   # note to self: metadata says this is most important
#     "heat_humidity": 31.0,
#     "city_risk": 0.8
# }

cache = {(43.15,-77.57): "High"}
def predict(lat, lon, rainfall_1h=0.0, rainfall_3h=0.0, rainfall_24h=0.0,humidity=70.0, temp=20.0, wind=10.0, month=6, isRainySzn=0, cityRisk=0.5):
    tup = (round(lat, 2), round(lon, 2))
    if tup in cache:
        return cache[tup]

    elev = float(elevation(lat, lon))
    hydro, drain = soil(lat, lon)

    soilScore = hydroRankings.get(hydro, 1)
    drainageScore = drainageRankings.get(drain, 0.5)

    rainIntensity = rainfall_1h
    rainPersistence = rainfall_3h / 3
    if (humidity / 100.0 <= 1.0):
        saturationIndex = humidity / 100.0
    elif (humidity / 100.0 > 1.0):
        saturationIndex = 1.0
    heatHumidity = temp * (humidity / 100.0)

    features = {
        "rainfall_1h": rainfall_1h,
        "rainfall_3h": rainfall_3h,
        "rainfall_24h": rainfall_24h,
        "humidity": humidity,
        "temperature": temp,
        "wind_speed": wind,
        "month": month,
        "is_rainy_season": isRainySzn,
        "elevation_m": elev,
        "distance_to_river_km": 0.1,       
        "soil_type_encoded": soilScore,
        "rain_intensity": rainIntensity,
        "rain_persistence": rainPersistence,
        "saturation_index": saturationIndex,
        "drainage_score": drainageScore,
        "heat_humidity": heatHumidity,
        "city_risk": cityRisk,
    }

    df = pd.DataFrame([features])
    scaled = scaler.transform(df)
    rawInt = model.predict(scaled)[0]
    raw = encoder.inverse_transform([rawInt])[0]  
    label = risk.get(raw, raw)

    cache[tup] = label
    return label

def label_to_number(risk):
    match risk:
        case "Safe":
            return 0
        case "Low":
            return 0.15
        case "Medium":
            return 0.4
        case "High":
            return 0.6
