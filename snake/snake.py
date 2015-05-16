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
    print "INITIALIZING WITH PORT: "+serialPort
    ledDisplay = led.dsclient.DisplayServerClientDisplay(serialport, 8123)
else:
    print "INITIALIZING WITH SIMULATOR ONLY."
    ledDisplay = led.dsclient.DisplayServerClientDisplay("localhost", 8123)

# use same size for sim and real LED panel
size = ledDisplay.size()
simDisplay = led.sim.SimDisplay(size)
screen = pygame.Surface(size)
gamestate = 1 #1=alive; 0=dead

class Snake:
    def __init__(self):
        self.init()

    def init(self):
        self.body = [pygame.Rect(45,10,1,1),pygame.Rect(46,10,1,1),pygame.Rect(47,10,1,1),pygame.Rect(48,10,1,1)]
        self.movement = "left"

    def setFood(self, food):
        self.food = food

    def setScreen(self, screen):
        self.screen = screen.get_rect()

    def turn(self, direction):
        if self.movement == "left" and direction == "right":
            pass
        elif self.movement == "right" and direction == "left":
            pass
        elif self.movement == "up" and direction == "down":
            pass
        elif self.movement == "down" and direction == "up":
            pass
        else:
            self.movement = direction

    def move(self):
        global fallbackSize
        global gamestate

        if self.movement == "left":
            self.body.insert(0,self.body[0].move(-1,0))
        if self.movement == "up":
            self.body.insert(0,self.body[0].move(0,-1))
        if self.movement == "right":
            self.body.insert(0,self.body[0].move(1,0))
        if self.movement == "down":
            self.body.insert(0,self.body[0].move(0,1))

        if not self.screen.contains(self.body[1]) or self.body[0] in self.body[1:]:
            gamestate = 0
            return
        
        if not self.body[0] == self.food.position:
            self.body.pop()
        else:
            self.food.move(self.body)

    def draw(self, surface):
        for pixel in self.body:
            surface.fill(WHITE, pixel)

    def len(self):
        return len(self.body)-1

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
        surface.fill(RED, self.position)

class ScoreBoard:
    def __init__(self, savefile="highscore.txt"):
        self.savefile = savefile
        self.scores = []
        if not os.path.isfile(self.savefile):
            self.scores.append(["ABC","7"])
            self.scores.append(["DEF","6"])
            self.scores.append(["GHI","5"])
            self.scores.append(["JKL","4"])
            with open(self.savefile, "wb") as f:
                writer = csv.writer(f)
                writer.writerows(self.scores)
        else:
            with open(self.savefile, "rb") as f:
                reader = csv.reader(f)
                for row in reader:
                    self.scores.append(row)
        print self.scores

    def append(self, score):
        print score
        for i in range(0, len(self.scores)):
            if score[1] >= int(self.scores[i][1]):
                self.scores.insert(i, score)
                self.scores.pop()
                with open(self.savefile, "wb") as f:
                    writer = csv.writer(f)
                    writer.writerows(self.scores)
                break
        print self.scores

def main():
    pygame.init()
    clock = pygame.time.Clock()
    
    global gamestate

    snake = Snake()
    food = Food()
    snake.setFood(food)
    snake.setScreen(screen)
    scoreboard = ScoreBoard()
    scored = False

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
                        snake.init()
                        food.init()
                        gamestate = 1
                        scored = False

            elif event.type == KEYUP:
                if event.key == K_UP or event.key == K_DOWN:
                    pass

        if gamestate == 1:
            screen.fill(BLACK)
            snake.move()
            snake.draw(screen)
            
            food.draw(screen)
        else:
            font = pygame.font.Font(None, 16)
            text1 = font.render("Game over", 0, RED)
            text1pos = text1.get_rect()
            text1pos.midtop = (screen.get_rect().centerx, -1)
            screen.blit(text1,text1pos)
            text2 = font.render("Score: "+str(snake.len()), 0, GREEN)
            text2pos = text2.get_rect()
            text2pos.midbottom = (screen.get_rect().centerx, 21)
            screen.blit(text2,text2pos)
            if not scored:
                scoreboard.append(["XYZ",snake.len()])
                scored = True

        simDisplay.update(screen)
        ledDisplay.update(screen)

        clock.tick(10)

main()
