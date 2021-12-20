import pygame
from config import *


class Explosion():
    def __init__(self, pos, points_multiplier = 0, blast_radius = 50, blast_color = NUKE_EXPLOSION, expand_rate = 3, dwell_time = 0):
        self.pos = pos                              # blast centre
        self.points_multiplier = points_multiplier  # only intercepters have multiplier > 0 so only valid intercepts result in score
        self.blast_radius = blast_radius            # maximum radius of blast
        self.blast_color = blast_color              # colour of explosion
        self.expand_rate = expand_rate              # speed of expansion
        self.dwell_time =  dwell_time                # time to stay at maximum radius
        self.radius = 0                             # current radius of explosion
        self.complete = False                       # is the explosion finished
    
    # draw the explosion
    def draw(self, screen):
        return pygame.draw.circle(screen, 
                            self.blast_color, 
                            self.pos, 
                            self.radius)

    # explosion logic
    def update(self):
        if not self.complete:
            self.radius += self.expand_rate
        if self.radius > self.blast_radius:
            #self.radius = 0
            self.complete = True
    
    # return the centre for distance / collision calculations
    def get_center(self):
        return self.pos
    
    # return the current blast radius for distance / collision calculations
    def get_radius(self):
        return self.radius
        
    def get_points_multiplier(self):
        return self.points_multiplier