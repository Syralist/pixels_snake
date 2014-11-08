import pygame, led, sys, os, random
from pygame.locals import *

""" A very simple arcade shooter demo :)
"""

random.seed()

BLACK = pygame.Color(0,0,0)
WHITE = pygame.Color(255, 255, 255)
RED = pygame.Color(255, 0, 0)

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

class Snake:
    def __init__(self):
        self.init()

    def init(self):
        self.body = [pygame.Rect(45,10,1,1),pygame.Rect(46,10,1,1),pygame.Rect(47,10,1,1),pygame.Rect(48,10,1,1),]
        self.movement = "left"

    def setFood(self, food):
        self.food = food

    def setScreen(self, screen):
        self.screen = screen.get_rect()

    def turn(self, direction):
        self.movement = direction

    def move(self):
        global fallbackSize

        if self.movement == "left":
            self.body.insert(0,self.body[0].move(-1,0))
        if self.movement == "up":
            self.body.insert(0,self.body[0].move(0,-1))
        if self.movement == "right":
            self.body.insert(0,self.body[0].move(1,0))
        if self.movement == "down":
            self.body.insert(0,self.body[0].move(0,1))

        if not self.screen.contains(self.body[1]) or self.body[0] in self.body[1:]:
            self.init()
            self.food.init()
            return
        
        if not self.body[0] == self.food.position:
            self.body.pop()
        else:
            self.food.move(self.body)

    def draw(self, surface):
        for pixel in self.body:
            surface.fill(WHITE, pixel)

class Food:
    def __init__(self):
        self.init()

    def init(self):
        self.position = pygame.Rect(20,10,1,1)

    def position(self):
        return self.position

    def move(self, snakebody):
        global fallbackSize
        while self.position in snakebody:
            self.position = pygame.Rect(random.randint(0,fallbackSize[0]-1),random.randint(0,fallbackSize[1]-1),1,1)

    def draw(self, surface):
        surface.fill(WHITE, self.position)

def main():
    clock = pygame.time.Clock()

    snake = Snake()
    food = Food()
    snake.setFood(food)
    snake.setScreen(screen)

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
                    pass

            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    pass

        screen.fill(BLACK)
        snake.move()
        snake.draw(screen)
        
        food.draw(screen)

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
