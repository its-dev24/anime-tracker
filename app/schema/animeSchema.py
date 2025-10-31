from pydantic import BaseModel
from typing import Optional


class AnimeBase(BaseModel):
    title: str
    genre: str
    total_episodes: int


class CreateAnime(AnimeBase):
    pass


class UpdateAnime(BaseModel):
    title: Optional[str]
    genre: Optional[str]
    total_episodes: Optional[int]
    episodes_watched: Optional[int]
    status: Optional[str]
    rating: Optional[float]
