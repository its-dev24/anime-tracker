"""
Tests for the Anime Tracker
"""

import unittest
import os
import json
from anime_tracker import AnimeTracker

class TestAnimeTracker(unittest.TestCase):
    """Test cases for AnimeTracker class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.test_file = "test_anime_data.json"
        self.tracker = AnimeTracker(self.test_file)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_add_anime(self):
        """Test adding an anime"""
        anime = self.tracker.add_anime("Naruto", 220, "Plan to Watch")
        self.assertEqual(anime['title'], "Naruto")
        self.assertEqual(anime['total_episodes'], 220)
        self.assertEqual(anime['status'], "Plan to Watch")
        self.assertEqual(anime['episodes_watched'], 0)
        self.assertIsNone(anime['rating'])
    
    def test_add_duplicate_anime(self):
        """Test that adding duplicate anime raises error"""
        self.tracker.add_anime("One Piece", 1000)
        with self.assertRaises(ValueError):
            self.tracker.add_anime("One Piece", 1000)
    
    def test_add_anime_invalid_status(self):
        """Test adding anime with invalid status"""
        with self.assertRaises(ValueError):
            self.tracker.add_anime("Test", 12, "InvalidStatus")
    
    def test_update_status(self):
        """Test updating anime status"""
        anime = self.tracker.add_anime("Bleach", 366)
        updated = self.tracker.update_status(anime['id'], "Watching")
        self.assertEqual(updated['status'], "Watching")
    
    def test_update_status_invalid(self):
        """Test updating to invalid status"""
        anime = self.tracker.add_anime("Test", 12)
        with self.assertRaises(ValueError):
            self.tracker.update_status(anime['id'], "InvalidStatus")
    
    def test_update_episodes(self):
        """Test updating episodes watched"""
        anime = self.tracker.add_anime("Death Note", 37)
        updated = self.tracker.update_episodes(anime['id'], 10)
        self.assertEqual(updated['episodes_watched'], 10)
    
    def test_update_episodes_auto_complete(self):
        """Test that updating to total episodes auto-completes"""
        anime = self.tracker.add_anime("Cowboy Bebop", 26)
        updated = self.tracker.update_episodes(anime['id'], 26)
        self.assertEqual(updated['episodes_watched'], 26)
        self.assertEqual(updated['status'], "Completed")
    
    def test_update_episodes_exceed_total(self):
        """Test that episodes cannot exceed total"""
        anime = self.tracker.add_anime("Test", 12)
        with self.assertRaises(ValueError):
            self.tracker.update_episodes(anime['id'], 15)
    
    def test_update_episodes_negative(self):
        """Test that episodes cannot be negative"""
        anime = self.tracker.add_anime("Test", 12)
        with self.assertRaises(ValueError):
            self.tracker.update_episodes(anime['id'], -1)
    
    def test_rate_anime(self):
        """Test rating an anime"""
        anime = self.tracker.add_anime("Steins;Gate", 24)
        updated = self.tracker.rate_anime(anime['id'], 9.5)
        self.assertEqual(updated['rating'], 9.5)
    
    def test_rate_anime_invalid_range(self):
        """Test that rating must be in valid range"""
        anime = self.tracker.add_anime("Test", 12)
        with self.assertRaises(ValueError):
            self.tracker.rate_anime(anime['id'], 11)
        with self.assertRaises(ValueError):
            self.tracker.rate_anime(anime['id'], -1)
    
    def test_get_anime_by_id(self):
        """Test getting anime by ID"""
        anime = self.tracker.add_anime("Fullmetal Alchemist", 64)
        found = self.tracker.get_anime_by_id(anime['id'])
        self.assertEqual(found['title'], "Fullmetal Alchemist")
    
    def test_get_anime_by_id_not_found(self):
        """Test getting non-existent anime"""
        result = self.tracker.get_anime_by_id(999)
        self.assertIsNone(result)
    
    def test_get_all_anime(self):
        """Test getting all anime"""
        self.tracker.add_anime("Anime 1", 12)
        self.tracker.add_anime("Anime 2", 24)
        self.tracker.add_anime("Anime 3", 13)
        all_anime = self.tracker.get_all_anime()
        self.assertEqual(len(all_anime), 3)
    
    def test_get_anime_by_status(self):
        """Test filtering anime by status"""
        self.tracker.add_anime("Anime 1", 12, "Watching")
        self.tracker.add_anime("Anime 2", 24, "Watching")
        self.tracker.add_anime("Anime 3", 13, "Completed")
        
        watching = self.tracker.get_anime_by_status("Watching")
        self.assertEqual(len(watching), 2)
        
        completed = self.tracker.get_anime_by_status("Completed")
        self.assertEqual(len(completed), 1)
    
    def test_delete_anime(self):
        """Test deleting an anime"""
        anime = self.tracker.add_anime("To Delete", 12)
        self.assertEqual(len(self.tracker.get_all_anime()), 1)
        
        self.tracker.delete_anime(anime['id'])
        self.assertEqual(len(self.tracker.get_all_anime()), 0)
    
    def test_delete_nonexistent_anime(self):
        """Test deleting non-existent anime"""
        with self.assertRaises(ValueError):
            self.tracker.delete_anime(999)
    
    def test_search_anime(self):
        """Test searching for anime"""
        self.tracker.add_anime("Attack on Titan", 25)
        self.tracker.add_anime("My Hero Academia", 13)
        self.tracker.add_anime("Attack on Titan Season 2", 12)
        
        results = self.tracker.search_anime("attack")
        self.assertEqual(len(results), 2)
        
        results = self.tracker.search_anime("hero")
        self.assertEqual(len(results), 1)
    
    def test_get_statistics(self):
        """Test getting statistics"""
        anime1 = self.tracker.add_anime("Anime 1", 12, "Watching")
        anime2 = self.tracker.add_anime("Anime 2", 24, "Completed")
        self.tracker.update_episodes(anime1['id'], 5)
        self.tracker.update_episodes(anime2['id'], 24)
        self.tracker.rate_anime(anime2['id'], 8.5)
        
        stats = self.tracker.get_statistics()
        self.assertEqual(stats['total'], 2)
        self.assertEqual(stats['total_episodes_watched'], 29)
        self.assertEqual(stats['average_rating'], 8.5)
        self.assertEqual(stats['by_status']['Watching'], 1)
        self.assertEqual(stats['by_status']['Completed'], 1)
    
    def test_data_persistence(self):
        """Test that data is saved and loaded correctly"""
        self.tracker.add_anime("Test Anime", 12)
        
        # Create new tracker instance with same file
        new_tracker = AnimeTracker(self.test_file)
        all_anime = new_tracker.get_all_anime()
        
        self.assertEqual(len(all_anime), 1)
        self.assertEqual(all_anime[0]['title'], "Test Anime")
    
    def test_id_generation_after_deletion(self):
        """Test that IDs are unique even after deletions"""
        anime1 = self.tracker.add_anime("Anime 1", 12)
        anime2 = self.tracker.add_anime("Anime 2", 24)
        self.tracker.delete_anime(anime1['id'])
        anime3 = self.tracker.add_anime("Anime 3", 13)
        
        # Anime 3 should have a unique ID, not reuse ID 1
        self.assertNotEqual(anime3['id'], anime1['id'])
        self.assertGreater(anime3['id'], anime2['id'])

if __name__ == '__main__':
    unittest.main()
