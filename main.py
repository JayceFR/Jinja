import pygame
import Assets.Scripts.framework as framework
import Assets.Scripts.background as backg
import math
import random 
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
tile_3 = tile_1.copy()
tile_3 = pygame.transform.flip(tile_3, True, False)
tile_4 = pygame.image.load("./Assets/Tiles/tile4.png").convert_alpha()
tile_5 = tile_4.copy()
tile_5 = pygame.transform.flip(tile_5, True, False)
tile_6 = pygame.image.load("./Assets/Tiles/tile5.png").convert_alpha()
tiles = [tile_1, tile_2, tile_3, tile_4, tile_5, tile_6]
player_img = pygame.image.load("./Assets/Sprites/player.png").convert_alpha()
player_img.set_colorkey((255,255,255))
#Map
map = framework.Map("./Assets/Maps/map.txt", tiles)
#Player 
player = framework.Player(50,50,player_img.get_width(),player_img.get_height(), player_img)
dash = False
extra_dash = True
check_for_dash = True
#Scroll
true_scroll = [0,0]
scroll = [0,0]
#Background Stripes 
bg = backg.background()
while run:
    clock.tick(60)
    time = pygame.time.get_ticks()
    display.fill((20,0,20))
    blur_surf = display.copy()
    bg.recursive_call(blur_surf)
    blur_surf.set_alpha(90)
    display.blit(blur_surf, (0,0))
    #Blitting The Map
    tile_rects = map.blit_map(display, scroll)
    #Calculating scroll
    true_scroll[0] += (player.get_rect().x - true_scroll[0] - 241) / 20
    true_scroll[1] += (player.get_rect().y - true_scroll[1] - 166) / 20
    scroll = true_scroll.copy()
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
    #Player Dash
    if dash:
        #Getting the mouse position
        mx , my = pygame.mouse.get_pos()
        mx = mx/2
        my = my/2
        m_pos = []
        m_pos.append(mx)
        m_pos.append(my)
        #Getting the 3rd vertex of the triangle
        point = (m_pos[0], player.get_rect().y + 16 - scroll[1])
        #Calculating distance between the points
        l1 = math.sqrt(math.pow((point[1] - (player.get_rect().y + 16 - scroll[1])), 2) + math.pow((point[0] - (player.get_rect().x + 20 - scroll[0])), 2))
        l2 = math.sqrt(math.pow((m_pos[1] - point[1]),2) + math.pow((m_pos[0] - point[0]),2))
        #Calculating the angle between them
        angle = math.atan2(l2,l1)
        angle = math.degrees(angle)
        #pygame.draw.line(display,(255,0,0), m_pos, point)
        #pygame.draw.line(display, (255,0,255), point, ((player.get_rect().x + 20 - scroll[0]), (player.get_rect().y + 16 - scroll[1])))
        player.dash(angle, m_pos, scroll, time)
        dash = not dash
    #Moving the Player
    player.move(tile_rects, time)
    #Drawing the Player
    player.draw(display, scroll)
    #Checkiung for Player Dash
    if not extra_dash:
        extra_dash = player.chech_for_dash()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:
                if player.chech_for_dash() == True:
                    dash = True
                else:
                    if extra_dash:
                        dash = True
                        extra_dash = False
    surf = pygame.transform.scale(display, (s_width, s_height))
    screen.blit(surf, (0,0))
    pygame.display.update()