import pygame as pg
import math

WIDTH= 1000
HEIGHT = 1000
TILE_SIZE = 50

screen = pg.display.set_mode((WIDTH, HEIGHT))
fps = 60
clock = pg.time.Clock()

TERRAIN_DICT = {"1":"../IMG/TERRAIN/square_room.png", "2":"../IMG/TERRAIN/ladder.png", "3":"../IMG/TERRAIN/exit.png"}


class World():

    def __init__(self):
        
        self.terrainGroup = pg.sprite.Group()
        self.enemyGroup = pg.sprite.Group()
        self.player = Player() 

        # Terrain Loading
        terrain = [("1", [250, 250]), ("1", [750, 250]), ("1", [250, 750]), ("1", [750, 750]), ("1", [250, 1250]), ("1", [750, 1250])]
        for x in terrain:
            map_piece = Terrain(TERRAIN_DICT[x[0]], x[1])
            self.terrainGroup.add(map_piece)

        # Entity Loading
        enemy = Goblin([1000, 1000])
        self.enemyGroup.add(enemy)



    # --- Player Collision --- #
    def check_col(self, rect, dx, dy):

        overlap_rects = []
        for terrain in self.terrainGroup:
            overlap_rects.append(terrain.check_overlap(rect, dx, dy))

        hl, hr, wt, wb = 0, 0, 0, 0
        for obj in overlap_rects:
            if obj.left == rect.left:
                hl += obj.height
            if obj.right == rect.right:
                hr += obj.height
            if obj.top == rect.top:
                wt += obj.width
            if obj.bottom == rect.bottom:
                wb += obj.width

        if wb == 0 or wt == 0:
            width = max(wt, wb)
        else:
            width = min(wt, wb)
        
        if hl == 0 or hr == 0:
            height = max(hl, hr)
        else:
            height = min(hl, hr)

        if dx < 0:
            dx += (rect.width - width)
        elif dx > 0:
            dx -= (rect.width - width)

        if dy < 0:
            dy += (rect.height - height)
        elif dy > 0:
            dy -= (rect.height - height)

        return dx, dy




class Terrain(pg.sprite.Sprite):

    def __init__(self, img, pos):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

    def check_overlap(self, rect, dx, dy):

        d_rect = self.rect.move(dx, dy)
        overlap_rect = d_rect.clip(rect)
        return overlap_rect

    def update(self, dx, dy):

        self.rect.x += dx
        self.rect.y += dy



class Player:

    def __init__(self):

        # Loading idle images
        self.idle_imagesR = []
        for x in range (4):
            self.idle_imagesR.append(pg.transform.scale(pg.image.load(f"../IMG/Player/IdleR/idle{x+1}.png").convert_alpha(), (60, 60)))

        self.idle_imagesL = []
        for x in range (4):
            self.idle_imagesL.append(pg.transform.scale(pg.image.load(f"../IMG/Player/IdleL/idle{x+1}.png").convert_alpha(), (60, 60)))

        # Loading Walking
        self.walkR_images = []
        for x in range (8):
            self.walkR_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkR/walk{x+1}.png").convert_alpha(), (64, 60)))
        
        self.walkU_images = []
        for x in range (8):
            self.walkU_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkU/walk{x+1}.png").convert_alpha(), (64, 60)))
        
        self.walkL_images = []
        for x in range (8):
            self.walkL_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkL/walk{x+1}.png").convert_alpha(), (84, 60)))

        self.walkD_images = []
        for x in range (8):
            self.walkD_images.append(pg.transform.scale(pg.image.load(f"../IMG/Player/WalkD/walk{x+1}.png").convert_alpha(), (60, 60)))

        self.direction = "D"
        self.moving = False
        self.animation_tick = 0
        self.speed = 0.1
        self.rect = pg.Rect((475, 470), (50, 60))

    def update(self):

        # Movement
        dx, dy = 0, 0
        self.moving = False
        self.speed = 0.1
        if key[pg.K_LCTRL]:
            self.speed = 0.2

        if key[pg.K_w]:
            dy += 20 * self.speed
            self.moving = True
            self.direction = "U"
        if key[pg.K_s]:
            dy -= 20 * self.speed
            self.moving = True
            self.direction = "D"
        if key[pg.K_a]:
            dx += 20 * self.speed
            self.moving = True
            self.direction = "L"
        if key[pg.K_d]:
            dx -= 20 * self.speed
            self.moving = True
            self.direction = "R"
        
        return dx, dy

    def draw(self):

        # Animation Handling
        if not self.moving:self.speed = 0.1
        self.animation_tick += self.speed

        if self.moving:
            if self.direction == "R":
                self.current_image = self.walkR_images[int((self.animation_tick*1.5) % 8)]
            elif self.direction == "U":
                self.current_image = self.walkU_images[int((self.animation_tick*1.5) % 8)]
            elif self.direction == "L":
                self.current_image = self.walkL_images[int((self.animation_tick*1.5) % 8)]
            elif self.direction == "D":
                self.current_image = self.walkD_images[int((self.animation_tick*1.5) % 8)]
        else:
            if self.direction == "R" or self.direction == "U":
                self.current_image = self.idle_imagesR[int(self.animation_tick % 4)]
            else:
                self.current_image = self.idle_imagesL[int(self.animation_tick % 4)]
        
        pos = [self.rect.x, self.rect.y]
        if self.direction == "L":               # NOT GOOD
            pos[0] -= 15                        
            if self.moving: pos[0] -= 7
        if self.direction == "D":
            pos[0] -= 5
            if not self.moving: pos[0] -= 5

        screen.blit(self.current_image, pos)



