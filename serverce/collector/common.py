from utils.format import format_timestamp, get_current_time
from constants.constants import DEFAULT_START_COLLECT_TIME
from .utils import create_client

def update_collected_time(name):
    """ 更新采集时间

    :Parameters:
    - `type` (DatabaseCollectionNames): 采集类型
    """

    [collection, client] = create_client('TIMESTAMPS')

    time = get_current_time()

    try:
        collection.update_one({"name": name}, {"$set": {"collected_timestamp": time, "collected_time": format_timestamp(time, '%Y-%m-%d %H:%M:%S')}}, upsert=True)
    finally:
        client.close()


def get_collected_time(name):
    """ 获取采集时间

    :Parameters:
    - `type` (DatabaseCollectionNames): 采集类型
    """
    [collection, client] = create_client('TIMESTAMPS')

    result = collection.find_one({"name": name})

    try:
        return format_timestamp(result['collected_timestamp'])
    except:
        return DEFAULT_START_COLLECT_TIME
    finally:
        client.close()