from fastapi.testclient import TestClient
from loguru import logger
import app

# Специальный клиент, который фактически на запускает сервер.
# Но позволяет его тестировать.
client = TestClient(app.app)

logger.add('logs.log')


# Все по правилам оформления тестов
def test_create_prediction():
    logger.info(" 1) Создание прогнозов:")
    response = client.post(
        "/predictions/{city_id}",
        json={"check_id": 1000000, "date": "31.12.2024", "temperature": "-7"},
    )
    assert response.status_code == 200, f"status_code: {response.status_code}"
    created_weather_id = response.json()["id"]
    print(response.json())
    return created_weather_id


created_weather_id = test_create_prediction()


def test_print_cities():
    logger.info("\n  2) Получить список городов:")
    response = client.get("/city/")
    assert response.status_code == 200, f"status_code: {response.status_code}"
    print(response.json())


def test_read_latest_weather():
    logger.info("\n  3) Получить последний прогноз погоды для города на текущий день:")
    response = client.get(f"/city/{5}")
    assert response.status_code == 200, f"status_code: {response.status_code}"
    print(response.json())


def test_weather_for_date():
    logger.info("\n  4) Получить список всех прогнозов на текущий день(или указанный):")
    response = client.get(
        f"/weather/{'05.06.2024'}",
    )
    assert response.status_code == 200, f"status_code: {response.status_code}"
    print(response.json())


def test_update_weather():
    logger.info("\n  5) Изменить прогноз:")
    response = client.put(
        f"/predictions/{created_weather_id}",
        json={
            "check_id": 1000001,
            "date": "31.12.2024",
            "temperature": "-8"
        },
    )
    assert response.status_code == 200, f"status_code: {response.status_code}"
    print(response.json())


def test_delete_weather():
    logger.info(f"\n  6) Удаление прогноза {created_weather_id}:")
    response = client.delete(f"/predictions/{created_weather_id}")
    assert response.status_code == 200, f"status_code: {response.status_code}"
    print(response.json())
