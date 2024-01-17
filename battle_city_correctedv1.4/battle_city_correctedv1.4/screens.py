import pygame
from abc import abstractmethod,ABC
from sprite import Player,Button, Enemy, Brick, WIDTH, HEIGHT,Iron,Grass,Water,Bridge
import sys
import os

money = 20

bullet_img = 'images/bullet.png'
player_img = 'images/tank.png'
enemy_img = 'images/rocket.png'

block_img = 'images/brick.png'
grass_img = 'images/grass.png'
iron_img = 'images/iron.png'
water_img = 'images/water.png'
bridge_img = 'images/oak_woods.jpg'

btn1 = 'images/play.png'
btn2 = 'images/armor.png'
btn3 = 'images/speed.png'
btn4 = 'images/power.png'
btn5 = 'images/shoot.png'

pygame.mixer.init()
game_music = 'sound/battle_sound.mp3'
menu_music = 'sound/menu.mp3'
click_sound = pygame.mixer.Sound('sound/click.mp3')
hit_sound = pygame.mixer.Sound('sound/hit.wav')
miss_sound = pygame.mixer.Sound('sound/miss.wav')
win_sound = pygame.mixer.Sound('sound/win.wav')
movement_sound = pygame.mixer.Sound('sound/drive.mp3')

class Screen(ABC):
    @abstractmethod
    def update(self):
        pass        
    
class ScreenManager():
    '''
    display settings,main screen
    '''
    def __init__(self)  :
        self.menu = MenuScreen(self)
        self.main_game = GameScreen(self)
        self.current = self.menu
        
    def update(self,window,events):
        self.current.update(window,events)
        
    def add_screen(self):
        pass
        


class MenuScreen(Screen):
    def __init__(self,manager) :
        self.manager = manager
        self.start_button = Button(100,30,btn1,210,190)
        self.quit_button = Button(400,100,bullet_img,200,100)
        self.upgrade1 = Button(70,260,btn2,170,240)
        self.upgrade2 = Button(190,260,btn3,170,240)
        self.upgrade3 = Button(340,260,btn4,110,240)
        self.upgrade4 = Button(460,260,btn5,110,240)
        

        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.load(menu_music)
        pygame.mixer.music.play(-1)
        

    def update(self,window,events):
        self.start_button.draw(window)
        self.quit_button.draw(window)
        self.upgrade1.draw(window)
        self.upgrade2.draw(window)
        self.upgrade3.draw(window)
        self.upgrade4.draw(window)
        self.process_events(events)

    def process_events(self,events):                
        for e in events:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 :
                if self.start_button.collidepoint(*e.pos):
                    click_sound.set_volume(0.3)
                    pygame.mixer.Sound.play(click_sound)
                    pygame.mixer.music.set_volume(0.1)
                    pygame.mixer.music.load(game_music)
                    pygame.mixer.music.play(-1)
                    self.manager.current = self.manager.main_game

                if self.quit_button.collidepoint(*e.pos):
                    pygame.mixer.Sound.play(click_sound)
                    sys.exit()

                if self.upgrade3.collidepoint(*e.pos):
                    pygame.mixer.Sound.play(click_sound)
                
                if self.upgrade1.collidepoint(*e.pos):
                    pygame.mixer.Sound.play(click_sound)

                if self.upgrade2.collidepoint(*e.pos):
                    pygame.mixer.Sound.play(click_sound)

                if self.upgrade4.collidepoint(*e.pos):
                    pygame.mixer.Sound.play(click_sound)

                    
                    
class GameScreen(Screen):
    def __init__(self,manager):
        self.manager = manager
        
        self.levels = self.load_levels('levels')
        self.next_level()
        
        
    def load_levels(self,folder_name):
        files =os.listdir(folder_name)
        for file in files:
            level = Level(os.path.join(folder_name,file),self)
            level.load()
            yield level
    
    def next_level(self):
        try:
            self.curent_level = next(self.levels)
        except StopIteration:
            self.manager.current = self.manager.menu
            self.levels = self.load_levels('levels')
        
    def update(self,window,events):
        self.curent_level.update(window,events)
            
 

