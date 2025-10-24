# 🐄 Got Cows Weather Dashboard

We've got weather data! Flying cows dependent on your location.

A fun weather dashboard application that displays real-time weather information with a flying cows theme. Built with Flask and containerized with Docker.

## Features

- Real-time weather data from NOAA, NWS, and OpenWeatherMap API
- Fun flying cows theme
- Fully Dockerized for easy deployment
- Production-ready with Gunicorn
- Health check endpoints
- Responsive design

## Prerequisites

- Docker and Docker Compose installed
- OpenWeatherMap API key (get one free at https://openweathermap.org/api)

## Quick Start with Docker

1. **Clone the repository**
   ```bash
   git clone https://github.com/Cart6278/got-cows-weather-dashboard.git
   cd got-cows-weather-dashboard
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenWeatherMap API key
   ```

3. **Build and run with Docker Compose**
   ```bash
   docker-compose up --build
   ```

4. **Access the application**
   Open your browser and navigate to: `http://localhost:5000`

## Docker Commands

### Build the Docker image
```bash
docker build -t weather-dashboard .
```

### Run the container
```bash
docker run -d -p 5000:5000 --env-file .env --name weather-dashboard weather-dashboard
```

### Stop the container
```bash
docker stop weather-dashboard
```

### View logs
```bash
docker logs -f weather-dashboard
```

### Using Docker Compose
```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up --build -d
```

## Local Development (without Docker)

1. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export OPENWEATHER_API_KEY=your_api_key_here
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

## API Endpoints

- `GET /` - Main dashboard page
- `GET /api/weather/<city>` - Get weather data for a specific city
- `GET /health` - Health check endpoint

## Configuration

Environment variables:
- `OPENWEATHER_API_KEY` - Your OpenWeatherMap API key (required)
- `PORT` - Application port (default: 5000)

## License

MIT License

## Contributing

This is a personal project, please reach out prior to contributing. Forking and building upon it for personal use is 
allowed and encouraged!
