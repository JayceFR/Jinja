import pygame
from pygame.locals import *
class Wave():
    def __init__(self,x,y,width,height, radius, facing_down) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        if facing_down:
            self.offset = -80
        else:
            self.offset = 100
        self.molecule_pos = []
        self.radius = radius
        self.molecules = []
        for x in range(width):
            self.molecules.append(Molecule(self.x, self.y, False, False))
            self.x += self.radius * 2
        self.molecules[width-1].it_is_last()
        self.molecules[0].it_is_last()
        self.molecules[10].colliding = True

    def chain_call(self, display, scroll):
        self.molecule_pos = []
        for pos, molecule in enumerate(self.molecules):
            if molecule.energy_transfer == True:
                molecule.energy_transfer = False
                if pos + 1 < len(self.molecules):
                    self.molecules[pos+1].colliding = True
                if pos - 1 >= 0:
                    self.molecules[pos - 1].colliding = True
                    self.molecules[pos - 1].from_right = True
                #else:
                    #self.molecules[len(self.molecules)-1].colliding = True
            molecule.oscillation()
            self.molecule_pos.append(list((molecule.get_loc()[0] - scroll[0], molecule.get_loc()[1] - scroll[1])))
            self.molecule_pos.append(list((molecule.get_og_x() - scroll[0], molecule.get_og_y() + self.offset  - scroll[1])))
        pygame.draw.polygon(display, (0,0,0), self.molecule_pos, 50)

class Molecule():
    def __init__(self, x ,y, from_left, from_right) -> None:
        self.x = x
        self.y = y
        self.og = [x,y]
        self.colliding = False
        self.energy_transfer = False
        self.tension = y - 50
        self.original_stage = y
        self.from_left = from_left
        self.from_right = from_right

    def oscillation(self):
        if self.colliding:
            self.y -= 5
            if self.y < self.tension:
                self.colliding = False
                self.energy_transfer = True
        if not self.colliding:
            if self.y < self.original_stage:
                self.y += 5

    def draw(self, display):
        pygame.draw.circle(display, (19,19,19), (self.x, self.y), 5)

    def get_og_x(self):
        return self.og[0]

    def get_og_y(self):
        return self.og[1]

    def get_loc(self):
        return [self.x, self.y]

    def collision(self):
        self.colliding = True

    def it_is_last(self):
        self.is_last = True

'''display = pygame.display.set_mode((1000,600))
run = True
water = Wave(250,200,40,5,5)
click = False
clock = pygame.time.Clock()
while run:
    clock.tick(60)
    display.fill((0,0,0))
    m_pos = pygame.mouse.get_pos()
    water.chain_call(display)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                click = True
    pygame.display.update()'''
