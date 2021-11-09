
'''
# settings ###################################################################################
'''
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

PIPE_VERT_DIST = 200  # vertical distance between pipes
NUM_PIPES_PER_FRAME = 3  # number of fully visible pipes per frame
PIPE_MOVEMENT_SPEED = 5  # 200 pixels per frame...
FIRST_PIPE_OFFSET = 300

MONITOR_REFRESH_RATE = 60.0  # TODO: is there any way to find it out programmatically?
updates_per_frame = 1

BACKGROUND_IMG = "back.png"

PIPE_IMG = "Mario_pipe.png"
PIPE_IMG_SCALE_X = 0.75

BIRD_IMG = "bird.png"
BIRD_IMG_SCALE = 0.2
BIRD_X_OFFSET = 100
GRAVITY_ACCL = 1
BIRD_JUMP_VEL = 15

NEURALNET_VISIBILITY_DIST = 500
