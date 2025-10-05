# Air Aware St. John's

**Air Aware St. John's** predicts NO₂ levels using NASA TEMPO satellite data and local weather. It estimates air quality for St. John's at the time of the satellite data, categorizes risk, and provides interactive maps, filling the gap where the city lacks ground monitoring.

## Architecture

1. **Input:** TEMPO satellite NO₂ data (.nc file) + local weather API key.  
2. **Processing:**  
   - Load satellite data  
   - Fetch weather data  
   - Merge datasets and clean  
   - Train Random Forest model  
3. **Prediction:** Estimate NO₂ levels for St. John's and classify risk levels.  
4. **Output:**  
   - **Backend APIs:**  
     - `/api/metrics` → RMSE, data points, weather factors  
     - `/api/predictions` → Predicted NO₂ and risk levels  
   - **Frontend:** Interactive web app showing an interactive map, risk-level filter, and metrics display

## Technology Used

- **Programming Language:** Python  
- **Web Framework:** Flask  
- **Machine Learning:** scikit-learn (Random Forest Regressor)  
- **Data Handling:** pandas, numpy, h5py  
- **APIs:** OpenWeatherMap API for weather data  
- **Frontend:** HTML, CSS, JavaScript, Leaflet.js for interactive maps  
- **Visualization:** Interactive map with risk-level filters  

## Getting Started

Code Excecution: https://github.com/m133b/Air-Aware-St-John-s-NASA-Hackathon-Project-2025/blob/main/TESTING/README.md

