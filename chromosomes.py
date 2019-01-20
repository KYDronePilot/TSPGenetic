"""
For handling individual chromosomes.

"""
import random
import prettytable
import matplotlib.pyplot as plt

from copy import deepcopy


class Nucleus:
    """
    For containing and managing chromosomes.

    Attributes:
        chromosomes (list): The chromosome population.
        cities (list[City]): Cities to solve for.
        pop_size (int): Size of chromosome population (must be divisible by 4).
        samples (list): The best chromosome distance from each population generated.

    """

    def __init__(self, cities, pop_size):
        self.chromosomes = []
        self.cities = cities
        self.pop_size = pop_size
        self.samples = []
        # Ensure population size is divisible by 4.
        if pop_size % 4 != 0:
            raise ValueError('Population size is not divisible by 4.')
        # Generate a population
        self.generate_population()

    def __str__(self):
        """
        Return a table of statistics of each chromosome.

        Returns: Table of statistics.

        """
        table = prettytable.PrettyTable([
            'Chromosomes',
            'Tour Distance',
            'Normed TD',
            'Inversed NTD',
            'Normed INTD',
            'Cumulative NINTD'
        ])
        for chromosome in self.chromosomes:
            table.add_row([
                str(chromosome),
                chromosome.tour_distance,
                chromosome.normed_td,
                chromosome.inversed_ntd,
                chromosome.normed_intd,
                chromosome.cumulative_nintd,
            ])
        return str(table)

    def plot_learning_curve(self, resolution=100):
        """
        Plot learning curve of how quickly the algorithm finds the best solution.

        Args:
            resolution (int): The number of samples to plot.

        """
        # Get the divisor to limit the number of samples.
        divisor = len(self.samples) // resolution
        if divisor == 0:
            divisor = 1
        # Get the step when collecting samples.
        step = len(self.samples) // divisor
        # Get samples.
        x = list(range(0, len(self.samples) + 1, step))
        y = [(self.samples + [self.chromosomes[0].tour_distance])[i] for i in x]
        # Setup plot.
        plt.grid(True)
        plt.title('TSP Learning Curve: {0}'.format(
            '[' + ', '.join(str(city) for city in self.cities) + ']'
        ))
        plt.xlabel('Samples (every {0} generations)'.format(step))
        plt.ylabel('Lowest Distance')
        plt.plot(x, y)
        plt.show()

    def generate_population(self):
        """
        Generate a population of chromosomes.

        """
        for i in range(self.pop_size):
            # Create new cities and a chromosome for them.
            new_cities = [deepcopy(city) for city in self.cities]
            chromosome = Chromosome(*new_cities)
            # Shuffle the cities and append chromosome.
            chromosome.shuffle()
            self.chromosomes.append(chromosome)

    def reproduce(self):
        """
        Reproduce half the chromosomes.

        """
        # Calculate all the statistics about each chromosome.
        self.calculate_all()
        # Get the best distance from the previous generation and add it to the samples.
        best = self.chromosomes[0].tour_distance
        self.samples.append(best)
        # Reproduce half of the population leaving the parents and removing those not reproduced.
        new_population = []
        for i in range(self.pop_size // 4):
            # Randomly select 2 parents.
            par_1 = self.random_select()
            par_2 = self.random_select()
            # Get copies of the parents (in case parents are selected more than once).
            par_1 = deepcopy(par_1)
            par_2 = deepcopy(par_2)
            # Generate new children-to-be from them.
            cld_1 = deepcopy(par_1)
            cld_2 = deepcopy(par_2)
            # Reproduce parent copies into actual children.
            cld_1.reproduce(cld_2)
            # Add them all into the new population.
            new_population += [par_1, par_2, cld_1, cld_2]
        # Update population.
        self.chromosomes = new_population
        # Give the new population a chance at mutating.
        for chromosome in self.chromosomes:
            chromosome.mutate()

    def reproduce_most_fit(self):
        """
        Variation of reproduction where only the best chromosomes can reproduce.

        """
        # Calculate all the statistics about each chromosome.
        self.calculate_all()
        # Get the best distance from the previous generation and add it to the samples.
        best = self.chromosomes[0].tour_distance
        self.samples.append(best)
        # Reproduce half of the population leaving the parents and removing those not reproduced.
        new_population = []
        for i in range(self.pop_size // 4):
            # Select two parents.
            par_1 = self.chromosomes[2 * i]
            par_2 = self.chromosomes[2 * i + 1]
            # Get copies of the parents (in case parents are selected more than once).
            par_1 = deepcopy(par_1)
            par_2 = deepcopy(par_2)
            # Generate new children-to-be from them.
            cld_1 = deepcopy(par_1)
            cld_2 = deepcopy(par_2)
            # Reproduce parent copies into actual children.
            cld_1.reproduce(cld_2)
            # Add them all into the new population.
            new_population += [par_1, par_2, cld_1, cld_2]
        # Update population.
        self.chromosomes = new_population
        # Give the new population a chance at mutating.
        for chromosome in self.chromosomes:
            chromosome.mutate()

    def random_select(self):
        """
        Randomly select a chromosome.

        Returns: Randomly selected chromosome.

        """
        rand_float = random.uniform(0.0, 1.0)
        # Get chromosome who's cnintd range contains this number.
        prev = 0.0
        for chromosome in self.chromosomes:
            if prev <= rand_float < chromosome.cumulative_nintd:
                return chromosome
        # Return last chromosome if random float was 1.0.
        return self.chromosomes[-1]

    def calculate_tour_distance(self):
        """
        Calculate the tour distance for each chromosome.

        """
        for chromosome in self.chromosomes:
            chromosome.tour_distance = chromosome.get_tour_distance()

    def calculate_ntd(self):
        """
        Calculate the normed tour distance for each chromosome.

        """
        # Get the total tour distance of all the chromosomes.
        total_distance = 0.0
        for chromosome in self.chromosomes:
            total_distance += chromosome.tour_distance
        # Normalize each tour distance.
        for chromosome in self.chromosomes:
            chromosome.normed_td = chromosome.tour_distance / total_distance

    def calculate_intd(self):
        """
        Calculate the inverse of each normed tour distance for each chromosome.

        """
        for chromosome in self.chromosomes:
            chromosome.inversed_ntd = 1 - chromosome.normed_td

    def calculate_nintd(self):
        """
        Calculate the normed, inversed, normed, tour distance for each chromosome.

        """
        # Get total of inversed normed tour distances.
        total = 0.0
        for chromosome in self.chromosomes:
            total += chromosome.inversed_ntd
        for chromosome in self.chromosomes:
            chromosome.normed_intd = chromosome.inversed_ntd / total

    def calculate_cnintd(self):
        """
        Calculate the cumulative, normed, inversed, normed, tour distance for each chromosome.

        """
        total = 0.0
        self.chromosomes[0].cumulative_nintd = self.chromosomes[0].normed_intd
        for i in range(1, len(self.chromosomes) - 1):
            total += self.chromosomes[i - 1].normed_intd
            self.chromosomes[i].cumulative_nintd = self.chromosomes[i].normed_intd + total
        # Make the last one 1.0.
        self.chromosomes[-1].cumulative_nintd = 1.0

    def calculate_all(self):
        """
        Calculate all statistic values for each chromosome.

        """
        self.calculate_tour_distance()
        self.calculate_ntd()
        self.calculate_intd()
        self.calculate_nintd()
        # Sort the chromosomes by tour distance, increasing.
        self.chromosomes.sort(key=lambda x: x.tour_distance)
        self.calculate_cnintd()


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
        Plot the tour.

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
                bbox=dict(
                    boxstyle='round,pad=0.5',
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

    def get_tour_distance(self):
        """
        Get the tour distance for this chromosome.

        Returns: Tour distance.

        """
        # Get distance from first through to last point.
        total = 0
        for i in range(self._length - 1):
            total += self.tour[i].dist(self.tour[i + 1])
        # Add distance from last back to first directly.
        total += self.tour[-1].dist(self.tour[0])
        return total


class City:
    """
    An individual city, located by coordinates.

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
