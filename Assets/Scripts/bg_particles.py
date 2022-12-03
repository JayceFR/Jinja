import pygame
import math
import random


class Master():
    def __init__(self) -> None:
        self.particles = []
        self.particle_generation_cooldown = 100
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
    
    def move(self, time):
        self.x += math.sin(time) + 5
        self.y += self.gravity
        if self.x > 1000 or self.y > 600:
            self.alive = False

    def draw(self, display):
        pygame.draw.circle(display, (120,0,0), (self.x, self.y), 3)