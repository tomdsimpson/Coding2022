# Flappy Bird for AI
# 11/09/22

# Importing  Modules
import pygame as pg
import neat as nt
import time
import os
import random
import math
pg.font.init()

# Initializing Game Variables
WIN_WIDTH = 500
WIN_HEIGHT = 800

BIRD_IMGS = [
    pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird1.png"))), 
    pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird2.png"))), 
    pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird3.png"))),
    pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bird2.png")))
    ]
PIPE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "pipe.png")))
BASE_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pg.transform.scale2x(pg.image.load(os.path.join("imgs", "bg.png")))
PLAY_IMG = pg.transform.scale2x(pg.image.load("imgs/play_btn.png"))
QUIT_IMG = pg.transform.scale2x(pg.image.load("imgs/quit_btn.png"))

STAT_FONT = pg.font.SysFont("comicsans", 50)

# Defining Classes 

class Button():

    def __init__(self, x, y, image):

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self, win):
        action = False

        # Getting mouse position
        pos = pg.mouse.get_pos()

        # Checking mouseover and click conditions
        if self.rect.collidepoint(pos) and pg.mouse.get_pressed()[0] == 1 and not self.clicked:
            action = True
            self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        win.blit(self.image, self.rect)

        return action



class Bird:

    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROT_VEL = 10
    ANIMATION_TIME = 5

    def __init__(self, x, y):

        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = 0
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        if self.tick_count >= 7:
            self.vel = -10.5
            self.tick_count = 0
            self.height = self.y

    def move(self):

        self.tick_count += 1

        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        if d >= 16:
            d = 16
        self.y = self.y + d

        # Tilt
        if d < 0: #CHECK THIS
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
    
    def draw(self, win):

        self.img_count += 1
        img = (self.img_count// self.ANIMATION_TIME) % 4
        self.img = self.IMGS[img]

        # Nose Dive
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2
        
        rotated_img = pg.transform.rotate(self.img, self.tilt)
        new_rect = rotated_img.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_img, new_rect.topleft)
    
    def get_mask(self):
        return pg.mask.from_surface(self.img)



class Pipe:

    GAP = 200
    VEL = 5

    def __init__(self, x):
        
        self.x = x
        self.height = 0
        self.gap = 100

        self.top = 0
        self.bottom = 0
        self.PIPE_TOP = pg.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        self.passed = False
        self.set_height()
    
    def set_height(self):

        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP
    
    def move(self):

        self.x -= self.VEL

    def draw(self, win):

        win.blit(self.PIPE_TOP, (self.x, self.top))
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    def collide(self, bird):

        bird_mask = bird.get_mask()
        top_mask = pg.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pg.mask.from_surface(self.PIPE_BOTTOM)

        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        if t_point or b_point:
            return True
        return False


class Base:

    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))





# --- Main Game Code --- #

def draw_window(win, bird, base, pipes, score, game_state):
    
    win.blit(BG_IMG, (0,0))
    
    if game_state == "PLAY":
        for pipe in pipes:
            pipe.draw(win)
        
        text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
        win.blit(text, (WIN_WIDTH - 10 -text.get_width(), 10))

        bird.draw(win)
    
    base.draw(win)


def main():
    
    win = pg.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pipes = [Pipe(700)]
    base = Base(730)
    clock = pg.time.Clock()
    score = 0
    game_state = "MENU"
    reset = False

    play_btn = Button(25, 200, PLAY_IMG)
    quit_btn = Button(275, 200, QUIT_IMG)


    run = True
    while run:
        
        clock.tick(30)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
        key = pg.key.get_pressed()

        base.move()

        if game_state == "PLAY":

            bird.move()

            if key[pg.K_SPACE]:
                bird.jump()

            add_pipe = False
            rem = []
            for pipe in pipes:

                if pipe.x + pipe.PIPE_BOTTOM.get_width() < 0:
                    rem.append(pipe)
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True
                pipe.move()

                if pipe.collide(bird):
                    reset = True
            
            if add_pipe:
                score += 1
                pipes.append(Pipe(700))
            
            for r in rem:
                pipes.remove(r)
            

            if bird.y + bird.img.get_height() >= 730:
                reset = True

        if reset:
            del bird
            game_state = "MENU"
            pipes = [Pipe(700)]
            reset = False
            score = 0
            print(pipes)


        # Drawing Stuff
        win.blit(BG_IMG, (0,0))
        
        if game_state == "PLAY":
            for pipe in pipes:
                pipe.draw(win)          
            text = STAT_FONT.render(f"Score: {score}", 1, (255, 255, 255))
            win.blit(text, (WIN_WIDTH - 10 -text.get_width(), 10))
            bird.draw(win)
        
        base.draw(win)

        if game_state == "MENU":

            if play_btn.draw(win):
                game_state = "PLAY"
                bird = Bird(230, 350)
            if quit_btn.draw(win):
                run = False

        pg.display.update()

    pg.quit()
    quit()

main()