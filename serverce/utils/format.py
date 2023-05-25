import datetime
import math
import time
import pandas
from typing import List


def get_current_time():
    """ 获取当前时间的时间戳 """
    return time.time()


def format_timestamp(timestamp, format='%Y%m%d'):
    """ 格式化时间戳 """
    dt_obj = datetime.datetime.fromtimestamp(timestamp)
    return dt_obj.strftime(format)


def clean_data(data: dict) -> dict:
    """ 清洗数据

    1. 将值为"-" 或者 "NaN" 的字段设置为None
    """
    cleaned_data = {}
    for k, v in data.items():
        if v == "-" or pandas.isna(v):
            cleaned_data[k] = None
        else:
            cleaned_data[k] = v
    return cleaned_data


def clean_data_list(data: List[dict]) -> List[dict]:
    """ 清洗数据列表

    1. 将值为"-"的字段设置为None
    """
    return [clean_data(row) for row in data]


def convert_dict_objectid_to_str(data: dict) -> dict:
    """
    将字典中的所有 ObjectId 转换为字符串
    """
    return {**data, 'id': str(data['_id'])} if '_id' in data else data


def convert_list_objectid_to_str(list: List[dict]) -> List[dict]:
    """
    将列表中的所有 ObjectId 转换为字符串
    """
    return [convert_dict_objectid_to_str(data) for data in list]
