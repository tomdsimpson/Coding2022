import pygame as pg
import math
import numpy
import time
import random

pg.init()

WIDTH= 1000
HEIGHT = 1000
TILE_SIZE = 50

screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Dungeon Battle")
fps = 60
clock = pg.time.Clock()
game_state = "menu"

TERRAIN_DICT = {"1":"../IMG/TERRAIN/square_room.png", "2":"../IMG/TERRAIN/corridor_horizontal.png", "3":"../IMG/TERRAIN/corridor_vertical.png"}

play_img = pg.image.load("../IMG/play_btn.png").convert()
icon_img = pg.transform.scale(pg.image.load("../IMG/icon.png"), (60, 60))
score_font = pg.font.SysFont("Ubuntu", 45)

# My Funcs
def convert_coords(world_coords, screen_coords): # coord [x, y]
  
    x = world_coords[0] - screen_coords[0]
    y = world_coords[1] - screen_coords[1]
    return [x, y]


def blit_centre(surface, rect, image, screen_pos):
        
        mid_x = rect.x + 0.5* rect.width
        mid_y = rect.y + 0.5* rect.height
        x = mid_x - 0.5* image.get_width()
        y = mid_y - 0.5* image.get_height()
        [x, y] = convert_coords([x,y], screen_pos)
        surface.blit(image, (x, y)) 

def find_nonzero_min(array):
    min = 9999
    for x in array:
        if x < min and x != 0:
            min = x
    if min == 9999:
        min = 0
    return min

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


class Button():

    def __init__(self, x, y, image):

        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # Getting mouse position
        pos = pg.mouse.get_pos()

        # Checking mouseover and click conditions
        if self.rect.collidepoint(pos) and pg.mouse.get_pressed()[0] == 1 and not self.clicked:
            action = True
            self.clicked = True

        if pg.mouse.get_pressed()[0] == 0:
            self.clicked = False

        screen.blit(self.image, self.rect)

        return action



class World():

    def __init__(self):
        
        self.terrainGroup = pg.sprite.Group()
        self.enemyGroup = pg.sprite.Group()
        self.portalGroup = pg.sprite.Group()
        self.player = Player()
        self.screen_pos = [-420, -170] 
        self.score = 0

        # Terrain Loading
        terrain = [("1", [0, 250]),("1", [0, 750]),("1", [1000, 0]),("1", [1000, 1000]),("1", [2000, 250]),("1", [2000, 750]), ("3", [1200, 500]), ("2", [500, 1150]), ("2", [500, 250]), ("2", [1500, 250]), ("2", [1500, 1150]),]
        for x in terrain:
            map_piece = Terrain(TERRAIN_DICT[x[0]], x[1])
            self.terrainGroup.add(map_piece)

        # Entity Loading
        coords = [(160, 660), (1160, 160), (1160, 1160), (2160, 660)]
        for x in coords:
            portal = Portal(x)
            self.portalGroup.add(portal)



    # --- Entity Collision --- #
    def get_non_overlap_sides(self, d_rect):
        
        overlap_rects = []
        for terrain in self.terrainGroup:
            overlap_rects.append(terrain.check_overlap(d_rect))

        hl, hr, wt, wb = 0, 0, 0, 0
        for obj in overlap_rects:
            if obj.left == d_rect.left:
                hl += obj.height
            if obj.right == d_rect.right:
                hr += obj.height
            if obj.top == d_rect.top:
                wt += obj.width
            if obj.bottom == d_rect.bottom:
                wb += obj.width

        wt = d_rect.width - wt
        wb = d_rect.width - wb
        hl = d_rect.height - hl
        hr = d_rect.height - hr

        return wt, wb, hl, hr


    def check_col(self, rect, dx, dy):

        new_dx = 0
        new_dy = 0

        # X
        d_rect = rect.move(dx, 0)
        wt, wb, hl, hr = self.get_non_overlap_sides(d_rect)
        if dx > 0:
            new_dx = dx - find_nonzero_min([wt, wb])
        elif dx < 0:
            new_dx = dx + find_nonzero_min([wt, wb])                     

        # Y
        d_rect = rect.move(0, dy)
        wt, wb, hl, hr = self.get_non_overlap_sides(d_rect)
        if dy > 0:
            new_dy = dy - find_nonzero_min([hl, hr])
        elif dy < 0:
            new_dy = dy + find_nonzero_min([hl, hr])       
        
        # Diag
        d_rect = rect.move(dx, dy)
        wt, wb, hl, hr = self.get_non_overlap_sides(d_rect)

        if wt != 0 or wb != 0:
            if new_dx == dx and new_dy == dy:
                new_dx = 0
        #if wt != 0 and hl != 0:
        #if wb != 0 and hr != 0:
        #if wb != 0 and hl != 0:



        return new_dx, new_dy



