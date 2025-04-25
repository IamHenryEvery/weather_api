from sqlalchemy.orm import Session
from . import models, schemas


def get_cities(db: Session):
    return db.query(models.City).all()


def add_city(db: Session, city: schemas.CityCreate):
    db_city = models.City(name=city)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def add_weather(db: Session, weather: schemas.WeatherCreate):
    db_weather = models.Weather(
        check_id=weather.check_id,
        date=weather.date,
        temperature=weather.temperature,
    )
    db.add(db_weather)
    db.commit()
    db.refresh(db_weather)
    return db_weather


def get_latest_weather_for_today(db: Session, city_id: int):
    latest_weather = (
        db.query(models.Check).filter(models.Check.city_id == city_id).order_by(models.Check.date.desc()).first()
    )
    return latest_weather


def get_weather_for_date(db: Session, target_date: str):
    weather_list = db.query(models.Weather).filter(models.Weather.date == target_date).all()
    return weather_list


def get_weather(db: Session, weather_id: int):
    return db.query(models.Weather).filter(models.Weather.id == weather_id).first()


def update_weather(
    weather_id: int, weather: schemas.WeatherUpdate, db: Session
):
    db_weather = (
        db.query(models.Weather)
        .filter(models.Weather.id == weather_id)
        .first()
    )
    if db_weather:
        update_data = weather.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_weather, key, value)
        db.commit()
        db.refresh(db_weather)
    return db_weather


def delete_weather(db: Session, weather_id: int):
    db_weather = (
        db.query(models.Weather)
        .filter(models.Weather.id == weather_id)
        .first()
    )
    if db_weather:
        db.delete(db_weather)
        db.commit()
    return db_weather
