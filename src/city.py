"""
For handling cities.

"""


class City:
    """
    An individual city, located by coordinates.

    Attributes:
        x (float): X-coordinate of city.
        y (float): Y-coordinate of city.
        num (int): The city number (identifier).

    """

    def __init__(self, x, y, num):
        self.x = x
        self.y = y
        self.num = num

    def __deepcopy__(self, memodict=None):
        """
        Deep copy a city.

        Returns: New city object.

        """
        return City(self.x, self.y, self.num)

    def dist(self, other):
        """
        Get the distance between self and other cities using euclidean distance formula.

        Args:
            other (City): The other city to which the distance is measured.

        Returns: Distance between cities.

        """
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def __eq__(self, other):
        """
        Check equality based on x and y values, as well as the city number.

        Args:
            other (City): Other City object.

        Returns: True if equal, False if not.

        """
        return self.num == other.num and self.x == other.x and self.y == other.y

    def __hash__(self):
        """
        Hash based on x, y, and city number values.

        Returns: Object hash.

        """
        return hash(self.x) + hash(self.y) + hash(self.num)

    def __str__(self):
        return str(self.num)
