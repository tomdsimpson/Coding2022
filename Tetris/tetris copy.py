# Tetris Game
# Started 05/04/22



# Importing modules
from typing import Counter
from matplotlib.pyplot import title
import pygame as pg
from pygame import mixer
import random as r
import pickle
pg.init()
mixer.pre_init(44100, -16, 2, 512)
mixer.init()

# Building game window (10x(20+3))
tile_size = 50
screen_width = tile_size * 10
screen_height = tile_size * 23

# Game variables
fps = 50
clock = pg.time.Clock()
colors = ["blue", "green", "red", "yellow"]
pickle_in = open("pattern_data", "rb")
patterns = pickle.load(pickle_in)
global piece_counter
piece_counter = 0
back_pos1 = 0
back_pos2 = 1151

# Fonts
title_font = pg.font.SysFont("Ubuntu", 60)
score_font = pg.font.SysFont("Ubuntu", 45)
menu_font = pg.font.SysFont("Ubuntu", 30)

# Colors
white = (255, 255, 255)

# Window Settings
screen = pg.display.set_mode((screen_width, screen_height))
pg.display.set_caption("Tetris")

# Initialising Tile group
tile_group = pg.sprite.Group()
inactive_pieces = []

# Images
restart_img = pg.image.load("./Images/Buttons/restart_btn.png").convert()
menu_img = pg.image.load("./Images/Buttons/quit_btn.png").convert()
play_img = pg.image.load("./Images/Buttons/play_btn.png").convert()
background1_img = pg.image.load("./Images/background1.png").convert_alpha()
background2_img = pg.image.load("./Images/background2.png").convert_alpha()

# Load Sounds
pg.mixer.music.load("./Sounds/backgroundMusic.wav")
#pg.mixer.music.play(-1, 0.0, 5000)
row_destroy = pg.mixer.Sound("./Sounds/completeRow.wav")



# --- Functions --- #
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

# --- Score Screen Functions --- #
# Find Min 2d array
def find_min(scores):
    minimum_score = scores[0][1]
    minimum_pos = 0
    for counter, x in enumerate(scores):
        if x[1] < minimum_score:
            minimum_score = x[1]
            minimum_pos = counter
    return minimum_score, minimum_pos

