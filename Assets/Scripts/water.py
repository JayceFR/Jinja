import pygame
from pygame.locals import *
import math
class Water():
    def __init__(self,x,y,width,height, radius) -> None:
        self.x = x 
        self.y = y
        self.width = width
        self.height = height
        self.radius = radius
        self.molecules = []
        self.molecule_pos = []
        for x in range(20):
            self.molecules.append(Molecule(self.x, self.y))
            self.x += self.radius * 2
        self.width = self.x + self.radius

    def chain_call(self, display):
        self.molecule_pos = []
        for pos, molecule in enumerate(self.molecules):
            if molecule.energy_transfer == True:
                molecule.energy_transfer = False
                if pos + 1 < len(self.molecules) and pos >= 10:
                    self.molecules[pos+1].colliding = True
                if pos - 1 >= 0 and pos <= 10:
                    self.molecules[pos - 1].colliding = True
            molecule.oscillation()
            self.molecule_pos.append(list((molecule.get_x(), molecule.get_y())))
            self.molecule_pos.append(list((molecule.get_x(), 300)))
            molecule.draw(display)
        #self.molecule_pos.append(list((self.molecules[0].get_x() - 5, self.molecules[0].get_y() + 20)))
        #self.molecule_pos.append(list((self.molecules[len(self.molecules)-1].get_x() + 5, self.molecules[len(self.molecules)-1].get_y() + 20)))
        return self.molecule_pos

    def colliding(self):
        self.molecules[10].colliding = True
    
class Molecule():
    def __init__(self, x ,y) -> None:
        self.x = x
        self.y = y
        self.colliding = False
        self.energy_transfer = False
        self.tension = y - 50
        self.angle = 0
        self.original_stage = y
    
    def oscillation(self):
        if self.colliding:
            self.y -= math.sin(math.radians(self.angle)) * 50
            self.angle = 50
            if self.angle > 360:
                self.angle = 0
            if self.y < self.tension:
                self.colliding = False
                self.energy_transfer = True
        if not self.colliding:
            self.angle = 0
            if self.y < self.original_stage:
                self.y += 5
    
    def draw(self, display):
        pass
        #pygame.draw.circle(display, (255,255,255), (self.x, self.y), 5)
    
    def get_x(self):
        return self.x

    def get_y(self):
        return self.y
    
    def collision(self):
        self.colliding = True

display = pygame.display.set_mode((1000,600))
run = True
water = Water(250,200,40,50,5)
click = False
clock = pygame.time.Clock()
colliding = False
collision_cooldown = 200
collision_last_update = 0
while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((0,0,0))
    m_pos = pygame.mouse.get_pos()
    coordinates = water.chain_call(display)
    pygame.draw.polygon(display, (0,0,150), coordinates, 9)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    key = pygame.key.get_pressed()
    if key[pygame.K_SPACE]:
        if time - collision_last_update > collision_cooldown:
            colliding = True
            collision_last_update = time
    if colliding:
        water.colliding()
        colliding = False
    pygame.display.update()
    