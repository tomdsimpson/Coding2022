# Pong game for AI control

# Import modules
import pygame as pg
import pickle
import math
import random as r
import neat
import os
pg.init()

# --- Defing Variables --- #

WIN_WIDTH = 1500
WIN_HEIGHT = 1000


fps = 60
clock = pg.time.Clock()
white = (255, 255, 255)
score_font = pg.font.SysFont("Ubuntu", 40)


# --- Defining Function ---#

def draw_midline(screen):
    for counter in range(WIN_HEIGHT//50):
        pg.draw.line(screen, (255, 255, 255), (WIN_WIDTH // 2, counter*50 +12.5), (WIN_WIDTH // 2, (counter+1)*50 -12.5))

def reflect(angle):
    return abs(angle-((angle-180)*2))

def find_dist(a, b):
     
     x = a.rect.x - b.rect.x
     y = a.rect.y - b.rect.y
     distance = math.sqrt(x**2 + y**2)
     return distance

def draw_text(screen, text, colour, x, y, font):
    img = font.render(text, True, colour)
    screen.blit(img, (x, y))   



# --- Defining Classes --- #

class Paddle:

    def __init__(self, x, y):
        self.rect = pg.Rect(0, 0, 25, 150)
        self.rect.x = x
        self.rect.y = y

    def move_up(self):
        dy = -10
        if self.rect.top + dy < 0:
            dy = self.rect.top
        self.rect.y += dy

    def move_down(self):
        dy = 10
        if self.rect.bottom + dy > WIN_HEIGHT:
            dy = WIN_HEIGHT - self.rect.bottom
        self.rect.y += dy

    def draw(self, screen, colour):
        pg.draw.rect(screen, colour, self.rect)



class Ball:

    def __init__(self, x, y):
        self.rect = pg.Rect(0, 0, 25, 25)
        self.rect.x = x
        self.rect.y = y
        self.direction = r.randint(-50, 50) / 100
        self.speed = 10
        self.score_a = 0
        self.score_b = 0
    
    def update(self, paddle1, paddle2): 

        troubleshoot = [False, False]
        dx = self.speed * math.cos(self.direction)
        dy = self.speed * math.sin(self.direction) * -1

        # Checking for collision

        # Bottom of screen
        if self.rect.bottom + dy >= WIN_HEIGHT:
            self.direction = 2*math.pi-self.direction
            #idy = dy
            dy = WIN_HEIGHT - self.rect.bottom
            dx = dy*math.tan(self.direction)#dx*(dy/idy)

        # Top of screen
        if self.rect.top + dy <= 0:
            self.direction = 2*math.pi-self.direction
            #idy = dy
            dy = self.rect.top
            dx = dy*math.tan(self.direction) #dx*(dy/idy)
            troubleshoot[0] = True

        # Paddle Collision
        collide = False
        if paddle2.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
            
            # Predictive section
            dx = self.rect.right - paddle2.rect.left
            dy = dx*math.tan(self.direction)
            scale_factor = abs((paddle2.rect.centery - self.rect.centery) / 110)
            
            if self.rect.centery < paddle2.rect.centery:
                self.direction = math.pi - scale_factor
            else:
                self.direction = math.pi + scale_factor

        elif paddle1.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
            
            # Predictive section
            dx = self.rect.left - paddle1.rect.right
            dy = dx*math.tan(self.direction)
            scale_factor = abs((paddle1.rect.centery - self.rect.centery) / 110)
            
            if self.rect.centery < paddle1.rect.centery:
                self.direction = scale_factor
            else:
                self.direction = 2*math.pi - scale_factor

        self.rect.x += dx
        self.rect.y += dy
        
        if self.rect.right >= 1500:
            self.score_a += 1
            self.rect.x = 750
            self.rect.y = 487.5
            self.direction = 0
        elif self.rect.left <= 0:
            self.score_b += 1
            self.rect.x = 750
            self.rect.y = 487.5
            self.direction = math.pi

    def draw(self, screen, colour):
        pg.draw.rect(screen, colour, self.rect)



# --- Game Loop --- #
def main(config):
    
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    ai_player = Paddle(1435, 375)
    player = Paddle(50, 375)
    ball = Ball(300, 487.5)
    pickle_in = open("pongAI", "rb")
    g = pickle.load(pickle_in)
    net = neat.nn.FeedForwardNetwork.create(g,config)
    
    running = True
    while running:

        clock.tick(fps)
        screen.fill((0, 0, 0))
        key = pg.key.get_pressed()

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

        # Paddle Movement
        output = net.activate((ball.rect.centery - ai_player.rect.centery, find_dist(ai_player, ball)))
        if output[0] > 0.5:
            pass
        else:
            if output[1] > 0.5:
                ai_player.move_up()
            if output[2] > 0.5:
                ai_player.move_down()

        if key[pg.K_UP]:
            player.move_up()
        if key[pg.K_DOWN]:
            player.move_down()

        ball.update(player, ai_player)

        # Drawing Objects
        player.draw(screen, white)
        ai_player.draw(screen, white)
        ball.draw(screen, white)
        draw_midline(screen)
        draw_text(screen, str(ball.score_a), white, 150, 50, score_font)
        draw_text(screen, str(ball.score_b), white, 1300, 50, score_font)
        
        pg.display.update()



if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEAT_CONFIG.txt")
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    main(config)