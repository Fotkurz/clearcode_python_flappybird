import random

import pygame, sys


def draw_floor():
    # draw first floor piece
    screen.blit(scaled_floor_surface, (floor_x_pos, 900))
    # draw second floor piece
    screen.blit(scaled_floor_surface, (floor_x_pos + width, 900))

def create_pipe():
    # gets height of pipe basaed on random choice from list
    random_pipe_pos = random.choice(pipe_heights)
    # draws bottom pipe
    bottom_pipe = scaled_pipe_surface.get_rect(midtop=(width+100, random_pipe_pos))
    # draws top pipe
    top_pipe = scaled_pipe_surface.get_rect(midbottom=(width+100, random_pipe_pos - 300))
    # return tuple
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    # moves each pipe in pipes list - 5 on x direction
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    # draw each pipe in pipes list
    for pipe in pipes:
        # if pipe bottom edge is greater than 1024, it means the image is on the bottom
        is_a_bottom_pipe = pipe.bottom >= height
        if is_a_bottom_pipe:
            screen.blit(scaled_pipe_surface, pipe) # draws the pipe if its a bottom pipe
        else:
            # flips the pipe 90 degrees
            flip_pipe = pygame.transform.flip(surface=scaled_pipe_surface, flip_x=False, flip_y=True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        bird_collided_the_pipe = bird_rect.colliderect(pipe)
        if bird_collided_the_pipe:
            return False

    bird_hit_screen_borders = bird_rect.top <= -100 or bird_rect.bottom >= 900
    if bird_hit_screen_borders:
        return False
    return True

def game_over():
    print("GAME OVER")
    pygame.quit()
    sys.exit()

def reset_game():
    bird_movement = 0
    floor_x_pos = 0
    gravity = 0
    pipe_list.clear()
    bird_rect.center = (100, height/2)

def rotate_bird(bird_surface):
    rotated_bird = pygame.transform.rotozoom(bird_surface, bird_movement * -3, 1)
    return rotated_bird

def bird_animation():
    new_bird_frame = bird_frames[bird_index]
    new_bird_rect = new_bird_frame.get_rect(center=(100, bird_rect.centery))
    return new_bird_frame, new_bird_rect


# initialize the pygame
pygame.init()

# Game Variables
gravity = 0.25
bird_movement = 0
width = 576
height = 1024
floor_x_pos = 0
game_active = True

# sets a window of width=width  and height=height
screen = pygame.display.set_mode(size=(width, height))
# used now to caps our framerate
clock = pygame.time.Clock()
# loads the background image from specific folder
# convert is not necessary but it converts the .png to a type of file
# made to work with pygame in a better way
bg_surface = pygame.image.load('assets/background-day.png').convert()
floor_surface = pygame.image.load('assets/base.png').convert()
scaled_bg_surface = pygame.transform.scale2x(bg_surface) # scaling the surface in 2 times
scaled_floor_surface = pygame.transform.scale2x(floor_surface)

# loading the 3 bird surface to use in frames
bird_downflap = pygame.image.load('assets/bluebird-downflap.png').convert_alpha() # alpha handles the black box in our rect
bird_midflap = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/bluebird-upflap.png').convert_alpha()
# scaling the 3 bird frames
scaled_bird_downflap = pygame.transform.scale2x(bird_downflap)
scaled_bird_midflap = pygame.transform.scale2x(bird_midflap)
scaled_bird_upflap = pygame.transform.scale2x(bird_upflap)
# adding the frames inside a list of frames
bird_frames = [scaled_bird_downflap, scaled_bird_midflap, scaled_bird_upflap]
# gets one frame from the list
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(100, height/2))

BIRD_FLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRD_FLAP,200)

# loading the pipes obstacles
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
scaled_pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = [] # list of obstacles
SPAWN_PIPE = pygame.USEREVENT # this SPAWN_PIPE is used to generate more pipes in our screen
pygame.time.set_timer(event=SPAWN_PIPE, millis=1200)
# list of pipe heights
pipe_heights = [400, 600, 800]
# while True to not close the window

while True:
    # searchs for pygame.QUIT event in pygame.event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # execute pygame.quit()
            pygame.quit()
            # calls sys.exit() for leaving with exit code 0 (success exit)
            sys.exit()
        # detects the use of 'spacebar'
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                # resets bird_movement to 0 so we can counter gravity
                bird_movement = 0
                # increase the bird y in 12 (decrease since '+' is down)
                bird_movement -= 10

            if event.key == pygame.K_SPACE and not game_active:
                game_active = True
                reset_game()

        # every time this event is trigger (checks set_time func above)
        if event.type == SPAWN_PIPE:
            # grabs the bottom+top pipes and extract to pipe_list
            pipe_list.extend(create_pipe())

        if event.type == BIRD_FLAP: # changing our frames based on BIRD_FLAP event
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0
            bird_surface, bird_rect = bird_animation()

    # puts one surface on another surface
    # bg_surface = surface,
    # dest = position on screen (0,0 = top-left = origin-point)
    screen.blit(source=scaled_bg_surface, dest=(0, 0))
    if game_active:
        game_active = check_collision(pipe_list)
        # Bird Momvent
        # adding our gravity to our bird_movement (each tick adds the gravity again)
        rotated_bird = rotate_bird(bird_surface)
        bird_movement += gravity
        # adding this movement to our bird_rect on the 'y' axis
        bird_rect.centery += bird_movement
        # draws our bird and its rectangle
        screen.blit(source=rotated_bird, dest=bird_rect)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1  # adds -1 to floor_x_pos each time the update occurs

    # draw two pieces of the floor img for restarting the loop
    # and making it look like if the floor has no end.
    draw_floor()
    end_screen_reach = floor_x_pos <= -width
    if end_screen_reach:
        # resets floor to 0
        floor_x_pos = 0


    # runs the update function
    pygame.display.update()
    clock.tick(60)

