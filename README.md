# Anime Tracker

A simple command-line application to track your anime watchlist. Keep track of what you're watching, what you've completed, and what you plan to watch!

## Features

- ✅ Add anime to your watchlist with title, total episodes, and status
- ✅ Track episodes watched and automatically mark as completed
- ✅ Update watch status (Plan to Watch, Watching, Completed, On Hold, Dropped)
- ✅ Rate anime on a 0-10 scale
- ✅ Search your watchlist
- ✅ View statistics about your watchlist
- ✅ Persistent data storage (JSON)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/its-dev24/anime-tracker.git
cd anime-tracker
```

2. Make sure you have Python 3.6+ installed:
```bash
python --version
```

## Usage

### Add an anime
```bash
python cli.py add "Attack on Titan" 25 "Watching"
```

### List all anime
```bash
python cli.py list
```

### List anime by status
```bash
python cli.py list "Watching"
python cli.py list "Completed"
```

### Update episodes watched
```bash
python cli.py update 1 episodes 12
```

### Update status
```bash
python cli.py update 1 status "Completed"
```

### Rate an anime
```bash
python cli.py update 1 rating 9.5
```

### Search for anime
```bash
python cli.py search "attack"
```

### View statistics
```bash
python cli.py stats
```

### Delete an anime
```bash
python cli.py delete 1
```

### Get help
```bash
python cli.py help
```

## Status Options

- **Plan to Watch** - Anime you plan to watch in the future
- **Watching** - Anime you're currently watching
- **Completed** - Anime you've finished watching
- **On Hold** - Anime you've paused
- **Dropped** - Anime you've stopped watching

## Running Tests

Run the test suite to verify everything works correctly:

```bash
python test_anime_tracker.py
```

## Data Storage

All anime data is stored in `anime_data.json` in the same directory. This file is automatically created when you add your first anime.

## Examples

```bash
# Add some anime
python cli.py add "Naruto" 220 "Plan to Watch"
python cli.py add "One Piece" 1000 "Watching"
python cli.py add "Death Note" 37 "Completed"

# Update progress
python cli.py update 2 episodes 50
python cli.py update 3 rating 9.0

# View your list
python cli.py list

# See statistics
python cli.py stats
```

## License

This project is open source and available for personal use.
