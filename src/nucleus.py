import random
import os.path
from datetime import datetime
from copy import deepcopy

import prettytable
from matplotlib import pyplot as plt

from src.chromosomes import Chromosome

# Where to save plots.
PLOT_DIR = 'plots'


class Nucleus:
    """
    For containing and managing the population (chromosomes).

    Attributes:
        chromosomes (list): The chromosome population.
        cities (list[src.city.City]): Cities to solve for.
        pop_size (int): Size of chromosome population (must be divisible by 4).
        samples (list): The best tour distance from each population generated.
        mutate_prob (int): Mutation probability.

    """

    def __init__(self, cities, pop_size, mutate_prob):
        self.chromosomes = []
        self.cities = cities
        self.pop_size = pop_size
        self.samples = []
        self.mutate_prob = mutate_prob
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
            'Tour Distance'
        ])
        for chromosome in self.chromosomes:
            table.add_row([
                str(chromosome),
                chromosome.tour_distance
            ])
        return str(table)

    def evolve(self, cnt):
        """
        Evolve the nucleus by reproducing a set amount of times.

        Args:
            cnt (int): The number of times to reproduce.

        """
        for i in range(cnt):
            self.reproduce()

    def plot_learning_curve(self, resolution=100):
        """
        Plot learning curve of how quickly the algorithm finds the best solution.

        Args:
            resolution (int): The number of samples to plot.

        """
        self.calculate_tour_distance()
        # Get the divisor to limit the number of samples.
        step = len(self.samples) // resolution
        if step == 0:
            step = 1
        # Get samples.
        x = list(range(0, len(self.samples) + 1, step))
        y = [(self.samples + [self.chromosomes[0].tour_distance])[i] for i in x]
        # Setup plot.
        plt.grid(True)
        plt.title('TSP Learning Curve: {0}'.format(str(self.chromosomes[0])))
        plt.xlabel('Samples (every {0} generations)'.format(step))
        plt.ylabel('Lowest Distance')
        plt.plot(x, y)
        # Save plot.
        timestamp = datetime.now().strftime('%m-%d-%Y_%I-%M-%S-%p')
        name = 'learning_curve_{0}.png'.format(timestamp)
        save_dir = os.path.join(os.path.abspath(PLOT_DIR), name)
        plt.savefig(save_dir, dpi=200)

    def generate_population(self):
        """
        Generate a population of chromosomes.

        """
        for i in range(self.pop_size):
            # Create new cities and chromosomes for them.
            new_cities = [deepcopy(city) for city in self.cities]
            chromosome = Chromosome(*new_cities)
            # Shuffle the cities and append chromosome.
            chromosome.shuffle()
            self.chromosomes.append(chromosome)

    def reproduce(self):
        """
        Reproduce the chromosomes where only the top 50% of chromosomes are allowed to reproduce.

        """
        # Re-calculate the tour distances
        self.calculate_tour_distance()
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
            chromosome.mutate(prob=self.mutate_prob)

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
        Calculate and sort by the tour distance for each chromosome.

        """
        for chromosome in self.chromosomes:
            chromosome.tour_distance = chromosome.get_tour_distance()
        self.chromosomes.sort(key=lambda x: x.tour_distance)