class Goblin(pg.sprite.Sprite):

    def __init__(self, pos):

        pg.sprite.Sprite.__init__(self)

        self.idle_image = pg.transform.scale(pg.image.load(f"../IMG/ENEMY/idle.png").convert_alpha(), (80, 80))
        self.image = self.idle_image
        self.walkD_images = []
        self.walkL_images = []
        self.walkU_images = []
        self.walkR_images = []
        self.attackD_images = []
        self.attackL_images = []
        self.attackU_images = []
        self.attackR_images = []
        self.speed = 2
        
        # Loading animations
        for x in range (8):
            self.walkD_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/WalkD/down{x+1}.png").convert_alpha(), (80, 80)))
        for x in range (8):
            self.walkL_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/WalkL/walk{x+1}.png").convert_alpha(), (80, 80)))
        for x in range (8):
            self.walkU_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/WalkU/walk{x+1}.png").convert_alpha(), (80, 80)))
        for x in range (8):
            self.walkR_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/WalkR/walkL{x+1}.png").convert_alpha(), (80, 80)))

        for x in range (3):
            self.attackD_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/AttackD/attack{x+1}.png").convert_alpha(), (80, 80)))
        for x in range (3):
            self.attackL_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/AttackL/attack{x+1}.png").convert_alpha(), (80, 80)))
        for x in range (3):
            self.attackU_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/AttackU/attack{x+1}.png").convert_alpha(), (80, 80)))
        for x in range (3):
            self.attackR_images.append(pg.transform.scale(pg.image.load(f"../IMG/ENEMY/AttackR/attack{x+1}.png").convert_alpha(), (80, 80)))


        self.direction = "L"
        self.moving = True
        self.animation_tick = 0
        self.rect = pg.Rect(pos, (50, 60))
        self.dx = 0
        self.dy = 0

    def update(self, player, dx, dy):

        #Calculate Direction and Distance
        x_diff = (player.x + 0.5*player.width) - (self.rect.x + 0.5*self.rect.width)
        y_diff = (player.y + 0.5*player.height) - (self.rect.y + 0.5*self.rect.height)
        distance = math.sqrt(x_diff**2 + y_diff**2)

        if distance < 500:
            self.dx = self.speed * (x_diff / (abs(x_diff) + abs(y_diff))) 
            self.dy = self.speed * (y_diff / (abs(x_diff) + abs(y_diff)))
            if self.moving != "Attack": self.moving = True 

            if distance < 50 and self.moving != "Attack": #Attack
                self.moving = "Attack"
                self.animation_tick = 0
                self.dx, self.dy = 0, 0

            if self.moving == True:    
                self.dx, self.dy = world.check_col(self.rect, self.dx, self.dy)

                if self.dy > 0:
                    self.direction = "D"
                elif self.dy < 0:
                    self.direction = "U"
                if self.dx > 0:
                    self.direction = "R"
                elif self.dx < 0:
                    self.direction = "L"
        
        else:
            self.moving = False
            self.direction = "D"
            self.dx, self.dy = 0, 0

        self.rect.x += (dx + self.dx)
        self.rect.y += (dy + self.dy)

        # Animation Handling
        self.animation_tick += 0.1
        print(self.dx)

        if self.moving == True:
            if self.direction == "R":
                self.image = self.walkR_images[int((self.animation_tick*1) % 8)]
            elif self.direction == "U":
                self.image = self.walkU_images[int((self.animation_tick*1) % 8)]
            elif self.direction == "L":
                self.image = self.walkL_images[int((self.animation_tick*1) % 8)]
            elif self.direction == "D":
                self.image = self.walkD_images[int((self.animation_tick*1) % 8)]
        
        if self.moving == "Attack":
            if self.animation_tick == 0.9:
                self.moving = True
            
            if self.direction == "L":
                #Attack Left
                self.image = self.attackL_images[int((self.animation_tick*1) % 3)]
            
            elif self.direction == "R":
                #Attack Right
                self.image = self.attackR_images[int((self.animation_tick*1) % 3)]
            
            elif self.direction == "U":
                #Attack Up
                self.image = self.attackU_images[int((self.animation_tick*1) % 3)]
            else:
                #Attack Down
                self.image = self.attackD_images[int((self.animation_tick*1) % 3)]
        
        else:
            self.image = self.idle_image
        


world = World()
run = True

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

    # Get movement
    dx, dy = world.player.update()
    dx, dy = world.check_col(world.player.rect, dx, dy)
    world.terrainGroup.update(dx, dy)
    # Check entity collision
    world.enemyGroup.update(world.player.rect, dx, dy)
    
    # Draw
    world.terrainGroup.draw(screen)
    world.enemyGroup.draw(screen) 
    world.player.draw()

    # Displaying content
    pg.display.update()