class Terrain(pg.sprite.Sprite):

    def __init__(self, img, pos):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def check_overlap(self, rect):

        overlap_rect = self.rect.clip(rect)
        return overlap_rect

    def update(self, screen, screen_pos):

        x, y = convert_coords([self.rect.x, self.rect.y], screen_pos)
        screen.blit(self.image, [x, y])




class Player:

    def __init__(self):

        # --- Image Loading --- #
        self.idle_imagesR = []
        self.idle_imagesL = []        
        self.walkR_images = []        
        self.walkU_images = []        
        self.walkL_images = []    
        self.walkD_images = []
        self.death_images = []
        self.attackR_images = []
        self.attackU_images = []
        self.attackL_images = []
        self.attackD_images = []

        for x in range (4):
            self.idle_imagesR.append(pg.transform.scale(pg.image.load(f"../IMG/Player/IdleR/idle{x+1}.png").convert_alpha(), (60, 60)))
        for x in range (4):
            self.idle_imagesL.append(pg.transform.scale(pg.image.load(f"../IMG/Player/IdleL/idle{x+1}.png").convert_alpha(), (60, 60)))
        for x in range (8):
            self.walkR_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkR/walk{x+1}.png").convert_alpha(), (64, 60)))
        for x in range (8):
            self.walkU_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkU/walk{x+1}.png").convert_alpha(), (64, 60)))
        for x in range (8):
            self.walkL_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkL/walk{x+1}.png").convert_alpha(), (84, 60)))
        for x in range (8):
            self.walkD_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkD/walk{x+1}.png").convert_alpha(), (60, 60)))
        for x in range(8):
            self.death_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/Death/death{x+1}.png").convert_alpha(), (60, 60)))
        for x in range(6):
            self.attackR_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/AttackR/attack{x+1}.png").convert_alpha(), (140, 140)))
        for x in range(6):
            self.attackL_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/AttackL/attack{x+1}.png").convert_alpha(), (140, 140)))
        for x in range(6):
            self.attackU_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/AttackU/attack{x+1}.png").convert_alpha(), (140, 140)))
        for x in range(6):
            self.attackD_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/AttackD/attack{x+1}.png").convert_alpha(), (140, 140)))

        # --- Attribute Initialisation --- #
        self.direction = "D"
        self.state = "idle"
        self.image = self.idle_imagesL[0]
        self.animation_tick = 0
        self.speed = 0.1
        self.life = 5
        self.rect = pg.Rect((50, 300), (50, 60))


    # --- State control / Input --- #
    def gain_input(self, key):

        # Initiate input data
        dx, dy = 0, 0
        self.speed = 0.1

        # User input gathering
        if self.state != "dying":
            if self.state != "attack":
                self.state = "idle"    

                if key[pg.K_LCTRL]:
                    self.speed = 0.2
                if key[pg.K_w]:
                    dy -= 20 * self.speed
                    self.state = "active"
                    self.direction = "U"
                if key[pg.K_s]:
                    dy += 20 * self.speed
                    self.state = "active"
                    self.direction = "D"
                if key[pg.K_a]:
                    dx -= 20 * self.speed
                    self.state = "active"
                    self.direction = "L"
                if key[pg.K_d]:
                    dx += 20 * self.speed
                    self.state = "active"
                    self.direction = "R"
                if key[pg.K_SPACE]:
                    self.state = "attack"
                    self.animation_tick = 0

        return dx, dy


    # --- Update values --- #
    def update(self, screen, screen_pos, score):

        # Death control
        if self.life == 0 and self.state != "dying":
            self.animation_tick = 0
            self.state = "dying"

        if self.animation_tick >= 7 and self.state == "dying":
            print("Dead")
            self.state = "dead"

        if self.state == "attack":
            if self.direction == "R":
                attack_rect = pg.Rect(self.rect.right, self.rect.top, 30, self.rect.height)
            elif self.direction == "U":
                attack_rect = pg.Rect(self.rect.left, self.rect.top-30, self.rect.width, 30)
            elif self.direction == "L":
                attack_rect = pg.Rect(self.rect.left-30, self.rect.top, 30, self.rect.height)
            elif self.direction == "D":
                attack_rect = pg.Rect(self.rect.left, self.rect.bottom, self.rect.width, 30)
            
            #pg.draw.rect(screen, (255,0,0), attack_rect.move(-world.screen_pos[0], -world.screen_pos[1]), 2)   #Hitbox

            for enemy in world.enemyGroup:
                if attack_rect.colliderect(enemy.rect):
                    enemy.kill()
                    score += 50


            if self.animation_tick >= 4:
                self.state = "idle"
                self.animation_tick = 0


        # Animation clock        
        if self.animation_tick >= 7:
            self.animation_tick = 0
        self.animation_tick += self.speed

        self.draw(screen, screen_pos)
        return score           


    # --- Animation and Blitting --- #
    def draw(self, screen, screen_pos):

        if self.state == "active":
            if self.direction == "R":
                self.image = self.walkR_images[int((self.animation_tick*1.5) % 8)]
            elif self.direction == "U":
                self.image = self.walkU_images[int((self.animation_tick*1.5) % 8)]
            elif self.direction == "L":
                self.image = self.walkL_images[int((self.animation_tick*1.5) % 8)]
            elif self.direction == "D":
                self.image = self.walkD_images[int((self.animation_tick*1.5) % 8)]
        
        elif self.state == "idle":
            if self.direction == "R" or self.direction == "U":
                self.image = self.idle_imagesR[int(self.animation_tick % 4)]
            else:
                self.image = self.idle_imagesL[int(self.animation_tick % 4)]
        
        elif self.state == "dying":
            self.image = self.death_images[int((self.animation_tick) % 8)]
        
        elif self.state == "attack":
            if self.direction == "R":
                self.image = self.attackR_images[int(self.animation_tick % 6)]
            elif self.direction == "L":
                self.image = self.attackL_images[int(self.animation_tick % 6)]
            elif self.direction == "U":
                self.image = self.attackU_images[int(self.animation_tick % 6)]
            elif self.direction == "D":
                self.image = self.attackD_images[int(self.animation_tick % 6)]

        blit_centre(screen, self.rect, self.image, screen_pos)



