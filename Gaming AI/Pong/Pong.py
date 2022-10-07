# Pong game for AI control

# Import modules
import pygame as pg
import pickle
import math
import random as r
import neat
import os

# --- Defing Variables --- #

WIN_WIDTH = 1500
WIN_HEIGHT = 1000


fps = 60
clock = pg.time.Clock()




# --- Defining Function ---#

def draw_midline(screen):
    for counter in range(WIN_HEIGHT//50):
        pg.draw.line(screen, (255, 255, 255), (WIN_WIDTH // 2, counter*50 +12.5), (WIN_WIDTH // 2, (counter+1)*50 -12.5))

def reflect(angle):
    return abs(angle-((angle-180)*2))


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
    
    def update(self, paddle):

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

        # Bouncing on left (fake player for training)
        if self.rect.left + dx <= 0:
            rand_angle = r.randint(0,56)/100
            self.direction = r.choice([rand_angle, 2*math.pi - rand_angle])
            #idx = dx
            dx = self.rect.left
            dy = dy*math.tan(self.direction)

        # Paddle Collision
        collide = False
        if paddle.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.rect.width, self.rect.height):
            
            troubleshoot[1] = True
            # Predictive section
            dx = self.rect.right - paddle.rect.left
            dy = dx*math.tan(self.direction)
            scale_factor = abs((paddle.rect.centery - self.rect.centery) / 110)
            
            if self.rect.centery > paddle.rect.centery:
                self.direction = math.pi - scale_factor
            else:
                self.direction = math.pi + scale_factor

            collide = True

        self.rect.x += dx
        self.rect.y += dy
        
        if troubleshoot[0] and troubleshoot[1]:
            print("YUUUUUUUUUP")

        if self.rect.right + dx >= 1500:
            return [True, collide]
        else:
            return [False, collide]

    def draw(self, screen, colour):
        pg.draw.rect(screen, colour, self.rect)



# --- Game Loop --- #
def main(genomes, config):
    
    screen = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    colours = [(25*x, 25*x, 25*x) for x in range(10)]
    
    nets = []
    ge = []
    players = []
    balls = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        players.append(Paddle(1435, 375))
        balls.append(Ball(300, 487.5))
        g.fitness = 0
        ge.append(g)
    
    
    running = True
    while running:

        clock.tick(fps)
        screen.fill((0, 0, 0))

        events = pg.event.get()
        for event in events:
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                quit()

        length = len(players)
        counter = 0

        while counter < length:

            ge[counter].fitness += 0.05
            output = nets[counter].activate((balls[counter].rect.centery - players[counter].rect.centery, balls[counter].rect.x))
            if output[0] > 0.5:
                players[counter].move_up()
            if output[1] < 0.5:
                players[counter].move_down()

            feedback = balls[counter].update(players[counter])
            if feedback[1]:
                ge[counter].fitness += 1
            if feedback[0]:
                ge[counter].fitness -= 1
                del(balls[counter])
                del(players[counter])
                del(colours[counter])
                del(nets[counter])
                del(ge[counter])
                length -= 1
            else:
                players[counter].draw(screen, colours[counter])
                balls[counter].draw(screen, colours[counter])
            counter += 1
        
        if len(players) == 0:
            running = False

        draw_midline(screen)
        pg.display.update()



def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, 
    neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "NEAT_CONFIG.txt")
    run(config_path)