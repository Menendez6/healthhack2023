#! /usr/bin/env python

from enum import Enum
import os
import sys
import random
import pygame
import serial
import time
from maze.text_to_speech import text_to_speech
from maze.maze_generator import generate_maze

# GLOBAL VARIABLES FOR THE GAME -----------------------------------
# Maze Dims
N = 6
M = 6
ROWS = 2*N + 1
COLUMNS = 2*M + 1

# Pygame Dims
SCREEN_WIDTH = 666
SCREEN_HEIGHT = 500
OBJECT_SIZE = SCREEN_HEIGHT // ROWS

# Media
AUDIO_DIR = "media/audio/"
SOUND_LIBRARY = {
    "animations": {
        "monster": "monster.mp3", "game_over": "game_over_track.mp3"
    },
    "introduction_tracks": {
        "base": "introduction-track-1_1.mp3",
        "pirates": "intro-track-2_pirates.mp3",
        "starwars": "intro-track-3-_starwars.mp3",
    },
    "other_tracks": {
        "instructions": "instructions.mp3",
    },
    "temp": {
        "text_to_speech": "speech.mp3",
    }
}
SOUND_LIBRARY = {
    k: {k2: os.path.join(AUDIO_DIR, v2) for k2, v2 in v.items()}
    for k, v in SOUND_LIBRARY.items()
}
# ----------------------------------------------------------------

# ARDUINO COMMUNICATION ------------------------------------------
# We need to set a signal when the game starts and when the game finishes
try:
    arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600,timeout=0.05)
except:
    print("Not connected_arduino")
# ----------------------------------------------------------------

# UTILS ------------------------------------------------------------


def write_read(x):
    try:
        arduino.write(bytes(x, 'utf-8'))
        print(x)
        time.sleep(0.05)
        data = arduino.readline()
        print(data)
        return data
    except:
        print("No arduino")

'''while True:
    write_read('1')
    time.sleep(1)
    write_read('2')
    time.sleep(1)
    write_read('4')
    time.sleep(1)'''

def reproduce_file(sound_file):
    sound = pygame.mixer.Sound(sound_file)
    sound.play()    


def play_text_as_sound(text: str):
    text_to_speech(text, SOUND_LIBRARY["temp"]["text_to_speech"])
    reproduce_file(SOUND_LIBRARY["temp"]["text_to_speech"])
# ----------------------------------------------------------------

# GAME UTILS ------------------------------------------------------
def play_instructions():
    reproduce_file(SOUND_LIBRARY["other_tracks"]["instructions"])

# GAME CLASSES ----------------------------------------------------


class Monster_Proximity(Enum):
    SUPER_CLOSE = 1
    CLOSE = 2
    FAR = 3


