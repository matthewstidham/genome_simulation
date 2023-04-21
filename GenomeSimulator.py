#!/usr/bin/env python3
import uuid
import random
from datetime import datetime


class GenomeSimulator:
    def __init__(self):
        self.generation = 1
        self.people = dict()
        self.starting_count = 32

    def setup(self):
        for _ in range(self.starting_count):
            value = uuid.uuid4()
            self.people[value] = {'name': value,
                                  'genome': [value] * 20_000,
                                  'generation': self.generation,
                                  'sex': random.randint(0, 1),
                                  'birth_year': random.randint(0, 10),
                                  'partner': None}

    def make_partners(self):
        self.generation += 1
        candidates = {key: value for key, value in self.people.items() if value['partner'] is None}
        if len(candidates) == 0:
            print('no candidates in generation %s' % self.generation)
            return 0
        males = {key: value for key, value in candidates.items() if value['sex'] == 1}
        females = {key: value for key, value in candidates.items() if value['sex'] == 0}
        total_children = (random.randint(1,6) + random.randint(1, 6)) / 2
        for count in range(min([len(males), len(females)])):
            for child in range(1, int(total_children)):
                genome = []
                father = list(males.values())[count]
                mother = list(females.values())[count]
                candidates[father['name']]['partner'] = mother['name']
                candidates[mother['name']]['partner'] = father['name']
                similarity = 0
                for gene in range(20_000):
                    if father['genome'][gene] == mother['genome'][gene]:
                        similarity += 1
                    if random.randint(0, 1) == 0:
                        genome.append(father['genome'][gene])
                    else:
                        genome.append(mother['genome'][gene])

                if similarity > 200:
                    break
                new_name = uuid.uuid4()
                birth_year = max(father['birth_year'], mother['birth_year']) + random.randint(20, 35)
                self.people[new_name] = {'name': new_name,
                                         'genome': genome,
                                         'generation': self.generation,
                                         'sex': random.randint(0, 1),
                                         'birth_year': birth_year,
                                         'partner': None}

    @staticmethod
    def genome_similarity(person_a, person_b):
        matching = 0
        for gene in range(20_000):
            if person_a['genome'][gene] == person_b['genome'][gene]:
                matching += 1
        return matching / 20_000 * 100

    def iterate_generations(self, generations):
        self.setup()
        for generation in range(1, generations):
            partners = self.make_partners()
            if partners == 0:
                return f"no matches in generation {generation}"
            print("generation %s: %s" % (generation, datetime.now()))