# Sorting Scores
def swap(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list

def sort_scores(max_scores):

    for x in range(1, len(max_scores)):
        value = max_scores[x][1]
        pointer = x-1
        while pointer >=0 and value > max_scores[pointer][1]:
            max_scores = swap(max_scores, pointer, pointer +1)
            pointer -= 1
    
    return max_scores



# --- Classes --- #
# Button class
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

# Text Input for scores
class Input_box():

    def __init__(self, x, y, w, font):
        super().__init__()
        self.color = white
        self.backcolor = None
        self.pos = (x, y) 
        self.width = w
        self.font = font
        self.active = True
        self.text = ""

    def update(self, event_list):

        # Functionality
        for event in event_list:
            if event.type == pg.KEYDOWN and self.active:
                if event.key == pg.K_RETURN:
                    self.active = False
                    game_engine.add_score(self.text)
                    self.text = ""
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if len(self.text) < 17:
                        self.text += event.unicode
        draw_text(self.text, self.font, self.color, self.pos[0], self.pos[1])

# Defining tile class
class Tile(pg.sprite.Sprite):

    def __init__(self, color, x, y, id, id2):
        pg.sprite.Sprite.__init__(self)

        self.image = pg.image.load(f"./Images/Tiles/{color}.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = tile_size
        self.height = tile_size
        self.id = id
        self.id2 = id2
        self.state = "falling"

    # Checking x and diagonal collisions
    def check_collision(self, dx, dy):

        x_col = False
        diag_col = False

        # Checking for y collision with tiles
        for tile in tile_group:

            # Self exception
            if tile.id == self.id:
                pass
            else:
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    x_col = True
                if tile.rect.colliderect(self.rect.x + dx, self.rect.y + dy, self.width, self.height):
                    diag_col = True

        if self.rect.x + dx < 0 or self.rect.x + dx > 450:
            x_col = True
            diag_col = True

        return x_col, diag_col

    # Checking y collisions
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

        if self.rect.y + dy > 1100:
            dy = 1150 - self.rect.bottom
            collision = True

        return collision, dy

    def update(self, pattern, pos):
        self.rect.y = pos[1] + (pattern[1]*tile_size)
        self.rect.x = pos[0] + (pattern[0]*tile_size)

# Defining Full piece class
class Piece():

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
            myTile = Tile(self.color, self.root_pos[0] + coord[0]*tile_size, self.root_pos[1] + coord[1]*tile_size, self.id, counter)
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


        if key[pg.K_LEFT] and self.cooldown1 <= 0:
            dx = -50
            self.cooldown1 = 5
        if key[pg.K_RIGHT] and self.cooldown1 <= 0:
            dx = 50
            self.cooldown1 = 5
        
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
                    if tile_y > 1100:
                        cancel = True
                        break                                                                                                                                                                                                   
                    elif tile_y < 0:
                        cancel = True
                        break
                
            if cancel == True:
                self.orient_pointer -= 1
                self.cooldown2 = 0

            for tile in self.tiles:
                tile.update(self.pattern[self.orient_pointer % len(self.pattern)][tile.id2], self.root_pos)

        # Checking collsion
        x_col = False
        xy_col = False
        for tile in self.tiles:
            a, b  = tile.check_collision(dx, dy)
            
            if a: x_col = True
            if b: xy_col = True
            
        if not xy_col:
            self.root_pos[0] += dx
            
            for tile in self.tiles:
                tile.update(self.pattern[self.orient_pointer % len(self.pattern)][tile.id2], self.root_pos)
            
            # Checking y collision
            for tile in self.tiles:
                collision, dy = tile.check_collision_y(dy)
                if collision == True:
                    break

        elif x_col:
            dx = 0
            self.root_pos[0] += dx

            for tile in self.tiles:
                tile.update(self.pattern[self.orient_pointer % len(self.pattern)][tile.id2], self.root_pos)

            # Checking y collision
            for tile in self.tiles:
                collision, dy = tile.check_collision_y(dy)
                if collision == True:
                    break

        elif not x_col:
            self.root_pos[0] += dx

            for tile in self.tiles:
                tile.update(self.pattern[self.orient_pointer % len(self.pattern)][tile.id2], self.root_pos)

            # Checking y collision
            for tile in self.tiles:
                collision, dy = tile.check_collision_y(dy)
                if collision == True:
                    break

        # Updating Tile Root Pos
        self.root_pos[1] += dy
        if dy <= 0:
            self.control = "collision"

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
        dx = 0

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
        elif dy < 0:
            print("What The")
        else:
            self.state = "stationary"
        
        for tile in self.tiles:
            tile.state = self.state



# --- Scoring System --- #
class utility:

    def __init__(self):
        self.rect = pg.Rect((1, 1), (500, 1))
        self.score = 0
        self.max_scores = [["Empty", 0] for x in range(10)]
        try:
            self.scores = open("scores.csv", "r")
        except:
            self.scores = open("scores.csv", "w")
            self.scores.close()
            self.scores = open("scores.csv", "r")

        for counter, line in enumerate(self.scores):
            line = (line.strip()).split(",")
            self.max_scores[counter][0] = line[0]
            self.max_scores[counter][1] = int(line[1])
        
        self.max_scores = sort_scores(self.max_scores)


    def show_score(self):
        draw_text("Score: " + (str(self.score)), score_font, white, 10, 10)

    def display_maxScores(self):
        draw_text("Tetris", title_font, white, 25, 100)
        draw_text("Top Scores", score_font, white, 50, 225)
        pg.draw.line(screen, white, (15, 160), (485, 160), 2)
        for counter, x in enumerate(self.max_scores):
            draw_text((f"{x[0]}   -------   {x[1]}"), menu_font, (255, 0, 50), 75, 80*counter+325)

    def add_score(self, name):
        # Checking if top 10 and replacing lowest score
        min_score, min_pos = find_min(self.max_scores)
        if self.score > min_score:
            self.max_scores[min_pos][0] = name
            self.max_scores[min_pos][1] = self.score
        self.max_scores = sort_scores(self.max_scores)

    def update_file(self):
        self.scores = open("scores.csv", "w")
        for x in range(10):
            self.scores.write(self.max_scores[x][0] + "," + str(self.max_scores[x][1]) + "\n")
        self.scores.close()

    def check_row(self):
        for row in range(20):
            
            self.rect.y = row*50+155
            collisions = 0

            for tile in tile_group:
                if self.rect.colliderect(tile.rect.x, tile.rect.y, tile.width, tile.height) and tile.state == "stationary":
                    collisions += 1
            
            if collisions == 10:
                for tile in tile_group:
                    if self.rect.colliderect(tile.rect.x, tile.rect.y, tile_size, tile_size):
                        tile.kill()
                self.score += 10
                row_destroy.play()


# Creating class instances
active_piece = Piece(piece_counter)
game_engine = utility()

restart_btn = Button(50, 50, restart_img)
menu_btn = Button(300, 50, menu_img)
play_btn = Button(225, 100, play_img)
quit_btn = Button(350, 100, menu_img)

score_box = Input_box(50, 450, 400, score_font)


# Game Loop
run = True
game_state = "menu"

while run:

    # Background and timing
    clock.tick(fps)
    screen.blit(background1_img, (0, back_pos1))
    screen.blit(background2_img, (0, back_pos2))
    #draw_grid()
    back_pos1 += 2
    back_pos2 += 2

    event_list = pg.event.get()

    # Checking if on screen
    if back_pos1 >= 1151:
        back_pos1 = -1150
    if back_pos2 >= 1151:
        back_pos2 = -1150

    #  Updating Game
    if game_state == "playing":
        
        for x in inactive_pieces:
            x.update()

        # 'Retiring' Piece
        if active_piece.update():
            inactive = inactive_piece(active_piece.tiles, active_piece.id)
            inactive_pieces.append(inactive)
            del(active_piece)

            # checking game end
            for x in inactive_pieces:
                for y in x.tiles:
                    if y.rect.y < 150:
                        game_state = "finished"

            # Adding new piece
            if game_state == "playing":
                piece_counter += 1
                active_piece = Piece(piece_counter)

        # Checking for complete rows and drawing
        pg.draw.line(screen, white, (0, tile_size*3), (screen_width, tile_size*3))
        tile_group.draw(screen)
        game_engine.check_row()
        game_engine.show_score()


    if game_state == "finished":

        #pg.draw.line(screen, white, (0, tile_size*3), (screen_width, tile_size*3))
        #tile_group.draw(screen)

        score_box.update(event_list)
        draw_text(f"You scored {game_engine.score} points!", score_font, white, 50, 200)
        pg.draw.line(screen, white, (0, 440), (500, 440))
        pg.draw.line(screen, white, (0, 510), (500, 510))
        draw_text("Enter Your Name:", menu_font, white, 50, 390)


        if restart_btn.draw():
            game_engine.score = 0
            tile_group.empty()
            for x in inactive_pieces:
                del(x)
            inactive_pieces = []
            active_piece = ""
            piece_counter = 0 
            active_piece = Piece(piece_counter)
            game_state = "playing"
            score_box.active = True

        if menu_btn.draw():
            game_engine.score = 0
            tile_group.empty()
            for x in inactive_pieces:
                del(x)
            inactive_pieces = []
            active_piece = ""
            piece_counter = 0
            active_piece = Piece(piece_counter)
            game_state = "menu"
            score_box.active = True



    if game_state == "menu":

        if play_btn.draw():
            game_state = "playing"
        
        if quit_btn.draw():
            run = False
        
        game_engine.display_maxScores()

    # Exit Functionality
    for event in event_list:
        if event.type == pg.QUIT:
            run = False
 
    # Displaying content
    pg.display.update()

# Updating File
game_engine.scores.close()
game_engine.update_file()
