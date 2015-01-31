import pygame, led, sys, os, random, csv
from pygame.locals import *

""" A very simple arcade shooter demo :)
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)
GREEN = pygame.Color(0, 255, 0)

# detect if a serial/USB port is given as argument
hasSerialPortParameter = ( sys.argv.__len__() > 1 )

# use 90 x 20 matrix when no usb port for real display provided
fallbackSize = ( 90, 20 )

if hasSerialPortParameter:
    serialPort = sys.argv[ 1 ]
    print "INITIALIZING WITH USB-PORT: "+serialPort
    ledDisplay = led.teensy.TeensyDisplay( serialPort, fallbackSize )
else:
    print "INITIALIZING WITH SIMULATOR ONLY."
    ledDisplay = led.teensy.TeensyDisplay( None, fallbackSize )

# use same size for sim and real LED panel
size = ledDisplay.size()
simDisplay = led.sim.SimDisplay(size)
screen = pygame.Surface(size)
gamestate = 1 #1=alive; 0=dead

class Flappy(pygame.sprite.Sprite):
    def __init__(self):
        super(Flappy, self).__init__()
        self.image = pygame.image.load("Sprites/flappy1.png").convert_alpha()
        self.rect = self.image.get_rect()

class Background(pygame.sprite.Sprite):
    def __init__(self):
        super(Background, self).__init__()
        self.image = pygame.image.load("Sprites/flappybackground.png").convert()
        self.rect = self.image.get_rect()

class Pipetop(pygame.sprite.Sprite):
    def __init__(self):
        super(Pipetop, self).__init__()
        self.image = pygame.image.load("Sprites/pipetop.png").convert()
        self.rect = self.image.get_rect()

class Pipebottom(pygame.sprite.Sprite):
    def __init__(self):
        super(Pipebottom, self).__init__()
        self.image = pygame.image.load("Sprites/pipebottom.png").convert()
        self.rect = self.image.get_rect()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    global gamestate

    scored = False

    flappy = Flappy()
    background = Background()
    pipetop1 = Pipetop()

    pipebottom1 = Pipebottom()

    flappygroup = pygame.sprite.Group()
    backgroundgroup = pygame.sprite.Group()
    pipegroup = pygame.sprite.Group()

    pipegroup.add(pipetop1)
    pipegroup.add(pipebottom1)

    flappygroup.add(flappy)
    flappygroup.add(pipegroup.sprites())

    backgroundgroup.add(background)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    snake.turn("up")
                elif event.key == K_DOWN:
                    snake.turn("down")
                elif event.key == K_LEFT:
                    snake.turn("left")
                elif event.key == K_RIGHT:
                    snake.turn("right")
                elif event.key == K_SPACE:
                    if gamestate == 0:
                        gamestate = 1
                        scored = False

            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    pass

        if gamestate == 1:
            screen.fill(BLACK)
            backgroundgroup.draw(screen)
            flappygroup.draw(screen)
        else:
            pass

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
