import collector.collector as collector
from database.index_maintenance import create_index

if __name__ == '__main__':
    # 采集 A 股所有报告期
    # collector.collect_report_dates()
    # 采集 A 股所有公司业绩
    # collector.collect_all_company_performance()
    # 采集 A 股最新状况
    # collector.collect_realtime_stocks()
    # 采集股票所属板块
    # collector.collect_belongs_board('688700')
    # 采集 A 股基本信息
    # collector.collect_stocks(['301337'])
    # 采集 A 股历史 (日线) 数据
    collector.collect_stocks_history()
    # 采集 A 股所有数据
    # collector.all()

    # create_index()