import pygame
from pygame.locals import *
pygame.init()

class Flame():
    def __init__(self, x, y) -> None:
        self.radius = 10
        self.x = x 
        self.y = y

    def generate_surf(self):
        surf = pygame.Surface((self.radius*2, self.radius*2))
        pygame.draw.circle(surf, (255,150,45), (self.radius, self.radius), self.radius)
        surf.set_colorkey((0,0,0))
        return surf

    def draw(self, display):
        pygame.draw.circle(display, (255,128,0), (self.x, self.y), self.radius)
        self.radius *= 6
        display.blit(self.generate_surf(), (int(self.x - self.radius), int(self.y - self.radius)), special_flags=BLEND_RGBA_ADD)
        self.radius /= 6