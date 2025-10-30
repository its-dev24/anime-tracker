# Example Usage of Anime Tracker

This file demonstrates the various features of the Anime Tracker application.

## Getting Started

### 1. Add your first anime
```bash
python cli.py add "Attack on Titan" 25 "Watching"
```

### 2. Add more anime with different statuses
```bash
python cli.py add "Naruto Shippuden" 500 "Plan to Watch"
python cli.py add "Death Note" 37 "Completed"
python cli.py add "One Punch Man" 12 "Watching"
python cli.py add "Steins;Gate" 24 "On Hold"
python cli.py add "Sword Art Online" 25 "Dropped"
```

## Tracking Your Progress

### Update episodes watched
```bash
# You're making progress on Attack on Titan
python cli.py update 1 episodes 15

# Finished One Punch Man (will auto-complete)
python cli.py update 4 episodes 12
```

### Update status manually
```bash
# Changed your mind about watching Sword Art Online
python cli.py update 6 status "Plan to Watch"

# Ready to continue Steins;Gate
python cli.py update 5 status "Watching"
```

### Rate anime you've completed
```bash
python cli.py update 3 rating 9.5  # Death Note
python cli.py update 4 rating 8.0  # One Punch Man
```

## Viewing Your Watchlist

### List all anime
```bash
python cli.py list
```

### Filter by status
```bash
# What am I currently watching?
python cli.py list "Watching"

# What's in my backlog?
python cli.py list "Plan to Watch"

# What have I completed?
python cli.py list "Completed"
```

### Search for specific anime
```bash
python cli.py search "attack"
python cli.py search "naruto"
```

### View statistics
```bash
python cli.py stats
```

## Managing Your List

### Delete anime you're no longer interested in
```bash
python cli.py delete 6
```

## Tips and Tricks

1. **Use quotes for multi-word titles**: `python cli.py add "My Hero Academia" 13`
2. **Update multiple fields**: Run update commands sequentially
3. **Track ongoing anime**: Set total episodes to 0 if you don't know the total count
4. **Auto-completion**: When you watch all episodes, the status automatically changes to "Completed"
5. **Ratings**: Use decimals for precise ratings (e.g., 8.5, 9.2)

## Sample Session

```bash
# Start tracking your anime
python cli.py add "Cowboy Bebop" 26 "Plan to Watch"
python cli.py add "Fullmetal Alchemist: Brotherhood" 64 "Watching"

# Start watching
python cli.py update 2 episodes 30

# Completed watching
python cli.py update 2 episodes 64
python cli.py update 2 rating 10

# Check your progress
python cli.py stats
```

## Advanced Usage

### Track seasonal anime (ongoing series)
```bash
# For anime still airing, you can set total episodes to 0
python cli.py add "Current Season Anime" 0 "Watching"
python cli.py update 3 episodes 5  # No validation on total
```

### Organize by status
```bash
# View what you're currently watching
python cli.py list "Watching"

# Plan your next watch
python cli.py list "Plan to Watch"

# Remember what you've completed
python cli.py list "Completed"
```
