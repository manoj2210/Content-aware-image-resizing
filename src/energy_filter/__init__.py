__all__ = ['energy_function']


def energy_function(x0: int, x1: int, y0: int, y1: int) -> float:
    return sum(pow((x0 - x1), 2) + pow((y0 - y1), 2))
