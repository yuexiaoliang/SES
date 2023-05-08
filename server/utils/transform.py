from constants.constants import COLUMN_MAPPING


def transform_row(data_row, column_mapping=COLUMN_MAPPING):
    """ 将映射字典应用到数据中的一行，并返回转换后的行。 """
    return {column_mapping[k]: v for k, v in data_row.items()}


def transform_data(data, column_mapping=COLUMN_MAPPING):
    """ 将映射字典应用到数据中的每一行，并返回转换后的数据。 """
    return [transform_row(row, column_mapping) for row in data]
