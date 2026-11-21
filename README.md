# London Cultural Map

An interactive web application that displays a map of London showing locations where films, songs, and other cultural elements were created or filmed.

## Tech Stack

- **Frontend:** React + Vite, Leaflet (OpenStreetMap)
- **Backend:** Python + Flask, SQLite
- **Database:** SQLite (via Flask-SQLAlchemy)

## Project Structure

```
FirstYearHack/
├── backend/          # Flask API server
├── frontend/         # React + Vite web app
├── data/             # Curated location data
└── README.md
```

## Setup Instructions

### Prerequisites
- Python 3.10+
- Node.js 18+
- pip and npm

### Backend Setup

```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Initialize and seed the database
python seed_data.py

# Run the server
python app.py
```

The backend API will be available at `http://localhost:5000`.

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/locations` | Get all locations (supports `?category=film` filter) |
| GET | `/api/locations/<id>` | Get a single location by ID |
| GET | `/api/categories` | Get all available categories |

## API Response Format

### Location Object
```json
{
  "id": 1,
  "name": "Tower Bridge",
  "description": "Famous London bridge featured in many films...",
  "category": "film",
  "latitude": 51.5055,
  "longitude": -0.0873,
  "address": "Tower Bridge Rd, London SE1 2UP",
  "media_url": "https://example.com/photo.jpg",
  "year": 2017
}
```

### Categories Response
```json
["film", "music", "literature", "tv", "theatre"]
```

## Categories

- **film** — Movie filming locations
- **music** — Music venues and recording locations
- **literature** — Literary landmarks and book-related locations
- **tv** — TV show filming locations
- **theatre** — Theatre venues and historic locations

## Team Branches

- `backend-api` — Backend + Data work
- `map-core` — Map + Markers work
- `ui-filtering` — UI + Filtering work
