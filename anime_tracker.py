"""
Anime Tracker - A simple application to track your anime watchlist
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional

class AnimeTracker:
    """Main class for managing anime watchlist"""
    
    STATUS_OPTIONS = ["Plan to Watch", "Watching", "Completed", "On Hold", "Dropped"]
    
    def __init__(self, data_file: str = "anime_data.json"):
        """Initialize the tracker with a data file"""
        self.data_file = data_file
        self.anime_list = self.load_data()
    
    def load_data(self) -> List[Dict]:
        """Load anime data from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                return []
        return []
    
    def save_data(self) -> None:
        """Save anime data to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.anime_list, f, indent=2)
    
    def add_anime(self, title: str, total_episodes: int = 0, status: str = "Plan to Watch") -> Dict:
        """Add a new anime to the watchlist"""
        if status not in self.STATUS_OPTIONS:
            raise ValueError(f"Invalid status. Choose from: {', '.join(self.STATUS_OPTIONS)}")
        
        # Check if anime already exists
        for anime in self.anime_list:
            if anime['title'].lower() == title.lower():
                raise ValueError(f"Anime '{title}' already exists in your watchlist")
        
        anime = {
            'id': len(self.anime_list) + 1,
            'title': title,
            'status': status,
            'episodes_watched': 0,
            'total_episodes': total_episodes,
            'rating': None,
            'added_date': datetime.now().isoformat(),
            'updated_date': datetime.now().isoformat()
        }
        
        self.anime_list.append(anime)
        self.save_data()
        return anime
    
    def update_status(self, anime_id: int, status: str) -> Dict:
        """Update the watch status of an anime"""
        if status not in self.STATUS_OPTIONS:
            raise ValueError(f"Invalid status. Choose from: {', '.join(self.STATUS_OPTIONS)}")
        
        anime = self.get_anime_by_id(anime_id)
        if not anime:
            raise ValueError(f"Anime with ID {anime_id} not found")
        
        anime['status'] = status
        anime['updated_date'] = datetime.now().isoformat()
        self.save_data()
        return anime
    
    def update_episodes(self, anime_id: int, episodes_watched: int) -> Dict:
        """Update the number of episodes watched"""
        anime = self.get_anime_by_id(anime_id)
        if not anime:
            raise ValueError(f"Anime with ID {anime_id} not found")
        
        if episodes_watched < 0:
            raise ValueError("Episodes watched cannot be negative")
        
        if anime['total_episodes'] > 0 and episodes_watched > anime['total_episodes']:
            raise ValueError(f"Episodes watched cannot exceed total episodes ({anime['total_episodes']})")
        
        anime['episodes_watched'] = episodes_watched
        anime['updated_date'] = datetime.now().isoformat()
        
        # Auto-update status if completed
        if anime['total_episodes'] > 0 and episodes_watched == anime['total_episodes']:
            anime['status'] = "Completed"
        
        self.save_data()
        return anime
    
    def rate_anime(self, anime_id: int, rating: float) -> Dict:
        """Rate an anime (0-10 scale)"""
        if not 0 <= rating <= 10:
            raise ValueError("Rating must be between 0 and 10")
        
        anime = self.get_anime_by_id(anime_id)
        if not anime:
            raise ValueError(f"Anime with ID {anime_id} not found")
        
        anime['rating'] = rating
        anime['updated_date'] = datetime.now().isoformat()
        self.save_data()
        return anime
    
    def get_anime_by_id(self, anime_id: int) -> Optional[Dict]:
        """Get anime by ID"""
        for anime in self.anime_list:
            if anime['id'] == anime_id:
                return anime
        return None
    
    def get_all_anime(self) -> List[Dict]:
        """Get all anime in the watchlist"""
        return self.anime_list
    
    def get_anime_by_status(self, status: str) -> List[Dict]:
        """Get all anime with a specific status"""
        if status not in self.STATUS_OPTIONS:
            raise ValueError(f"Invalid status. Choose from: {', '.join(self.STATUS_OPTIONS)}")
        
        return [anime for anime in self.anime_list if anime['status'] == status]
    
    def delete_anime(self, anime_id: int) -> bool:
        """Delete an anime from the watchlist"""
        anime = self.get_anime_by_id(anime_id)
        if not anime:
            raise ValueError(f"Anime with ID {anime_id} not found")
        
        self.anime_list.remove(anime)
        self.save_data()
        return True
    
    def search_anime(self, query: str) -> List[Dict]:
        """Search for anime by title"""
        query = query.lower()
        return [anime for anime in self.anime_list if query in anime['title'].lower()]
    
    def get_statistics(self) -> Dict:
        """Get statistics about the watchlist"""
        stats = {
            'total': len(self.anime_list),
            'by_status': {}
        }
        
        for status in self.STATUS_OPTIONS:
            stats['by_status'][status] = len(self.get_anime_by_status(status))
        
        total_episodes = sum(anime['episodes_watched'] for anime in self.anime_list)
        stats['total_episodes_watched'] = total_episodes
        
        rated_anime = [anime for anime in self.anime_list if anime['rating'] is not None]
        if rated_anime:
            avg_rating = sum(anime['rating'] for anime in rated_anime) / len(rated_anime)
            stats['average_rating'] = round(avg_rating, 2)
        else:
            stats['average_rating'] = None
        
        return stats
