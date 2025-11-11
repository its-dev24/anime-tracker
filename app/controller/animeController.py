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
