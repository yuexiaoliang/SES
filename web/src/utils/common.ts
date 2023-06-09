export function generateMultipleArray(
  multiple: number,
  max: number = 250,
  min: number = 0
): number[] {
  return Array.from({ length: max }, (_, i) => i + 1).filter(
    (n) => n % multiple === min
  );
}

export function formatPrice(price?: number, unit: string = "亿"): string {
  if (!price) return "-";

  if (!unit) return price.toFixed(2);

  let result = price;

  switch (unit) {
    case "万":
      result = price / 10000;
      break;
    case "千万":
      result = price / 10000000;
      break;
    case "亿":
      result = price / 100000000;
      break;
  }

  return result.toFixed(2);
}
