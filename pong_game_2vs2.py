import random
import sys
import pygame
from pygame.locals import *
import pygame.freetype
import math

pygame.init()

# setup texte
pygame.freetype.init()
myfont = pygame.font.Font(None, 32)  # taille texte 20
titleFont = pygame.font.Font(None, 64)

# setup window
width, height = 800, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong")

# setup fps
clock = pygame.time.Clock()

# variables
player_life = 1
winner = None
score_top = 0
score_bottom = 0

# constants
BLUE = pygame.Color("#00ffcc")
LIGHT_GREY = pygame.Color("#0d8876")
GRIS = pygame.Color("#154143")
NOIR = pygame.Color("#1a1221")

BALL_RADIUS = 10
INITIAL_BALL_SPEED = 3.0
XMIN, YMIN = 0, 0
XMAX, YMAX = width, height

# init
pad_x1 = XMAX / 3 * 2
pad_x2 = XMAX / 3
pad_x3 = XMAX / 3 * 2
pad_x4 = XMAX / 3


def pad_scored(where, pad1, pad2, pad3, pad4):
    bottom = [pad1, pad2]
    top = [pad3, pad4]
    if where == "bottom":
        padint = random.randint(0, 1)
        pad = bottom[padint]
    else:
        padint = random.randint(0, 1)
        pad = top[padint]
    return pad


def print_window(chain, x, y):
    Text = myfont.render(chain, 1, GRIS)
    textRect = Text.get_rect(center=(x, y))
    screen.blit(Text, textRect)


class Balle:
    def speed_per_angle(self, angle):
        self.vx = self.speed * math.cos(math.radians(angle))
        self.vy = self.speed * math.sin(math.radians(angle))
        self.pad = None

    def __init__(self):
        self.x, self.y = (XMAX / 2, YMAX / 2)
        self.speed = INITIAL_BALL_SPEED  # initial speed
        self.speed_per_angle(60)  # speed vector
        self.on_pad = True

    def print_on_screen(self):
        pygame.draw.rect(screen, BLUE,
                         (int(self.x - BALL_RADIUS), int(self.y - BALL_RADIUS), 2 * BALL_RADIUS, 2 * BALL_RADIUS), 0)

    def pad_bounce(self, pad):
        diff = pad.x - self.x
        total_length = pad.length / 2 + BALL_RADIUS
        angle = 90 + 80 * diff / total_length
        self.speed_per_angle(angle)

    def move(self, pad1, pad2, pad3, pad4):
        global score_top
        global score_bottom

        if self.pad == None:
            self.pad = pad1
        if self.on_pad:
            if self.pad.y > YMAX / 2:
                self.y = self.pad.y - 2 * BALL_RADIUS
                self.x = self.pad.x
            else:
                self.y = self.pad.y + 2 * BALL_RADIUS
                self.x = self.pad.x
        else:
            self.x += self.vx
            self.y += self.vy
            if pad1.collision_balle(self) and self.vy > 0:
                self.pad_bounce(pad1)
                self.vy = -self.vy
                self.speed += 0.2
            elif pad2.collision_balle(self) and self.vy > 0:
                self.pad_bounce(pad2)
                self.vy = -self.vy
                self.speed += 0.2
            elif pad3.collision_balle(self) and self.vy < 0:
                self.pad_bounce(pad3)
                self.speed += 0.2
            elif pad4.collision_balle(self) and self.vy < 0:
                self.pad_bounce(pad4)
                self.speed += 0.2

            if self.x + BALL_RADIUS > XMAX:
                self.vx = -self.vx
            if self.x - BALL_RADIUS < XMIN:
                self.vx = -self.vx
            if self.y + BALL_RADIUS > YMAX:
                self.pad = pad_scored("bottom", pad1, pad2, pad3, pad4)
                self.on_pad = True
                score_top += 1
                self.speed = INITIAL_BALL_SPEED
            if self.y - BALL_RADIUS < YMIN:
                self.pad = pad_scored("top", pad1, pad2, pad3, pad4)
                self.on_pad = True
                score_bottom += 1
                self.speed = INITIAL_BALL_SPEED


