## Download the Folder directly: 
https://drive.google.com/drive/folders/1FEotSk6qxiK7LNduFcjqvhRyzMe5joSa?usp=drive_link

## Folder Structure

<img width="696" height="273" alt="image" src="https://github.com/user-attachments/assets/a97917aa-c2a3-499c-8594-9f255434e022" />


## Getting Started

### Prerequisites
- Python 3.8+ installed
- Packages: `Flask`, `pandas`, `numpy`, `h5py`, `scikit-learn`, `requests`  
  (You can install them with `pip install -r requirements.txt`)

### Steps to Run
1. **Download TEMPO NO₂ Data**
   - Direct File Link: https://drive.google.com/file/d/1Hkzni5iG2M7TA-8ICOdOQ4jnktSY5672/view?usp=drive_link
   - Download the `.nc` file from [NASA Earthdata](https://search.earthdata.nasa.gov/search/granules?p=C2930763263-LARC_CLOUD&pg[0][v]=f&pg[0][gsk]=-start_date&tl=1725287065.877!4!!) or use Direct File Link.

3. **Get OpenWeather API Key**  
   - Sign up at [OpenWeatherMap](https://openweathermap.org/api) to get a free API key.

4. **Run the App**
   - Open a terminal and navigate to the project folder.
   - Run:  
     ```bash
     pip install flask pandas numpy scikit-learn h5py requests os
     ```
   - Then Run the Python script:  
     ```bash
     python app.py
     ```
   - You will be prompted to **enter the path to your TEMPO `.nc` file** and **your OpenWeather API key**. The app will load the data and start the Flask server.

5. **Open the Frontend**
   - Open a browser and go to: [http://127.0.0.1:5000](http://127.0.0.1:5000)
   - Explore the interactive map, risk-level filters, and metrics.

### Notes
- Make sure your `.nc` file path is correct.
- The API key is required to fetch live weather data; without it, the app will skip weather features.
