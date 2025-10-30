# API Usage Examples

This file demonstrates the various features of the Anime Tracker API.

## Getting Started

### 1. Start the API server
```bash
python main.py
```

The API will be available at `http://localhost:8000`

### 2. View Interactive Documentation
Open your browser and navigate to:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## cURL Examples

### Add anime to your watchlist
```bash
# Add anime with full details
curl -X POST http://localhost:8000/anime \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Attack on Titan",
    "total_episodes": 75,
    "status": "Watching"
  }'

# Add anime with minimal details (defaults to "Plan to Watch")
curl -X POST http://localhost:8000/anime \
  -H "Content-Type: application/json" \
  -d '{"title": "Naruto Shippuden", "total_episodes": 500}'

# Add completed anime
curl -X POST http://localhost:8000/anime \
  -H "Content-Type: application/json" \
  -d '{"title": "Death Note", "total_episodes": 37, "status": "Completed"}'
```

### View your watchlist
```bash
# Get all anime
curl http://localhost:8000/anime

# Filter by status
curl http://localhost:8000/anime?status=Watching
curl http://localhost:8000/anime?status=Completed
curl "http://localhost:8000/anime?status=Plan%20to%20Watch"

# Get specific anime by ID
curl http://localhost:8000/anime/1
```

### Update your progress
```bash
# Update episodes watched
curl -X PATCH http://localhost:8000/anime/1 \
  -H "Content-Type: application/json" \
  -d '{"episodes_watched": 50}'

# Change status
curl -X PATCH http://localhost:8000/anime/2 \
  -H "Content-Type: application/json" \
  -d '{"status": "Watching"}'

# Rate an anime
curl -X PATCH http://localhost:8000/anime/3 \
  -H "Content-Type: application/json" \
  -d '{"rating": 9.5}'

# Update multiple fields at once
curl -X PATCH http://localhost:8000/anime/1 \
  -H "Content-Type: application/json" \
  -d '{
    "episodes_watched": 75,
    "status": "Completed",
    "rating": 9.0
  }'
```

### Search and Statistics
```bash
# Search for anime
curl http://localhost:8000/anime/search/attack
curl http://localhost:8000/anime/search/naruto

# Get statistics
curl http://localhost:8000/stats
```

### Delete anime
```bash
# Remove anime from watchlist
curl -X DELETE http://localhost:8000/anime/1
```

## JavaScript/React Examples

### Fetch API
```javascript
// Get all anime
async function getAllAnime() {
  const response = await fetch('http://localhost:8000/anime');
  const anime = await response.json();
  console.log(anime);
}

// Add new anime
async function addAnime(title, totalEpisodes, status) {
  const response = await fetch('http://localhost:8000/anime', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title,
      total_episodes: totalEpisodes,
      status
    })
  });
  return await response.json();
}

// Update anime
async function updateAnime(id, updates) {
  const response = await fetch(`http://localhost:8000/anime/${id}`, {
    method: 'PATCH',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(updates)
  });
  return await response.json();
}

// Delete anime
async function deleteAnime(id) {
  await fetch(`http://localhost:8000/anime/${id}`, {
    method: 'DELETE'
  });
}

// Search anime
async function searchAnime(query) {
  const response = await fetch(`http://localhost:8000/anime/search/${query}`);
  return await response.json();
}

// Get statistics
async function getStats() {
  const response = await fetch('http://localhost:8000/stats');
  return await response.json();
}
```

### React Component Example
```javascript
import { useState, useEffect } from 'react';

function AnimeTracker() {
  const [animeList, setAnimeList] = useState([]);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    fetchAnime();
  }, [filter]);

  const fetchAnime = async () => {
    const url = filter 
      ? `http://localhost:8000/anime?status=${filter}`
      : 'http://localhost:8000/anime';
    const response = await fetch(url);
    const data = await response.json();
    setAnimeList(data);
  };

  const addAnime = async (title, episodes) => {
    await fetch('http://localhost:8000/anime', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        title,
        total_episodes: episodes,
        status: 'Plan to Watch'
      })
    });
    fetchAnime();
  };

  const updateEpisodes = async (id, episodes) => {
    await fetch(`http://localhost:8000/anime/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ episodes_watched: episodes })
    });
    fetchAnime();
  };

  return (
    <div>
      <h1>My Anime Watchlist</h1>
      {/* Your component JSX */}
    </div>
  );
}
```

## Python Examples

### Using requests library
```python
import requests

BASE_URL = "http://localhost:8000"

# Add anime
response = requests.post(f"{BASE_URL}/anime", json={
    "title": "One Piece",
    "total_episodes": 1000,
    "status": "Watching"
})
anime = response.json()
print(anime)

# Get all anime
response = requests.get(f"{BASE_URL}/anime")
all_anime = response.json()

# Filter by status
response = requests.get(f"{BASE_URL}/anime", params={"status": "Watching"})
watching = response.json()

# Update anime
anime_id = 1
response = requests.patch(f"{BASE_URL}/anime/{anime_id}", json={
    "episodes_watched": 100,
    "rating": 9.0
})

# Search
response = requests.get(f"{BASE_URL}/anime/search/one")
results = response.json()

# Get statistics
response = requests.get(f"{BASE_URL}/stats")
stats = response.json()
print(f"Total anime: {stats['total']}")
print(f"Episodes watched: {stats['total_episodes_watched']}")

# Delete anime
response = requests.delete(f"{BASE_URL}/anime/1")
```

## Complete Workflow Example

```bash
# Start fresh
python main.py &

# Add some anime
curl -X POST http://localhost:8000/anime -H "Content-Type: application/json" \
  -d '{"title": "Cowboy Bebop", "total_episodes": 26, "status": "Plan to Watch"}'

curl -X POST http://localhost:8000/anime -H "Content-Type: application/json" \
  -d '{"title": "Fullmetal Alchemist: Brotherhood", "total_episodes": 64, "status": "Watching"}'

curl -X POST http://localhost:8000/anime -H "Content-Type: application/json" \
  -d '{"title": "Steins;Gate", "total_episodes": 24, "status": "Watching"}'

# Update progress
curl -X PATCH http://localhost:8000/anime/2 -H "Content-Type: application/json" \
  -d '{"episodes_watched": 30}'

curl -X PATCH http://localhost:8000/anime/3 -H "Content-Type: application/json" \
  -d '{"episodes_watched": 24, "status": "Completed", "rating": 10}'

# View your list
curl http://localhost:8000/anime | python -m json.tool

# Check what you're watching
curl http://localhost:8000/anime?status=Watching | python -m json.tool

# View statistics
curl http://localhost:8000/stats | python -m json.tool

# Search
curl http://localhost:8000/anime/search/full | python -m json.tool
```

## Testing Tips

1. **Use the interactive docs**: Visit http://localhost:8000/docs to test endpoints visually
2. **Format JSON responses**: Pipe curl output through `python -m json.tool` for pretty printing
3. **Save responses**: Use `-o filename.json` with curl to save responses
4. **View headers**: Add `-v` flag to curl for verbose output with headers
5. **Test error cases**: Try invalid IDs, duplicate titles, invalid status values to see error handling

## Status Values

Remember to use these exact strings for status:
- "Plan to Watch"
- "Watching"
- "Completed"
- "On Hold"
- "Dropped"

## API Response Codes

- `200 OK` - Successful GET/PATCH request
- `201 Created` - Successfully created new anime
- `204 No Content` - Successfully deleted anime
- `400 Bad Request` - Invalid input data
- `404 Not Found` - Anime with specified ID not found
- `422 Unprocessable Entity` - Validation error
