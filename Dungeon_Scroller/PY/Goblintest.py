import pygame as pg
import math

WIDTH= 1000
HEIGHT = 1000
TILE_SIZE = 50

screen = pg.display.set_mode((WIDTH, HEIGHT))
fps = 60
clock = pg.time.Clock()

TERRAIN_DICT = {"1":"../IMG/TERRAIN/square_room.png", "2":"../IMG/TERRAIN/corridor_horizontal.png", "3":"../IMG/TERRAIN/corridor_vertical.png"}

# My Funcs
def convert_coords(world_coords, screen_coords): # coord [x, y]
  
    x = world_coords[0] - screen_coords[0]
    y = world_coords[1] - screen_coords[1]
    return [x, y]


def blit_centre(surface, rect, image):
        
        mid_x = rect.x + 0.5* rect.width
        mid_y = rect.y + 0.5* rect.height
        x = mid_x - 0.5* image.get_width()
        y = mid_y - 0.5* image.get_height()
        # CONVERT
        surface.blit(image, (x, y)) 



class World():

    def __init__(self):
        
        self.terrainGroup = pg.sprite.Group()
        self.enemyGroup = pg.sprite.Group()
        self.player = Player() 

        # Terrain Loading
        terrain = [("1", [250, 250]), ("2", [750, 450]), ("3", [450, 750]), ("1", [1250, 250]), ("1", [1250, 1250]), ("1", [250, 1250]), ("2", [750, 1450]), ("3", [1450, 750])]
        for x in terrain:
            map_piece = Terrain(TERRAIN_DICT[x[0]], x[1])
            self.terrainGroup.add(map_piece)

        # Entity Loading
        #enemy = Goblin([1000, 1000])
        #self.enemyGroup.add(enemy)



    # --- Entity Collision --- #
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

        # --- Image Loading --- #
        self.idle_imagesR = []
        self.idle_imagesL = []        
        self.walkR_images = []        
        self.walkU_images = []        
        self.walkL_images = []    
        self.walkD_images = []
        self.death_images = []

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

        # --- Attribute Initialisation --- #
        self.direction = "D"
        self.state = "idle"
        self.image = self.idle_imagesL[0]
        self.animation_tick = 0
        self.speed = 0.1
        self.life = 5
        self.rect = pg.Rect((475, 470), (50, 60))


    # --- State control / Input --- #
    def update(self):

        # Initiate input data
        dx, dy = 0, 0
        self.speed = 0.1

        # Death control
        if self.life < 1:
            self.state = "dying"
            if self.animation_tick >= 7:
                print("Dead")
                self.state = "dead"

        # User input gathering
        else:
            self.state = "idle"    
            if key[pg.K_LCTRL]:
                self.speed = 0.2
            if key[pg.K_w]:
                dy += 20 * self.speed
                self.state == "active"
                self.direction = "U"
            if key[pg.K_s]:
                dy -= 20 * self.speed
                self.state = "active"
                self.direction = "D"
            if key[pg.K_a]:
                dx += 20 * self.speed
                self.state = "active"
                self.direction = "L"
            if key[pg.K_d]:
                dx -= 20 * self.speed
                self.state = "active"
                self.direction = "R"
                
        # Animation clock        
        if self.animation_tick >= 7:
            self.animation_tick = 0
        self.animation_tick += self.speed    

        return dx, dy


    # --- Animation and Blitting --- #
    def draw(self):

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

        blit_centre(screen, self.rect, self.image)
        pg.draw.rect(screen, (255,255,255), self.rect, 2)



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
    def update(self, player, dx, dy):

        # --- Determine Behaviour --- #
        x_diff = (player.x + 0.5*player.width) - (self.rect.x + 0.5*self.rect.width)
        y_diff = (player.y + 0.5*player.height) - (self.rect.y + 0.5*self.rect.height)
        distance = math.sqrt(x_diff**2 + y_diff**2)

        if distance < 500:
            self.state = "moving"
            if distance < 50:
                self.state = "attack"
        else:
            self.state = "idle"

        # --- Execute Behaviour --- #
        # Movement
        if self.state == "moving":

            self.dx = self.speed * (x_diff / (abs(x_diff) + abs(y_diff))) 
            self.dy = self.speed * (y_diff / (abs(x_diff) + abs(y_diff)))
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

        self.rect.x += (dx + self.dx)
        self.rect.y += (dy + self.dy)
        
        # Attack
        if self.state == "attack":
            
            if self.animation_tick > 1 and self.animation_tick < 2:
                attack_rect = pg.Rect(self.rect.x - 10, self.rect.y - 10, 70, 80)
                pg.draw.rect(screen, (255,0,0), attack_rect, 2)

                if self.rect.colliderect(world.player.rect):
                    self.player_hit = True

            # Ending Attack
            if self.animation_tick > 3:
                self.state = "moving"
                self.animation_tick = 0

                if self.player_hit:
                    world.player.life -= 1
                    self.player_hit = False

        # Animation Clock
        self.animation_tick += 0.1            
        self.draw(screen)


    # --- Animations and blitting --- #
    def draw(self, screen):

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

        blit_centre(screen, self.rect, self.image)
        pg.draw.rect(screen, (255,255,255), self.rect, 2)   
        


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
    if world.player.state != "dead":
        dx, dy = world.player.update()
        dx, dy = world.check_col(world.player.rect, dx, dy)
        world.terrainGroup.update(dx, dy)
        world.terrainGroup.draw(screen)
        world.player.draw()        
        world.enemyGroup.update(world.player.rect, dx, dy)

    # Displaying content
    pg.display.update()