class Goblin(pg.sprite.Sprite):

    def __init__(self, pos):
        pg.sprite.Sprite.__init__(self)

        # --- Image Loading --- #
        
        self.walkD_images = []
        self.walkL_images = []
        self.walkU_images = []
        self.walkR_images = []
        self.attackD_images = []
        self.attackL_images = []
        self.attackU_images = []
        self.attackR_images = []

        self.idle_image = pg.image.load(f"../IMG/ENEMY/idle.png").convert_alpha()
        for x in range (8):
            self.walkD_images.append(pg.image.load(f"../IMG/ENEMY/WalkD/down{x+1}.png").convert_alpha())
        for x in range (8):
            self.walkL_images.append(pg.image.load(f"../IMG/ENEMY/WalkL/walk{x+1}.png").convert_alpha())
        for x in range (8):
            self.walkU_images.append(pg.image.load(f"../IMG/ENEMY/WalkU/walk{x+1}.png").convert_alpha())
        for x in range (8):
            self.walkR_images.append(pg.image.load(f"../IMG/ENEMY/WalkR/walkL{x+1}.png").convert_alpha())
        for x in range (3):
            self.attackD_images.append(pg.image.load(f"../IMG/ENEMY/AttackD/attack{x+1}.png").convert_alpha())
        for x in range (3):
            self.attackL_images.append(pg.image.load(f"../IMG/ENEMY/AttackL/attack{x+1}.png").convert_alpha())
        for x in range (3):
            self.attackU_images.append(pg.image.load(f"../IMG/ENEMY/AttackU/attack{x+1}.png").convert_alpha())
        for x in range (3):
            self.attackR_images.append(pg.image.load(f"../IMG/ENEMY/AttackR/attack{x+1}.png").convert_alpha())

        # --- Attribute Initialisation --- #
        self.speed = 2
        self.image = self.idle_image
        self.direction = "L"
        self.state = "idle"
        self.animation_tick = 0
        self.rect = pg.Rect(pos, (50, 60))
        self.dx = 0
        self.dy = 0
        self.player_hit = False


    # --- AI Behaviour --- #
    def update(self,screen, screen_pos, player):

        # --- Determine Behaviour --- #
        x_diff = (player.x + 0.5*player.width) - (self.rect.x + 0.5*self.rect.width)
        y_diff = (player.y + 0.5*player.height) - (self.rect.y + 0.5*self.rect.height)
        distance = math.sqrt(x_diff**2 + y_diff**2)

        if distance < 750:
            self.state = "moving"
            if distance < 50:
                self.state = "attack"
        else:
            self.state = "moving"
            x_diff = random.randint(-50, 50)
            y_diff = random.randint(-50, 50)

        # --- Execute Behaviour --- #
        # Movement
        if self.state == "moving":

            if x_diff == 0:
                self.dy = 2 * numpy.sign(y_diff)
                self.dx = 0
            elif y_diff == 0:
                self.dx = 2 * numpy.sign(x_diff)
                self.dy = 0
            else:
                self.dx = numpy.sign(x_diff) * self.speed * math.sqrt(1 - (y_diff / (abs(x_diff) + abs(y_diff)))**2) 
                self.dy = numpy.sign(y_diff) * self.speed * math.sqrt(1 - (x_diff / (abs(x_diff) + abs(y_diff)))**2)
            
            self.dx = round(self.dx, 0)
            self.dy = round(self.dy, 0)

            self.dx, self.dy = world.check_col(self.rect, self.dx, self.dy)

            if abs(self.dx) > abs(self.dy):
                if self.dx > 0:
                    self.direction = "R"
                else:
                    self.direction = "L"
            else:
                if self.dy > 0:
                    self.direction = "D"
                else:
                    self.direction = "U"
        
        else:
            self.dx, self.dy = 0, 0

        self.rect.x += (self.dx)
        self.rect.y += (self.dy)
        
        # Attack
        if self.state == "attack":
            
            if self.animation_tick > 1 and self.animation_tick < 2:
                attack_rect = pg.Rect(self.rect.x - 10, self.rect.y - 10, 70, 80)

                if attack_rect.colliderect(world.player.rect):
                    self.player_hit = True

            # Ending Attack
            if self.animation_tick > 3:
                self.state = "moving"
                self.animation_tick = 0

                if self.player_hit and world.player.life != 0:
                    world.player.life -= 1
                    self.player_hit = False

        # Animation Clock
        self.animation_tick += 0.1            
        self.draw(screen, screen_pos)


    # --- Animations and blitting --- #
    def draw(self, screen, screen_pos):

        if self.state == "moving":
            if self.direction == "R":
                self.image = self.walkR_images[int((self.animation_tick*1) % 8)]
            elif self.direction == "U":
                self.image = self.walkU_images[int((self.animation_tick*1) % 8)]
            elif self.direction == "L":
                self.image = self.walkL_images[int((self.animation_tick*1) % 8)]
            elif self.direction == "D":
                self.image = self.walkD_images[int((self.animation_tick*1) % 8)]
            
        elif self.state == "attack":
            if self.direction == "L":
                self.image = self.attackL_images[int((self.animation_tick) % 3)]
            elif self.direction == "R":
                self.image = self.attackR_images[int((self.animation_tick) % 3)]
            elif self.direction == "U":
                self.image = self.attackU_images[int((self.animation_tick) % 3)]
            else:
                self.image = self.attackD_images[int((self.animation_tick) % 3)] 

        elif self.state == "idle":
            self.image = self.idle_image

        blit_centre(screen, self.rect, self.image, screen_pos)



