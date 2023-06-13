import pygame as pg
import random
import time
from pygame.locals import *

# VARIABLES
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDTH = 2 * SCREEN_WIDTH
GROUND_HEIGHT = 100

PIPE_WIDTH = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

wing_sound = 'game_assets/wing.wav'
hit_sound = 'game_assets/hit.wav'

pg.mixer.init()


class Bird(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.images = [
            pg.image.load('game_assets/redbird-upflap.png').convert_alpha(),
            pg.image.load('game_assets/redbird-midflap.png').convert_alpha(),
            pg.image.load('game_assets/redbird-downflap.png').convert_alpha()
        ]

        self.speed = SPEED
        self.current_image = 0
        self.image = pg.image.load('game_assets/redbird-upflap.png').convert_alpha()
        self.mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDTH / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        self.speed += GRAVITY

        # Update height
        self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def flap_wings(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]


class Pipe(pg.sprite.Sprite):

    def __init__(self, inverted, xpos, ysize):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load('game_assets/pipe-green.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (PIPE_WIDTH, PIPE_HEIGHT))

        self.rect = self.image.get_rect()
        self.rect[0] = xpos

        if inverted:
            self.image = pg.transform.flip(self.image, False, True)
            self.rect[1] = -(self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pg.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pg.sprite.Sprite):

    def __init__(self, xpos):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.image.load('game_assets/base.png').convert_alpha()
        self.image = pg.transform.scale(self.image, (GROUND_WIDTH, GROUND_HEIGHT))

        self.mask = pg.mask.from_surface(self.image)

        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT

    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -sprite.rect[2]


def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted


def show_game_over_screen():
    game_over_font = pg.font.Font(None, 36)
    game_over_text = game_over_font.render("Game Over", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))

    restart_font = pg.font.Font(None, 24)
    restart_text = restart_font.render("Press ENTER to EXIT", True, (255, 255, 255))
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    screen.blit(game_over_text, game_over_rect)
    screen.blit(restart_text, restart_rect)
    pg.display.flip()

    # Wait for the player to press ENTER to restart the game
    waiting = True
    while waiting:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    waiting = False


pg.init()
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption('Flappy Bird by MUHIT KHAN')

BACKGROUND = pg.image.load('game_assets/background-night.png')
BACKGROUND = pg.transform.scale(BACKGROUND, (SCREEN_WIDTH, SCREEN_HEIGHT))
BEGIN_IMAGE = pg.image.load('game_assets/message.png').convert_alpha()

bird_group = pg.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pg.sprite.Group()

for i in range(2):
    ground = Ground(GROUND_WIDTH * i)
    ground_group.add(ground)

pipe_group = pg.sprite.Group()
for i in range(2):
    pipes = get_random_pipes(SCREEN_WIDTH * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pg.time.Clock()

begin = True
game_over = False

while begin:
    clock.tick(15)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pg.mixer.music.load(wing_sound)
                pg.mixer.music.play()
                begin = False

    screen.blit(BACKGROUND, (0, 0))
    screen.blit(BEGIN_IMAGE, (120, 150))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    bird.flap_wings()
    ground_group.update()

    bird_group.draw(screen)
    ground_group.draw(screen)

    pg.display.update()

while not game_over:
    clock.tick(15)

    for event in pg.event.get():
        if event.type == QUIT:
            pg.quit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                bird.bump()
                pg.mixer.music.load(wing_sound)
                pg.mixer.music.play()

    screen.blit(BACKGROUND, (0, 0))

    if is_off_screen(ground_group.sprites()[0]):
        ground_group.remove(ground_group.sprites()[0])
        new_ground = Ground(GROUND_WIDTH - 20)
        ground_group.add(new_ground)

    if is_off_screen(pipe_group.sprites()[0]):
        pipe_group.remove(pipe_group.sprites()[0])
        pipe_group.remove(pipe_group.sprites()[0])

        pipes = get_random_pipes(SCREEN_WIDTH * 2)

        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])

    bird_group.update()
    ground_group.update()
    pipe_group.update()

    bird_group.draw(screen)
    pipe_group.draw(screen)
    ground_group.draw(screen)

    pg.display.update()

    if pg.sprite.groupcollide(bird_group, ground_group, False, False, pg.sprite.collide_mask) or \
            pg.sprite.groupcollide(bird_group, pipe_group, False, False, pg.sprite.collide_mask):
        pg.mixer.music.load(hit_sound)
        pg.mixer.music.play()
        time.sleep(1)
        show_game_over_screen()
        game_over = True