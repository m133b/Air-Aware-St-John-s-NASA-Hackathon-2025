## Download the Folder directly: 
https://drive.google.com/drive/folders/1FEotSk6qxiK7LNduFcjqvhRyzMe5joSa?usp=drive_link

## Folder Structure
```bash
Project_Files/
│
├── Nasa_Data/
│   └── nasa_data.nc
│
├── static/ #Front End
│   ├── index.html
│   ├── styles.css
│   └── app.js
│
└── app.py
 ```

## Getting Started

### Prerequisites
- Python 3.8+ installed
- Packages: `Flask`, `pandas`, `numpy`, `h5py`, `scikit-learn`, `requests`  
  

### Steps to Run
1. **Download TEMPO NO₂ Data**
   - Direct File Link: https://drive.google.com/drive/folders/1-aEERqIyn3ayjeRNBzGynn64ZaY6Q6UL?usp=sharing
   - Download the `.nc` file from [NASA Earthdata](https://search.earthdata.nasa.gov/search/granules?p=C2930763263-LARC_CLOUD&pg[0][v]=f&pg[0][gsk]=-start_date&tl=1725287065.877!4!!) or use Direct File Link.

3. **Get OpenWeather API Key**  
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api) to get a free API key.

4. **Run the App**
   - Open a terminal and navigate to the project folder.
   - Run:  
     ```bash
     pip install flask pandas numpy scikit-learn h5py requests 
     ```
   - Then Run the Python script:  
     ```bash
     python app.py
     ```
   - You will be prompted to **enter the path to your TEMPO `.nc` file** and **your OpenWeather API key**. The app will load the data and start the Flask server.

5. **Open the Frontend**
   - Open a browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)
      - Note: This URL works only on your own computer.
   - Explore the interactive map, risk-level filters, and metrics.

### Notes
- Make sure your `.nc` file path is correct.
- The API key is required to fetch live weather data; without it, the app will skip weather features.
