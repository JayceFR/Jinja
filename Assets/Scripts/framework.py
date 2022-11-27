import pygame

class Player():
    def __init__(self,x, y, width, height):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.speed = 5
        self.acceleration = 0.05
        self.deceleration = 0.5
        self.gravity = 9.81
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.jump_frame = 0
        self.jump_cooldown = 500
        self.jump_last_update = 0
        self.was_moving_right = False
        self.was_moving_left = False
        self.display_x = 0
        self.display_y = 0

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
            if time - self.jump_last_update > self.jump_cooldown:
                self.jump = True
                self.jump_last_update = time
    
        self.movement = [0,0]
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
                self.movement[1] += self.gravity
        if not self.moving_left and not self.moving_right:
            if self.was_moving_right:
                self.speed -= self.deceleration
                self.movement[0] += self.speed
                if self.speed <= 5:
                    self.was_moving_right = False
            if self.was_moving_left:
                self.speed -= self.deceleration
                self.movement[1] -= self.speed
                if self.speed <= 5:
                    self.speed = 5
                    self.was_moving_left = False
        if self.moving_right:
            self.movement[0] += self.speed
            self.was_moving_right = True
            if self.speed < 8:
                self.speed += self.acceleration
            self.moving_right = not self.moving_right
        if self.moving_left:
            self.movement[0] -= self.speed
            self.was_moving_left = True
            if self.speed < 8:
                self.speed += self.acceleration
            self.moving_left = not self.moving_left
        

        collision_type = self.collision_checker(tiles)
        

    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        pygame.draw.rect(display, (255,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
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
        x = 0
        y = 0 
        for row in self.map:
            x = 0 
            for element in row:
                if element == "1":
                    window.blit(self.tiles[0], (x * 16 - scroll[0], y * 16 - scroll[1]) )
                if element == "2":
                    window.blit(self.tiles[1], (x * 16 - scroll[0], y * 16 - scroll[1]))
                if element == "3":
                    window.blit(self.tiles[2], (x * 16 - scroll[0], y * 16 - scroll[1]))
                if element == "4":
                    window.blit(self.tiles[3], (x * 16 - scroll[0], y * 16 - scroll[1]))
                if element == "5":
                    window.blit(self.tiles[4], (x * 16 - scroll[0], y * 16 - scroll[1]))
                if element == "6":
                    window.blit(self.tiles[5], (x * 16 - scroll[0], y * 16 - scroll[1]))
                if element != "0":
                    tile_rects.append(pygame.rect.Rect(x*16, y*16, 16,16))
                x += 1
            y += 1
        return tile_rects