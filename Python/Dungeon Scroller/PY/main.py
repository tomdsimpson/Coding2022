# Dungeon Scroller
import pygame as pg
# Scroll testing

WIDTH= 1000
HEIGHT = 1000
TILE_SIZE = 50

screen = pg.display.set_mode((WIDTH, HEIGHT))
fps = 60
clock = pg.time.Clock()

def clip(surface, x, y, x_size, y_size): #Get a part of the image
    handle_surface = surface.copy() #Sprite that will get process later
    clipRect = pg.Rect(x,y,x_size,y_size) #Part of the image
    handle_surface.set_clip(clipRect) #Clip or you can call cropped
    image = surface.subsurface(handle_surface.get_clip()) #Get subsurface
    return image.copy() #Return





class World:

    def __init__(self):
        pass



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

        self.direction = False
        self.moving = False
        self.animation_tick = 0
        self.speed = 0.1

    def movement(self, offset_x, offset_y):

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
        

        
        if abs(offset_x) > 50:
            offset_x = 0
        if abs(offset_y) > 50:
            offset_y = 0

        return offset_x, offset_y

    def draw(self):

        # Animation Handling
        if not self.moving:self.speed = 0.1
        self.animation_tick += self.speed

        if self.moving:
            if self.direction == "R":
                screen.blit(self.walkR_images[int((self.animation_tick*1.5) % 8)], (475, 525))
            elif self.direction == "U":
                screen.blit(self.walkU_images[int((self.animation_tick*1.5) % 8)], (475, 525))
            elif self.direction == "L":
                screen.blit(self.walkL_images[int((self.animation_tick*1.5) % 8)], (455, 525))
            elif self.direction == "D":
                screen.blit(self.walkD_images[int((self.animation_tick*1.5) % 8)], (475, 525))
        else:
            if self.direction == "R" or self.direction == "U":
                screen.blit(self.idle_imagesR[int(self.animation_tick % 4)], (475, 525))
            else:
                screen.blit(self.idle_imagesL[int(self.animation_tick % 4)], (475, 525))





        






# Initialising classes
game_world = World()
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

    offset_x, offset_y = player.movement(offset_x, offset_y)
    player.draw()

    # Exit Functionality
    for event in event_list:
        if event.type == pg.QUIT:
            run = False
 
    # Displaying content
    pg.display.update()