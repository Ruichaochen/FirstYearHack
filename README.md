# London Cultural Map

An interactive web application that displays a map of London showing locations where films, songs, and other cultural elements were created or filmed.

## Tech Stack

- **Frontend:** React + Vite, MapLibre GL JS (OpenStreetMap)
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

# Initialize and seed the database with curated data
python seed_data.py

# Or import from a CSV file
python import_csv.py /path/to/your/data.csv
python import_csv.py /path/to/your/data.csv --clear  # Clear existing data first

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
  "qid": "Q123456",
  "name": "Tower Bridge",
  "description": "Famous London bridge featured in many films...",
  "category": "film",
  "category_label": "Filming Location",
  "latitude": 51.5055,
  "longitude": -0.0873,
  "address": "Tower Bridge Rd, London SE1 2UP",
  "country": "United Kingdom",
  "iso": "GB",
  "fame_rank": 1,
  "fame_tier": "high",
  "image": "https://upload.wikimedia.org/...",
  "wikipedia": "https://en.wikipedia.org/wiki/...",
  "wikidata": "https://www.wikidata.org/wiki/...",
  "top_modelled": "Movie One;Movie Two",
  "top_productions": "Action Film;Drama Film",
  "productions_list": [
    {"id": 1, "name": "Movie One", "production_type": "top_modelled", "source": "csv_top_modelled"},
    {"id": 2, "name": "Movie Two", "production_type": "top_modelled", "source": "csv_top_modelled"}
  ],
  "year": 2017
}
```

### CSV Import
The `backend/import_csv.py` script imports locations from a CSV file with these columns:
```
qid,name,category,category_label,resolution,latitude,longitude,country,iso,
fame_rank,fame_tier,productions,wiki_productions,modelled_for,top_modelled,
set_only,top_productions,description,wikipedia,wikidata,image,image_page,url,
image_by,image_licence,image_licence_url,verified_productions,top_verified
```

Semi-colon separated values in `top_modelled`, `top_productions`, `verified_productions`, and `top_verified` are automatically split into individual `Production` records linked to each location via a many-to-many relationship.

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
