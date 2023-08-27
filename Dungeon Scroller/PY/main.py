# Dungeon Scroller
import pygame as pg
# Scroll testing

WIDTH= 1000
HEIGHT = 1000
TILE_SIZE = 50

screen = pg.display.set_mode((WIDTH, HEIGHT))
fps = 60
clock = pg.time.Clock()


def ColorMask(image, mask_color):
    mask_image = image.convert()
    mask_image.set_colorkey(mask_color)
    mask = pg.mask.from_surface(mask_image)
    mask.invert()
    return mask

class World:

    def __init__(self, terrain):
        
        # Load Assets - read in level ...
        self.terrain = []
        for x in terrain:
            terrain_img = pg.image.load(f"../IMG/TERRAIN/{x[0]}.png").convert_alpha()
            terrain_pos = x[1]
            self.terrain.append(Terrain(terrain_img, terrain_pos))

    def update(self, offset_x, offset_y):
        
        overlap_x, overlap_y = 0, 0
        for x in self.terrain:

            a, b = x.check_col(offset_x, offset_y)
            overlap_x += a
            overlap_y += b

        if overlap_x > 50: overlap_x = 50
        if overlap_y > 60: overlap_y = 60

        offset_x = offset_x+(overlap_x-50)
        offset_y = offset_y+(overlap_y-60)

        for x in self.terrain:
            x.position[0] += (offset_x)
            x.position[1] += (offset_y)

        return offset_x, offset_y

    def draw(self, screen):
        for x in self.terrain:
            x.draw(screen)

class Terrain():

    def __init__(self, image, position):

        self.image = image
        self.position = position
        self.rect = self.image.get_rect()

    def check_col(self, offset_x, offset_y):

        #X Plane
        x_overlap = min([525 - (self.position[0]+offset_x), (self.position[0]+self.rect.width + offset_x) - 475])
        y_overlap = min([530 - (self.position[1]+offset_y), (self.position[1]+self.rect.height + offset_y) - 470])
        
        if x_overlap < 0:
            x_overlap = 0
        if y_overlap < 0:
            y_overlap = 0
        
        return x_overlap, y_overlap
        

    def update(self, offset_x, offset_y):
        
        self.position[0] += offset_x
        self.position[1] += offset_y

    def draw(self, screen):
        
        screen.blit(self.image, self.position)



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

    def update(self, offset_x, offset_y):

        # Movement
        offset_x, offset_y = 0, 0

        self.moving = False
        self.speed = 0.1
    
        if key[pg.K_LCTRL]:
            self.speed = 0.2

        if key[pg.K_w]:
            offset_y += 20 * self.speed
            self.moving = True
            self.direction = "U"
        if key[pg.K_s]:
            offset_y -= 20 * self.speed
            self.moving = True
            self.direction = "D"
        if key[pg.K_a]:
            offset_x += 20 * self.speed
            self.moving = True
            self.direction = "L"
        if key[pg.K_d]:
            offset_x -= 20 * self.speed
            self.moving = True
            self.direction = "R"
        
        return offset_x, offset_y

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
        
        pos = [self.rect.left, self.rect.top]
        if self.direction == "L":               # NOT GOOD
            pos[0] -= 15                        
            if self.moving: pos[0] -= 7
        if self.direction == "D":
            pos[0] -= 5
            if not self.moving: pos[0] -= 5

        screen.blit(self.current_image, pos)
        pg.draw.rect(screen, (255, 255, 255), self.rect, 5)







# Initialising classes
game_world = World([("square_room", [250, 0]), ("square_room", [250, 500])])
player = Player()
offset_x = 0
offset_y = 0
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
    
    # Set world movement
    offset_x, offset_y = player.update(offset_x, offset_y)
    
    # Check collisons
    offset_x, offset_y = game_world.update(offset_x, offset_y)
    
    # Draw entities
    game_world.draw(screen)
    player.draw()
    
    print(offset_x)

    # Displaying content
    pg.display.update()