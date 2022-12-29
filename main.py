import pygame
import Assets.Scripts.framework as framework
import Assets.Scripts.background as backg
import Assets.Scripts.bg_particles as bg_particles
import Assets.Scripts.wave as wave
import Assets.Scripts.Sword as Sword
import Assets.Scripts.grass as g
import math
import random
import time as t
from pygame.locals import *
pygame.init()
s_width = 1000
s_height = 600
screen = pygame.display.set_mode((s_width,s_height))
display = pygame.Surface((s_width//2, s_height//2))
def blit_tree(display, tree_img, tree_locs, scroll):
    tree_screen = display.copy()
    for loc in tree_locs:
        tree_screen.blit(tree_img, (loc[0] - scroll[0], loc[1] - scroll[1] - 160))
    tree_screen.set_alpha(170)
    display.blit(tree_screen, (0,0))

def create_drones(drones, drone_loc, drone_animation, snow_ball_img):
    for loc in drone_loc:
        drones.append(framework.Drones(loc[0], loc[1], drone_animation[0].get_width(), drone_animation[0].get_height(), drone_animation, snow_ball_img))
    return drones

def create_gift(gifts, x, y, gift_images):
    random_number = random.randint(0,len(gift_images)-1)
    gifts.append(framework.Gifts(x,y,gift_images[random_number].get_width(), gift_images[random_number].get_height(), gift_images[random_number], random_number))
    return gifts

def blit_drones(drones, display, scroll, player, time, dt):
    for pos, drone in sorted(enumerate(drones), reverse=True):
        if drone.alive:
            dt = drone.move(scroll, player, time, display, dt)
            drone.draw(display, scroll)
        else:
            drones.pop(pos)
    return dt

def blit_spikes(spikes, display, scroll, player, time):
    for pos, spike in sorted(enumerate(spikes), reverse=True):
        spike.move(time)
        spike.draw(display, scroll)
        if spike.get_rect().colliderect(player.get_rect()):
            player.health = 0

def blit_grass(grasses, display, scroll, player):
    for grass in grasses:
        if grass.get_rect().colliderect(player.get_rect()):
            grass.colliding()
        grass.draw(display, scroll)


def get_image(sheet, frame, width, height, scale, colorkey):
    image = pygame.Surface((width, height)).convert_alpha()
    image.blit(sheet, (0, 0), ((frame * width), 0, width, height))
    image = pygame.transform.scale(image, (width * scale, height * scale))
    image.set_colorkey(colorkey)
    return image

def draw_text(text, font, text_col, x, y, display):
    img = font.render(text, True, text_col)
    display.blit(img, (x, y))

def game_loop(level):
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
    tree_img = pygame.image.load("./Assets/Sprites/tree.png").convert_alpha()
    tree_img_copy = tree_img.copy()
    tree_img = pygame.transform.scale(tree_img_copy, (tree_img_copy.get_width() * 3, tree_img_copy.get_height()*3))
    player_img = pygame.image.load("./Assets/Sprites/player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (player_img.get_width()*1.5, player_img.get_height()*1.5))
    player_img.set_colorkey((255,255,255))
    player_idle_img = pygame.image.load("./Assets/Sprites/player_idle.png").convert_alpha()
    player_run_img = pygame.image.load("./Assets/Sprites/player_run.png").convert_alpha()
    #drone_img = pygame.image.load("./Assets/Sprites/drone.png").convert_alpha()
    katana_img = pygame.image.load("./Assets/Sprites/katana.png").convert_alpha()
    katana = katana_img.copy()
    katana = pygame.transform.scale(katana_img, (katana_img.get_width()*1.5, katana_img.get_height()*1.5))
    katana.set_colorkey((255,255,255))
    snow_ball_img = pygame.image.load("./Assets/Sprites/snow_ball.png").convert_alpha()
    snow_ball_img.set_colorkey((0,0,0))
    flake_img = pygame.image.load("./Assets/Sprites/flake.png").convert_alpha()
    flake_img.set_colorkey((0,0,0))
    spike_img = pygame.image.load("./Assets/Sprites/spike_idle.png").convert_alpha()
    spike_img.set_colorkey((0,0,0))
    snow_flake1_img = pygame.image.load("./Assets/Sprites/snow_flake1.png").convert_alpha()
    snow_flake1 = snow_flake1_img.copy()
    snow_flake1 = pygame.transform.scale(snow_flake1_img, (snow_flake1_img.get_width()*2, snow_flake1.get_height()*2))
    snow_flake2_img = pygame.image.load("./Assets/Sprites/snow_flake2.png").convert_alpha()
    snow_flake2 = snow_flake2_img.copy()
    snow_flake2 = pygame.transform.scale(snow_flake2_img, (snow_flake2_img.get_width()*2, snow_flake2_img.get_height()*2))
    green_gift = pygame.image.load("./Assets/Sprites/green_gift.png").convert_alpha()
    red_gift = pygame.image.load("./Assets/Sprites/red_gift.png").convert_alpha()
    blue_gift = pygame.image.load("./Assets/sprites/blue_gift.png").convert_alpha()
    santa_img = pygame.image.load("./Assets/Sprites/santa.png").convert_alpha()
    santa = santa_img.copy()
    santa = pygame.transform.scale(santa_img, (santa_img.get_width()*2, santa_img.get_height()*2))
    arrow_img = pygame.image.load("./Assets/Sprites/arrow.png").convert_alpha()
    arrow = arrow_img.copy()
    arrow = pygame.transform.scale(arrow_img, (arrow_img.get_width()*2, arrow_img.get_height() * 2))
    arrow.set_colorkey((0,0,0))
    #Map
    map = framework.Map("./Assets/Maps/"+level, tiles)
    #Fonts
    font = pygame.font.Font("./Assets/Fonts/jayce.ttf", 30)
    font2 = pygame.font.Font("./Assets/Fonts/jayce.ttf", 25)
    #Texts
    tutorial_texts = ["Winja! We are in a crisis ", "Winter is a season of joy ", "It is the time of sharing. But... ", "Winter has been swallowed by evil", "Winter is now against Christmas ", "They have stolen our gifts ", "Only  You  Winja  Can  Save", "Christmas!", "Save The Presents At Any Cost ", "WASD for movement", "Space To Jump", "K or Left-Click to ki.?!", "To Bring Peace", "Remeber! You can Cycle Through", "The Map by Falling", "But The Gifts Can Not!", "Destroy The Winter Sprites And...", "Collect All The Presents", "All The Best Winja" ]
    current_tutorial_text = 0
    speech_cooldown = 5000
    speech_last_update = 0

    #Player
    player_idle_animation = []
    player_run_animation = []
    for x in range(4):
        player_idle_animation.append(get_image(player_idle_img, x, 14, 28, 1.5, (255,255,255)))
        player_run_animation.append(get_image(player_run_img, x, 14, 28, 1.5, (255,255,255)))
    player = framework.Player(160,50,player_img.get_width(),player_img.get_height(), player_idle_animation, player_run_animation)
    dash = False
    extra_dash = True
    check_for_dash = True
    #player_attacks = [[colliderect, current_time, time_delay]]
    player_attacks  = []
    #Scroll
    true_scroll = [0,0]
    scroll = [0,0]
    #Flakes
    drones = []
    drone_animation = [snow_flake1, snow_flake2]
    drone_spawn = True
    #Grass
    grasses = []
    grass_loc = []
    grass_spawn = True
    grass_last_update = 0
    grass_cooldown = 50
    #Sword
    p_sword = Sword.sword(50,50,katana.get_width(),katana.get_height(),katana)
    #Spikes
    spike_loc = []
    spike_spawn = True
    spikes = []
    spike_animation = []
    for x in range(2):
        spike_animation.append(get_image(spike_img, x, 7, 13, 4.6, (0,0,0)))
    #Background Stripes
    bg = backg.background()
    bg_particle_effect = bg_particles.Master()
    #Sparks
    sparks = []
    #Polly
    polly_loc = []
    pollies = []
    polly_img_dup = pygame.image.load("./Assets/Sprites/polly.png").convert_alpha()
    polly_img = polly_img_dup.copy()
    polly_img = pygame.transform.scale(polly_img_dup, (polly_img_dup.get_width() * 2, polly_img.get_height() * 2))
    polly_img.set_colorkey((0,0,0))
    polly_spawn = True
    #Gifts
    gifts = []
    gift_images = [green_gift, red_gift, blue_gift]
    gift_particles = [(170,222,110), (225,128,128), (0,128,255)]
    #BackGround Settings
    lightning = False
    lightning_cooldown = 2000
    lightning_colors = [[(0,64,0), (0,128,64), (0,255,0)], [(255,0,0), (128,0,0), (128,64,64)], [(255,255,0), (255,128,64), (255,255,128), (255,128,0)]]
    lightning_color = lightning_colors[0]
    lightning_last_update = 0
    lightning_alpha = 255
    if level == "game_over.txt":
        lightning = True
        for x in range(200):
            create_gift(gifts, random.randint(50,2000)//2, -200 , gift_images)
    #After Death Settings
    just_died = True
    #Time
    last_time = t.time()
    while run:
        clock.tick(60)
        dt = t.time() - last_time
        dt *= 60
        last_time = t.time()
        time = pygame.time.get_ticks()
        #Checking For Lightning
        if not lightning:
            if time - lightning_last_update > lightning_cooldown:
                lightning = False
                lightning_alpha = 255
                lightning_color = lightning_colors[random.randint(0,len(lightning_colors) - 1)]
                lightning_last_update = time
            display.fill((15,27,55))
            blur_surf = display.copy()
            bg.recursive_call(blur_surf)
            blur_surf.set_alpha(80)
        else:
            display.fill(lightning_color[random.randint(0,len(lightning_color) - 1)])
            blur_surf = display.copy()
            blur_surf.set_alpha(lightning_alpha)
            lightning_alpha -= 5
            if lightning_alpha < 100:
                lightning = False
        display.blit(blur_surf, (0,0))
        #Blitting The Map
        tile_rects, tree_locs, drone_loc, grass_loc, spike_loc, polly_loc, arrow_loc = map.blit_map(display, scroll)
        #Creating Items
        if drone_spawn:
            drones = create_drones(drones, drone_loc, drone_animation, flake_img)
            drone_spawn = False
        if grass_spawn:
            for loc in grass_loc:
                x_pos = loc[0]
                while x_pos < loc[0] + 32:
                    x_pos += 2.5
                    grasses.append(g.grass([x_pos, loc[1]+14], 2, 18))
            grass_spawn = False
        if polly_spawn:
            for loc in polly_loc:
                pollies.append(framework.Polly(loc[0], loc[1], polly_img.get_width(), polly_img.get_height(), snow_ball_img, polly_img))
            polly_spawn = False
        if spike_spawn:
            for loc in spike_loc:
                spikes.append(framework.Spike(loc[0], loc[1], spike_animation[0].get_width(), spike_animation[0].get_height(), spike_animation ))
            spike_spawn = False
        if arrow_loc != []:
            for loc in arrow_loc:
                display.blit(arrow, (loc[0] - scroll[0], loc[1] - scroll[1]))
        #Blitting Items before Blitting Player
        blit_tree(display, tree_img, tree_locs, scroll)
        #dt = blit_drones(drones, display, scroll, player, time, dt)
        for pos, drone in sorted(enumerate(drones), reverse=True):
            if drone.alive:
                dt = drone.move(scroll, player, time, display, dt)
                drone.draw(display, scroll)
            else:
                create_gift(gifts, drone.get_rect().x, -200 , gift_images)
                drones.pop(pos)
        blit_spikes(spikes, display, scroll, player, time)
        for pos, polly in sorted(enumerate(pollies), reverse=True):
            if polly.alive:
                dt = polly.move(player, scroll, display, time, dt)
                polly.draw(display, scroll)
            else:
                create_gift(gifts, polly.get_rect().x, 0, gift_images)
                pollies.pop(pos)

        if gifts != []:
            for pos, gift in sorted(enumerate(gifts), reverse = True):
                gift.move(tile_rects)
                gift.draw(display, scroll)
                if level != "game_over.txt":
                    if gift.get_rect().colliderect(player.get_rect()):
                        for x in range(20):
                            sparks.append(framework.Spark([gift.get_rect().x - scroll[0] + gift.get_width()//2, gift.get_rect().y - scroll[1] + gift.get_height()//2],math.radians(random.randint(0,360)), random.randint(2, 5), gift_particles[gift.get_pos()], 2, 2))
                        gifts.pop(pos)
        #Movement of grass
        if time - grass_last_update > grass_cooldown:
            for grass in grasses:
                grass.move()
            grass_last_update = time
        #Calculating scroll
        true_scroll[0] += (player.get_rect().x - true_scroll[0] - 241)
        true_scroll[1] += (player.get_rect().y - true_scroll[1] - 166)
        scroll = true_scroll.copy()
        scroll[0] = int(scroll[0])
        scroll[1] = int(scroll[1])
        #Checking For Player Attack
        if player_attacks != []:
            for pos, attack in sorted(enumerate(player_attacks), reverse=True):
                if time - attack[1] < attack[2]:
                    if drones != []:
                        for drone in drones:
                            if attack[0].colliderect(drone.get_rect()):
                                drone.health -= 2
                                dt = 0.2
                                scroll[0] += random.randint(-20,20)
                                scroll[1] += random.randint(-20,20)
                                for x in range(20):
                                    sparks.append(framework.Spark([drone.get_rect().x - scroll[0] + drone_animation[0].get_width()//2, drone.get_rect().y - scroll[1] + drone_animation[0].get_height()//2],math.radians(random.randint(0,360)), random.randint(2, 5),(95, 205, 228), 1, 0))
                    if pollies != []:
                        for polly in pollies:
                            if attack[0].colliderect(polly.get_rect()):
                                polly.health -= 2
                                if polly.health <= 0:
                                    polly.alive = False
                                dt = 0.2
                                scroll[0] += random.randint(-20,20)
                                scroll[1] += random.randint(-20,20)
                                for x in range(20):
                                    sparks.append(framework.Spark([polly.get_rect().x - scroll[0] + polly_img.get_width()//2, polly.get_rect().y - scroll[1] + polly_img.get_height()//2],math.radians(random.randint(0,360)), random.randint(2, 5),(255, 255, 255), 1, 0))
                else:
                    player_attacks.pop(pos)
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
        if player.alive:
            #Moving the Player
            player.move(tile_rects, time, dt)
            #Drawing the Player
            facing_left = player.draw(display, scroll)
            #Sword
            p_sword.update((player.get_rect().x, player.get_rect().y), facing_left)
            p_sword.blit(display, scroll)
        #Background Particles
        bg_particle_effect.recursive_call(time, display, scroll, dt)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                return 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    player_attacks.append(list((p_sword.attack(), time, 500)))
            if event.type == pygame.KEYDOWN:
                if event.key == 107:
                    player_attacks.append(list((p_sword.attack(), time, 500)))
        #Sparks Blitting
        if sparks != []:
            for i, spark in sorted(enumerate(sparks), reverse=True):
                spark.move(dt)
                spark.draw(display)
                if not spark.alive:
                    sparks.pop(i)
        #Blitting Items After Blitting The Player
        blit_grass(grasses, display, scroll, player)
        #Checking whether player has died
        if level == "tutorial.txt":
            pygame.draw.rect(display, (0,0,0), pygame.rect.Rect(0,200,600,200))
            draw_text(tutorial_texts[current_tutorial_text], font2, (255,255,255), 84, 230, display )
            if current_tutorial_text % 2 == 0:
                draw_text("Ho Ho Ho Ho Ho ...", font2, (255,0,0), 120, 250, display  )
            if time - speech_last_update > speech_cooldown:
                current_tutorial_text += 1
                if current_tutorial_text >= len(tutorial_texts):
                    run = False
                speech_last_update = time
            display.blit(santa, (10,220))
        else:
            if player.health <=0 :
                player.alive = False
                sparks.append(framework.Spark([player.get_rect().x - scroll[0] + player_idle_animation[0].get_width()//2, player.get_rect().y - scroll[1] + player_idle_animation[0].get_height()//2],math.radians(random.randint(0,360)), random.randint(6, 7),(125, 112, 113), 10, 0))
            else:
                #Checking whether the player has completed the level
                if drones == [] and pollies == [] and gifts == []:
                    run = False
        surf = pygame.transform.scale(display, (s_width, s_height))
        screen.blit(surf, (0,0))
        pygame.display.update()
    return 0

def main_loop():
    #0 -> Player has completed the level
    #1 -> Player has closed the Game
    levels = ["tutorial.txt", "level1.txt", "level2.txt", "level3.txt", "level4.txt", "level5.txt", "game_over.txt"]
    #levels = ["level1.txt"]
    current_level = 0
    #Music
    pygame.mixer.music.load("./Assets/Music/WinjaBgMusic.wav")
    pygame.mixer.music.set_volume(0.8)
    pygame.mixer.music.play(-1)
    while current_level < len(levels):
        level_done = game_loop(levels[current_level])
        if level_done == 0:
            current_level += 1
        if level_done == 1:
            #Player Closed The Game
            current_level = len(levels) + 1

main_loop()
