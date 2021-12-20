import pygame
import math
from config import *
from functions import *
from explosion import Explosion


class Missile():
    def __init__(self, origin_pos, target_pos, incoming = True, speed = 1, points = 10, trail_color = WARHEAD_TRAIL, warhead_color = WARHEAD):
        self.origin_pos = origin_pos                # starting position of missile
        self.target_pos = target_pos                # end position of missile
        if incoming == True:                        # is this missile incoming (1 = yes[default], -1 = no)
            self.incoming = 1
        else:
            self.incoming = -1                  
        self.speed = speed                          # missile speed
        self.points = points                        # points awarded for destroying missile
        self.travel_dist = 1                        # distance traveled by missile
        self.warhead_color = warhead_color          # warhead colour
        self.trail_color = trail_color              # missile trail colour
        self.warhead_size = 2                       # warhead display size
        self.trail_width = 1                        # missile trail width
        self.pos = origin_pos                       # current position of warhead
        self.x = target_pos[0] - origin_pos[0]      # distance from x origin to x target
        self.y = target_pos[1] - origin_pos[1]      # distance from y origin to y target
        if self.y != 0 :
            self.m = self.x / self.y                # slop of missile trajectory
        else:
            self.m = 1
        self.angle = math.atan(self.m)              # angle of missile trajectory
        self.dist_to_target = distance(
                                origin_pos, 
                                target_pos)         # full distance to target position
        self.detonated = False                      # has the missile detonated
        
    # draw the missile and trail
    def draw(self, screen):
        # draw the missile trail
        pygame.draw.line(screen, 
                        self.trail_color, 
                        self.origin_pos, 
                        self.pos, 
                        self.trail_width)
        # draw the warhead
        pygame.draw.circle(screen, 
                        self.warhead_color, 
                        self.pos, 
                        self.warhead_size)

    # update missile logic
    def update(self, explosion_list):
        if not self.detonated:
            self.pos = (self.origin_pos[0] + int(self.travel_dist * math.sin(self.angle) * self.incoming), 
                        self.origin_pos[1] + int(self.travel_dist * math.cos(self.angle) * self.incoming))
            self.travel_dist += self.speed
        # reached target point, now detonate
        if self.travel_dist > self.dist_to_target and not self.detonated:
            self.explode(explosion_list)
    
    # detonate and create explosion
    def explode(self, explosion_list):
        self.detonated = True
        if self.incoming != 1:
            points_multiplier = 1
            explosion_radius = INTERCEPT_RADIUS
            explosion_color = INTERCEPT_EXPLOSION
        else:
            points_multiplier = 0
            explosion_radius = NUKE_RADIUS
            explosion_color = NUKE_EXPLOSION

        explosion_list.append(Explosion(self.pos, points_multiplier, explosion_radius, explosion_color))

    # return the current position
    def get_pos(self):
        return self.pos

    def get_points(self):
        return self.points
