import json
import requests
import datetime
import os
import time

from utils.JsonUtils import read_json
from utils.SySQL import SQLManager


class GetWeather:
    def __init__(self):
        self.baseUrl = r"http://d1.weather.com.cn/sk_2d/"
        self.headers = {'Accept': "*/*",
                        'Accept-Encoding': 'gzip, deflate',
                        'Accept-Language': 'keep-alive',
                        'Connection': '',
                        'Cookie': 'f_city=上海|101020100|; Hm_lvt_080dabacb001ad3dc8b9b9049b36d43b=1637305568,1637734650,1639644011,1639710627; Hm_lpvt_080dabacb001ad3dc8b9b9049b36d43b=1639723697'.encode(
                            "utf-8").decode("latin1"),
                        'Host': 'd1.weather.com.cn',
                        'Referer': 'http://www.weather.com.cn/',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36', }
        self.cityDict = {}
        current_path = os.path.dirname(__file__)
        self.cityDict = read_json(current_path + "/china.json")
        self.category = read_json(current_path + "/category.json")
    def __getWeatherInfo__(self):
        sqlManager = SQLManager()
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        count = 0
        for city, id in self.cityDict.items():
            try:
                PageUrl = self.baseUrl + id + ".html?_" + str(int(time.time() * 1000))
                response = requests.get(PageUrl, headers=self.headers, allow_redirects=False)
                response.encoding = "utf-8"
                self.htmlResult = response.text
                data = json.loads(self.htmlResult.replace("var dataSK=", ""))
                nameen = data["nameen"]  # 城市拼音
                cityname = city  # 城市名称
                city_sql = "select count(id) as `i` from citys where  city_name='" + cityname + "' and city_py='" + nameen + "'"
                i = sqlManager.get_one(city_sql)['i']
                if i == 0:
                    city_insert_sql = "insert into citys values (NULL,'" + cityname + "','" + nameen + "','" + nameen + "')"
                    sqlManager.moddify(city_insert_sql)
                temp = data["temp"]  # 当前温度
                WD = data["WD"]  # 风向
                WS = data["WS"].replace("级", "")  # 风力
                wse = data["wse"].replace("km/h", "")  # 风速
                sd = data["sd"].replace("%", "")  # 湿度
                weather = data["weather"]  # 天气
                record_date = today  # 时间
                record_time = data["time"]  # 时分
                rain24h = data["rain24h"]  # 降雨量
                aqi = data["aqi"]  # 时分
                print("[INFO ]正在处理数据:", data)
                judge_sql = "select count(id) as `i` from `CurrentWeather` where cityname='" + cityname + "' and record_date='" + record_date + "' and record_time='" + record_time + "'"
                sql = "INSERT INTO `CurrentWeather` VALUES (null, '" + self.category[cityname] + "', '" + cityname + "', '" + record_date + "', '" + record_time + "', " + str(
                    temp) + ", '" + WD + "', " + WS + ", " + wse + ", " + sd + ", '" + weather + "', " + rain24h + "," + aqi + ", '" + time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime()) + "',0);"
                i = sqlManager.get_one(judge_sql)['i']

                if int(i) > 0:
                    continue
                update_sql = "update `CurrentWeather` set is_old = 1  where cityname='" + cityname + "'"  # 更新旧数据
                # delete_sql = "delete from `CurrentWeather` where record_date = '" + record_date + "' and cityname='" + cityname + "'"  # 删除之前一天数据
                count += 1
                sqlManager.moddify(update_sql)
                # sqlManager.moddify(delete_sql)
                sqlManager.moddify(sql)
            except Exception as e:
                continue
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql = "insert into slog VALUES (NULL, \"【爬虫启动】爬取数据全国气象数据运行成功,获取数据：" + str(
            count) + "条\",\"" + t + "\")"
        sqlManager.moddify(sql)
        sqlManager.close()

    def __main__(self):
        print("[INFO ]全国实时气象数据爬虫启动，时间【" + str(datetime.datetime.now()) + "】")
        self.__getWeatherInfo__()
        print("[INFO ]全国实时气象数据爬虫完成，时间【" + str(datetime.datetime.now()) + "】")


# 后台调用爬虫
def weather_china():
    weather = GetWeather()
    weather.__main__()