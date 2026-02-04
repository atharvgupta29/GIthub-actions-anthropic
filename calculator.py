from typing import List, Optional


def divide(a: float, b: float) -> float:
    """
    Divide a by b.

    Raises:
        ValueError: if b is zero.
    """
    if b == 0:
        raise ValueError("Division by zero is not allowed.")
    return a / b


def average(numbers: List[float]) -> Optional[float]:
    """
    Compute the average of a list of numbers.

    Returns:
        The average value, or None if the list is empty.
    """
    if not numbers:
        return None
    return sum(numbers) / len(numbers)


def normalize(numbers: List[float]) -> List[float]:
    """
    Normalize a list of numbers to the range [0, 1].

    If all numbers are the same, returns a list of zeros.
    """
    if not numbers:
        return []

    min_val = min(numbers)
    max_val = max(numbers)

    if min_val == max_val:
        return [0.0 for _ in numbers]

    return [(x - min_val) / (max_val - min_val) for x in numbers]


def moving_average(numbers: List[float], window_size: int) -> List[float]:
    """
    Compute the moving average over a sliding window.

    Args:
        numbers: List of numeric values.
        window_size: Size of the moving window (must be > 0 and <= len(numbers)).

    Returns:
        A list of moving averages.

    Raises:
        ValueError: if window_size is invalid.
    """
    if window_size <= 0:
        raise ValueError("window_size must be greater than zero.")

    if window_size > len(numbers):
        raise ValueError("window_size cannot be larger than the list length.")

    result = []
    for i in range(len(numbers) - window_siz_
