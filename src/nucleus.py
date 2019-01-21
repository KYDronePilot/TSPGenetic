import random
from copy import deepcopy

import prettytable
from matplotlib import pyplot as plt

from src.chromosomes import Chromosome


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

    def evolve(self, cnt):
        """
        Evolve the nucleus by reproducing a set amount of times.

        Args:
            cnt (int): The number of times to reproduce.

        """
        for i in range(cnt):
            self.reproduce_most_fit()

    def plot_learning_curve(self, resolution=100):
        """
        Plot learning curve of how quickly the algorithm finds the best solution.

        Args:
            resolution (int): The number of samples to plot.

        """
        self.calculate_all()
        # Get the divisor to limit the number of samples.
        step = len(self.samples) // resolution
        if step == 0:
            step = 1
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
            # Create new cities and chromosomes for them.
            new_cities = [deepcopy(city) for city in self.cities]
            chromosome = Chromosome(*new_cities)
            # Shuffle the cities and append chromosome.
            chromosome.shuffle()
            self.chromosomes.append(chromosome)

    def reproduce(self):
        """
        Reproduce half the chromosomes choosing at random which ones to use.

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
            chromosome.mutate(prob=self.mutate_prob)

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
