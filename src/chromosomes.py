"""
For handling individual chromosomes.

"""

import random
import matplotlib.pyplot as plt

from copy import deepcopy


class Chromosome:
    """
    An individual chromosome, i.e. a possible tour.

    Attributes:
        tour (list): A particular tour.
        _length (int): The tour length (number of cities).
        tour_distance (float): Current tour distance.
        normed_td (float): Current normalized, tour distance.
        inversed_ntd (float): Inversed, normalized, tour distance.
        normed_intd (float): Normed, inverted, normalized, tour distance.
        cumulative_nintd (float): Current cumulative, normalized, inversed, normalized, tour distance.

    """
    # Position variations of label text if there are collisions.
    LABEL_SHIFT = {
        1: (-20, -20),
        2: (20, -20),
        3: (-20, 20),
        4: (20, 20)
    }

    def __init__(self, *args):
        self.tour = list(args)
        self._length = len(args)
        self.tour_distance = 0.0
        self.normed_td = 0.0
        self.inversed_ntd = 0.0
        self.normed_intd = 0.0
        self.cumulative_nintd = 0.0

    def __str__(self):
        """
        Format the cities as a list.

        Returns: Formatted list of cities.

        """
        return '[' + ', '.join((str(city) for city in self.tour)) + ']'

    def __deepcopy__(self, memodict=None):
        """
        Create a new chromosome.

        Returns: A new chromosome.

        """
        # Create a copy of cities.
        new_cities = [deepcopy(city) for city in self.tour]
        return Chromosome(*new_cities)

    def plot(self):
        """
        Plot the tour using MatPlotLib.

        """
        # Set up the plot.
        plt.grid(True)
        plt.title('TSP Tour: {0}'.format(self))
        plt.xlabel('X')
        plt.ylabel('Y')
        city_x = [city.x for city in self.tour]
        city_y = [city.y for city in self.tour]
        # Scatter plot the cities.
        plt.scatter(city_x, city_y)
        # Plot lines connecting points.
        plt.plot(city_x + city_x[:1], city_y + city_y[:1])
        # Label the cities.
        point_cnt = {}
        for i, text in enumerate((city.num for city in self.tour)):
            # If point has already been plotted, shift label placement.
            coords = (city_x[i], city_y[i])
            if coords in point_cnt:
                point_cnt[coords] += 1
                text_loc = Chromosome.LABEL_SHIFT[point_cnt[coords]]
            else:
                point_cnt[coords] = 1
                text_loc = Chromosome.LABEL_SHIFT[1]
            plt.annotate(
                text,
                (city_x[i], city_y[i]),
                xytext=text_loc,
                textcoords='offset points',
                ha='right',
                va='bottom',
                fontsize='small',
                bbox=dict(
                    boxstyle='round,pad=0.2',
                    fc='yellow',
                    alpha=0.5
                ),
                arrowprops=dict(
                    arrowstyle='->',
                    connectionstyle='arc3,rad=0'
                )
            )
        plt.show()

    def shuffle(self):
        """
        Shuffle the cities randomly.

        """
        random.shuffle(self.tour)

    def mutate(self, prob=10000):
        """
        Mutate by swapping two cities with a set probability.

        Args:
            prob (int): Probability of mutating (default 10,000).

        """
        rand_val = random.randint(1, prob)
        # If val is not a certain value, exit.
        if rand_val != 1:
            return
        # Get two random values.
        city_1 = random.randint(0, self._length - 1)
        city_2 = random.randint(0, self._length - 1)
        # Swap cities.
        self.tour[city_1], self.tour[city_2] = self.tour[city_2], self.tour[city_1]
        # DEBUG
        print('Mutation occured')

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
            src_tour (list): List from which the tour is being crossed over.
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
            src_tour (list): List from which the tour is being crossed over.
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

    def get_tour_distance(self):
        """
        Get the tour distance for this chromosome.

        Returns: Tour distance.

        """
        # Get distance from first through to last point.
        total = 0
        for i in range(self._length - 1):
            total += self.tour[i].dist(self.tour[i + 1])
        # Add distance from last back to first.
        total += self.tour[-1].dist(self.tour[0])
        return total
