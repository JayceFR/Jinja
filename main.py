import pygame
import Assets.Scripts.framework as framework
pygame.init()
s_width = 1000
s_height = 600
screen = pygame.display.set_mode((s_width,s_height))
display = pygame.Surface((s_width//2, s_height//2))
#Game Variables
run = True
clock = pygame.time.Clock()
#Loading Images
tile_1 = pygame.image.load("./Assets/Tiles/tile1.png").convert_alpha()
tile_2 = pygame.image.load("./Assets/Tiles/tile2.png").convert_alpha()
tile_3 = pygame.image.load("./Assets/Tiles/tile3.png").convert_alpha()
tile_4 = pygame.image.load("./Assets/Tiles/tile4.png").convert_alpha()
tile_5 = tile_4.copy()
tile_5 = pygame.transform.flip(tile_5, True, False)
tile_6 = pygame.image.load("./Assets/Tiles/tile5.png").convert_alpha()
tiles = [tile_1, tile_2, tile_3, tile_4, tile_5, tile_6]
#Map
map = framework.Map("./Assets/Maps/map.txt", tiles)
#Player 
player = framework.Player(50,50,16,16)
#Scroll
true_scroll = [0,0]
scroll = [0,0]
while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((0,0,0))
    #Blitting The Map
    tile_rects = map.blit_map(display, scroll)
    #Calculating scroll
    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 241) / 20
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 166) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #Moving the Player
    player.move(tile_rects, time)
    #Drawing the Player
    player.draw(display, scroll)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    surf = pygame.transform.scale(display, (s_width, s_height))
    screen.blit(surf, (0,0))
    pygame.display.update()