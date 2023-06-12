// 格式化数字，保留三位小数
export function formatNumber(num: number, precision = 3) {
  return Number(num.toFixed(precision));
}