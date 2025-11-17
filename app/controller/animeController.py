from sqlalchemy.orm import Session
import app.model as model
import app.schema as schema


async def get_animes(db: Session) -> list[model.Anime]:

    all_posts = db.query(model.Anime).all()
    return all_posts


async def create_anime(new_anime: schema.CreateAnime, db: Session) -> model.Anime:
    anime: model.Anime = model.Anime(user_id=1, **new_anime.model_dump())
    db.add(anime)
    db.commit()
    db.refresh(anime)
    return anime


async def mark_episode_as_completed(anime_id: int, db: Session):
    anime_to_update = db.query(model.Anime).filter(model.Anime.id == anime_id).first()
    if not anime_to_update:
        return None
    anime_to_update.episodes_watched += 1
    db.commit()
    db.refresh(anime_to_update)
    return anime_to_update


# TODO Change Status of Anime
async def update_anime_status(id: int, anime_status: str, db: Session):
    anime_to_update = db.query(model.Anime).filter(model.Anime.id == id).first()
    if not anime_to_update:
        return None
    anime_to_update.status = anime_status
    db.commit()
    db.refresh(anime_to_update)
    return anime_to_update


# TODO Rate Anime
async def rate_an_anime(id: int, rating: float, db: Session):
    pass


# TODO Remove anime
async def remove_anime(id: int, db: Session):
    pass


# TODO Update anime episodes
async def update_anime_details(id: int, updated_anime: schema.UpdateAnime, db: Session):
    pass
