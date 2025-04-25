from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from bestconfig import Config
from loguru import logger
from app import models
import sqlite3
import json
import sys


def db_upload(fill=False):
    config = Config("config.ini", exclude_default=True)
    logger.add("logs.log")
    connect = sqlite3.connect(f"{config['Database']['dbname']}")
    if fill:
        engine = create_engine(f"sqlite:///{config['Database']['dbname']}")
        Base = declarative_base()
        try:
            with open("weather_data.json", encoding="utf-8") as f:
                weather_data = json.load(f)
            with open("cities.json", encoding="utf-8") as f:
                cities = json.load(f)
            logger.info("Данные прочитаны")
        except Exception as e:
            logger.error(f"При чтении данных возникла ошибка: {e}")
            sys.exit(1)
        # Создаем таблицы в базе данных
        try:
            Base.metadata.create_all(engine)
            logger.info("Таблицы созданы")
        except Exception as e:
            logger.error(f"При создании таблиц возникла ошибка: {e}")
            sys.exit(1)
        # Создаем сессию
        Session = sessionmaker(bind=engine)
        session = Session()
        # Заполняем таблицу City
        try:
            for el in cities:
                city = models.City(name=el)
                session.add(city)
        except Exception as e:
            logger.error(f"Ошибка при заполнении таблицы 'city': {e}")
            session.rollback()
            sys.exit(1)
        # Заполняем таблицу Check
        try:
            for res in weather_data:
                city_id = (
                    session.query(models.City.id).filter_by(name=res["city"]).first()
                )[0]
                check = models.Check(
                    city_id=city_id, date=res['date']
                )
                session.add(check)
        except Exception as e:
            logger.error(f"Ошибка при заполнении таблицы 'check': {e}")
            session.rollback()
            sys.exit(1)
        # Заполняем таблицу Weather
        try:
            for ind, res in enumerate(weather_data, start=1):
                weather = models.Weather(
                    check_id=ind, date=res['date'],
                    temperature=res["temperature"]
                )
                session.add(weather)
        except Exception as e:
            logger.error(f"Ошибка при заполнении таблицы 'weather':{e}")
            session.rollback()
            sys.exit(1)
        # Применяем изменения в базе данных
        try:
            session.commit()
            logger.info("Изменения зафиксированы")
        except Exception as e:
            logger.error(f"Ошибка при применении изменений:{e}")
            session.rollback()
            sys.exit(1)
        session.close()
    connect.close()


db_upload(True)
