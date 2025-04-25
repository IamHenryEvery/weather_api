from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True


class CheckBase(BaseModel):
    city_id: int
    date: str


class CheckResponse(CheckBase):
    id: int

    class Config:
        from_attributes = True


class WeatherBase(BaseModel):
    check_id: int
    date: str
    temperature: str


class WeatherCreate(WeatherBase):
    pass


class WeatherUpdate(WeatherBase):
    pass


class WeatherResponse(WeatherBase):
    id: int

    class Config:
        from_attributes = True
