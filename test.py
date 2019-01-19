from chromosomes import City, Chromosome

cities_1 = [City(0, 0, x) for x in range(1, 10)]
cities_2 = [City(0, 0, x) for x in range(10, 20)]

chrom_1 = Chromosome(*cities_1)
chrom_2 = Chromosome(*cities_2)

# TODO: Continue building a test.
