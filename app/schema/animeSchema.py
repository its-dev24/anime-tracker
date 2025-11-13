from pydantic import BaseModel
from typing import Optional


class AnimeBase(BaseModel):
    title: str
    genre: str
    total_episodes: int


class CreateAnime(AnimeBase):
    pass


class UpdateAnime(BaseModel):
    title: Optional[str] = None
    genre: Optional[str] = None
    total_episodes: Optional[int] = None
    episodes_watched: Optional[int] = None
    status: Optional[str] = None
    rating: Optional[float] = None


class AnimeQUery(BaseModel):
    title: Optional[str] = None
    rating: Optional[float] = None
    genre: Optional[float] = None


class AnimeResponse(BaseModel):
    id: int
    title: str
    genre: str
    total_episodes: int
    episodes_watched: Optional[int] = None
    status: Optional[str] = None
    rating: Optional[float] = None

    class Config:
        from_attributes = True
