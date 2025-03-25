# encoding:utf-8
import requests
from bs4 import BeautifulSoup
import datetime
import time
import os
from utils.JsonUtils import read_json
from utils.SySQL import SQLManager


# 获取前N个月
def getTheMonth(n):
    date = datetime.datetime.today()
    month = date.month
    year = date.year
    for i in range(n):
        if month == 1:
            year -= 1
            month = 12
        else:
            month -= 1
    return datetime.date(year, month, 1).strftime('%Y%m')


def weather_history(month_num=12):
    sqlManager = SQLManager()
    current_path = os.path.dirname(__file__)
    citys = read_json(current_path + "/city_pinyin.json")
    for city, pinyin in citys.items():
        print("[INFO ]" + city + "历史气象数据爬虫启动，时间【最近" + str(month_num) + "月】")
        urls = ["http://lishi.tianqi.com/" + pinyin + "/" + getTheMonth(i) + ".html" for i in range(month_num)]
        count = 0
        headers = {
            'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'Connection': 'keep-alive',
            'Cookie': '',
            'Host': 'lishi.tianqi.com',
            'Referer': 'http://www.weather.com.cn/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36 Edg/99.0.1150.46'}
        for url in urls:
            response = requests.get(url, headers=headers)
            time.sleep(3)
            soup = BeautifulSoup(response.text, 'html.parser')
            weather_list = soup.find("ul", class_="thrui")
            li_list = weather_list.select('li')
            for li in li_list:
                divs = li.select('div')
                select_sql = "select count(id) as `i` from historyweather where cityname='" + city + "' and record_date='" + \
                             divs[
                                 0].get_text().split()[0] + "'"
                insert_history_sql = "insert into historyweather values(NULL,'上海','" + city + "','" + \
                                     divs[
                                         0].get_text().split()[0] + "'," + divs[1].get_text().replace('℃', "") + "," + \
                                     divs[
                                         2].get_text().replace('℃',
                                                               "") + ",'" + \
                                     divs[3].get_text() + "','" + divs[4].get_text().split()[0] + "'," + \
                                     divs[4].get_text().split()[1].replace("级", "") + ",'" + time.strftime(
                    "%Y-%m-%d %H:%M:%S",
                    time.localtime()) + "')"
                if sqlManager.get_one(select_sql)['i'] == 0:
                    sqlManager.moddify(insert_history_sql)
                    count += 1
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        slog_sql = "insert into slog VALUES (NULL, \"【爬虫运行】" + city + "历史气象数据爬虫爬取数据：" + str(
            count) + "条\",\"" + t + "\")"
        sqlManager.moddify(slog_sql)

        print("[INFO ]" + city + "历史气象数据爬虫完成，时间【最近" + str(month_num) + "月】")
    time.sleep(60)
    sqlManager.close()


if __name__ == '__main__':
    weather_history(36)
