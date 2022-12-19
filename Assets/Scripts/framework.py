import pygame
import math

class Player():
    def __init__(self,x, y, width, height, image):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.speed = 3
        self.acceleration = 0.05
        self.deceleration = 0.5
        self.gravity = 3
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.jump_frame = 0
        self.jump_cooldown = 200
        self.jump_last_update = 0
        self.was_moving_right = False
        self.was_moving_left = False
        self.display_x = 0
        self.display_y = 0
        self.is_dash = False
        self.dash_cooldown = 100
        self.dash_last_update = 0
        self.dash_angle = 0
        self.collision_type = {}
        self.player_img = image

    def collision_test(self, tiles):
        hitlist = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hitlist.append(tile)
        return hitlist
    
    def collision_checker(self, tiles):
        collision_types = {"top": False, "bottom": False, "right": False, "left": False}
        self.rect.x += self.movement[0]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[0] > 0:
                self.rect.right = tile.left
                collision_types["right"] = True
            elif self.movement[0] < 0:
                self.rect.left = tile.right
                collision_types["left"] = True
        self.rect.y += self.movement[1]
        hit_list = self.collision_test(tiles)
        for tile in hit_list:
            if self.movement[1] > 0:
                self.rect.bottom = tile.top
                collision_types["bottom"] = True
            if self.movement[1] < 0:
                self.rect.top = tile.bottom
                collision_types["top"] = True
        return collision_types

    def move(self, tiles, time):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.moving_left = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.moving_right = True
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.collision_type['bottom']:
                if time - self.jump_last_update > self.jump_cooldown:
                    self.jump = True
                    self.jump_last_update = time
        self.movement = [0,0]
        if self.is_dash:
            self.movement[0] += math.cos(math.radians(self.dash_angle)) * 30
            self.movement[1] -= math.sin(math.radians(self.dash_angle)) * 30
            if time - self.dash_last_update > self.dash_cooldown:
                self.is_dash = False
                self.dash_last_update = time
        if self.jump:
            if self.jump_frame < 5:
                self.jump_frame += 0.8
                self.movement[1] -= 10
            else:
                self.jump = False
        if not self.jump:
            if self.jump_frame > 0:
                self.movement[1] += 10
                self.jump_frame -= 0.8
            else:
                if not self.is_dash:
                    self.movement[1] += self.gravity
        if not self.moving_left and not self.moving_right:
            if self.was_moving_right:
                self.speed -= self.deceleration
                self.movement[0] += self.speed
                if self.speed <= 3:
                    self.was_moving_right = False
            if self.was_moving_left:
                self.speed -= self.deceleration
                self.movement[1] -= self.speed
                if self.speed <= 3:
                    self.speed = 3
                    self.was_moving_left = False
        if self.moving_right:
            self.movement[0] += self.speed
            self.was_moving_right = True
            if self.speed < 6:
                self.speed += self.acceleration
            self.moving_right = not self.moving_right
        if self.moving_left:
            self.movement[0] -= self.speed
            self.was_moving_left = True
            if self.speed < 6:
                self.speed += self.acceleration
            self.moving_left = not self.moving_left

        self.collision_type = self.collision_checker(tiles)

    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display.blit(self.player_img, self.rect)
        #pygame.draw.rect(display, (255,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def chech_for_dash(self):
        if self.collision_type['top'] or self.collision_type['bottom'] or self.collision_type['right'] or self.collision_type['left']:
            return True
        else:
            return False
    
    def dash(self, angle, m_pos, scroll, time):
        if self.rect.y - scroll[1] > m_pos[1]:
            #The vampire is bottom of the player 
            if self.rect.x - scroll[0] > m_pos[0]:
                #The vampire is to the right 
                self.facing_right = False
                angle = 180 - angle
        else:
            #The vampire is top of the player 
            if self.rect.x - scroll[0] > m_pos[0]:
                #The vampire is to the top right 
                self.facing_right = False
                angle = 180 + angle
            else:
                #The vampire is to the top left
                angle = 360 - angle
        self.is_dash = True
        self.dash_last_update = time
        self.dash_angle = angle
    
    def get_rect(self):
        return self.rect

