"""
Solve TSP with brute force.

"""
from src.city import City

assignment_cities = [
    City(1, 1, 1),
    City(5, 4, 2),
    City(4, 8, 3),
    City(3, 5, 4),
    City(7, 6, 5),
    City(8, 7, 6),
    City(4, 8, 7),
    City(2, 4, 8),
    City(9, 2, 9)
]


def tsp_recursive(cities_left, foundation):
    """
    Solve recursively.

    Args:
        cities_left (list): Cities left to choose from.
        foundation (list): Tour that is built on.

    Returns:
        Least tour distance.

    """
    if not cities_left:
        # Get distance from first through to last point.
        total = 0
        for i in range(len(foundation) - 1):
            total += foundation[i].dist(foundation[i + 1])
        # Add distance from last back to first directly.
        total += foundation[-1].dist(foundation[0])
        # Absolutely stop when best path found.
        if total == 27.220359980699765:
            print('[', ', '.join((str(city) for city in foundation)), ']')
        return total
    distances = []
    for city in cities_left:
        new_cities_left = cities_left.copy()
        new_cities_left.remove(city)
        new_foundation = foundation.copy()
        new_foundation.append(city)
        dist = tsp_recursive(new_cities_left, new_foundation)
        distances.append(dist)
    return min(distances)


if __name__ == '__main__':
    print(tsp_recursive(assignment_cities, []))
