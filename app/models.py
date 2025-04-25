from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


# Определяем модель для таблицы City
class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True)
    name = Column(String)


# Определяем модель для таблицы Check
class Check(Base):
    __tablename__ = "check"

    id = Column(Integer, primary_key=True)
    city_id = Column(Integer, ForeignKey('city.id'))
    date = Column(String)


# Определяем модель для таблицы Weather
class Weather(Base):
    __tablename__ = "weather"

    id = Column(Integer, primary_key=True)
    check_id = Column(Integer, ForeignKey('check.id'))
    date = Column(String)
    temperature = Column(String)
