"""
Weather Dashboard Application
A simple weather dashboard that displays weather data with flying cows theme
"""

from flask import Flask, render_template, jsonify
import os
import requests

app = Flask(__name__)

# Configuration
API_KEY = os.environ.get('OPENWEATHER_API_KEY', '')
PORT = int(os.environ.get('PORT', 5000))

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/weather/<city>')
def get_weather(city):
    """Get weather data for a city"""
    if not API_KEY:
        return jsonify({
            'error': 'API key not configured',
            'message': 'Please set OPENWEATHER_API_KEY environment variable'
        }), 500
    
    try:
        url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return jsonify(response.json())
    except requests.RequestException as e:
        return jsonify({
            'error': 'Failed to fetch weather data',
            'message': str(e)
        }), 500

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'weather-dashboard'}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
