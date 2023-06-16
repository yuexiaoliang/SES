# SES - ShortEdgeSystem

## 后端

卖出当天的价格计算方式为：上一天收盘价 + 上一天收盘价 * 止损比率 + 阈值


两种模拟交易：

1. 单只模拟，对单只股票进行模拟操作
2. 真实模拟，指完全根据持仓以及可用金额对所有股票进行模拟，依赖单只模拟进行选股、
   - 每次买入对所有股票进行近期单只模拟，然后选择排名靠前的进行买入。

## 前端

总体交易模拟图表：

1. 柱状图来表示每月盈利
2. 饼图表示以年或 n 年为单位的收益比例
3. 矩形树图表示各股票的收益
4. 有个收益排名版块
