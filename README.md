# Anime Tracker API

A FastAPI-based REST API to track your anime watchlist. Keep track of what you're watching, what you've completed, and what you plan to watch!

## Features

- ✅ RESTful API built with FastAPI
- ✅ Add anime to your watchlist with title, total episodes, and status
- ✅ Track episodes watched and automatically mark as completed
- ✅ Update watch status (Plan to Watch, Watching, Completed, On Hold, Dropped)
- ✅ Rate anime on a 0-10 scale
- ✅ Search your watchlist
- ✅ View statistics about your watchlist
- ✅ Persistent data storage (JSON)
- ✅ CORS enabled for React frontend integration
- ✅ Interactive API documentation (Swagger UI)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/its-dev24/anime-tracker.git
cd anime-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the API

Start the FastAPI server:
```bash
python main.py
```

Or using uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at: `http://localhost:8000`

## API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### Root
- `GET /` - API information and available status options

### Anime Management
- `GET /anime` - Get all anime (optional query param: `status`)
- `GET /anime/{anime_id}` - Get specific anime by ID
- `POST /anime` - Add new anime to watchlist
- `PATCH /anime/{anime_id}` - Update anime information
- `DELETE /anime/{anime_id}` - Delete anime from watchlist

### Search & Statistics
- `GET /anime/search/{query}` - Search anime by title
- `GET /stats` - Get watchlist statistics

## Usage Examples

### Add an anime
```bash
curl -X POST http://localhost:8000/anime \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Attack on Titan",
    "total_episodes": 25,
    "status": "Watching"
  }'
```

### Get all anime
```bash
curl http://localhost:8000/anime
```

### Filter by status
```bash
curl http://localhost:8000/anime?status=Watching
```

### Update episodes watched
```bash
curl -X PATCH http://localhost:8000/anime/1 \
  -H "Content-Type: application/json" \
  -d '{"episodes_watched": 12}'
```

### Update status
```bash
curl -X PATCH http://localhost:8000/anime/1 \
  -H "Content-Type: application/json" \
  -d '{"status": "Completed"}'
```

### Rate an anime
```bash
curl -X PATCH http://localhost:8000/anime/1 \
  -H "Content-Type: application/json" \
  -d '{"rating": 9.5}'
```

### Search for anime
```bash
curl http://localhost:8000/anime/search/attack
```

### View statistics
```bash
curl http://localhost:8000/stats
```

### Delete an anime
```bash
curl -X DELETE http://localhost:8000/anime/1
```

## Status Options

- **Plan to Watch** - Anime you plan to watch in the future
- **Watching** - Anime you're currently watching
- **Completed** - Anime you've finished watching
- **On Hold** - Anime you've paused
- **Dropped** - Anime you've stopped watching

## Response Models

### Anime Object
```json
{
  "id": 1,
  "title": "Attack on Titan",
  "status": "Watching",
  "episodes_watched": 12,
  "total_episodes": 25,
  "rating": 9.5,
  "added_date": "2025-10-30T18:00:00",
  "updated_date": "2025-10-30T18:30:00"
}
```

### Statistics
```json
{
  "total": 10,
  "by_status": {
    "Plan to Watch": 3,
    "Watching": 2,
    "Completed": 4,
    "On Hold": 1,
    "Dropped": 0
  },
  "total_episodes_watched": 250,
  "average_rating": 8.5
}
```

## Frontend Integration

This API is CORS-enabled and ready to integrate with a React frontend. The API accepts and returns JSON data, making it easy to consume from any JavaScript framework.

Example React fetch:
```javascript
// Add anime
const response = await fetch('http://localhost:8000/anime', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    title: 'Naruto',
    total_episodes: 220,
    status: 'Plan to Watch'
  })
});
const anime = await response.json();
```

## Running Tests

Run the core tracker tests:
```bash
python test_anime_tracker.py
```

Run the API tests:
```bash
python test_api.py
```

## Data Storage

All anime data is stored in `anime_data.json` in the same directory. This file is automatically created when you add your first anime.

## Development

The project structure:
- `main.py` - FastAPI application with API endpoints
- `anime_tracker.py` - Core anime tracking logic
- `test_anime_tracker.py` - Unit tests for core functionality
- `test_api.py` - API endpoint tests
- `requirements.txt` - Python dependencies

## License

This project is open source and available for personal use.
