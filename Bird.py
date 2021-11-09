from __future__ import annotations

import numpy as np
import pyglet
from icecream import ic

import settings
from NeuralNet import NeuralNet
from settings import WINDOW_HEIGHT, NEURALNET_VISIBILITY_DIST, BIRD_JUMP_VEL, GRAVITY_ACCL


class Bird(pyglet.sprite.Sprite):
    def __init__(self, brain: NeuralNet, bird_img, batch: pyglet.graphics.Batch, group: pyglet.graphics.group, x_offset: int, default_y: int):
        # anchor centre, for rotations...
        bird_img.anchor_x = bird_img.width // 2
        bird_img.anchor_y = bird_img.height // 2

        super().__init__(img=bird_img, batch=batch, group=group)
        self.scale = settings.BIRD_IMG_SCALE
        self.brain = brain  # the neural net object, backing the bird
        self.default_batch = batch
        self.batch = batch
        self.x_offset = x_offset
        self.default_y = default_y
        self.score = 0
        self.velocity_y = 0
        self.died = False
        self.x = x_offset
        self.y = default_y
        #self.color = (np.random.randint(low=0, high=255), np.random.randint(low=0, high=255), np.random.randint(low=0, high=255))

    def take_decision(self, y_dist_to_top_pipe: float,
                      y_dist_to_bottom_pipe: float,
                      x_dist_to_pipe: float):
        max_vel = settings.WINDOW_HEIGHT // 2
        bird_vel = self.velocity_y / max_vel

        y_dist_to_top_pipe = abs(y_dist_to_top_pipe / WINDOW_HEIGHT)
        y_dist_to_bottom_pipe = abs(y_dist_to_bottom_pipe / WINDOW_HEIGHT)
        if x_dist_to_pipe > NEURALNET_VISIBILITY_DIST:
            x_dist_to_pipe = 1
        else:
            x_dist_to_pipe = abs(x_dist_to_pipe / NEURALNET_VISIBILITY_DIST)

        if y_dist_to_top_pipe < 0 or y_dist_to_top_pipe > 1:
            ic(y_dist_to_top_pipe, "out of bounds")
        if y_dist_to_bottom_pipe < 0 or y_dist_to_bottom_pipe > 1:
            ic(y_dist_to_bottom_pipe, "out of bounds")
        if x_dist_to_pipe > 1:
            ic(x_dist_to_pipe, "out of bounds")
        if bird_vel < -1 or bird_vel > 1:
            ic(bird_vel, "out of bounds")

        if self.brain.get_choice(np.array([[bird_vel, y_dist_to_top_pipe, y_dist_to_bottom_pipe, x_dist_to_pipe]])) > 0.5:
            self._jump()

    def _jump(self):
        if self.velocity_y <= 0:
            self.velocity_y += BIRD_JUMP_VEL

    def update_movement(self):
        self.velocity_y -= GRAVITY_ACCL
        self.y += self.velocity_y

    def mate(self, other: Bird) -> Bird:
        child = Bird(bird_img=self.image,
                     batch=self.default_batch,
                     group=self.group,
                     x_offset=self.x_offset,
                     default_y=self.default_y,
                     brain=self.brain.mate(other.brain))
        return child

    def get_clone(self) -> Bird:
        child = Bird(bird_img=self.image,
                     batch=self.default_batch,
                     group=self.group,
                     x_offset=self.x_offset,
                     default_y=self.default_y,
                     brain=self.brain)
        return child

    def die(self):
        self.died = True
        self.batch = None  # remove from batch, so it won't draw...

    def get_x_dist(self, coord: float) -> float:
        # FIXME: pos, neg dist...!!!
        # + self.width // 2, as it's anchored in the centre...
        return coord - (self.x + self.width // 2)

    def get_y_dist(self, coord: float) -> float:
        # FIXME: pos, neg dist...!!!
        # + self.height // 2, as it's anchored in the centre...
        return coord - (self.y + self.height // 2)
