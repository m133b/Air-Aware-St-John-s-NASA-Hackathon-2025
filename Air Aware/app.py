
from flask import Flask, jsonify, send_from_directory, request
import h5py
import pandas as pd
import numpy as np
import requests
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import os

app = Flask(__name__, static_folder="static")

# -------------------------
# 1️⃣ Ask user for inputs
file_path = input("Enter path to your TEMPO .nc file: ").strip().strip('"')
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File not found: {file_path}")

API_KEY = input("Enter your OpenWeather API key: ").strip()
if not API_KEY:
    raise ValueError("You must provide a valid OpenWeather API key!")

# -------------------------
# 2️⃣ Load Satellite Data
try:
    with h5py.File(file_path, 'r') as f:
        no2 = f['product']['vertical_column_troposphere'][:]
        lat = f['latitude'][:]
        lon = f['longitude'][:]
except Exception as e:
    raise RuntimeError(f"Error reading satellite data: {e}")

lat_grid, lon_grid = np.meshgrid(lat, lon, indexing='ij')
df = pd.DataFrame({
    'latitude': lat_grid.ravel(),
    'longitude': lon_grid.ravel(),
    'NO2': no2[0].ravel()
})

df['NO2'] = df['NO2'].replace(-1e30, np.nan)
df = df.dropna().reset_index(drop=True)
df['timestamp'] = pd.to_datetime("2025-09-16 11:43:11")

# -------------------------
# 3️⃣ Weather Data
lat0, lon0 = 47.5615, -52.7126
url = f"http://api.openweathermap.org/data/2.5/forecast?lat={lat0}&lon={lon0}&appid={API_KEY}&units=metric"

try:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    weather_data = response.json()
    weather_df = pd.json_normalize(weather_data['list'])
    weather_df['timestamp'] = pd.to_datetime(weather_df['dt_txt'])
    weather_df = weather_df[['timestamp', 'main.temp', 'main.humidity', 'wind.speed', 'wind.deg']]
except Exception as e:
    print(f"[WARNING] Could not fetch weather data: {e}")
    weather_df = pd.DataFrame(columns=['timestamp','main.temp','main.humidity','wind.speed','wind.deg'])

# -------------------------
# 4️⃣ Merge and clean
merged_df = pd.merge_asof(
    df.sort_values('timestamp'),
    weather_df.sort_values('timestamp'),
    on='timestamp',
    direction='nearest'
)
merged_df['NO2_prev'] = merged_df['NO2'].shift(1).fillna(merged_df['NO2'].mean())
feature_cols = ['main.temp', 'main.humidity', 'wind.speed', 'wind.deg', 'NO2_prev']

# -------------------------
# 5️⃣ Train model
if len(merged_df) < 2:
    raise RuntimeError("Not enough data to train the model.")

sample_df = merged_df.sample(n=min(5000,len(merged_df)), random_state=42).reset_index(drop=True)
X = sample_df[feature_cols].fillna(0)
y = sample_df['NO2'].fillna(0)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
rf = RandomForestRegressor(n_estimators=50, max_depth=12, random_state=42, n_jobs=-1)
rf.fit(X_train, y_train)

y_pred = rf.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, y_pred))

# -------------------------
# 6️⃣ Filter for St. Johns only
lat_min, lat_max = 47.45, 47.75
lon_min, lon_max = -52.90, -52.60

stjohns_df = merged_df[
    (merged_df['latitude'] >= lat_min) & (merged_df['latitude'] <= lat_max) &
    (merged_df['longitude'] >= lon_min) & (merged_df['longitude'] <= lon_max)
].reset_index(drop=True)

stjohns_df['predicted_NO2'] = rf.predict(stjohns_df[feature_cols].fillna(0))
stjohns_df['predicted_risk'] = pd.cut(
    stjohns_df['predicted_NO2'],
    bins=[0, 3e15, 6e15, 1e16, 2e16],
    labels=['Low','Moderate','High','Very High']
)

# -------------------------
# 7️⃣ API endpoints
@app.route("/api/metrics")
def get_metrics():
    return jsonify({
        "points": f"{len(stjohns_df):,}",
        "rmse": f"{rmse:.2e}",
        "factors": len(feature_cols),
        "period": "Sept 16-17, 2025"
    })

@app.route("/api/predictions")
def get_predictions():
    risk_level = request.args.get("risk", "all")
    
    if risk_level == "all":
        filtered = stjohns_df
    else:
        filtered = stjohns_df[stjohns_df['predicted_risk'] == risk_level]
    
    data = []
    for _, row in filtered.iterrows():
        data.append({
            "latitude": float(row['latitude']),
            "longitude": float(row['longitude']),
            "predicted_NO2": float(row['predicted_NO2']),
            "predicted_risk": str(row['predicted_risk'])
        })
    return jsonify(data)

# -------------------------
# Serve frontend
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(app.static_folder, path)

# -------------------------
if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)




