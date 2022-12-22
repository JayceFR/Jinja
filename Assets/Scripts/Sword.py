import pygame
import math 
import random

class sword():
    def __init__(self, x, y, width, height, image) -> None:
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.image = image
        self.facing_left = False
        self.display_x = 0
        self.display_y = 0
    
    def update(self, player_loc, facing_left):
        self.facing_left = facing_left
        if not self.facing_left:
            self.rect.x = player_loc[0] + 12
        else:
            self.rect.x = player_loc[0] - 12
        self.rect.y = player_loc[1] 
    
    def blit(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        if not self.facing_left:
            display.blit(self.image, self.rect)
        else:
            flip = self.image.copy()
            flip = pygame.transform.flip(flip, True, False)
            display.blit(flip, self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def attack(self):
        return self.rect