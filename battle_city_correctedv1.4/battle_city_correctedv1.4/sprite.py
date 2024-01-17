import pygame 
import math
import time
import random


# Определите WIDTH и HEIGHT
WIDTH, HEIGHT = 800, 600
PLAYER_IMG = 'images/tank.png'
BULLET_IMG = 'images/bullet.png'
ENEMY_IMG = 'images/rocket.png'

pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('sound/shoot.mp3')
movement_sound = pygame.mixer.Sound('sound/drive.mp3')


class GameSprite(pygame.sprite.Sprite):
    def __init__(self,x,y,img,width,height):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(img),(width,height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
    def draw(self,window):
        window.blit(self.image,(self.rect.x,self.rect.y))
        
    def collidepoint(self,x,y):
        return self.rect.collidepoint(x,y)
        

class Button(GameSprite):
    pass
        
class TransitionButton(Button):
    def __init__(self,x,y,img,width,height,screen,goal):
        super().__init__(x, y, img, width, height)
        self.screen = screen
        self.goal = goal
        
    def on_pressed(self):
        self.screen.manager.current = self.screen.manager.main_game 
        


class Player(GameSprite):
    def __init__(self, x, y, img, width, height, name, health, level,bullets):
        super().__init__(x, y, img, width, height)
        self.name = name
        self.health = health
        self.level = level
        self.speed = 10
        self.angle = 20
        self.bullets = bullets
        self.original_image = pygame.transform.scale(pygame.image.load(img), (width, height))
        self.rect = pygame.Rect(x, y, width, height)
        self.current_time= time.time()

    def update(self, window,blocks_col):
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_w] and self.rect.x >= 0:
            self.rect.y -= self.speed
            movement_sound.set_volume(0.1)
            pygame.mixer.Sound.play(movement_sound)
            if pygame.sprite.spritecollide(self,blocks_col,False):
                self.rect.y += self.speed
        else: 
            pygame.mixer.Sound.stop(movement_sound)

        if keys[pygame.K_s]:
            self.rect.y += self.speed
            movement_sound.set_volume(0.1)
            pygame.mixer.Sound.play(movement_sound)
            if pygame.sprite.spritecollide(self,blocks_col,False):
                self.rect.y -= self.speed
        else: 
            pygame.mixer.Sound.stop(movement_sound)       
            

        if keys[pygame.K_a]:
            self.rect.x -= self.speed
            movement_sound.set_volume(0.1)
            pygame.mixer.Sound.play(movement_sound)
            if pygame.sprite.spritecollide(self,blocks_col,False):
                self.rect.x += self.speed
        else: 
            pygame.mixer.Sound.stop(movement_sound)

        if keys[pygame.K_d]:
            self.rect.x += self.speed
            movement_sound.set_volume(0.1)
            pygame.mixer.Sound.play(movement_sound)
            if pygame.sprite.spritecollide(self,blocks_col,False):
                self.rect.x -= self.speed
        else: 
            pygame.mixer.Sound.stop(movement_sound)


        self.angle = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.rect.centery,
                                             pygame.mouse.get_pos()[0] - self.rect.centerx))

        rotated_image = pygame.transform.rotate(self.original_image, -self.angle-84)
        self.image = rotated_image
        # self.rect = rotated_image.get_rect(center=self.rect.center)
        self.draw(window)

        
        
    def shoot(self):
        if time.time() - self.current_time >=0:
            bullet = Bullet(self.rect.x,self.rect.y + 15,BULLET_IMG,5,15,self.angle,self.bullets)
            pygame.mixer.music.pause()
            shoot_sound.set_volume(0.1)
            pygame.mixer.Sound.play(shoot_sound)
            pygame.mixer.music.unpause()
            self.current_time = time.time()
        
 
# class Tower(GameSprite):
#     def __init__(self, x, y, img, width, height):
#         super().__init__(x, y, img, width, height)
#         self.speed = 5

#     def update(self):
#         # Получаем текущие координаты мыши
#         mouse_x, mouse_y = pygame.mouse.get_pos()
#         # Поворачиваем башню в сторону мыши
#         angle = pygame.math.Vector2(mouse_x - self.rect.centerx, mouse_y - self.rect.centery).angle_to((1, 0))
#         self.image = pygame.transform.rotate(self.image, -angle)
#         self.rect = self.image.get_rect(center=self.rect.center) 
        
