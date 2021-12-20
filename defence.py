import pygame
import math
from config import *
from missile import Missile


class Defence():
    def __init__(self):
        self.pos = (SCREENSIZE[0] // 2, SCREENSIZE[1] - GROUND_LEVEL)
        self.target_pos = pygame.mouse.get_pos()            # mouse pointer is target point
        self.gun_end = self.pos                             # end point of gun barrel - will be set to correct value on first update
        self.gun_size = 18                                  # lenght of gun barrel
        self.color = DEFENCE                                # colour of the defence turret
        self.x = self.target_pos[0] - self.pos[0]           # distance from x origin to x target
        self.y = self.target_pos[1] - self.pos[1]           # distance from y origin to y target
        self.m = 0                                        # slop of gun barrel - will be set to correct value on first update
        self.angle = math.atan(self.m)                      # angle of gun barrel
        self.destroyed = False                              # has the defence been destroyed
        self.ammo = 30                                      # number of missiles
        

    def draw(self, screen):
        # draw the base
        pygame.draw.circle(screen, 
                            self.color, 
                            self.pos, 
                            8)
        # draw the launcher
        pygame.draw.line(screen, 
                        self.color, 
                        self.pos, 
                        self.gun_end, 
                        3)
    
    def update(self):
        # update target point to wherever mouse is pointed
        self.target_pos = pygame.mouse.get_pos()
        # calculate line to target point
        self.x = self.target_pos[0] - self.pos[0]       # distance from x origin to x target
        self.y = self.target_pos[1] - self.pos[1]       # distance from y origin to y target
        if self.y != 0:
            self.m = self.x / self.y                    # slop of gun barrel
        self.angle = math.atan(self.m) + math.pi        # angle of gun barrel
        self.gun_end = (self.pos[0] + int(self.gun_size * math.sin(self.angle)), 
                        self.pos[1] + int(self.gun_size * math.cos(self.angle)))

    def shoot(self, missile_list):
        if self.ammo > 0:
            # create new missile(origin, target, false=launch up, speed, points, trail color, warhead color)
            missile_list.append(Missile(self.pos, self.target_pos, False, 8, 0, INTERCEPTER_TRAIL, INTERCEPTER))
            self.ammo -= 1
    
    def get_ammo(self):
        return self.ammo
    
    def set_ammo(self, ammo):
        self.ammo = ammo