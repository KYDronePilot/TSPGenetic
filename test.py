from src.chromosomes import Chromosome
from src.city import City
import random

cities_1 = [City(0, 0, x) for x in range(1, 5)]
cities_2 = [City(0, 0, x) for x in range(5, 9)]

cities = [
    City(0, 0, 1),
    City(0, 1, 2),
    City(1, 1, 3),
    City(1, 0, 4)
]

random.shuffle(cities_1)
random.shuffle(cities_2)

chrom_1 = Chromosome(*cities_1)
chrom_2 = Chromosome(*cities_2)

if __name__ == '__main__':
    print(chrom_1)
    print(chrom_2)

    chrom_1.reproduce(chrom_2)

    print(chrom_1)
    print(chrom_2)
