"""
For handling individual chromosomes.

"""
import random

from copy import deepcopy


class Chromosome:
    """
    An individual chromosome, i.e. a possible tour.

    Attributes:
        tour (list): A particular tour.
        _length (int): The tour length (number of cities).

    """

    def __init__(self, *args):
        self.tour = list(args)
        self._length = len(args)

    def __str__(self):
        """
        Format the cities as a list.

        Returns: Formatted list of cities.

        """
        return '[' + ', '.join((str(city) for city in self.tour)) + ']'

    def mutate(self):
        """
        Mutate by swapping two cities with a 1:10000 probability.

        """
        rand_val = random.randint(1, 10000)
        # If val is not a certain value, exit.
        if rand_val != 522:
            return
        # Get two random values.
        city_1 = random.randint(0, self._length - 1)
        city_2 = random.randint(0, self._length - 1)
        # Swap cities.
        self.tour[city_1], self.tour[city_2] = self.tour[city_2], self.tour[city_1]

    def reproduce(self, other):
        """
        Reproduce self and other into two new children using order crossover.

        Args:
            other (Chromosome): The other chromosome in reproduction.

        """
        # Randomly select a start and stop position for crossing over (pick).
        start = random.randint(0, self._length - 1)
        end = random.randint(0, self._length)
        # Exit if indices are same.
        if start == end:
            return
        # Create new base tours for self and other.
        tour_self = deepcopy(self.tour)
        tour_other = deepcopy(other.tour)
        # Check which crossover method should be used.
        if start < end:
            # Cross over to self.
            self.inclusive_crossover(
                start,
                end,
                other.tour,
                tour_self
            )
            # Cross over to other.
            self.inclusive_crossover(
                start,
                end,
                self.tour,
                tour_other
            )
        # Else, do exclusive crossover.
        else:
            # Cross over to self.
            self.exclusive_crossover(
                start,
                end,
                other.tour,
                tour_self
            )
            # Cross over to other.
            self.exclusive_crossover(
                start,
                end,
                self.tour,
                tour_other
            )
        # Update tours.
        self.tour = tour_self
        other.tour = tour_other

    def exclusive_crossover(self, start, end, src_tour, dest_tour):
        """
        Cross over tours when second pick index is less than the first (exclusive).

        Args:
            start (int): Starting index of pick.
            end (int): Ending index of pick (non-inclusive).
            src_tour (list): List from which the tour is being crossed-over.
            dest_tour (list): Destination tour which is being crossed into.

        """
        # Indices for starting in source and destination.
        src_i = start
        dest_i = end
        # Get dict of pick cities.
        pick = {}
        for i in range(0, end):
            pick[dest_tour[i]] = True
        for i in range(start, self._length):
            pick[dest_tour[i]] = True
        # Cross over cities between end and start indices.
        while dest_i < start:
            # If city isn't in pick, bring it over.
            if src_tour[src_i] not in pick:
                dest_tour[dest_i] = src_tour[src_i]
                dest_i += 1
            src_i = (src_i + 1) % self._length

    def inclusive_crossover(self, start, end, src_tour, dest_tour):
        """
        Cross cities from one tour into another where pick is inclusive.

        Args:
            start (int): Starting index of pick.
            end (int): Ending index of pick (non-inclusive).
            src_tour (list): List from which the tour is being crossed-over.
            dest_tour (list): Destination tour which is being crossed into.

        """
        # Indices for starting in source and destination.
        src_i = start
        dest_i = 0
        # Make dict of pick elements.
        pick = {dest_tour[x]: True for x in range(start, end)}
        # Cross-over elements before start.
        while dest_i < start:
            # If city isn't in pick, bring it over.
            if src_tour[src_i] not in pick:
                dest_tour[dest_i] = src_tour[src_i]
                dest_i += 1
            src_i = (src_i + 1) % self._length
        # Cross over elements after end.
        dest_i = end
        while dest_i < self._length:
            # If not in pick, bring over.
            if src_tour[src_i] not in pick:
                dest_tour[dest_i] = src_tour[src_i]
                dest_i += 1
            src_i = (src_i + 1) % self._length


class City:
    """
    An individual city, located by coordinates.

    """

    def __init__(self, x, y, num):
        self.num = num
        self.x = x
        self.y = y

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