class Enemy(GameSprite):
    def __init__(self, x, y, img, width, height, Enemy_bullets_group):
        super().__init__(x, y, img, width, height)
        self.health = 10
        self.player = None
        self.speed = 1
        self.direction = (0, -1)
        self.original_image = pygame.transform.scale(pygame.image.load(ENEMY_IMG), (width, height))
        self.angle = 0
        self.bullet_speed = 5
        self.shoot_cooldown = 60
        self.shoot_timer = 0
        self.Enemy_bullets_group = Enemy_bullets_group 

    def take_damage(self, damage, owner):
        if owner is None or owner != self:
            self.kill()

    def set_player(self, player):
        self.player = player

    def update(self, window, blocks_col, blocks_unc):
        if self.player:
            distance_to_player = self.distance_to_player()

            if self.player_in_sight() and distance_to_player > 150:
                angle = math.degrees(math.atan2(self.player.rect.centery - self.rect.centery,
                                                self.player.rect.centerx - self.rect.centerx))
                
                self.image = pygame.transform.rotate(self.original_image, angle)
                
                new_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
                collided_blocks_col = any(new_rect.colliderect(block.rect) for block in blocks_col)
                collided_blocks_unc = any(new_rect.colliderect(block.rect) for block in blocks_unc)

                if not collided_blocks_col and not collided_blocks_unc:
                    can_move = True
                    all_blocks = pygame.sprite.Group(blocks_unc, blocks_col)
                    for block in all_blocks.sprites():
                        if block.rect.colliderect(new_rect):
                            if block.block_type in [Water, Iron, Brick]:
                                can_move = False
                                break

                    if can_move:
                        self.rect.x += self.speed * math.cos(math.radians(angle))
                        self.rect.y += self.speed * math.sin(math.radians(angle))
                else:
                    self.angle += 180 
                    
            elif not self.player_in_sight():
                self.wander(window, blocks_col, blocks_unc)

            elif self.player_in_sight() and distance_to_player <= 150:
                if self.shoot_timer <= 0:
                    print("Shoot")
                    self.shoot(window)
                    self.shoot_timer = self.shoot_cooldown
                else:
                    self.shoot_timer -= 1
                
        self.draw(window)

    def shoot(self, window):
        angle = math.atan2(self.player.rect.centery - self.rect.centery,
                           self.player.rect.centerx - self.rect.centerx)
        angle_degrees = math.degrees(angle)

        self.image = pygame.transform.rotate(self.original_image, angle_degrees)

        bullet = Enemy_Bullet(self.rect.centerx, self.rect.centery, BULLET_IMG, 5, 15, angle_degrees, self.Enemy_bullets_group)
        bullet.set_player(bullet)
        self.Enemy_bullets_group.add(bullet)

    def player_in_sight(self):
        if self.distance_to_player() < 200:
            player_direction = pygame.math.Vector2(self.player.rect.x - self.rect.x, self.player.rect.y - self.rect.y)
            enemy_direction = pygame.math.Vector2(self.speed * math.cos(math.radians(self.angle)),
                                                  self.speed * math.sin(math.radians(self.angle)))
            player_direction.normalize_ip()
            enemy_direction.normalize_ip()
            cross_product = player_direction.cross(enemy_direction)

            return cross_product > 0

        return False

    def distance_to_player(self):
        return math.hypot(self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery)

    def wander(self, window, blocks_col, blocks_unc):
        if random.randint(1, 100) > 100:
            self.angle = random.uniform(0, 360)

        x_change = self.speed * math.cos(math.radians(self.angle))
        y_change = self.speed * math.sin(math.radians(self.angle))

        new_rect = pygame.Rect(self.rect.x + x_change, self.rect.y + y_change, self.rect.width, self.rect.height)
        collided_blocks_col = any(new_rect.colliderect(block.rect) for block in blocks_col)
        collided_blocks_unc = any(new_rect.colliderect(block.rect) for block in blocks_unc)

        if not collided_blocks_col and not collided_blocks_unc:
            # Проверка на выход за границы
            if 20 <= self.rect.x + x_change <= window.get_width() - self.rect.width and 20 <= self.rect.y + y_change <= window.get_height() - self.rect.height:
                self.rect.x += x_change
                self.rect.y += y_change
        else:

            self.angle += 180

        self.draw(window)


class Bullet(GameSprite):
    def __init__(self, x, y, img, width, height, angle, bullets_group):
        super().__init__(x, y, img, width, height)
        self.damage = 1
        self.speed = 11
        self.angle = math.radians(angle)
        bullets_group.add(self)
        
        self.img_angle = math.degrees(math.atan2(pygame.mouse.get_pos()[1] - self.rect.centery,
                                             pygame.mouse.get_pos()[0] - self.rect.centerx))

        rotated_image = pygame.transform.rotate(self.image, -self.img_angle-84)
        self.image = rotated_image
     


    def update(self,window):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)

        self.draw(window)

class Enemy_Bullet(GameSprite):
    def __init__(self, x, y, img, width, height, angle, Enemy_bullets_group):
        super().__init__(x, y, img, width, height)
        self.damage = 1
        self.speed = 11
        self.angle = math.radians(angle)
        self.player = None
        
        
     
    def set_player(self, player):
        self.player = player

    def update(self,window):
        self.rect.x += self.speed * math.cos(self.angle)
        self.rect.y += self.speed * math.sin(self.angle)



        self.draw(window)
        

def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Your Game")

    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()

    player = Player(WIDTH // 2, HEIGHT // 2, PLAYER_IMG, 50, 50, 'Player', 100, 1)
    all_sprites.add(player)

    # Создаем несколько врагов и добавляем их в группу enemies
    enemy1 = Enemy(100, 100, ENEMY_IMG, 50, 50)
    enemy2 = Enemy(200, 200, ENEMY_IMG, 50, 50)
    enemies.add(enemy1, enemy2)
    all_sprites.add(enemy1, enemy2)

    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.shoot()

        all_sprites.update(window)
        window.fill((255, 255, 255))

        # Отрисовка объектов
        all_sprites.draw(window)
        bullets.draw(window)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

class Brick(GameSprite):
    def __init__(self, x, y, img, width, height,): 
        super().__init__(x, y, img, width, height)
    def update(self,window):
        self.draw(window)

class Iron(GameSprite):
    def __init__(self, x, y, img, width, height,): 
        super().__init__(x, y, img, width, height)
    def update(self,window):
        self.draw(window)
        
class Grass(GameSprite):
    def __init__(self, x, y, img, width, height,): 
        super().__init__(x, y, img, width, height)
    def update(self,window):
        self.draw(window)

class Water(GameSprite):
    def __init__(self, x, y, img, width, height,): 
        super().__init__(x, y, img, width, height)
    def update(self,window):
        self.draw(window)

class Bridge(GameSprite):
    def __init__(self, x, y, img, width, height,): 
        super().__init__(x, y, img, width, height)
    def update(self,window):
        self.draw(window)
