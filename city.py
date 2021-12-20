import pygame
from config import *

class City():
    def __init__(self, number, max_cities):
        self.pos = (number * SCREENSIZE[0] // (max_cities + 1), SCREENSIZE[1] - GROUND_LEVEL)   # set position of the cities
        self.color = CITY
        self.size = 10
        self.destroyed = False      # might not be needed if I just remove city from list

    def draw(self, screen):
        # might not be needed if I just remove city from list
        if self.destroyed != True:
            return pygame.draw.circle(screen, self.color, self.pos, self.size)
    
    def update(self):
        pass

    # might not be needed if I just remove city from list
    def set_destroyed(self, status):
        self.destroyed = status
    
    # might not be needed if I just remove city from list
    def get_destroyed(self):
        return self.destroyed

    def get_pos(self):
        return self.pos
