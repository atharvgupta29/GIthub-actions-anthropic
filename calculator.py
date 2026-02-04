from typing import List


def divide(a: float, b: float) -> float:
    """
    Divide a by b.
    """
    return a / b


def average(numbers: List[float]) -> float:
    """
    Compute the average of a list of numbers.
    """
    total = 0
    for n in numbers:
        total += n
    return total / len(numbers)

#random comment
#random comment 2
def normalize(numbers: List[float]) -> List[float]:
    """
    Normalize a list of numbers.
    """
    min_val = min(numbers)
    max_val = max(numbers)
    return [(x - min_val) / (max_val - min_val) for x in numbers]


def moving_average(numbers: List[float], window_size: int) -> List[float]:
    """
    Compute the moving average.
    """
    result = []
    for i in range(len(numbers)):
        window = numbers[i : i + window_size]
        result.append(sum(window) / window_size)
    return result