class Portal(pg.sprite.Sprite):

    def __init__(self, coord):
        pg.sprite.Sprite.__init__(self)

        self.rect = pg.Rect((coord[0], coord[1]), (50, 50))
        self.animation_tick = 0
        self.cooldown = 5
        self.time = time.time()

        self.idle_images = []
        for x in range(15):
            self.idle_images.append(pg.transform.scale(pg.image.load(f"../IMG/PORTAL/portal{x+1}.png").convert_alpha(), (180, 180)))
        self.image = self.idle_images[0]


    def update(self, screen, screen_pos, enemy_group):

        if time.time() - self.time > self.cooldown:
            
            self.time = time.time()
            if self.cooldown > 1:   
                self.cooldown -= 0.1
            enemy_group.add(Goblin((self.rect.x+60, self.rect.y+60)))

        self.animation_tick += 0.15
        if self.animation_tick > 15:
            self.animation_tick = 0

        self.draw(screen, screen_pos)

    def draw(self, screen, screen_pos):

        self.image = self.idle_images[int(self.animation_tick % 15)]
        x, y = convert_coords((self.rect.x, self.rect.y), screen_pos)
        screen.blit(self.image, (x, y))



run = True

play_btn = Button(450, 300, play_img)

while run:
    
    # Maintenance
    clock.tick(fps)
    event_list = pg.event.get()
    key = pg.key.get_pressed()
    screen.fill((0, 0, 0))

    # Exit Functionality
    for event in event_list:
        if event.type == pg.QUIT:
            run = False
    
    if game_state == "playing":
        # Get movement
        dx, dy = world.player.gain_input(key)
        if world.player.state == "active":
            dx, dy = world.check_col(world.player.rect, dx, dy)
        world.screen_pos[0] += dx
        world.screen_pos[1] += dy
        world.player.rect.x += dx
        world.player.rect.y += dy   
        
        world.terrainGroup.update(screen, world.screen_pos)
        world.portalGroup.update(screen, world.screen_pos, world.enemyGroup)
        world.score = world.player.update(screen, world.screen_pos, world.score)     
        world.enemyGroup.update(screen, world.screen_pos, world.player.rect)

        draw_text(f"Score:  {world.score}", score_font, (255,255,255), 10, 70)
        draw_text(f"Lives:     x{world.player.life}", score_font, (255,255,255), 10, 10)
        screen.blit(icon_img, (120, 10))
        
        if world.player.state == "dead":
            game_state = "menu"
            del(world)
    
    else:

        if play_btn.draw():
            world = World()
            game_state = "playing"


    # Displaying content
    pg.display.update()