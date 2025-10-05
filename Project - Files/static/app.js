const METRICS_API = 'http://127.0.0.1:5000/api/metrics';
const PREDICTIONS_API = 'http://127.0.0.1:5000/api/predictions';

async function loadMetrics() {
  try {
    const res = await fetch(METRICS_API);
    const json = await res.json();
    
    // Set text values directly (no animation)
    if (json.period) document.getElementById('metric-period').textContent = json.period;
    if (json.rmse) document.getElementById('metric-rmse').textContent = json.rmse;
    
    // Animate numeric values
    if (json.points) {
      const pointsValue = parseInt(json.points.replace(/,/g, ''));
      animateValue(document.getElementById('metric-points'), 0, pointsValue, 1000, true);
    }
    if (json.factors) {
      animateValue(document.getElementById('metric-factors'), 0, json.factors, 800, false);
    }
  } catch(err) { 
    console.error('Metrics API error:', err);
  }
}

function animateValue(element, start, end, duration, addCommas = false) {
  const range = end - start;
  const increment = range / (duration / 16);
  let current = start;
  
  const timer = setInterval(() => {
    current += increment;
    if (current >= end) {
      current = end;
      clearInterval(timer);
    }
    const displayValue = Math.floor(current);
    element.textContent = addCommas ? displayValue.toLocaleString() : displayValue;
  }, 16);
}

let map;
function initMap() {
  map = L.map('map').setView([47.6, -52.75], 11);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  loadPredictions();
}

async function loadPredictions(riskLevel='all') {
  try {
    const res = await fetch(`${PREDICTIONS_API}?risk=${riskLevel}`);
    const data = await res.json();

    if (window.predictionLayer) window.predictionLayer.clearLayers();
    window.predictionLayer = L.layerGroup().addTo(map);

    const riskColors = { 
      Low:'#10b981', 
      Moderate:'#f59e0b', 
      High:'#f97316', 
      'Very High':'#ef4444' 
    };

    data.forEach(d => {
      L.circle([d.latitude, d.longitude], {
        radius: 200,
        color: riskColors[d.predicted_risk],
        fillColor: riskColors[d.predicted_risk],
        fillOpacity: 0.7
      }).bindPopup(`Predicted NO₂: ${d.predicted_NO2.toExponential(2)}<br>Risk: ${d.predicted_risk}`)
        .addTo(window.predictionLayer);
    });
  } catch(err) {
    console.error('Predictions API error:', err);
  }
}

document.getElementById('riskSelect').addEventListener('change', e => {
  loadPredictions(e.target.value);
});

document.addEventListener('DOMContentLoaded', () => {
  initMap();
  loadMetrics();
});