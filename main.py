"""
FastAPI application for the Anime Tracker
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
from anime_tracker import AnimeTracker

app = FastAPI(
    title="Anime Tracker API",
    description="API for tracking your anime watchlist",
    version="1.0.0"
)

# Enable CORS for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize tracker
tracker = AnimeTracker()

# Pydantic models for request/response
class AnimeCreate(BaseModel):
    title: str = Field(..., min_length=1, description="Title of the anime")
    total_episodes: int = Field(default=0, ge=0, description="Total number of episodes")
    status: str = Field(default="Plan to Watch", description="Watch status")

class AnimeUpdate(BaseModel):
    status: Optional[str] = Field(None, description="Watch status")
    episodes_watched: Optional[int] = Field(None, ge=0, description="Number of episodes watched")
    rating: Optional[float] = Field(None, ge=0, le=10, description="Rating (0-10)")

class AnimeResponse(BaseModel):
    id: int
    title: str
    status: str
    episodes_watched: int
    total_episodes: int
    rating: Optional[float]
    added_date: str
    updated_date: str

class ErrorResponse(BaseModel):
    detail: str

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Anime Tracker API",
        "version": "1.0.0",
        "docs": "/docs",
        "status_options": tracker.STATUS_OPTIONS
    }

@app.get("/anime", response_model=List[AnimeResponse], tags=["Anime"])
async def get_all_anime(status: Optional[str] = None):
    """
    Get all anime or filter by status
    
    - **status**: Optional filter by watch status
    """
    if status:
        if status not in tracker.STATUS_OPTIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status. Choose from: {', '.join(tracker.STATUS_OPTIONS)}"
            )
        return tracker.get_anime_by_status(status)
    return tracker.get_all_anime()

@app.get("/anime/{anime_id}", response_model=AnimeResponse, tags=["Anime"])
async def get_anime(anime_id: int):
    """
    Get a specific anime by ID
    
    - **anime_id**: ID of the anime to retrieve
    """
    anime = tracker.get_anime_by_id(anime_id)
    if not anime:
        raise HTTPException(status_code=404, detail=f"Anime with ID {anime_id} not found")
    return anime

@app.post("/anime", response_model=AnimeResponse, status_code=201, tags=["Anime"])
async def create_anime(anime: AnimeCreate):
    """
    Add a new anime to the watchlist
    
    - **title**: Title of the anime
    - **total_episodes**: Total number of episodes (default: 0)
    - **status**: Watch status (default: "Plan to Watch")
    """
    try:
        result = tracker.add_anime(anime.title, anime.total_episodes, anime.status)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.patch("/anime/{anime_id}", response_model=AnimeResponse, tags=["Anime"])
async def update_anime(anime_id: int, update: AnimeUpdate):
    """
    Update an anime's information
    
    - **anime_id**: ID of the anime to update
    - **status**: New watch status (optional)
    - **episodes_watched**: Number of episodes watched (optional)
    - **rating**: Rating from 0-10 (optional)
    """
    try:
        anime = tracker.get_anime_by_id(anime_id)
        if not anime:
            raise HTTPException(status_code=404, detail=f"Anime with ID {anime_id} not found")
        
        # Update fields that are provided
        if update.status is not None:
            anime = tracker.update_status(anime_id, update.status)
        
        if update.episodes_watched is not None:
            anime = tracker.update_episodes(anime_id, update.episodes_watched)
        
        if update.rating is not None:
            anime = tracker.rate_anime(anime_id, update.rating)
        
        return tracker.get_anime_by_id(anime_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/anime/{anime_id}", status_code=204, tags=["Anime"])
async def delete_anime(anime_id: int):
    """
    Delete an anime from the watchlist
    
    - **anime_id**: ID of the anime to delete
    """
    try:
        tracker.delete_anime(anime_id)
        return None
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@app.get("/anime/search/{query}", response_model=List[AnimeResponse], tags=["Anime"])
async def search_anime(query: str):
    """
    Search for anime by title
    
    - **query**: Search query string
    """
    return tracker.search_anime(query)

@app.get("/stats", tags=["Statistics"])
async def get_statistics():
    """
    Get watchlist statistics
    
    Returns total anime count, episodes watched, average rating, and breakdown by status
    """
    return tracker.get_statistics()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
