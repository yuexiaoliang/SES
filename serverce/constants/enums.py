from enum import Enum


class DatabaseConfig(Enum):
    pass


class DatabaseNames(Enum):
    STOCK = "stock"


class DatabaseCollectionNames(Enum):
    STOCKS = "stocks"
    STOCKS_HISTORY = "stocks_history"
    TIMESTAMPS = "timestamps"
    REPORT_DATES = "report_dates"
    ALL_COMPANY_PERFORMANCE = "all_company_performance"
