"""
Tests for the FastAPI Anime Tracker API
"""

import unittest
import os
import json
from fastapi.testclient import TestClient
from main import app, tracker

class TestAnimeTrackerAPI(unittest.TestCase):
    """Test cases for Anime Tracker API"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.client = TestClient(app)
        self.test_file = "test_api_anime_data.json"
        # Reset tracker with test file
        tracker.data_file = self.test_file
        tracker.anime_list = []
        tracker.next_id = 1
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def tearDown(self):
        """Clean up after tests"""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("status_options", data)
    
    def test_create_anime(self):
        """Test creating an anime via API"""
        response = self.client.post(
            "/anime",
            json={"title": "Naruto", "total_episodes": 220, "status": "Plan to Watch"}
        )
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], "Naruto")
        self.assertEqual(data["total_episodes"], 220)
        self.assertEqual(data["status"], "Plan to Watch")
    
    def test_create_anime_duplicate(self):
        """Test creating duplicate anime returns error"""
        self.client.post("/anime", json={"title": "One Piece"})
        response = self.client.post("/anime", json={"title": "One Piece"})
        self.assertEqual(response.status_code, 400)
    
    def test_get_all_anime(self):
        """Test getting all anime"""
        self.client.post("/anime", json={"title": "Anime 1"})
        self.client.post("/anime", json={"title": "Anime 2"})
        
        response = self.client.get("/anime")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
    
    def test_get_anime_by_id(self):
        """Test getting specific anime by ID"""
        create_response = self.client.post("/anime", json={"title": "Bleach"})
        anime_id = create_response.json()["id"]
        
        response = self.client.get(f"/anime/{anime_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Bleach")
    
    def test_get_anime_not_found(self):
        """Test getting non-existent anime"""
        response = self.client.get("/anime/999")
        self.assertEqual(response.status_code, 404)
    
    def test_update_anime_status(self):
        """Test updating anime status"""
        create_response = self.client.post("/anime", json={"title": "Death Note"})
        anime_id = create_response.json()["id"]
        
        response = self.client.patch(
            f"/anime/{anime_id}",
            json={"status": "Watching"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "Watching")
    
    def test_update_anime_episodes(self):
        """Test updating episodes watched"""
        create_response = self.client.post("/anime", json={"title": "Attack on Titan", "total_episodes": 25})
        anime_id = create_response.json()["id"]
        
        response = self.client.patch(
            f"/anime/{anime_id}",
            json={"episodes_watched": 12}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["episodes_watched"], 12)
    
    def test_update_anime_rating(self):
        """Test updating anime rating"""
        create_response = self.client.post("/anime", json={"title": "Steins;Gate"})
        anime_id = create_response.json()["id"]
        
        response = self.client.patch(
            f"/anime/{anime_id}",
            json={"rating": 9.5}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["rating"], 9.5)
    
    def test_update_anime_invalid_rating(self):
        """Test that invalid rating returns error"""
        create_response = self.client.post("/anime", json={"title": "Test"})
        anime_id = create_response.json()["id"]
        
        response = self.client.patch(
            f"/anime/{anime_id}",
            json={"rating": 11}
        )
        self.assertEqual(response.status_code, 422)  # Validation error
    
    def test_delete_anime(self):
        """Test deleting an anime"""
        create_response = self.client.post("/anime", json={"title": "To Delete"})
        anime_id = create_response.json()["id"]
        
        response = self.client.delete(f"/anime/{anime_id}")
        self.assertEqual(response.status_code, 204)
        
        # Verify it's deleted
        get_response = self.client.get(f"/anime/{anime_id}")
        self.assertEqual(get_response.status_code, 404)
    
    def test_search_anime(self):
        """Test searching for anime"""
        self.client.post("/anime", json={"title": "Attack on Titan"})
        self.client.post("/anime", json={"title": "My Hero Academia"})
        self.client.post("/anime", json={"title": "Attack on Titan Season 2"})
        
        response = self.client.get("/anime/search/attack")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
    
    def test_filter_by_status(self):
        """Test filtering anime by status"""
        self.client.post("/anime", json={"title": "Anime 1", "status": "Watching"})
        self.client.post("/anime", json={"title": "Anime 2", "status": "Completed"})
        self.client.post("/anime", json={"title": "Anime 3", "status": "Watching"})
        
        response = self.client.get("/anime?status=Watching")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data), 2)
    
    def test_get_statistics(self):
        """Test getting statistics"""
        create1 = self.client.post("/anime", json={"title": "Anime 1", "total_episodes": 12, "status": "Watching"})
        create2 = self.client.post("/anime", json={"title": "Anime 2", "total_episodes": 24, "status": "Completed"})
        
        id1 = create1.json()["id"]
        id2 = create2.json()["id"]
        
        self.client.patch(f"/anime/{id1}", json={"episodes_watched": 5})
        self.client.patch(f"/anime/{id2}", json={"episodes_watched": 24, "rating": 8.5})
        
        response = self.client.get("/stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["total"], 2)
        self.assertEqual(data["total_episodes_watched"], 29)

if __name__ == '__main__':
    unittest.main()
