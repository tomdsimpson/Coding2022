# Tetris Game
# Started 05/04/22

'''

- expamd window
- better background
- menu
- Sounds

'''

# Importing modules
from tkinter.filedialog import test
from turtle import window_height
import pygame as pg
import random as r
import pickle
pg.init()

# Building game window (10x20)
tile_size = 50
screen_width = tile_size * 10
screen_height = tile_size * 20

fps = 50
clock = pg.time.Clock()
colors = ["blue", "green", "red", "yellow"]
pickle_in = open("pattern_data", "rb")
patterns = pickle.load(pickle_in)
global piece_counter
piece_counter = 0

score_font = pg.font.SysFont("Bauhaus 93", 40)

screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Tetris")

# Initialising Tile group
tile_group = pg.sprite.Group()
inactive_pieces = []

# drawing grid
def draw_grid():
    for line in range(0, screen_width//tile_size + 1):
        pg.draw.line(screen, (255, 0, 0), (tile_size * line, 0), (line * tile_size, screen_height))
    for line in range(0, screen_height//tile_size + 1):
        pg.draw.line(screen, (255, 0, 0), (0, line * tile_size), (screen_width, line * tile_size))

# Drawing text function
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))



# Defining tile class
class tile(pg.sprite.Sprite):

    def __init__(self, color, x, y, id, id2):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(f"./Images/{color}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = tile_size
        self.height = tile_size
        self.id = id
        self.id2 = id2
        self.state = "falling"

    def check_collision_y(self, dy):
        collision = False

        # Checking for y collision with tiles
        for tile in tile_group:

            # Self exception
            if tile.id == self.id:
                pass
            else:
                if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    dy = tile.rect.top - self.rect.bottom
                    collision = True

        if self.rect.y + dy > 950:
            dy = 1000 - self.rect.bottom
            collision = True

        
        return collision, dy


    def check_collision_x(self, dx):
     
        collision = False

        for tile in tile_group:

            # Self exception
            if tile.id == self.id:
                pass
            elif dx > 0:
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = tile.rect.left - self.rect.right
                    collision = True
            else:
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = tile.rect.right - self.rect.left
                    collision = True

        if self.rect.x + dx > 450:
            dx = 500 - self.rect.right
            collision = True
        elif self.rect.x + dx < 0:
            dx = 0 + self.rect.left
            collision = True

        return collision, dx

    def update(self, pattern, pos):
        self.rect.y = pos[1] + (pattern[1]*tile_size)
        self.rect.x = pos[0] + (pattern[0]*tile_size)



# Defining Full piece class
class piece():

    def __init__(self, identifier):
        self.color = r.choice(colors)
        self.pattern = r.choice(patterns)
        self.id = identifier
        self.tiles = []
        self.control = "active"
        self.cooldown1 = 0
        self.cooldown2 = 0
        self.root_pos = [50, -50]
        self.orient_pointer = 0
        self.state = "falling"

        # Making tiles
        counter = 0
        for coord in self.pattern[self.orient_pointer % len(self.pattern)]:
            myTile = tile(self.color, self.root_pos[0] + coord[0]*tile_size, self.root_pos[1] + coord[1]*tile_size, self.id, counter)
            self.tiles.append(myTile)
            tile_group.add(myTile)
            counter += 1

    def update(self):

        # Initialising Variables
        collision = False
        dx = 0
        dy = 2
        key = pg.key.get_pressed()
        self.cooldown1 -= 1
        self.cooldown2 -= 1

        # X movement
        key = pg.key.get_pressed()

        # Updating piece list
        self.tiles = []
        for tile in tile_group:
            if tile.id == self.id:
                self.tiles.append(tile)


        # --- While Player Controlled --- #
        if self.control == "active":

            if key[pg.K_LEFT] and self.cooldown1 <= 0:
                dx = -50
                self.cooldown1 = 5
            if key[pg.K_RIGHT] and self.cooldown1 <= 0:
                dx = 50
                self.cooldown1 = 5
        
            # Checking X collsion
            for tile in self.tiles:
                collision, dx = tile.check_collision_x(dx)
                if collision:
                    break

            self.root_pos[0] += dx


            # Speed Down
            if key[pg.K_DOWN]:
                dy = 25


            # Tile Rotaion
            if key[pg.K_SPACE] and self.cooldown2 <= 0:
                self.orient_pointer += 1
                self.cooldown2 = 10
                cancel = False
                # Checking for collision
                for tile in self.tiles:

                        # New Coords
                        tile_y = self.root_pos[1] + int(self.pattern[self.orient_pointer % len(self.pattern)][tile.id2][1])*tile_size
                        tile_x = self.root_pos[0] + int(self.pattern[self.orient_pointer % len(self.pattern)][tile.id2][0])*tile_size

                        # Other tile collision
                        for otherTile in tile_group:
                            if otherTile.id != tile.id:
                                if otherTile.rect.colliderect(tile_x, tile_y, 50, 50):
                                    cancel = True
                                    break

                        # Bounds check x
                        if tile_x > 450:
                            cancel = True
                            break
                        elif tile_x < 0:
                            cancel = True
                            break

                        # Bounds check y
                        if tile_y > 950:
                            cancel = True
                            break
                        elif tile_y < 0:
                            cancel = True
                            break
                
                if cancel == True:
                    self.orient_pointer -= 1
                    self.cooldown2 = 0


        for tile in self.tiles:
            collision, dy = tile.check_collision_y(dy)
            if collision:
                self.control = "collision"
                break

        # Updating Tile Root Pos
        self.root_pos[1] += dy

        # Moving tiles
        for tile in self.tiles:
            tile.update(self.pattern[self.orient_pointer % len(self.pattern)][tile.id2], self.root_pos)

        # Controlable
        if self.control == "collision":
            self.control = "expired" 
            return True
        return False


class inactive_piece():

    def __init__(self, tile_list, id):

        self.tiles = tile_list
        self.id = id
        self.state = "stationary"

    def update(self):

        # Initialising Variables
        global piece_counter
        collision = False
        dy = 2

        # Updating piece list
        self.tiles = []
        for tile in tile_group:
            if tile.id == self.id:
                self.tiles.append(tile)

        # --- Split Check --- #
        present_tiles = []
        for x in self.tiles:
            present_tiles.append(x.id2)
        if len(self.tiles) == 2 or len(self.tiles) == 3:
            if 1 not in present_tiles and 0 in present_tiles:
                piece_counter += 1
                self.tiles[present_tiles.index(0)].id = piece_counter
                inactive_pieces.append(inactive_piece(self.tiles[present_tiles.index(0)], piece_counter))
                del(self.tiles[present_tiles.index(0)])

            present_tiles = []
            for x in self.tiles:
                present_tiles.append(x.id2)

            if 2 not in present_tiles and 3 in present_tiles:
                piece_counter += 1
                self.tiles[present_tiles.index(3)].id = piece_counter
                inactive_pieces.append(inactive_piece(self.tiles[present_tiles.index(3)], piece_counter))
                del(self.tiles[present_tiles.index(3)])
     
        # Checking y collision
        for tile in self.tiles:
            collision, dy = tile.check_collision_y(dy)
            if collision == True:
                break
        
        for tile in self.tiles:
            tile.rect.y += dy
        
        if dy > 0:
            self.state = "falling"
        else:
            self.state = "stationary"
        
        for tile in self.tiles:
            tile.state = self.state



# --- Scoring System --- #
class utility:

    def __init__(self):
        self.rect = pg.Rect((1, 1), (500, 1))
        self.score = 0

    def update(self):
        draw_text(str(self.score), score_font, (255, 255, 255), tile_size, 15)

    def check_row(self):
        for row in range(20):
            
            self.rect.y = row*50+5
            collisions = 0

            for tile in tile_group:
                if self.rect.colliderect(tile.rect.x, tile.rect.y, tile.width, tile.height) and tile.state == "stationary":
                    collisions += 1
            
            if collisions == 10:
                for tile in tile_group:
                    if self.rect.colliderect(tile.rect.x, tile.rect.y, tile_size, tile_size):
                        tile.kill()
                self.score += 10



active_piece = piece(piece_counter)
game_engine = utility()

# Game Loop
run = True
game_over = False
while run:

    clock.tick(fps)
    screen.fill((0, 0, 0))
    #draw_grid()
    game_engine.update()


    #  Updating Game
    if not game_over:

        for x in inactive_pieces:
            x.update()

        # 'Retiring' Piece
        if active_piece.update():

            inactive = inactive_piece(active_piece.tiles, active_piece.id)
            inactive_pieces.append(inactive)
            del(active_piece)
            
            # Advancing id counter
            piece_counter += 1
            active_piece = piece(piece_counter)

        game_engine.check_row()

        # checking game end
        for x in tile_group:
            if x.rect.y == -50:
                game_over = True


    for event in pg.event.get():

        # Exiting window
        if event.type == pg.QUIT:
            run = False
 
    tile_group.draw(screen)
    pg.display.update()