#Map
class Map():
    def __init__(self, map_loc, tiles):
        self.map = [] 
        self.tiles = tiles
        f = open(map_loc, "r")
        data = f.read()
        f.close()
        data = data.split("\n")
        for row in data:
            self.map.append(list(row))
    
    def blit_map(self, window, scroll):
        tile_rects = []
        tree_loc = []
        x = 0
        y = 0 
        for row in self.map:
            x = 0 
            for element in row:
                if element == "1":
                    window.blit(self.tiles[0], (x * 32 - scroll[0], y * 32 - scroll[1]) )
                if element == "2":
                    window.blit(self.tiles[1], (x * 32 - scroll[0], y * 32 - scroll[1]))
                if element == "3":
                    window.blit(self.tiles[2], (x * 32 - scroll[0], y * 32 - scroll[1]))
                if element == "4":
                    window.blit(self.tiles[3], (x * 32 - scroll[0], y * 32 - scroll[1]))
                if element == "5":
                    window.blit(self.tiles[4], (x * 32 - scroll[0], y * 32 - scroll[1]))
                if element == "6":
                    window.blit(self.tiles[5], (x * 32 - scroll[0], y * 32 - scroll[1]))
                if element == "t":
                    tree_loc.append(list((x * 32, y * 32)))
                if element != "0" and element != "t":
                    tile_rects.append(pygame.rect.Rect(x*32, y*32, 32,32))
                x += 1
            y += 1
        return tile_rects, tree_loc

class Drones():
    def __init__(self, x, y, height, width) -> None:
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.display_x = 0
        self.display_y = 0
        self.fire_particles = []
        self.fire_cooldown = 500
        self.fire_last_update = 0
        self.speed = 5
    
    def move(self, scroll, player, time, display):
        #point = (self.rect.x, player.get_rect().y)
        point = (player.get_rect().x, self.rect.y)
        #pygame.draw.line(display, (255,0,0), (self.rect.x-scroll[0], self.rect.y-scroll[1]), (point[0] - scroll[0], point[1] - scroll[1]))
        #pygame.draw.line(display, (255,255,0), (point[0] - scroll[0], point[1] - scroll[1]), (player.get_rect().x - scroll[0], player.get_rect().y - scroll[1]))
        l1 = math.sqrt(math.pow((point[0] - self.rect.x), 2) + math.pow((point[1] - self.rect.y), 2))
        l2 = math.sqrt(math.pow((player.get_rect().x - point[0]), 2) + math.pow((player.get_rect().y - point[1]), 2))
        angle = math.degrees(math.atan2(l2, l1))
        if self.rect.y - scroll[1] > player.get_rect().y - scroll[1]:
            if self.rect.x - scroll[0] > player.get_rect().x - scroll[0]:
                self.facing_right = False
                angle = 180 - angle
        else: 
            if self.rect.x - scroll[0] > player.get_rect().x - scroll[0]:
                angle = 180 + angle
            else:
                angle = 360 - angle
        #self.rect.y = player.get_rect().y - 70
        #self.rect.y -= math.sin(math.radians(angle)) * self.speed
        self.rect.x += math.cos(math.radians(angle)) * self.speed
        if time - self.fire_last_update > self.fire_cooldown:
            self.fire_particles.append(Drone_Bullets(self.rect.x - scroll[0], self.rect.y - scroll[1], 3, 3, angle))
            self.fire_last_update = time
        if self.fire_particles != []:
            for particle in self.fire_particles:
                particle.move()
                particle.draw(display, scroll)

    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        pygame.draw.rect(display, (255,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
class Drone_Bullets():
    def __init__(self, x, y, width, height, angle) -> None:
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.speed = 4
        self.angle = angle
        self.display_x = 0
        self.display_y = 0
    
    def move(self):
        self.rect.y -= math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
    
    def draw(self, display, scroll):
        pygame.draw.rect(display, (255,0,0), self.rect)