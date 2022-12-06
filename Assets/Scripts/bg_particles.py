import pygame
import math
import random
from pygame.locals import *

class Master():
    def __init__(self) -> None:
        self.particles = []
        self.particle_generation_cooldown = 2000
        self.particle_generation_last_update = 0

    def add_particles(self):
        self.particles.append(Particles(random.randint(0,1000)//2, random.randint(0,50)//2, 5))
    
    def recursive_call(self, time, display):
        if self.particles != []:
            for pos, particle in sorted(enumerate(self.particles), reverse=True):
                particle.move(time)
                particle.draw(display)
                if not particle.alive:
                    self.particles.pop(pos)
        if time - self.particle_generation_last_update > self.particle_generation_cooldown:
            self.particle_generation_last_update = time
            self.add_particles()


class Particles():
    def __init__(self, x, y, speed) -> None:
        self.x = x
        self.y = y
        self.speed = speed
        self.gravity = 5
        self.alive = True
        self.angle = random.randint(0,360)
        self.angle_change_cooldown = 100
        self.angel_change_last_update = 0
        self.radius = 3
    
    def move(self, time):
        if time - self.angel_change_last_update > self.angle_change_cooldown:
            self.angel_change_last_update = time
            self.angle += random.randint(0,10)
            if self.angle > 360:
                self.angle = 0  
        self.x += math.sin(math.radians(self.angle))
        self.y += 0.5
        if self.x > 1000 or self.y > 600:
            self.alive = False

    def draw(self, display):
        pygame.draw.circle(display, (255, 255, 255), (self.x, self.y), self.radius)
        self.radius *= 2
        display.blit(self.circle_surf(), (int(self.x- self.radius), int(self.y - self.radius)), special_flags=BLEND_RGB_ADD)
        self.radius /= 2
    
    def circle_surf(self):
        surf = pygame.Surface((self.radius * 2, self.radius * 2))
        pygame.draw.circle(surf, (20, 20, 60), (self.radius, self.radius), self.radius)
        surf.set_colorkey((0, 0, 0))
        return surf