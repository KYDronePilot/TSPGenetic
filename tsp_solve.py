#!/usr/bin/env python3
"""
Main file for running the program.

"""
import sys
import json
import matplotlib.pyplot as plt

from src.nucleus import Nucleus
from src.city import City

# Help dialog.
HELP = """\
Usage:  python3 tsp_solve.py <args> <optional args>

Args:
    -p <population size>
    -g <number of generations>
    -m <mutation probability>

Optional Args (just the flag, no following value):
    --plot (show best tour and learning curve plots)
    --table (print table of population information after evolving)

"""


class Args:
    """
    For loading arguments.

    Attributes:
        args (list): Arguments passed to the script.
        population_size (int): The size of the population.
        generations_cnt (int): The number of generations to produce.
        mutation_prob (int): The probability of a mutation occurring.
        plot (bool): Whether the best tour and learning curve should be plotted.
        table (bool): Whether or not a table of the population should be printed.

    """

    def __init__(self):
        self.args = sys.argv[1:]
        self.population_size = None
        self.generations_cnt = None
        self.mutation_prob = None
        self.plot = False
        self.table = False

    def need_help(self):
        """
        Check if help dialog is requested.

        Returns: True is help needed, False if not.

        """
        return '-h' in self.args or '--help' in self.args

    def load_args(self):
        """
        Load program arguments.

        Returns:
            True if all attributes were set, False if not.

        """
        i = 0
        while i < len(self.args):
            if '-p' == self.args[i] and i < len(self.args) - 1:
                self.population_size = int(self.args[i + 1])
                i += 1
            elif '-g' == self.args[i] and i < len(self.args) - 1:
                self.generations_cnt = int(self.args[i + 1])
                i += 1
            elif '-m' == self.args[i] and i < len(self.args) - 1:
                self.mutation_prob = int(self.args[i + 1])
                i += 1
            elif '--plot' == self.args[i]:
                self.plot = True
            elif '--table' == self.args[i]:
                self.table = True
            i += 1
        # Check if all required attributes were set.
        if None in (self.population_size, self.generations_cnt, self.mutation_prob):
            return False
        return True


if __name__ == '__main__':
    # Load in the arguments.
    args = Args()
    # If help needed, print dialog and exit.
    if args.need_help():
        print(HELP)
        exit(0)
    # Load args, exiting if not all required attributes are set.
    if not args.load_args():
        print('Not all parameters specified', HELP, sep='\n')
        exit(0)
    # Create a city for each entry.
    with open('cities.json') as data:
        raw_cities = json.load(data)
    cities = []
    for city in raw_cities['cities']:
        new_city = City(city['x_coord'], city['y_coord'], city['label'])
        cities.append(new_city)
    # Generate a nucleus.
    nuc = Nucleus(cities, args.population_size, args.mutation_prob)
    # Evolve it.
    nuc.evolve(args.generations_cnt)
    # If specified, plot the best tour and learning curve.
    if args.plot:
        nuc.chromosomes[0].plot()
        # Clear plot.
        plt.cla()
        nuc.plot_learning_curve()
    # If specified, print out the latest generation.
    if args.table:
        print(nuc)
    # Print out the best tour.
    print('Best tour:', nuc.chromosomes[0])
    print('Distance: {0:.2f}'.format(nuc.chromosomes[0].tour_distance))
