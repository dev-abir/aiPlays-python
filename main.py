import os
import random

import numpy as np
import pyglet
from icecream import ic

from Bird import Bird
from Ecosystem import Ecosystem
from NeuralNet import NeuralNet
from settings import *

pyglet.resource.path = ["resources"]
pyglet.resource.reindex()

main_batch = pyglet.graphics.Batch()

# groups, to make sure the background is drawn before forground
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)

# TODO: make this game resizable
# TODO: add an icon to the window?
window = pyglet.window.Window(WINDOW_WIDTH, WINDOW_HEIGHT, resizable=False)

updates_per_frame_label = pyglet.text.Label(f"updates per frame: {updates_per_frame}", font_size=20, color=(0, 0, 0, 255))
max_score_label = pyglet.text.Label(font_size=20, x=window.width // 2, y=window.height - 50, color=(0, 0, 0, 255))


background_image = pyglet.resource.image(BACKGROUND_IMG)
# TODO: is it a must to create a sprite for images...?
background_image_sprite = pyglet.sprite.Sprite(img=background_image, batch=main_batch, group=background)

bottom_pipes_image = pyglet.resource.image(PIPE_IMG)
top_pipes_image = pyglet.resource.image(PIPE_IMG, flip_y=True)
bottom_pipes = []
top_pipes = []
for i in range(NUM_PIPES_PER_FRAME + 1):
    posx = FIRST_PIPE_OFFSET + (i * (window.width // NUM_PIPES_PER_FRAME))
    bottom_pipe = pyglet.sprite.Sprite(img=bottom_pipes_image, x=posx, batch=main_batch, group=foreground)
    bottom_pipe.y = random.randint(-bottom_pipe.height, window.height - (bottom_pipe.height + PIPE_VERT_DIST))
    bottom_pipe.scale_x = PIPE_IMG_SCALE_X
    bottom_pipes.append(bottom_pipe)

for i in range(NUM_PIPES_PER_FRAME + 1):
    posx = FIRST_PIPE_OFFSET + (i * (window.width // NUM_PIPES_PER_FRAME))
    top_pipe = pyglet.sprite.Sprite(img=top_pipes_image, x=posx, batch=main_batch, group=foreground)
    top_pipe.y = bottom_pipes[i].y + PIPE_VERT_DIST + (top_pipe.height * 2)
    top_pipe.scale_x = PIPE_IMG_SCALE_X
    top_pipes.append(top_pipe)

first_pipe_idx = 0

ecosystem = Ecosystem(
    population_size=30,
    num_generations=30,
    holdout=10,
    bird_spawner_func=lambda: Bird(
        brain=NeuralNet([4, 16, 16, 1]),
        bird_img=pyglet.resource.image(BIRD_IMG),
        batch=main_batch,
        group=foreground,
        x_offset=BIRD_X_OFFSET,
        default_y=window.height // 2
    )
)

'''
# event handlers ###################################################################################
'''


@window.event
def on_key_press(symbol, modifier):
    global updates_per_frame
    if symbol == pyglet.window.key.UP:
        updates_per_frame += 1
        updates_per_frame_label.text = f"updates per frame: {updates_per_frame}"
    if symbol == pyglet.window.key.DOWN:
        updates_per_frame = updates_per_frame - 1 if updates_per_frame > 1 else 1
        updates_per_frame_label.text = f"updates per frame: {updates_per_frame}"


def update(dt):
    # TODO: probably, we shouldn't use dt, for neural nets...?
    # TODO: update order...? does it matter? rn it's, enemy_update->decision->player_update
    global first_pipe_idx
    for _ in range(updates_per_frame):
        # TODO: do these for bottom and top pipes in one loop?
        for pipe in bottom_pipes:
            if pipe.x <= -pipe.width:
                first_pipe_idx -= 1  # TODO: do this line once only... (fix this, by using 1 loop...)
                new_pipe = pipe
                new_pipe.x = bottom_pipes[-1].x + window.width // NUM_PIPES_PER_FRAME
                bottom_pipes.remove(pipe)
                bottom_pipes.append(new_pipe)
            pipe.x -= PIPE_MOVEMENT_SPEED
        for pipe in top_pipes:
            if pipe.x <= -pipe.width:
                new_pipe = pipe
                new_pipe.x = top_pipes[-1].x + window.width // NUM_PIPES_PER_FRAME
                top_pipes.remove(pipe)
                top_pipes.append(new_pipe)
            pipe.x -= PIPE_MOVEMENT_SPEED

        all_birds_died = True
        for bird in ecosystem.birds:
            if not bird.died:
                all_birds_died = False

                # first top pipe up corner coord
                coord_top_pipe = top_pipes[first_pipe_idx].y - top_pipes[first_pipe_idx].height
                coord_bottom_pipe = coord_top_pipe - PIPE_VERT_DIST  # same for bottom pipe...

                x_dist_to_pipe = bird.get_x_dist(top_pipes[first_pipe_idx].x)
                y_dist_to_top_pipe = bird.get_y_dist(coord_top_pipe)
                y_dist_to_bottom_pipe = bird.get_y_dist(coord_bottom_pipe)

                bird.take_decision(y_dist_to_top_pipe=y_dist_to_top_pipe,
                                   y_dist_to_bottom_pipe=y_dist_to_bottom_pipe,
                                   x_dist_to_pipe=x_dist_to_pipe)
                bird.update_movement()

                if x_dist_to_pipe <= 0:
                    if y_dist_to_top_pipe <= 0 or y_dist_to_bottom_pipe >= 0:
                        bird.die()
                    if x_dist_to_pipe <= -top_pipes[first_pipe_idx].width:
                        bird.score += 1
                        first_pipe_idx = first_pipe_idx + 1 if first_pipe_idx + 1 < len(top_pipes) else 0
                elif bird.get_y_dist(window.height) <= 0 or bird.get_y_dist(0) >= 0:
                    bird.die()

        # TODO: this is being calculated twice...(here and in ecosystem class)
        max_score_label.text = f"max score: {str(np.max([bird.score for bird in ecosystem.birds]))} | " \
                               f"gen id: {ecosystem.generation_id}"

        if all_birds_died:
            ecosystem.new_generation()

            # reset the pipes position...
            first_pipe_idx = 0
            for i in range(NUM_PIPES_PER_FRAME + 1):
                posx = FIRST_PIPE_OFFSET + (i * (window.width // NUM_PIPES_PER_FRAME))
                bottom_pipes[i].y = random.randint(-bottom_pipe.height, window.height - (bottom_pipe.height + PIPE_VERT_DIST))
                bottom_pipes[i].x = posx
            for i in range(NUM_PIPES_PER_FRAME + 1):
                posx = FIRST_PIPE_OFFSET + (i * (window.width // NUM_PIPES_PER_FRAME))
                top_pipes[i].x = posx
                top_pipes[i].y = bottom_pipes[i].y + PIPE_VERT_DIST + (top_pipes[i].height * 2)

@window.event
def on_draw():
    window.clear()
    main_batch.draw()
    updates_per_frame_label.draw()  # drawing at last, so that it's drawn above everything... (TODO: better way?)
    max_score_label.draw()  # same reason as above...

if __name__ == "__main__":
    # pyglet.clock.schedule_interval(update, 1/(MONITOR_REFRESH_RATE * updates_per_frame))
    pyglet.clock.schedule_interval(update, 1 / MONITOR_REFRESH_RATE)
    pyglet.app.run()
