import pygame
import math

class Player():
    def __init__(self,x, y, width, height, player_idle, player_run):
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.speed = 3
        self.acceleration = 0.03
        self.deceleration = 0.5
        self.gravity = 3
        self.moving_right = False
        self.moving_left = False
        self.jump = False
        self.jump_frame = 0
        self.jump_cooldown = 200
        self.jump_last_update = 0
        self.player_idle_animation = player_idle
        self.player_run_animation = player_run
        self.frame = 0
        self.frame_cooldown = 500
        self.frame_last_update = 0
        self.was_moving_right = False
        self.was_moving_left = False
        self.display_x = 0
        self.display_y = 0
        self.is_dash = False
        self.dash_cooldown = 100
        self.dash_last_update = 0
        self.turn_left = False
        self.facing_left = False
        self.dash_angle = 0
        self.collision_type = {}
        self.idle = False

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

    def move(self, tiles, time, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            if not self.facing_left:
                self.facing_left = True
            self.moving_left = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            if self.facing_left:
                self.facing_left = False
            self.moving_right = True
        if keys[pygame.K_SPACE] or keys[pygame.K_w]:
            if self.collision_type['bottom']:
                if time - self.jump_last_update > self.jump_cooldown:
                    self.jump = True
                    self.jump_last_update = time
        self.movement = [0,0]
        if time - self.frame_last_update > self.frame_cooldown:
            self.frame_last_update = time
            self.frame += 1
            if self.frame > 3:
                self.frame = 0
        
        if not self.moving_left and not self.moving_right:
            self.frame_cooldown = 500
            self.idle = True
        else:
            self.frame_cooldown = 100
            self.idle = False
            if self.moving_left:
                self.turn_left = True
            else:
                self.turn_left = False
        if self.is_dash:
            self.movement[0] += math.cos(math.radians(self.dash_angle)) * 30 * dt
            self.movement[1] -= math.sin(math.radians(self.dash_angle)) * 30 * dt
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
                    self.movement[1] += self.gravity * dt
        if not self.moving_left and not self.moving_right:
            if self.was_moving_right:
                self.speed -= self.deceleration
                self.movement[0] += self.speed * dt
                if self.speed <= 3:
                    self.was_moving_right = False
            if self.was_moving_left:
                self.speed -= self.deceleration
                self.movement[1] -= self.speed * dt
                if self.speed <= 3:
                    self.speed = 3
                    self.was_moving_left = False
        if self.moving_right:
            self.movement[0] += self.speed * dt
            self.was_moving_right = True
            if self.speed < 6:
                self.speed += self.acceleration
            self.moving_right = not self.moving_right
        if self.moving_left:
            self.movement[0] -= self.speed * dt
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
        #display.blit(self.player_img, self.rect)
        if self.idle:
            if not self.facing_left:
                display.blit(self.player_idle_animation[self.frame], self.rect)
            else:
                player_flip = self.player_idle_animation[self.frame].copy()
                player_flip = pygame.transform.flip(player_flip, True, False)
                display.blit(player_flip, self.rect)
        else:
            if self.turn_left:
                player_flip = self.player_run_animation[self.frame].copy()
                player_flip = pygame.transform.flip(player_flip, True, False)
                display.blit(player_flip, self.rect)
            else:
                display.blit(self.player_run_animation[self.frame], self.rect)
        #pygame.draw.rect(display, (255,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
        return self.turn_left
    
    def chech_for_dash(self):
        if self.collision_type['top'] or self.collision_type['bottom'] or self.collision_type['right'] or self.collision_type['left']:
            return True
        else:
            return False
    
    def dash(self, angle, m_pos, scroll, time):
        if self.rect.y - scroll[1] > m_pos[1]:
            if self.rect.x - scroll[0] > m_pos[0]: 
                self.facing_right = False
                angle = 180 - angle
        else:
            if self.rect.x - scroll[0] > m_pos[0]:
                self.facing_right = False
                angle = 180 + angle
            else:
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
    def __init__(self, x, y, height, width, drone_animation) -> None:
        self.rect = pygame.rect.Rect(x, y, width, height)
        self.display_x = 0
        self.display_y = 0
        self.fire_particles = []
        self.frame = 0
        self.health = 100
        self.alive = True
        self.frame_update_cooldown = 100
        self.frame_last_update = 0
        self.drone_animation = drone_animation
        self.fire_cooldown = 2000
        self.fire_last_update = 0
        self.speed = 5
    
    def draw_health_bar(self, display):
        ratio = self.health / 100
        pygame.draw.rect(display, (255,255,255), (self.rect.x - 20, self.rect.y - 2, 104  , 17//2))
        pygame.draw.rect(display, (255,0,0), (self.rect.x - 18, self.rect.y, 100  , 15//2))
        pygame.draw.rect(display, (255,255,0), (self.rect.x - 18, self.rect.y, 100 * ratio , 15//2))
    
    def move(self, scroll, player, time, display):
        #point = (self.rect.x, player.get_rect().y)
        if time - self.frame_last_update > self.frame_update_cooldown:
            self.frame += 1
            if self.frame > 1:
                self.frame = 0
            self.frame_last_update = time
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
            self.fire_particles.append(Drone_Bullets(self.rect.x - scroll[0] + 32, self.rect.y - scroll[1] + 32, 3, 3, angle, time))
            self.fire_last_update = time
        if self.fire_particles != []:
            for pos, particle in sorted(enumerate(self.fire_particles), reverse=True):
                particle.move(time)
                particle.draw(display, (self.rect.x - scroll[0] + 32, self.rect.y - scroll[1] + 32))
                if not particle.alive:
                    self.fire_particles.pop(pos)

    def draw(self, display, scroll):
        self.display_x = self.rect.x
        self.display_y = self.rect.y
        self.rect.x -= scroll[0]
        self.rect.y -= scroll[1]
        display.blit(self.drone_animation[self.frame], (self.rect.x, self.rect.y))
        self.draw_health_bar(display)
        #pygame.draw.rect(display, (255,0,0), self.rect)
        self.rect.x = self.display_x
        self.rect.y = self.display_y
    
    def get_rect(self):
        return self.rect
    
class Drone_Bullets():
    def __init__(self, x, y, width, height, angle, time) -> None:
        self.rect = pygame.rect.Rect(x,y,width,height)
        self.speed = 30
        self.alive = True
        self.start_time = time
        self.die_after = 100
        self.angle = angle
        self.display_x = 0
        self.display_y = 0
    
    def move(self, current_time):
        self.rect.y -= math.sin(math.radians(self.angle)) * self.speed
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
        if current_time - self.start_time > self.die_after:
            self.alive = False
        #if self.rect.y < 0 or self.rect.y > 900 or self.rect.x < 0 or self.rect.x > 20000:
        #    self.alive = False
    
    def draw(self, display, start_pos):
        pygame.draw.line(display, (255,0,0), start_pos, (self.rect.x, self.rect.y))
        pygame.draw.rect(display, (255,0,0), self.rect)


#Sparks
class Spark():
    def __init__(self, loc, angle, speed, color, scale=1, type=0):
        self.loc = loc
        self.angle = angle
        self.speed = speed
        self.scale = scale
        self.color = color
        self.alive = True
        self.type = type

    def point_towards(self, angle, rate):
        rotate_direction = ((angle - self.angle + math.pi * 3) % (math.pi * 2)) - math.pi
        try:
            rotate_sign = abs(rotate_direction) / rotate_direction
        except ZeroDivisionError:
            rotate_sign = 1
        if abs(rotate_direction) < rate:
            self.angle = angle
        else:
            self.angle += rate * rotate_sign

    def calculate_movement(self, dt):
        return [math.cos(self.angle) * self.speed * dt, math.sin(self.angle) * self.speed * dt]

    # gravity and friction
    def velocity_adjust(self, friction, force, terminal_velocity, dt):
        movement = self.calculate_movement(dt)
        movement[1] = min(terminal_velocity, movement[1] + force * dt)
        movement[0] *= friction
        self.angle = math.atan2(movement[1], movement[0])
        # if you want to get more realistic, the speed should be adjusted here

    def move(self, dt):
        movement = self.calculate_movement(dt)
        self.loc[0] += movement[0]
        self.loc[1] += movement[1]

        #Type of sparks
        if self.type == 0:
            self.point_towards(math.pi / 2, 0.02)
        if self.type == 1:
            self.velocity_adjust(0.975, 0.2, 8, dt)
        if self.type == 2:
            self.angle += 0.1

        self.speed -= 0.1

        if self.speed <= 0:
            self.alive = False

    def draw(self, surf, offset=[0, 0]):
        if self.alive:
            points = [
                [self.loc[0] + math.cos(self.angle) * self.speed * self.scale,
                 self.loc[1] + math.sin(self.angle) * self.speed * self.scale],
                [self.loc[0] + math.cos(self.angle + math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] + math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
                [self.loc[0] - math.cos(self.angle) * self.speed * self.scale * 3.5,
                 self.loc[1] - math.sin(self.angle) * self.speed * self.scale * 3.5],
                [self.loc[0] + math.cos(self.angle - math.pi / 2) * self.speed * self.scale * 0.3,
                 self.loc[1] - math.sin(self.angle + math.pi / 2) * self.speed * self.scale * 0.3],
            ]
            pygame.draw.polygon(surf, self.color, points)