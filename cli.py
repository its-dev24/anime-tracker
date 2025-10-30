#!/usr/bin/env python3
"""
Command-line interface for the Anime Tracker
"""

import sys
from anime_tracker import AnimeTracker

def print_help():
    """Print help information"""
    help_text = """
Anime Tracker - Track your anime watchlist

Commands:
  add <title> [total_episodes] [status]    Add a new anime
  list [status]                            List all anime or by status
  update <id> <field> <value>              Update anime (field: status, episodes, rating)
  delete <id>                              Delete an anime
  search <query>                           Search anime by title
  stats                                    Show statistics
  help                                     Show this help message

Status options: "Plan to Watch", "Watching", "Completed", "On Hold", "Dropped"

Examples:
  python cli.py add "Attack on Titan" 25 "Watching"
  python cli.py list
  python cli.py list "Watching"
  python cli.py update 1 episodes 12
  python cli.py update 1 status "Completed"
  python cli.py update 1 rating 9.5
  python cli.py search "attack"
  python cli.py stats
  python cli.py delete 1
"""
    print(help_text)

def format_anime(anime):
    """Format anime for display"""
    rating_str = f"{anime['rating']}/10" if anime['rating'] is not None else "Not rated"
    episodes_str = f"{anime['episodes_watched']}"
    if anime['total_episodes'] > 0:
        episodes_str += f"/{anime['total_episodes']}"
    
    return f"[{anime['id']}] {anime['title']}\n    Status: {anime['status']}\n    Episodes: {episodes_str}\n    Rating: {rating_str}"

def main():
    """Main CLI function"""
    tracker = AnimeTracker()
    
    if len(sys.argv) < 2:
        print_help()
        return
    
    command = sys.argv[1].lower()
    
    try:
        if command == "help":
            print_help()
        
        elif command == "add":
            if len(sys.argv) < 3:
                print("Error: Please provide anime title")
                return
            
            title = sys.argv[2]
            total_episodes = int(sys.argv[3]) if len(sys.argv) > 3 else 0
            status = sys.argv[4] if len(sys.argv) > 4 else "Plan to Watch"
            
            anime = tracker.add_anime(title, total_episodes, status)
            print(f"✓ Added: {anime['title']}")
            print(format_anime(anime))
        
        elif command == "list":
            status_filter = sys.argv[2] if len(sys.argv) > 2 else None
            
            if status_filter:
                anime_list = tracker.get_anime_by_status(status_filter)
                print(f"\n=== {status_filter} ===")
            else:
                anime_list = tracker.get_all_anime()
                print("\n=== All Anime ===")
            
            if not anime_list:
                print("No anime found.")
            else:
                for anime in anime_list:
                    print(format_anime(anime))
                    print()
        
        elif command == "update":
            if len(sys.argv) < 5:
                print("Error: Usage: update <id> <field> <value>")
                return
            
            anime_id = int(sys.argv[2])
            field = sys.argv[3].lower()
            value = sys.argv[4]
            
            if field == "status":
                anime = tracker.update_status(anime_id, value)
                print(f"✓ Updated status to: {value}")
            elif field == "episodes":
                anime = tracker.update_episodes(anime_id, int(value))
                print(f"✓ Updated episodes watched to: {value}")
            elif field == "rating":
                anime = tracker.rate_anime(anime_id, float(value))
                print(f"✓ Updated rating to: {value}/10")
            else:
                print(f"Error: Unknown field '{field}'. Use: status, episodes, or rating")
                return
            
            print(format_anime(anime))
        
        elif command == "delete":
            if len(sys.argv) < 3:
                print("Error: Please provide anime ID")
                return
            
            anime_id = int(sys.argv[2])
            anime = tracker.get_anime_by_id(anime_id)
            if anime:
                tracker.delete_anime(anime_id)
                print(f"✓ Deleted: {anime['title']}")
            else:
                print(f"Error: Anime with ID {anime_id} not found")
        
        elif command == "search":
            if len(sys.argv) < 3:
                print("Error: Please provide search query")
                return
            
            query = sys.argv[2]
            results = tracker.search_anime(query)
            
            print(f"\n=== Search results for '{query}' ===")
            if not results:
                print("No anime found.")
            else:
                for anime in results:
                    print(format_anime(anime))
                    print()
        
        elif command == "stats":
            stats = tracker.get_statistics()
            print("\n=== Watchlist Statistics ===")
            print(f"Total anime: {stats['total']}")
            print(f"Total episodes watched: {stats['total_episodes_watched']}")
            if stats['average_rating']:
                print(f"Average rating: {stats['average_rating']}/10")
            print("\nBy Status:")
            for status, count in stats['by_status'].items():
                if count > 0:
                    print(f"  {status}: {count}")
        
        else:
            print(f"Error: Unknown command '{command}'")
            print_help()
    
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
