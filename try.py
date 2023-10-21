#! /usr/bin/env python

import os
import sys
import random
import pygame
import serial
import time

#We need to set a signal when the game starts and when the game finishes
arduino = serial.Serial(port='/dev/ttyACM0', baudrate=115200, timeout=.1)

def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

# Class for the orange dude
class Player(object):
    
    def __init__(self):
        self.rect = pygame.Rect(32, 32, 32, 32)
        self.hasKey = False
        self.counter = 0
        self.position = []

    def move(self, dx, dy):
        
        # Move each axis separately. Note that this checks for collisions both times.
        if dx != 0:
            self.move_single_axis(dx, 0)
        if dy != 0:
            self.move_single_axis(0, dy)

    def move_single_axis(self, dx, dy):
        
        # Move the rect
        self.rect.x += dx
        self.rect.y += dy

        # If you collide with a wall, move out based on velocity
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                if dx > 0: # Moving right; Hit the left side of the wall
                    self.rect.right = wall.rect.left
                    value = write_read('2')
                if dx < 0: # Moving left; Hit the right side of the wall
                    self.rect.left = wall.rect.right
                    value = write_read('4')
                if dy > 0: # Moving down; Hit the top side of the wall
                    self.rect.bottom = wall.rect.top
                    value = write_read('3')
                if dy < 0: # Moving up; Hit the bottom side of the wall
                    self.rect.top = wall.rect.bottom
                    value = write_read('1')

        if self.rect.colliderect(door_rect) and not player.hasKey:
            if dx > 0: # Moving right; Hit the left side of the wall
                self.rect.right = wall.rect.left
                value = write_read('2')
            if dx < 0: # Moving left; Hit the right side of the wall
                self.rect.left = wall.rect.right
                value = write_read('4')
            if dy > 0: # Moving down; Hit the top side of the wall
                self.rect.bottom = wall.rect.top
                value = write_read('3')
            if dy < 0: # Moving up; Hit the bottom side of the wall
                self.rect.top = wall.rect.bottom
                value = write_read('1')


# Nice class to hold a wall rect
class Wall(object):
    
    def __init__(self, pos):
        walls.append(self)
        #self.rect = pygame.Rect(pos[0], pos[1], 16, 16)
        self.rect = pygame.Rect(pos[0], pos[1], 32, 32)

# Initialise pygame
os.environ["SDL_VIDEO_CENTERED"] = "1"
pygame.init()

# Set up the display
pygame.display.set_caption("Get the key to exit the maze !")
screen = pygame.display.set_mode((666, 500))

clock = pygame.time.Clock()
walls = [] # List to hold the walls
player = Player() # Create the player

# Holds the level layout in a list of strings.
level = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W                  W",
    "W         WWWWWW   W",
    "W   WWWW       W   W",
    "W   W        WWWW  W",
    "W WWW  WWWW        W",
    "W   W     W W      W",
    "W   W     W   WW   D",
    "W   WWW WWW   M W  W",
    "W     W   W   W W  W",
    "WWW   W   WWWWW W  W",
    "W W      WW        W",
    "W W   WWWW   WWW   W",
    "W     W    E   W   W",
    "WWWWWWWWWWWWWWWWWWWW",
]

# Parse the level string above. W = wall, E = exit key, M = monster
x = y = 0
for row in level:
    for col in row:
        if col == "W":
            Wall((x, y))
        if col == "E":
            #end_rect = pygame.Rect(x, y, 16, 16)
            end_rect = pygame.Rect(x, y, 16, 16)
        if col == "M":
            #monster_rect = pygame.Rect(x,y,16,16)
            monster_rect = pygame.Rect(x, y, 32, 32)
        if col == "D": 
            door_rect = pygame.Rect(x,y,32,32)
        x += 32 #16
    y += 32 #16
    x = 0

move_left = False
move_right = False
move_up = False
move_down = False
running = True
while running:

    clock.tick(60)
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            running = False
        if e.type == pygame.KEYDOWN: 
            if e.key == pygame.K_LEFT:
                player.move(-32, 0)
            if e.key == pygame.K_RIGHT:
                player.move(32, 0)
            if e.key == pygame.K_UP:
                player.move(0, -32)
            if e.key == pygame.K_DOWN:
                player.move(0, 32)
            
    
    if player.rect.colliderect(door_rect) and player.hasKey:
        pygame.quit()
        sys.exit()
    
    if player.rect.colliderect(monster_rect):
        pygame.quit()
        sys.exit()

    if player.rect.colliderect(end_rect):
        end_rect = pygame.Rect(x, y, 0, 0) #makes key disappear
        player.hasKey = True

    # Draw the scene
    screen.fill((0, 0, 0)) #color bg
    for wall in walls:
        pygame.draw.rect(screen, (255, 255, 255), wall.rect)
 #color wall 
    pygame.draw.rect(screen, (255, 200, 0), end_rect) #color end box
    pygame.draw.rect(screen, (255, 0, 0), player.rect)
    pygame.draw.rect(screen, (100, 149, 237), monster_rect)
    pygame.draw.rect(screen,(102,76,40),door_rect )
    #pygame.image.load("/char.gif")
    # gfxdraw.filled_circle(screen, 255, 200, 5, (0,128,0))
    pygame.display.flip()
    clock.tick(360)

pygame.quit()