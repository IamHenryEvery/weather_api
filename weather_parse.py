from bs4 import BeautifulSoup as bs
import requests as req
from loguru import logger
import json
import arrow


def main():
    url = "https://weather.rambler.ru/"
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/96.0.4664.51 Safari/537.36"
    }
    city_names = []
    hrefs = []
    weather = []
    counter = 0
    now = arrow.now()
    logger.add("logs.log")
    html = bs(req.get(url + "world/rossiya/", headers=headers).text, "lxml")
    regions = html.find_all(class_="AyDi")
    for region in regions:
        reg_link = region.find("a", class_="kgSF")["href"]
        reg_name = region.find("a", class_="kgSF").find("span").text
        reg_html = bs(req.get(url + reg_link, headers=headers).text, "lxml")
        cities = reg_html.find_all(class_="K5tk")
        for city in cities:
            city_link = city.find("a", class_="MJZ5")["href"]
            city_name = city.find("a", class_="MJZ5").find("span").text
            city_names.append(city_name)
            hrefs.append(city_link)
            weather_html = bs(req.get(url + city_link, headers=headers).text, "lxml")
            cur_temp = weather_html.find(class_="HhSR MBvM").text
            cur_temp = cur_temp[: cur_temp.find("°")]
            weather.append(
                {
                    "city": city_name,
                    "temperature": cur_temp,
                    "date": now.format("DD.MM.YYYY"),
                }
            )
            week_temp = weather_html.find_all(class_="AY6t")
            for i, el in enumerate(week_temp, 1):
                new_temp = el.text[: el.text.find("°")]
                weather.append(
                    {
                        "city": city_name,
                        "temperature": new_temp,
                        "date": now.shift(days=i).format("DD.MM.YYYY"),
                    }
                )
            counter += 1
            if counter == 1000:
                break
        logger.info(f"Регион '{reg_name}' спаршен")
        if counter == 1000:
            break

    with open("cities.json", "w", encoding="utf-8") as f:
        json.dump(city_names, f, ensure_ascii=False, indent=4)

    with open("weather_data.json", "w", encoding="utf-8") as f:
        json.dump(weather, f, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    main()