class Level():
    def __init__(self,filename,game):
        self.game = game
        self.filename= filename
        self.load()

    def load(self):
        self.block_size =20
        self.load_map(self.filename)
        self.bullets = pygame.sprite.Group()
        self.Enemy_bullets_group = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.player = Player(200,530,player_img,40,40,'vadym',3,1,self.bullets)
        self.enemies.add(Enemy(720,150,enemy_img,40,40, self.Enemy_bullets_group))
        
        for enemy in self.enemies:
            enemy.set_player(self.player)

        for enemy_bullet in self.Enemy_bullets_group:
            enemy_bullet.set_player(self.player)
    
    def update(self,window,events):
        for e in events:
            # if e.type == pygame.KEYDOWN: and e.key == pygame.K_SPACE:
            if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1 :
                    self.player.shoot()
        
        self.Echeck_bullets_collisions()
        self.check_bullets_collisions()

        player_hit = pygame.sprite.spritecollide(self.player, self.Enemy_bullets_group, True)
        if player_hit:
            self.player.health -= 1
            if self.player.health <= 0:
                sys.exit()
        
        if not self.enemies:
            self.game.next_level()
            # pygame.time.delay(2000)
            win_sound.set_volume(0.3)
            pygame.mixer.Sound.play(win_sound)
        
        self.player.update(window,self.blocks_col)
        self.enemies.update(window, self.blocks_col, self.blocks_unc)
        # self.enemies.draw(window)
        self.bullets.update(window)
        self.Enemy_bullets_group.update(window)
        self.blocks_col.update(window)
        self.blocks_unc.update(window)
        
    def load_map(self,filename):
        with open(filename, 'r', encoding='utf-8') as file:
            self.blocks_col = pygame.sprite.Group()
            self.blocks_unc = pygame.sprite.Group()
            for y,line in enumerate(file.readlines()):
                for x,block in enumerate(line.replace('\n','')):
                    if block =='1':
                        self.blocks_col.add(Brick(self.block_size*x,self.block_size*y,block_img,self.block_size,self.block_size))
                    if block =='2':
                        self.blocks_col.add(Iron(self.block_size*x,self.block_size*y,iron_img,self.block_size,self.block_size))
                    if block =='3':
                        self.blocks_unc.add(Grass(self.block_size*x,self.block_size*y,grass_img,self.block_size,self.block_size))  
                    if block =='4':
                        self.blocks_col.add(Water(self.block_size*x,self.block_size*y,water_img,self.block_size,self.block_size)) 
                    if block =='5':
                        self.blocks_unc.add(Bridge(self.block_size*x,self.block_size*y,bridge_img,self.block_size,self.block_size))                    

    def check_bullets_collisions(self):
        collided_blocks=pygame.sprite.groupcollide(self.blocks_col,self.bullets,False,False)
        for block in collided_blocks:
            if isinstance(block,Brick):
                block.kill()
                [bullet.kill() for bullet in collided_blocks[block]]
            if isinstance(block,Iron):
                [bullet.kill() for bullet in collided_blocks[block]]
                pygame.mixer.Sound.play(miss_sound)

    def Echeck_bullets_collisions(self):
        collided_blocks=pygame.sprite.groupcollide(self.blocks_col,self.Enemy_bullets_group, False,False)
        for block in collided_blocks:
            if isinstance(block,Brick):
                block.kill()
                [bullet.kill() for bullet in collided_blocks[block]]
            if isinstance(block,Iron):
                [bullet.kill() for bullet in collided_blocks[block]]
                pygame.mixer.Sound.play(miss_sound)
                
        collided_enemies = pygame.sprite.groupcollide(self.enemies,self.bullets,False,True)
        for enemy in collided_enemies:
            hit_sound.set_volume(0.2)
            pygame.mixer.Sound.play(hit_sound)
            enemy.kill()
            

        # Проверка границ окна
        # if bullet.rect.bottom < 0 or bullet.rect.right < 0 or bullet.rect.left > WIDTH:
        #     bullet.kill()


                    
        