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


# TODO  Mark episodes as watched
async def mark_episode_as_completed(anime_id: int, db: Session):
    anime_to_update = db.query(model.Anime).filter(model.Anime.id == anime_id).first()
    if not anime_to_update:
        return None
    anime_to_update.episodes_watched += 1
    db.commit()
    db.refresh(anime_to_update)
    return anime_to_update


# TODO Change Status of Anime

# TODO Rate Anime

# TODO Remove anime

# TODO Update anime episodes
