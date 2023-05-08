import datetime
import time


def get_current_time():
    """ 获取当前时间的时间戳 """
    return time.time()


def format_timestamp(timestamp, format='%Y%m%d'):
    """ 格式化时间戳 """
    dt_obj = datetime.datetime.fromtimestamp(timestamp)
    return dt_obj.strftime(format)
