from fastapi import APIRouter, HTTPException, status, Depends
from app.controller import get_animes, create_anime, mark_episode_as_completed
from sqlalchemy.orm import Session
from app.database import get_db
from typing import List
from app.schema import AnimeResponse, CreateAnime

animerouter = APIRouter(prefix="/anime", tags=["Anime"])


@animerouter.get("", status_code=status.HTTP_200_OK, response_model=List[AnimeResponse])
async def get_all_anime(db: Session = Depends(get_db)):
    posts = await get_animes(db)
    return posts


@animerouter.post("", status_code=status.HTTP_201_CREATED, response_model=AnimeResponse)
async def create_new_anime(new_anime: CreateAnime, db: Session = Depends(get_db)):
    anime = await create_anime(new_anime, db)
    return anime


@animerouter.put("/{id}", status_code=status.HTTP_200_OK)
async def update_episode(id: int, db: Session = Depends(get_db)):
    anime_updated = await mark_episode_as_completed(id, db)
    return anime_updated