# Class for the orange dude
class Player(object):

    def __init__(self):
        self.rect = pygame.Rect(OBJECT_SIZE, OBJECT_SIZE,
                                OBJECT_SIZE, OBJECT_SIZE)
        self.hasKey = False
        self.counter = 0
        self.monster_proximity = Monster_Proximity.FAR
        self.position = [(self.rect.left)//OBJECT_SIZE,
                         (self.rect.top)//OBJECT_SIZE]
        self.allow_move= True
        self.counter = 0

    def move(self, dx, dy):
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0 and self.allow_move:
            self.move_single_axis(dx, 0)
        if dy != 0 and self.allow_move:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):

        # Move the rect
        self.rect.x += dx
        self.rect.y += dy
        self.position = [(self.rect.left)//OBJECT_SIZE,
                         (self.rect.top)//OBJECT_SIZE]

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                self.rect.x -= dx
                self.rect.y -= dy
                if dx > 0:  # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                    value = write_read('2')
                    self.rect
                if dx < 0:  # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                    value = write_read('4')
                if dy > 0:  # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                    value = write_read('3')
                if dy < 0:  # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
                    value = write_read('1')

        if self.rect.colliderect(door.rect) and not player.hasKey:
            self.rect.x -= dx
            self.rect.y -= dy
            if dx > 0:  # Moving right; Hit the left side of the wall
                self.rect.right = door.rect.left
                value = write_read('2')
            if dx < 0:  # Moving left; Hit the right side of the wall
                self.rect.left = door.rect.right
                value = write_read('4')
            if dy > 0:  # Moving down; Hit the top side of the wall
                self.rect.bottom = door.rect.top
                value = write_read('3')
            if dy < 0:  # Moving up; Hit the bottom side of the wall
                self.rect.top = door.rect.bottom
                value = write_read('1')
        
        self.position = [(self.rect.left)//OBJECT_SIZE, (self.rect.top)//OBJECT_SIZE]
        
        print(f"Player position {self.rect.x, self.rect.y}")
        print(f"Player position {player.position}")

    def distance_x(self, obj):
        return (self.position[0] - obj.position[0])

    def distance_y(self, obj):
        return (self.position[1] - obj.position[1])

    # calculate the degree of closeness of the monster to the player
    def monster_distance(self, monster, dist_ant):
        if monster.position == None:
            return
        dist_x = abs(self.distance_x(monster))
        dist_y = abs(self.distance_y(monster))
        dist = (dist_x**2 + dist_y**2)**(1/2)
        sound = pygame.mixer.Sound(SOUND_LIBRARY["animations"]["monster"])
        if dist <= 1 and dist_ant > 1:
            self.monster_proximity = Monster_Proximity.SUPER_CLOSE
            print('super_close')
            sound.set_volume(1)
            sound.play()
        elif 1 < dist <= 2 and (dist_ant <= 1 or dist_ant > 2):
            self.monster_proximity = Monster_Proximity.CLOSE
            print('close')
            sound.set_volume(0.3)
            sound.play()
        elif 2 < dist <= 3 and (dist_ant <= 2 or dist_ant > 3):
            print('far')
            self.monster_proximity = Monster_Proximity.FAR
            sound.set_volume(0.1)
            sound.play()
        return dist

    def info(self):  # gives information on obstacles around the current position

        # def monster_check (self):
        x = self.position[0]
        y = self.position[1]

        up = [x, y - 1]
        down = [x, y + 1]
        left = [x - 1, y]
        right = [x + 1, y]
        
        commandmsg = ""
        for wall in walls:
            msg = ""
            if wall.position == up:
                print("Il y a un mur en haut")
                msg += "Mur en haut"
            elif wall.position == down:
                print("Il y a un mur en bas")
                msg += "Mur en bas"
            elif wall.position == left:
                print("Il y a un mur à gauche")
                msg += "Mur à gauche"
            elif wall.position == right:
                print("Il y a un mur à droite")
                msg += "Mur à droite"
            commandmsg += msg + " "

        for monster in monsters:
            if monster.position == up:
                print("Il y a un monstre en haut!")
                msg += "Monstre en haut"
            elif monster.position == down:
                print("Il y a un monstre en bas!")
                msg += "Monstre en bas"
            elif monster.position == left:
                print("Il y a un monstre à gauche!")
                msg += "Monstre à gauche"
            elif monster.position == right:
                print("Il y a un monstre à droite!")
                msg += "Monstre à droite"
            commandmsg += msg + " "
        if commandmsg.replace(" ", "") == "":
            commandmsg = "Rien autour de vous"
        play_text_as_sound(commandmsg)

    def hint(self):
        if self.hasKey:
            dist_x_objective = self.distance_x(door)
            dist_y_objective = self.distance_y(door)
            objective = "sortie"
        else:
            dist_x_objective = self.distance_x(key)
            dist_y_objective = self.distance_y(key)
            objective = "clé"
        if dist_x_objective < 0:
            dist_x_objective = str(abs(dist_x_objective)) + " cases à droite"
        else:
            dist_x_objective = str(abs(dist_x_objective)) + " cases à gauche"
        if dist_y_objective < 0:
            dist_y_objective = str(abs(dist_y_objective)) + " cases en bas"
        else:
            dist_y_objective = str(abs(dist_y_objective)) + " cases en haut"
        message = "la " + objective + " est " + \
            dist_x_objective + " et " + dist_y_objective
        print("la", objective, "est", dist_x_objective, "et", dist_y_objective)
        play_text_as_sound(message)

    def kill_monster(self, monster):
        player.allow_move = True
        monster.rect = pygame.Rect(x, y, 0, 0) #A bit hardcoded to delete the monster, this has to be changed
        #hackillo ...
        monsters = []
        monster.position = None
        self.counter = 0


class Key(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], OBJECT_SIZE//2, OBJECT_SIZE//2)
        self.position = [(self.rect.left)//OBJECT_SIZE,
                         (self.rect.top)//OBJECT_SIZE]


class Monster(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], OBJECT_SIZE, OBJECT_SIZE)
        self.position = [(self.rect.left)//OBJECT_SIZE,
                         (self.rect.top)//OBJECT_SIZE]
        monsters.append(self)


class Door(object):
    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], OBJECT_SIZE, OBJECT_SIZE)
        self.position = [(self.rect.left)//OBJECT_SIZE,
                         (self.rect.top)//OBJECT_SIZE]


# Nice class to hold a wall rect
class Wall(object):

    def __init__(self, pos):
        self.rect = pygame.Rect(pos[0], pos[1], OBJECT_SIZE, OBJECT_SIZE)
        self.position = [(self.rect.left)//OBJECT_SIZE, (self.rect.top)//OBJECT_SIZE]
        walls.append(self)
# ----------------------------------------------------------------


# GAME LOGIC ------------------------------------------------------
# First we randomly select a story

# def select_narrative():

#  def start_game():

pygame.mixer.init()
selected_track = random.choice(
    list(SOUND_LIBRARY["introduction_tracks"].values()))
#reproduce_file(selected_track)


# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get the key to exit the maze !")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
walls = []  # List to hold the walls
monsters = []  # list to hold the monsters (letterM)
player = Player()  # Create the player

# Holds the level layout in a list of strings.
# for reference
# level = [
#     "WWWWWWWWWWWWWWWWWWWW",
#     "W                  W",
#     "W         WWWWWW   W",
#     "W   WWWW       W   W",
#     "W   W        WWWW  W",
#     "W WWW  WWWW        W",
#     "W   W     W W      W",
#     "W   W     W   WW   D",
#     "W   WWW WWW   M W  W",
#     "W     W   W   W W  W",
#     "WWW   W   WWWWW W  W",
#     "W W      WW        W",
#     "W W   WWWW   WWW   W",
#     "W     W    E   W   W",
#     "WWWWWWWWWWWWWWWWWWWW",
# ]

level = generate_maze(N, M)

print(len(level))
print(len(level[0]))
for row in level:
    print(row)

# Parse the level string above. W = wall, E = exit key, M = monster
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            # end_rect = pygame.Rect(x, y, 16, 16)
            # end_rect = pygame.Rect(x, y, 16, 16)
            key = Key((x, y))
        if col == "M":
            # monster_rect = pygame.Rect(x,y,16,16)
            monster = Monster((x, y))
        if col == "D":
            # door_rect = pygame.Rect(x,y,32,32)
            door = Door((x, y))
        x += OBJECT_SIZE  # 16
    y += OBJECT_SIZE  # 16
    x = 0

move_left = False
move_right = False
move_up = False
move_down = False
running = True

dist = 100

while running:

    clock.tick(60)
    for monster in monsters:
        dist = player.monster_distance(monster, dist)
        # print(player.monster_distance)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            print("LOL")
            sys.exit()

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_s and player.rect.colliderect(monster.rect):
                player.kill_monster(monster)
            if e.key == pygame.K_SPACE:
                player.hint()
            if e.key == pygame.K_a:
                print("A")
                player.info()
            if e.key == pygame.K_LEFT:
                player.move(-OBJECT_SIZE, 0)
            if e.key == pygame.K_RIGHT:
                player.move(OBJECT_SIZE, 0)
            if e.key == pygame.K_UP:
                player.move(0, -OBJECT_SIZE)
            if e.key == pygame.K_DOWN:
                player.move(0, OBJECT_SIZE)
            if e.key == pygame.K_r:
                play_instructions()

    if player.rect.colliderect(door.rect) and player.hasKey:
        pygame.quit()
        sys.exit()

    #We should add here a block movement variable blocks the character until you kill him or die
    if player.rect.colliderect(monster.rect):
        player.allow_move = False
        if player.counter == 0:
            play_text_as_sound("Monstre, combat")
            while pygame.mixer.get_busy() == True:
                time.sleep(0.01)

        player.counter += 1
        if (player.counter >= 100):
            sound = pygame.mixer.Sound(SOUND_LIBRARY["animations"]["game_over"])
            sound.set_volume(1)
            sound.play()
            while pygame.mixer.get_busy() == True:
                time.sleep(0.1)
            pygame.quit()
            sys.exit()

    if player.rect.colliderect(key.rect):
        key.rect = pygame.Rect(x, y, 0, 0)  # makes key disappear
        player.hasKey = True
        play_text_as_sound("Vous avez trouvé la clé, recherche de la porte")

    # Draw the scene
    screen.fill((0, 0, 0))  # color bg
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
 # color wall
    pygame.draw.rect(screen, (255, 200, 0), key.rect)  # color end box
    pygame.draw.rect(screen, (255, 0, 0), player.rect)
    pygame.draw.rect(screen, (100, 149, 237), monster.rect)
    pygame.draw.rect(screen, (102, 76, 40), door.rect)
    # pygame.image.load("/char.gif")
    # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
    pygame.display.flip()
    clock.tick(360)

# ----------------------------------------------------------------
pygame.quit()
