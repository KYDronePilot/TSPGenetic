from chromosomes import City, Chromosome
import random

cities_1 = [City(0, 0, x) for x in range(1, 5)]
cities_2 = [City(0, 0, x) for x in range(5, 9)]

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
