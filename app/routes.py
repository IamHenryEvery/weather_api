from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/predictions/{city_id}", response_model=schemas.WeatherResponse)
def create_weather(weather: schemas.WeatherCreate, db: Session = Depends(get_db)):
    return crud.add_weather(db=db, weather=weather)


@router.get("/city/", response_model=list[schemas.CityResponse])
def read_cities(db: Session = Depends(get_db)):
    city_info = crud.get_cities(db=db)
    return city_info


@router.get("/city/{city_id}", response_model=schemas.CheckResponse)
def read_latest_weather(city_id: int, db: Session = Depends(get_db)):
    weather = crud.get_latest_weather_for_today(db=db, city_id=city_id)
    if weather is None:
        raise HTTPException(status_code=404, detail="Weather not found")
    return weather


@router.get("/weather/{target_date}", response_model=list[schemas.WeatherResponse])
def read_weather_for_date(target_date: str, db: Session = Depends(get_db)):
    weather_list = crud.get_weather_for_date(db, target_date)
    if not weather_list:
        raise HTTPException(
            status_code=404, detail="Weather not found for the given date"
        )
    return weather_list


@router.put("/predictions/{weather_id}",
            response_model=schemas.WeatherResponse)
def update_weather(
    weather_id: int,
    weather: schemas.WeatherUpdate,
    db: Session = Depends(get_db),
):
    return crud.update_weather(db=db, weather_id=weather_id, weather=weather)


@router.delete(
    "/predictions/{weather_id}", response_model=schemas.WeatherResponse)
def delete_weather(weather_id: int, db: Session = Depends(get_db)):
    return crud.delete_weather(db=db, weather_id=weather_id)