class Pad():
    def __init__(self, y):
        self.x = (XMIN + XMAX) / 2
        self.y = y
        self.length = 10 * BALL_RADIUS

    def print_on_screen(self, x):
        pygame.draw.rect(screen, BLUE,
                         (int(self.x - self.length / 2), int(self.y - BALL_RADIUS), self.length, 2 * BALL_RADIUS), 0)

    def move(self, x):
        if x - self.length / 2 < XMIN:
            self.x = XMIN + self.length / 2
        elif x + self.length / 2 > XMAX:
            self.x = XMAX - self.length / 2
        else:
            self.x = x

    def collision_balle(self, balle):
        vertical = abs(self.y - balle.y) < 2 * BALL_RADIUS
        horizontal = abs(self.x - balle.x) < self.length / 2 + BALL_RADIUS
        return vertical and horizontal


class Game:
    def __init__(self):
        self.balle = Balle()
        # bottom team
        self.pad1 = Pad(YMAX - 5 * BALL_RADIUS)
        self.pad2 = Pad(YMAX - 15 * BALL_RADIUS)
        # top team
        self.pad3 = Pad(YMIN + 5 * BALL_RADIUS)
        self.pad4 = Pad(YMIN + 15 * BALL_RADIUS)

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

    def update(self):
        global pad_x1
        global pad_x2
        global pad_x3
        global pad_x4

        keys = pygame.key.get_pressed()
        if keys[K_LEFT] or keys[K_RIGHT]:
            vectorpad_x1 = - (keys[K_LEFT] - keys[K_RIGHT])
            pad_x1 += vectorpad_x1 * 10
            if pad_x1 > XMAX:
                pad_x1 = XMAX - 1
            elif pad_x1 < XMIN:
                pad_x1 = XMIN + 1

        if keys[K_b] or keys[K_n]:
            vectorpad_x2 = - (keys[K_b] - keys[K_n])
            pad_x2 += vectorpad_x2 * 10
            if pad_x2 > XMAX:
                pad_x2 = XMAX - 1
            elif pad_x2 < XMIN:
                pad_x2 = XMIN + 1

        if keys[K_g] or keys[K_h]:
            vectorpad_x3 = - (keys[K_g] - keys[K_h])
            pad_x3 += vectorpad_x3 * 10
            if pad_x3 > XMAX:
                pad_x3 = XMAX - 1
            elif pad_x3 < XMIN:
                pad_x3 = XMIN + 1

        if keys[K_t] or keys[K_y]:
            vectorpad_x4 = - (keys[K_t] - keys[K_y])
            pad_x4 += vectorpad_x4 * 10
            if pad_x4 > XMAX:
                pad_x4 = XMAX - 1
            elif pad_x4 < XMIN:
                pad_x4 = XMIN + 1

        if keys[K_SPACE] and self.balle.on_pad:
            self.balle.on_pad = False

        self.balle.move(self.pad1, self.pad2, self.pad3, self.pad4)
        self.pad1.move(pad_x1)
        self.pad2.move(pad_x2)
        self.pad3.move(pad_x3)
        self.pad4.move(pad_x4)

    def print_on_screen(self):
        screen.fill(NOIR)  # on efface l'écran
        self.balle.print_on_screen()
        self.pad1.print_on_screen(self.pad1.x)
        self.pad2.print_on_screen(self.pad2.x)
        self.pad3.print_on_screen(self.pad3.x)
        self.pad4.print_on_screen(self.pad4.x)
        print_window("Score : " + str(score_top), int(5 * BALL_RADIUS), int((YMAX / 3) * 2))
        print_window("Score : " + str(score_bottom), int(5 * BALL_RADIUS), int(YMAX / 3))


game = Game()

while True:
    game.events()
    game.update()
    game.print_on_screen()
    pygame.display.flip()  # send the image to gpu
    clock.tick(120)  # set to 120 fps

pygame.quit()