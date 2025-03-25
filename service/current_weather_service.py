from entity.model import CurrentWeather
from utils.JsonUtils import get_class_one, get_class_list
from utils.PageUtils import get_page_start, PageData
from utils.Result import Result
from utils.SySQL import SQLManager

"""
全国区域气象数据相关业务逻辑服务层
"""


# 根据ID查询数据
def select_current_weather_by_city(city):
    sql = "SELECT * FROM CurrentWeather WHERE cityname=%s order by create_time desc limit 1"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, city)
    sqlManager.close()
    return data


# 根据ID查询数据
def select_current_weather_by_id(id):
    sql = "SELECT * FROM CurrentWeather WHERE id=%s"
    sqlManager = SQLManager()
    data = sqlManager.get_one(sql, id)
    current_weather = get_class_one(data, CurrentWeather)
    sqlManager.close()
    return current_weather


def select_current_weather_list(page, limit, where):
    page, limit, where = get_page_start(int(page), int(limit), where)
    params_sql = get_search_params(where)
    data_sql = "SELECT * FROM CurrentWeather WHERE 1=1 " + params_sql + " ORDER BY id DESC LIMIT %s,%s"
    count_sql = "SELECT COUNT(id) as i FROM CurrentWeather WHERE 1=1 " + params_sql
    sqlManager = SQLManager()
    data = sqlManager.get_list(data_sql, (page, limit))  # 获取分页数据
    count = sqlManager.get_one(count_sql)['i']  # 获取数据总数
    current_weather = get_class_list(data, CurrentWeather)
    page_result = PageData(count, current_weather)
    return page_result


# 查询条件处理
def get_search_params(where):
    sql = ''
    if where:
        if where['cityname'] and len(where['cityname']) > 0:
            sql = sql + " AND cityname like '%%" + where['cityname'] + "%%' "
        if where['record_date'] and len(where['record_date']) > 0:
            sql = sql + " AND record_date = '" + where['record_date'] + "' "
    return sql


# 获取气象列表
def get_weather_list():
    sql = "select weather from CurrentWeather group by weather"
    sqlManager = SQLManager()
    weather_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        weather_list.append(i['weather'])
    sqlManager.close()
    return weather_list


# 获取风向列表
def get_wd_list():
    sql = "select wd from CurrentWeather group by wd"
    sqlManager = SQLManager()
    wd_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        wd_list.append(i['wd'])
    sqlManager.close()
    return wd_list


# 获取城市列表
def get_city_list():
    sql = "select cityname from CurrentWeather group by cityname"
    sqlManager = SQLManager()
    city_list = []
    data = sqlManager.get_list(sql)
    for i in data:
        city_list.append(i['cityname'])
    sqlManager.close()
    return city_list


# 插入天气数据
def insert_current_weather(data):
    sqlManager = SQLManager()
    check_sql = "select count(id) as `i` from `CurrentWeather` where cityname=%s and record_date= %s and record_time=%s"
    count = sqlManager.get_one(check_sql, (data['cityname'], data['record_date'], data['record_time']))['i']
    if count > 0:
        return Result(False, "数据重复")
    sql = "INSERT INTO CurrentWeather (province,cityname,record_date,record_time,temp,wd,ws,wse,sd,weather,rain,aqi) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    sqlManager.instert(sql, (
        data['province'], data['cityname'], data['record_date'], data['record_time'], data['temp'], data['wd'],
        data['ws'], data['wse'],
        data['sd'], data['weather'], data['rain'], data['aqi']))
    sqlManager.close()
    return Result(True, "添加成功")


# 修改天气
def edit_current_weather(data):
    sqlManager = SQLManager()
    sql = "update CurrentWeather SET temp=%s,wd=%s,ws=%s,wse=%s,sd=%s,weather=%s,rain=%s,aqi=%s where id=%s"
    sqlManager.moddify(sql, (data['temp'], data['wd'], data['ws'], data['wse'],
                             data['sd'], data['weather'], data['rain'], data['aqi'], data['id']))
    sqlManager.close()
    return Result(True, "修改成功")


#
def del_current_weather(id):
    sqlManager = SQLManager()
    sql = "DELETE FROM CurrentWeather where id=%s"
    sqlManager.moddify(sql, id)
    sqlManager.close()
    return Result(True, "删除成功")


#
def del_current_weather_list(ids):
    sqlManager = SQLManager()
    sql = "DELETE FROM CurrentWeather where id in (" + ids + ")"
    sqlManager.moddify(sql)
    sqlManager.close()
    return Result(True, "删除成功")


def get_current_weather(id):
    sqlManager = SQLManager()
    sql = "select * from `CurrentWeather` where id=%s "
    data = sqlManager.get_one(sql, id)
    sqlManager.close()
    return data
