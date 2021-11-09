import pyglet.graphics
from icecream import ic

from Bird import Bird
from NeuralNet import NeuralNet

import numpy as np


class Ecosystem:
    def __init__(self, population_size: int, num_generations: int, holdout: int, bird_spawner_func):
        self.population_size = population_size
        self.num_generations = num_generations
        self.birds = []
        self.generation_id = 1
        self.max_score = 0
        self.holdout = holdout
        self.bird_spawner_func = bird_spawner_func
        for _ in range(population_size):
            self.birds.append(bird_spawner_func())

    def new_generation(self):
        self.generation_id += 1

        # arrange birds in descending order of their scores
        # TODO: any better way of doing this...?
        scores = [bird.score for bird in self.birds]
        self.birds = [self.birds[x] for x in np.argsort(scores)[::-1]]
        self.max_score = np.max(scores)

        new_population = []

        if self.max_score == 0 and self.generation_id % 15 == 0:
            # if for every 15 generations passed, no one scored above 0,
            # then demolish the species...
            for _ in range(self.population_size):
                new_population.append(self.bird_spawner_func())
        else:
            for i in range(self.population_size):
                parent_1_idx = i % self.holdout  # parent_1_idx will be within 0 to self.holdout - 1
                # TODO: why np.random.exponential...?
                parent_2_idx = min(self.population_size - 1, int(np.random.exponential(self.holdout)))
                offspring = self.birds[parent_1_idx].mate(self.birds[parent_2_idx])
                new_population.append(offspring)

            new_population[-1] = self.birds[0].get_clone()  # Ensure best organism survives
            # new_population[-1].color = (255, 0, 0)
        self.birds = new_population

    def max_gen_reached(self) -> bool:
        return self.num_generations == self.generation_id
