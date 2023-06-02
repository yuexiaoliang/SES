export function generateMultipleArray(
  multiple: number,
  max: number = 250,
  min: number = 0
): number[] {
  return Array.from({ length: max }, (_, i) => i + 1).filter(
    (n) => n % multiple === min
  );
}
