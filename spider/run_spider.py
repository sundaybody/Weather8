import time

from spider.china_weather_spider import weather_china
from spider.city_weather_spider import weather_city
from spider.history_weather_spider import weather_history

while(True):
    time.sleep(10)
    weather_china()
    # weather_history()

    # weather_city()
