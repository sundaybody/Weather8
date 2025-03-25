from entity.model import City
from utils.PageUtils import deal_data
from utils.SySQL import SQLManager
from utils.JsonUtils import get_class_list


# 获取城市列表
def get_city_list():
    sql = "select * from citys"
    sqlManager = SQLManager()
    data = sqlManager.get_list(sql)
    city_list = get_class_list(data, City)
    sqlManager.close()
    return deal_data(city_list)
